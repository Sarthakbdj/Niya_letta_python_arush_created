#!/usr/bin/env python3
"""
Advanced Conversation Memory System
Implements best practices for Letta memory optimization:
- Specialized memory blocks
- Intelligent consolidation
- Adaptive learning with confidence
- Smart context injection
- Memory health monitoring
"""

import sqlite3
import json
import time
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class ConversationStage(Enum):
    GREETING = "greeting"
    GETTING_TO_KNOW = "getting_to_know"
    DEEP_CONVERSATION = "deep_conversation"
    TOPIC_CONTINUATION = "topic_continuation"
    EMOTIONAL_SUPPORT = "emotional_support"
    CASUAL_CHAT = "casual_chat"

class MemoryPriority(Enum):
    CRITICAL = "critical"  # Name, core identity
    HIGH = "high"         # Preferences, important facts
    MEDIUM = "medium"     # Opinions, interests
    LOW = "low"          # Casual mentions

@dataclass
class UserFact:
    fact_type: str
    value: str
    confidence: float
    priority: MemoryPriority
    first_mentioned: datetime
    last_confirmed: datetime
    confirmation_count: int

class AdvancedConversationMemory:
    def __init__(self, db_path: str = "advanced_conversation_memory.db"):
        self.db_path = db_path
        self.init_database()
        
        # Memory optimization settings
        self.max_memory_block_length = {
            "user_essence": 200,
            "relationship_state": 150,
            "conversation_context": 150,
            "emotional_context": 100
        }
        
        # High-value information patterns
        self.high_value_patterns = {
            "identity": [r"my name is (\w+)", r"i am (\w+)", r"call me (\w+)"],
            "preferences": [r"my favorite (\w+) is (\w+)", r"i love (\w+)", r"i hate (\w+)"],
            "facts": [r"i work as", r"i study", r"i live in", r"i have a"],
            "emotions": [r"i feel", r"i'm (happy|sad|excited|worried|stressed)"],
            "relationships": [r"my (boyfriend|girlfriend|husband|wife|partner)"]
        }

    def init_database(self):
        """Initialize advanced database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enhanced conversation sessions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_messages INTEGER DEFAULT 0,
                conversation_stage TEXT DEFAULT 'greeting',
                emotional_state TEXT,
                trust_level REAL DEFAULT 0.5,
                relationship_depth TEXT DEFAULT 'acquaintance',
                summary TEXT,
                dominant_topics TEXT,  -- JSON array
                user_personality_traits TEXT  -- JSON object
            )
        ''')
        
        # Enhanced messages with conversation analysis
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                message_num INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_message TEXT,
                priya_response TEXT,
                sentiment TEXT,
                emotion_intensity REAL,
                topics TEXT,  -- JSON array
                high_value_extractions TEXT,  -- JSON array
                conversation_stage TEXT,
                memory_references TEXT,  -- JSON array of referenced memories
                FOREIGN KEY (session_id) REFERENCES conversation_sessions (session_id)
            )
        ''')
        
        # User facts with confidence and priority
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                fact_type TEXT,  -- 'name', 'preference', 'emotion', 'relationship'
                category TEXT,   -- 'identity', 'interests', 'personality', 'history'
                key_phrase TEXT,
                value TEXT,
                confidence REAL,
                priority TEXT,   -- 'critical', 'high', 'medium', 'low'
                first_mentioned TIMESTAMP,
                last_confirmed TIMESTAMP,
                confirmation_count INTEGER DEFAULT 1,
                contradictions TEXT,  -- JSON array of contradictory statements
                FOREIGN KEY (session_id) REFERENCES conversation_sessions (session_id)
            )
        ''')
        
        # Memory health metrics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_health (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                retention_score REAL,
                consistency_score REAL,
                learning_velocity REAL,
                context_relevance REAL,
                memory_efficiency REAL,
                FOREIGN KEY (session_id) REFERENCES conversation_sessions (session_id)
            )
        ''')
        
        # Emotional timeline
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emotional_timeline (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                emotion TEXT,
                intensity REAL,
                triggers TEXT,  -- JSON array
                context TEXT,
                FOREIGN KEY (session_id) REFERENCES conversation_sessions (session_id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def start_session(self, user_id: str = "default_user") -> str:
        """Start new conversation session with advanced tracking"""
        session_id = f"session_{int(time.time())}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversation_sessions 
            (session_id, user_id, conversation_stage, trust_level)
            VALUES (?, ?, ?, ?)
        ''', (session_id, user_id, ConversationStage.GREETING.value, 0.3))
        
        conn.commit()
        conn.close()
        
        return session_id

    def add_message_with_analysis(self, session_id: str, message_num: int, 
                                 user_message: str, priya_response: str):
        """Add message with comprehensive analysis"""
        
        # Extract high-value information
        high_value_info = self.extract_high_value_info([{
            'user_message': user_message,
            'priya_response': priya_response
        }])
        
        # Analyze sentiment and emotion
        sentiment_analysis = self.analyze_advanced_sentiment(user_message)
        
        # Detect conversation stage
        conversation_stage = self.detect_conversation_stage(session_id, user_message)
        
        # Extract topics
        topics = self.extract_topics(user_message + " " + priya_response)
        
        # Find memory references in Priya's response
        memory_refs = self.find_memory_references(priya_response, session_id)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert message with analysis
        cursor.execute('''
            INSERT INTO messages 
            (session_id, message_num, user_message, priya_response, sentiment, 
             emotion_intensity, topics, high_value_extractions, conversation_stage, memory_references)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, message_num, user_message, priya_response,
              sentiment_analysis['sentiment'], sentiment_analysis['intensity'],
              json.dumps(topics), json.dumps(high_value_info),
              conversation_stage.value, json.dumps(memory_refs)))
        
        # Update session
        cursor.execute('''
            UPDATE conversation_sessions 
            SET last_activity = CURRENT_TIMESTAMP, 
                total_messages = total_messages + 1,
                conversation_stage = ?,
                emotional_state = ?
            WHERE session_id = ?
        ''', (conversation_stage.value, sentiment_analysis['sentiment'], session_id))
        
        # Store high-value facts
        for info in high_value_info:
            self.store_user_fact_with_confidence(
                session_id, info['fact_type'], info['category'],
                info['key_phrase'], info['value'], info['confidence'], info['priority']
            )
        
        # Track emotional evolution
        if sentiment_analysis['emotion']:
            cursor.execute('''
                INSERT INTO emotional_timeline (session_id, emotion, intensity, triggers, context)
                VALUES (?, ?, ?, ?, ?)
            ''', (session_id, sentiment_analysis['emotion'], sentiment_analysis['intensity'],
                  json.dumps(sentiment_analysis.get('triggers', [])), user_message[:100]))
        
        conn.commit()
        conn.close()

    def extract_high_value_info(self, messages: List[Dict]) -> List[Dict]:
        """Extract high-value information with priority and confidence scoring"""
        high_value = []
        
        for msg in messages:
            user_msg = msg['user_message'].lower()
            
            # Identity information (CRITICAL priority)
            for pattern in self.high_value_patterns['identity']:
                matches = re.findall(pattern, user_msg, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0] if match else ""
                    high_value.append({
                        'fact_type': 'identity',
                        'category': 'core_identity',
                        'key_phrase': 'name',
                        'value': match,
                        'confidence': 0.95,
                        'priority': MemoryPriority.CRITICAL
                    })
            
            # Preferences (HIGH priority)
            for pattern in self.high_value_patterns['preferences']:
                matches = re.findall(pattern, user_msg, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        key, value = match if len(match) >= 2 else (match[0], "")
                    else:
                        key, value = "preference", match
                    
                    high_value.append({
                        'fact_type': 'preference',
                        'category': 'interests',
                        'key_phrase': key,
                        'value': value,
                        'confidence': 0.85,
                        'priority': MemoryPriority.HIGH
                    })
            
            # Emotional states (MEDIUM priority)
            for pattern in self.high_value_patterns['emotions']:
                matches = re.findall(pattern, user_msg, re.IGNORECASE)
                for match in matches:
                    high_value.append({
                        'fact_type': 'emotion',
                        'category': 'emotional_state',
                        'key_phrase': 'current_feeling',
                        'value': match,
                        'confidence': 0.7,
                        'priority': MemoryPriority.MEDIUM
                    })
            
            # Direct statements (HIGH priority)
            direct_statements = [
                r"my (\w+) is (\w+)",
                r"i work as (\w+)",
                r"i study (\w+)",
                r"i live in (\w+)"
            ]
            
            for pattern in direct_statements:
                matches = re.findall(pattern, user_msg, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple) and len(match) >= 2:
                        key, value = match
                        high_value.append({
                            'fact_type': 'personal_info',
                            'category': 'life_details',
                            'key_phrase': key,
                            'value': value,
                            'confidence': 0.9,
                            'priority': MemoryPriority.HIGH
                        })
        
        return high_value

    def store_user_fact_with_confidence(self, session_id: str, fact_type: str, 
                                      category: str, key_phrase: str, value: str, 
                                      confidence: float, priority: MemoryPriority):
        """Store user fact with confidence-based updating"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check for existing fact
        cursor.execute('''
            SELECT * FROM user_facts 
            WHERE session_id = ? AND fact_type = ? AND key_phrase = ?
        ''', (session_id, fact_type, key_phrase))
        
        existing_fact = cursor.fetchone()
        
        if existing_fact:
            old_confidence = existing_fact[6]  # confidence column
            old_value = existing_fact[5]       # value column
            
            # Check for contradiction
            if self.facts_contradict(old_value, value):
                if confidence > old_confidence + 0.2:
                    # New info is significantly more confident
                    cursor.execute('''
                        UPDATE user_facts 
                        SET value = ?, confidence = ?, last_confirmed = CURRENT_TIMESTAMP,
                            confirmation_count = confirmation_count + 1
                        WHERE session_id = ? AND fact_type = ? AND key_phrase = ?
                    ''', (value, confidence, session_id, fact_type, key_phrase))
                else:
                    # Log contradiction but keep old fact
                    contradictions = json.loads(existing_fact[11] or "[]")
                    contradictions.append({
                        "value": value,
                        "confidence": confidence,
                        "timestamp": datetime.now().isoformat()
                    })
                    cursor.execute('''
                        UPDATE user_facts 
                        SET contradictions = ?
                        WHERE session_id = ? AND fact_type = ? AND key_phrase = ?
                    ''', (json.dumps(contradictions), session_id, fact_type, key_phrase))
            else:
                # Reinforce existing fact
                combined_confidence = min((old_confidence + confidence) / 2 + 0.1, 1.0)
                cursor.execute('''
                    UPDATE user_facts 
                    SET confidence = ?, last_confirmed = CURRENT_TIMESTAMP,
                        confirmation_count = confirmation_count + 1
                    WHERE session_id = ? AND fact_type = ? AND key_phrase = ?
                ''', (combined_confidence, session_id, fact_type, key_phrase))
        else:
            # New fact
            cursor.execute('''
                INSERT INTO user_facts 
                (session_id, fact_type, category, key_phrase, value, confidence, priority,
                 first_mentioned, last_confirmed)
                VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ''', (session_id, fact_type, category, key_phrase, value, confidence, priority.value))
        
        conn.commit()
        conn.close()

    def generate_optimized_memory_blocks(self, session_id: str) -> List[Dict]:
        """Generate optimized memory blocks with specialization"""
        
        # Get user profile
        user_essence = self.build_user_essence(session_id)
        relationship_state = self.build_relationship_state(session_id)
        conversation_context = self.build_conversation_context(session_id)
        emotional_context = self.build_emotional_context(session_id)
        
        # Base persona (immutable)
        memory_blocks = [{
            "label": "persona",
            "value": "You are Priya, a warm and caring AI companion who speaks in a mix of English and Hindi. You're empathetic, curious about the user's life, and build genuine connections. You remember important details and show interest in the user's wellbeing.",
            "immutable": True
        }]
        
        # Specialized memory blocks
        if user_essence:
            memory_blocks.append({
                "label": "user_essence",
                "value": user_essence[:self.max_memory_block_length["user_essence"]],
                "max_length": self.max_memory_block_length["user_essence"]
            })
        
        if relationship_state:
            memory_blocks.append({
                "label": "relationship_state", 
                "value": relationship_state[:self.max_memory_block_length["relationship_state"]],
                "max_length": self.max_memory_block_length["relationship_state"]
            })
        
        if conversation_context:
            memory_blocks.append({
                "label": "conversation_context",
                "value": conversation_context[:self.max_memory_block_length["conversation_context"]],
                "max_length": self.max_memory_block_length["conversation_context"]
            })
        
        if emotional_context:
            memory_blocks.append({
                "label": "emotional_context",
                "value": emotional_context[:self.max_memory_block_length["emotional_context"]],
                "max_length": self.max_memory_block_length["emotional_context"]
            })
        
        return memory_blocks

    def build_user_essence(self, session_id: str) -> str:
        """Build concise user essence from high-confidence facts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get critical and high priority facts
        cursor.execute('''
            SELECT fact_type, key_phrase, value, confidence 
            FROM user_facts 
            WHERE session_id = ? AND priority IN ('critical', 'high') AND confidence > 0.7
            ORDER BY priority DESC, confidence DESC
            LIMIT 10
        ''', (session_id,))
        
        facts = cursor.fetchall()
        conn.close()
        
        if not facts:
            return ""
        
        essence_parts = []
        
        # Extract name
        name_facts = [f for f in facts if f[1] == 'name']
        if name_facts:
            essence_parts.append(name_facts[0][2])  # User's name
        
        # Extract key characteristics
        preferences = [f for f in facts if f[0] == 'preference']
        if preferences:
            pref_text = " | ".join([f"{f[1]}: {f[2]}" for f in preferences[:3]])
            essence_parts.append(pref_text)
        
        # Extract personality traits
        personal_info = [f for f in facts if f[0] == 'personal_info']
        if personal_info:
            info_text = " | ".join([f"{f[1]}: {f[2]}" for f in personal_info[:2]])
            essence_parts.append(info_text)
        
        return " | ".join(essence_parts)

    def build_relationship_state(self, session_id: str) -> str:
        """Build relationship state summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get session info
        cursor.execute('''
            SELECT conversation_stage, trust_level, relationship_depth, total_messages
            FROM conversation_sessions WHERE session_id = ?
        ''', (session_id,))
        
        session_info = cursor.fetchone()
        conn.close()
        
        if not session_info:
            return ""
        
        stage, trust, depth, msg_count = session_info
        
        # Build relationship summary
        parts = [
            f"Stage: {stage}",
            f"Trust: {trust:.1f}/1.0",
            f"Depth: {depth or 'developing'}",
            f"Messages: {msg_count}"
        ]
        
        return " | ".join(parts)

    def build_conversation_context(self, session_id: str) -> str:
        """Build recent conversation context"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get recent topics and emotional state
        cursor.execute('''
            SELECT topics, sentiment, user_message 
            FROM messages 
            WHERE session_id = ? 
            ORDER BY message_num DESC 
            LIMIT 5
        ''', (session_id,))
        
        recent_messages = cursor.fetchall()
        conn.close()
        
        if not recent_messages:
            return ""
        
        # Extract recent topics
        all_topics = []
        for msg in recent_messages:
            if msg[0]:  # topics
                topics = json.loads(msg[0])
                all_topics.extend(topics)
        
        unique_topics = list(set(all_topics))[:3]
        
        # Get dominant sentiment
        sentiments = [msg[1] for msg in recent_messages if msg[1]]
        dominant_sentiment = max(set(sentiments), key=sentiments.count) if sentiments else "neutral"
        
        parts = [
            f"Recent topics: {', '.join(unique_topics)}" if unique_topics else "",
            f"User mood: {dominant_sentiment}",
            "Active conversation flow"
        ]
        
        return " | ".join([p for p in parts if p])

    def build_emotional_context(self, session_id: str) -> str:
        """Build emotional context summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get recent emotional timeline
        cursor.execute('''
            SELECT emotion, intensity, triggers 
            FROM emotional_timeline 
            WHERE session_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 3
        ''', (session_id,))
        
        emotions = cursor.fetchall()
        conn.close()
        
        if not emotions:
            return ""
        
        # Build emotional summary
        current_emotion = emotions[0][0] if emotions else "neutral"
        avg_intensity = sum([e[1] for e in emotions]) / len(emotions) if emotions else 0.5
        
        parts = [
            f"Current emotion: {current_emotion}",
            f"Intensity: {avg_intensity:.1f}/1.0"
        ]
        
        return " | ".join(parts)

    def assess_memory_health(self, session_id: str) -> Dict[str, float]:
        """Assess memory system health and effectiveness"""
        
        retention_score = self.calculate_retention_score(session_id)
        consistency_score = self.calculate_consistency_score(session_id)
        learning_velocity = self.calculate_learning_velocity(session_id)
        context_relevance = self.calculate_context_relevance(session_id)
        
        health_metrics = {
            'retention_score': retention_score,
            'consistency_score': consistency_score,
            'learning_velocity': learning_velocity,
            'context_relevance': context_relevance,
            'overall_health': (retention_score + consistency_score + learning_velocity + context_relevance) / 4
        }
        
        # Store health metrics
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO memory_health 
            (session_id, retention_score, consistency_score, learning_velocity, context_relevance, memory_efficiency)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (session_id, retention_score, consistency_score, learning_velocity, 
              context_relevance, health_metrics['overall_health']))
        
        conn.commit()
        conn.close()
        
        # Trigger optimization if needed
        if health_metrics['overall_health'] < 0.6:
            self.trigger_memory_optimization(session_id)
        
        return health_metrics

    def calculate_retention_score(self, session_id: str) -> float:
        """Calculate how well memories are retained across resets"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count memory references in recent messages
        cursor.execute('''
            SELECT memory_references FROM messages 
            WHERE session_id = ? AND memory_references IS NOT NULL
            ORDER BY message_num DESC LIMIT 10
        ''', (session_id,))
        
        references = cursor.fetchall()
        conn.close()
        
        if not references:
            return 0.5  # Neutral score
        
        # Calculate retention based on reference frequency
        total_refs = sum([len(json.loads(ref[0])) for ref in references if ref[0]])
        max_possible = len(references) * 3  # Assume max 3 references per message
        
        return min(total_refs / max(max_possible, 1), 1.0)

    def calculate_consistency_score(self, session_id: str) -> float:
        """Calculate consistency of stored facts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT contradictions FROM user_facts 
            WHERE session_id = ? AND contradictions IS NOT NULL
        ''', (session_id,))
        
        contradictions = cursor.fetchall()
        
        cursor.execute('''
            SELECT COUNT(*) FROM user_facts WHERE session_id = ?
        ''', (session_id,))
        
        total_facts = cursor.fetchone()[0]
        conn.close()
        
        if total_facts == 0:
            return 1.0
        
        contradiction_count = len(contradictions)
        return max(1.0 - (contradiction_count / total_facts), 0.0)

    def calculate_learning_velocity(self, session_id: str) -> float:
        """Calculate how quickly new information is being learned"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count facts learned in recent messages
        cursor.execute('''
            SELECT COUNT(*) FROM user_facts 
            WHERE session_id = ? AND first_mentioned > datetime('now', '-1 hour')
        ''', (session_id,))
        
        recent_facts = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT total_messages FROM conversation_sessions WHERE session_id = ?
        ''', (session_id,))
        
        total_messages = cursor.fetchone()[0] or 1
        conn.close()
        
        # Learning velocity = facts per message
        return min(recent_facts / max(total_messages, 1), 1.0)

    def calculate_context_relevance(self, session_id: str) -> float:
        """Calculate how relevant context injection is"""
        # This would require analyzing how often injected context is actually used
        # For now, return a baseline score
        return 0.7

    def trigger_memory_optimization(self, session_id: str):
        """Auto-optimize memory when issues detected"""
        
        # Clean up low-confidence memories
        self.cleanup_uncertain_memories(session_id)
        
        # Consolidate similar memories
        self.consolidate_similar_memories(session_id)
        
        # Boost confidence of validated memories
        self.reinforce_validated_memories(session_id)

    def cleanup_uncertain_memories(self, session_id: str):
        """Remove low-confidence, unconfirmed memories"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM user_facts 
            WHERE session_id = ? AND confidence < 0.3 AND confirmation_count = 1
        ''', (session_id,))
        
        conn.commit()
        conn.close()

    def consolidate_similar_memories(self, session_id: str):
        """Consolidate redundant or similar memories"""
        # Implementation would involve similarity detection and merging
        pass

    def reinforce_validated_memories(self, session_id: str):
        """Boost confidence of consistently referenced facts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE user_facts 
            SET confidence = MIN(confidence + 0.1, 1.0)
            WHERE session_id = ? AND confirmation_count > 2
        ''', (session_id,))
        
        conn.commit()
        conn.close()

    # Helper methods for analysis
    def analyze_advanced_sentiment(self, text: str) -> Dict:
        """Advanced sentiment analysis with emotion detection"""
        emotions = {
            'happy': ['happy', 'joy', 'excited', 'great', 'amazing', 'wonderful'],
            'sad': ['sad', 'down', 'depressed', 'upset', 'disappointed'],
            'angry': ['angry', 'mad', 'frustrated', 'annoyed', 'furious'],
            'anxious': ['worried', 'anxious', 'nervous', 'stressed', 'concerned'],
            'love': ['love', 'adore', 'cherish', 'care', 'affection']
        }
        
        text_lower = text.lower()
        detected_emotions = []
        
        for emotion, keywords in emotions.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_emotions.append(emotion)
        
        # Simple sentiment scoring
        positive_words = ['good', 'great', 'happy', 'love', 'amazing', 'wonderful']
        negative_words = ['bad', 'sad', 'hate', 'terrible', 'awful', 'horrible']
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            sentiment = 'positive'
            intensity = min(pos_count / 3, 1.0)
        elif neg_count > pos_count:
            sentiment = 'negative'
            intensity = min(neg_count / 3, 1.0)
        else:
            sentiment = 'neutral'
            intensity = 0.5
        
        return {
            'sentiment': sentiment,
            'intensity': intensity,
            'emotion': detected_emotions[0] if detected_emotions else None,
            'triggers': detected_emotions
        }

    def detect_conversation_stage(self, session_id: str, user_message: str) -> ConversationStage:
        """Detect current conversation stage"""
        
        # Get message count
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT total_messages FROM conversation_sessions WHERE session_id = ?', (session_id,))
        result = cursor.fetchone()
        message_count = result[0] if result else 0
        conn.close()
        
        user_msg_lower = user_message.lower()
        
        # Stage detection logic
        if message_count <= 2:
            return ConversationStage.GREETING
        elif any(word in user_msg_lower for word in ['feel', 'emotion', 'sad', 'happy', 'worried']):
            return ConversationStage.EMOTIONAL_SUPPORT
        elif any(word in user_msg_lower for word in ['dream', 'future', 'relationship', 'love', 'life']):
            return ConversationStage.DEEP_CONVERSATION
        elif message_count <= 8:
            return ConversationStage.GETTING_TO_KNOW
        else:
            return ConversationStage.CASUAL_CHAT

    def extract_topics(self, text: str) -> List[str]:
        """Enhanced topic extraction"""
        topic_keywords = {
            "music": ["music", "song", "sing", "dance", "beat", "guitar", "piano", "band"],
            "love": ["love", "relationship", "romantic", "heart", "feelings", "dating"],
            "work": ["work", "job", "career", "office", "boss", "colleague", "business"],
            "family": ["family", "mother", "father", "sister", "brother", "parents"],
            "hobbies": ["hobby", "activity", "fun", "enjoy", "interest", "passion"],
            "travel": ["travel", "trip", "vacation", "visit", "journey", "explore"],
            "food": ["food", "eat", "cook", "restaurant", "meal", "dinner"],
            "technology": ["tech", "computer", "phone", "app", "software", "internet"],
            "sports": ["sport", "game", "play", "team", "exercise", "fitness"],
            "education": ["school", "study", "learn", "university", "college", "education"]
        }
        
        text_lower = text.lower()
        detected_topics = []
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_topics.append(topic)
        
        return detected_topics

    def find_memory_references(self, priya_response: str, session_id: str) -> List[str]:
        """Find what memories Priya referenced in her response"""
        
        # Get stored facts
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT key_phrase, value FROM user_facts WHERE session_id = ?', (session_id,))
        facts = cursor.fetchall()
        conn.close()
        
        references = []
        response_lower = priya_response.lower()
        
        for key_phrase, value in facts:
            if value.lower() in response_lower or key_phrase.lower() in response_lower:
                references.append(f"{key_phrase}: {value}")
        
        return references

    def facts_contradict(self, old_value: str, new_value: str) -> bool:
        """Check if two facts contradict each other"""
        
        # Simple contradiction detection
        contradictory_pairs = [
            (['love', 'like'], ['hate', 'dislike']),
            (['happy', 'joy'], ['sad', 'depressed']),
            (['single'], ['married', 'relationship']),
        ]
        
        old_lower = old_value.lower()
        new_lower = new_value.lower()
        
        for positive, negative in contradictory_pairs:
            old_positive = any(word in old_lower for word in positive)
            old_negative = any(word in old_lower for word in negative)
            new_positive = any(word in new_lower for word in positive)
            new_negative = any(word in new_lower for word in negative)
            
            if (old_positive and new_negative) or (old_negative and new_positive):
                return True
        
        return False
