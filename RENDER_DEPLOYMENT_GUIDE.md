# Niya AI Girlfriend - Render.com Deployment Guide

## 🚀 Quick Deployment Steps

### Option 1: Web Service Deployment (Recommended)

1. **Connect Your Repository to Render.com**
   - Go to [Render.com](https://render.com) and sign up/login
   - Connect your GitHub repository containing this code
   - Click "New +" → "Web Service"

2. **Configure Web Service Settings**
   ```
   Name: niya-ai-girlfriend
   Environment: Python 3
   Region: Oregon (US West)
   Branch: master
   Build Command: pip install -r requirements.txt
   Start Command: python priya_chat.py
   Plan: Starter ($7/month) or Free
   ```

3. **Add Environment Variables**
   Go to Environment section and add these variables:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   PINECONE_INDEX_NAME=niya-production
   EMBEDDING_MODEL=text-embedding-3-small
   LETTA_BASE_URL=http://localhost:8283
   LETTA_MODE=local
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete (5-10 minutes)
   - Your app will be available at: `https://your-service-name.onrender.com`

### Option 2: Docker Deployment

1. **Use Docker Configuration**
   - In Build & Deploy settings, set:
   ```
   Dockerfile Path: ./Dockerfile.render
   ```

2. **Environment Variables** (same as above)

### Option 3: Blueprint Deployment (Advanced)

1. **Use render.yaml**
   - The included `render.yaml` file contains the full configuration
   - Simply connect your repo and Render will auto-detect the blueprint

## 🔧 Configuration Details

### Required Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key from platform.openai.com
- `PINECONE_API_KEY`: Your Pinecone API key (optional, for enhanced features)
- `PORT`: Automatically set by Render.com

### Optional Environment Variables
- `PINECONE_INDEX_NAME`: Index name for Pinecone (default: niya-production)
- `EMBEDDING_MODEL`: OpenAI embedding model (default: text-embedding-3-small)
- `LETTA_MODE`: Set to 'local' for local processing

## 🌐 Accessing Your App

Once deployed, your app will have two interfaces:

1. **Web Chat Interface**: `https://your-app.onrender.com/`
   - Direct chat with Priya AI girlfriend
   - Modern, responsive UI
   - Real-time messaging

2. **API Endpoints**:
   - `POST /api/message` - Send messages to AI
   - `GET /health` - Health check
   - `POST /api/reset` - Reset AI agent

## 🐛 Troubleshooting

### Common Issues:

1. **Deployment Fails**
   - Check that all environment variables are set
   - Ensure OPENAI_API_KEY is valid
   - Check build logs for specific errors

2. **AI Not Responding**
   - Verify OPENAI_API_KEY is working
   - Check application logs in Render dashboard
   - Try resetting the agent via `/api/reset`

3. **Frontend Not Loading**
   - Ensure static files are being served correctly
   - Check that the deployment includes the `deployment/static/` folder

### View Logs:
- Go to your Render dashboard
- Click on your service
- Click "Logs" tab to see real-time application logs

## 📊 Performance Optimization

### Free Tier Limitations:
- Service may sleep after 15 minutes of inactivity
- 750 hours/month limit
- Slower cold starts

### Paid Tier Benefits:
- Always-on service
- Faster response times
- Better reliability
- Custom domains

## 🔒 Security Notes

1. **Environment Variables**: Keep your API keys secure in Render's environment variables
2. **HTTPS**: Render provides free SSL certificates
3. **CORS**: Already configured for cross-origin requests

## 🚀 Next Steps

After successful deployment:

1. **Test the Chat Interface**: Visit your deployed URL
2. **Test API Endpoints**: Use tools like Postman to test `/api/message`
3. **Monitor Usage**: Check Render dashboard for usage statistics
4. **Scale if Needed**: Upgrade to paid plans for better performance

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review Render.com documentation
3. Check application logs for specific error messages

---

**Happy Deployment! 🎉**

Your Niya AI Girlfriend is now ready to chat with users worldwide! 