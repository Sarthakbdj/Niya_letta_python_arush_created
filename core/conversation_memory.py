#!/usr/bin/env python3
"""
Conversation Memory System
Maintains context across agent resets using database persistence
"""

import sqlite3
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

class ConversationMemory:
    def __init__(self, db_path: str = "conversation_memory.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for conversation memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Conversation sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_messages INTEGER DEFAULT 0,
                summary TEXT,
                mood TEXT,
                topics TEXT  -- JSON array of discussed topics
            )
        ''')
        
        # Individual messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                message_num INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_message TEXT,
                priya_response TEXT,
                sentiment TEXT,
                topics TEXT,  -- JSON array
                FOREIGN KEY (session_id) REFERENCES conversation_sessions (session_id)
            )
        ''')
        
        # Relationship insights table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relationship_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                insight_type TEXT,  -- 'preference', 'memory', 'emotion', 'topic_interest'
                key_phrase TEXT,
                value TEXT,
                confidence REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES conversation_sessions (session_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def start_session(self, user_id: str = "default_user") -> str:
        """Start a new conversation session"""
        session_id = f"session_{int(time.time())}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversation_sessions (session_id, user_id)
            VALUES (?, ?)
        ''', (session_id, user_id))
        
        conn.commit()
        conn.close()
        
        return session_id
    
    def add_message(self, session_id: str, message_num: int, 
                   user_message: str, priya_response: str):
        """Add a message exchange to memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Extract topics and sentiment (simple keyword extraction)
        topics = self._extract_topics(user_message + " " + priya_response)
        sentiment = self._analyze_sentiment(user_message)
        
        cursor.execute('''
            INSERT INTO messages 
            (session_id, message_num, user_message, priya_response, sentiment, topics)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (session_id, message_num, user_message, priya_response, 
              sentiment, json.dumps(topics)))
        
        # Update session activity
        cursor.execute('''
            UPDATE conversation_sessions 
            SET last_activity = CURRENT_TIMESTAMP, 
                total_messages = total_messages + 1
            WHERE session_id = ?
        ''', (session_id,))
        
        # Extract relationship insights
        insights = self._extract_insights(user_message, priya_response)
        for insight in insights:
            cursor.execute('''
                INSERT INTO relationship_insights
                (session_id, insight_type, key_phrase, value, confidence)
                VALUES (?, ?, ?, ?, ?)
            ''', (session_id, insight['type'], insight['key'], 
                  insight['value'], insight['confidence']))
        
        conn.commit()
        conn.close()
    
    def get_conversation_summary(self, session_id: str, 
                               last_n_messages: int = 10) -> Dict[str, Any]:
        """Get conversation summary for agent context"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get recent messages
        cursor.execute('''
            SELECT user_message, priya_response, sentiment, topics
            FROM messages 
            WHERE session_id = ?
            ORDER BY message_num DESC
            LIMIT ?
        ''', (session_id, last_n_messages))
        
        recent_messages = cursor.fetchall()
        
        # Get relationship insights
        cursor.execute('''
            SELECT insight_type, key_phrase, value, confidence
            FROM relationship_insights
            WHERE session_id = ?
            ORDER BY confidence DESC
            LIMIT 10
        ''', (session_id,))
        
        insights = cursor.fetchall()
        
        # Get session info
        cursor.execute('''
            SELECT total_messages, mood, topics
            FROM conversation_sessions
            WHERE session_id = ?
        ''', (session_id,))
        
        session_info = cursor.fetchone()
        
        conn.close()
        
        # Build summary
        summary = {
            "total_messages": session_info[0] if session_info else 0,
            "recent_topics": self._get_recent_topics(recent_messages),
            "user_preferences": self._build_preferences(insights),
            "conversation_mood": session_info[1] if session_info else "neutral",
            "key_memories": self._build_key_memories(recent_messages),
            "relationship_insights": [
                {
                    "type": insight[0],
                    "key": insight[1], 
                    "value": insight[2],
                    "confidence": insight[3]
                } for insight in insights
            ]
        }
        
        return summary
    
    def generate_context_prompt(self, session_id: str) -> str:
        """Generate context prompt for new agents"""
        summary = self.get_conversation_summary(session_id)
        
        if summary["total_messages"] == 0:
            return "This is the start of a new conversation. Be warm and welcoming."
        
        context_parts = [
            f"CONVERSATION CONTEXT (Total messages: {summary['total_messages']}):",
            ""
        ]
        
        if summary["recent_topics"]:
            context_parts.append(f"Recent topics: {', '.join(summary['recent_topics'])}")
        
        if summary["user_preferences"]:
            context_parts.append("User preferences:")
            for pref in summary["user_preferences"][:3]:  # Top 3
                context_parts.append(f"  - {pref}")
        
        if summary["key_memories"]:
            context_parts.append("Key memories from recent conversation:")
            for memory in summary["key_memories"][:2]:  # Top 2
                context_parts.append(f"  - {memory}")
        
        context_parts.extend([
            "",
            f"Conversation mood: {summary['conversation_mood']}",
            "Continue the conversation naturally, maintaining consistency with the established relationship."
        ])
        
        return "\n".join(context_parts)
    
    def _extract_topics(self, text: str) -> List[str]:
        """Simple topic extraction using keywords"""
        topics = []
        topic_keywords = {
            "love": ["love", "relationship", "romantic", "heart", "feelings"],
            "music": ["music", "song", "sing", "dance", "beat"],
            "dreams": ["dream", "future", "hope", "wish", "aspire"],
            "colors": ["color", "blue", "red", "green", "teal", "purple"],
            "seasons": ["spring", "summer", "winter", "autumn", "weather"],
            "hobbies": ["hobby", "activity", "fun", "enjoy", "interest"],
            "emotions": ["happy", "sad", "excited", "calm", "peaceful"]
        }
        
        text_lower = text.lower()
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        positive_words = ["love", "happy", "great", "wonderful", "amazing", "beautiful"]
        negative_words = ["sad", "bad", "terrible", "awful", "hate"]
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        else:
            return "neutral"
    
    def _extract_insights(self, user_msg: str, priya_response: str) -> List[Dict]:
        """Extract relationship insights from conversation"""
        insights = []
        
        # Look for preferences mentioned
        if "favorite" in user_msg.lower():
            insights.append({
                "type": "preference",
                "key": "user_favorite",
                "value": user_msg,
                "confidence": 0.8
            })
        
        # Look for emotional expressions
        emotions = ["happy", "sad", "excited", "love", "care"]
        for emotion in emotions:
            if emotion in user_msg.lower():
                insights.append({
                    "type": "emotion",
                    "key": emotion,
                    "value": user_msg,
                    "confidence": 0.7
                })
        
        return insights
    
    def _get_recent_topics(self, messages: List) -> List[str]:
        """Get recent topics from messages"""
        all_topics = []
        for msg in messages:
            if msg[3]:  # topics column
                topics = json.loads(msg[3])
                all_topics.extend(topics)
        
        # Return unique topics
        return list(set(all_topics))
    
    def _build_preferences(self, insights: List) -> List[str]:
        """Build user preferences from insights"""
        preferences = []
        for insight in insights:
            if insight[0] == "preference":
                preferences.append(f"{insight[1]}: {insight[2]}")
        return preferences
    
    def _build_key_memories(self, messages: List) -> List[str]:
        """Build key memories from recent messages"""
        memories = []
        for msg in messages[:3]:  # Last 3 exchanges
            if len(msg[0]) > 20:  # Substantial user message
                memories.append(f"User said: {msg[0][:100]}...")
        return memories

    def cleanup_old_sessions(self, days_old: int = 7):
        """Clean up old conversation sessions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        cursor.execute('''
            DELETE FROM messages 
            WHERE session_id IN (
                SELECT session_id FROM conversation_sessions 
                WHERE last_activity < ?
            )
        ''', (cutoff_date,))
        
        cursor.execute('''
            DELETE FROM relationship_insights
            WHERE session_id IN (
                SELECT session_id FROM conversation_sessions 
                WHERE last_activity < ?
            )
        ''', (cutoff_date,))
        
        cursor.execute('''
            DELETE FROM conversation_sessions 
            WHERE last_activity < ?
        ''', (cutoff_date,))
        
        conn.commit()
        conn.close()
