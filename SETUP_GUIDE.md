# WhatsApp Business API + OpenAI Integration Setup Guide

This guide will help you set up your WhatsApp Business API integration with OpenAI to create an AI-powered WhatsApp bot.

## Prerequisites

1. **Meta Developer Account**: Create one at [developers.facebook.com](https://developers.facebook.com/)
2. **WhatsApp Business App**: Set up in your Meta developer account
3. **OpenAI API Key**: Get one from [platform.openai.com](https://platform.openai.com/)
4. **ngrok Account**: For webhook tunneling (free tier available)
5. **Python 3.7+**: Installed on your system

## Step 1: WhatsApp Business API Setup

### 1.1 Create Meta App
1. Go to [developers.facebook.com](https://developers.facebook.com/)
2. Click "Create App" → Select "Business" → Choose your app type
3. Add WhatsApp to your app from the product catalog

### 1.2 Configure WhatsApp
1. In your app dashboard, go to **WhatsApp** → **Getting Started**
2. Note down your **Phone Number ID** (you'll need this later)
3. Go to **API Setup** and get your **Access Token** (24-hour token for testing)
4. For production, create a **System User** for longer-lasting tokens:
   - Go to [business.facebook.com/settings/system-users](https://business.facebook.com/settings/system-users)
   - Create a system user and assign your WhatsApp app with full control
   - Generate a token (60 days or never expire)

### 1.3 Get Required Information
From your Meta App Dashboard, collect:
- **APP_ID**: Found in App Dashboard
- **APP_SECRET**: Found in App Dashboard  
- **PHONE_NUMBER_ID**: Found in WhatsApp → Getting Started
- **ACCESS_TOKEN**: From API Setup or System User
- **VERSION**: Use "v18.0" (latest)

## Step 2: OpenAI Setup

### 2.1 Get API Key
1. Go to [platform.openai.com](https://platform.openai.com/)
2. Create an account and get your API key
3. Add billing information (required for API usage)

### 2.2 Create Assistant (Optional)
You can either:
- Use the setup script: `python start/setup_assistant.py`
- Or create manually in OpenAI dashboard and get the assistant ID

## Step 3: Environment Configuration

### 3.1 Create .env File
Copy `example.env` to `.env` and fill in your details:

```bash
# WhatsApp Business API Configuration
ACCESS_TOKEN="your_access_token_here"
APP_ID="your_app_id_here"
APP_SECRET="your_app_secret_here"
RECIPIENT_WAID="" # Leave empty - will be set automatically
VERSION="v18.0"
PHONE_NUMBER_ID="your_phone_number_id_here"
VERIFY_TOKEN="your_custom_verify_token_here"

# OpenAI Configuration
OPENAI_API_KEY="your_openai_api_key_here"
OPENAI_ASSISTANT_ID="your_assistant_id_here"

# Optional: Customize your assistant
ASSISTANT_NAME="WhatsApp AI Assistant"
ASSISTANT_INSTRUCTIONS="You're a helpful WhatsApp assistant. Be friendly, concise, and helpful in your responses."
```

### 3.2 Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 4: Webhook Setup

### 4.1 Start Your App
```bash
python run.py
```
Your app will run on `http://localhost:8000`

### 4.2 Set Up ngrok
1. Sign up at [ngrok.com](https://ngrok.com/)
2. Download and authenticate ngrok
3. Create a static domain (free tier available)
4. Run ngrok:
```bash
ngrok http 8000 --domain your-domain.ngrok-free.app
```

### 4.3 Configure Webhook
1. In your Meta App Dashboard, go to **WhatsApp** → **Configuration**
2. Click **Edit** next to Webhook
3. Set **Callback URL**: `https://your-domain.ngrok-free.app/webhook`
4. Set **Verify Token**: Use the same value as in your `.env` file
5. Click **Verify and Save**
6. Go to **Manage** and subscribe to **messages** field
7. Test the webhook by clicking **Test**

## Step 5: Testing

### 5.1 Test the Integration
1. Add your WhatsApp number to contacts
2. Send a message to your WhatsApp Business number
3. Check your app logs for incoming messages
4. Verify you receive an AI-generated response

### 5.2 Troubleshooting
- **Webhook not receiving messages**: Check ngrok URL and webhook configuration
- **Messages not sending**: Verify ACCESS_TOKEN and PHONE_NUMBER_ID
- **AI not responding**: Check OPENAI_API_KEY and OPENAI_ASSISTANT_ID
- **Thread errors**: Check if threads_db file is writable

## Step 6: Production Deployment

### 6.1 Get Production Phone Number
1. Go to [business.facebook.com/wa/manage/home/](https://business.facebook.com/wa/manage/home/)
2. Add a phone number to your WhatsApp Business Account
3. Update your `.env` with the new PHONE_NUMBER_ID

### 6.2 Deploy to Production
- Use a proper hosting service (Heroku, AWS, etc.)
- Set up a domain with SSL
- Update webhook URL to your production domain
- Use environment variables for sensitive data

## File Structure

```
python-whatsapp-bot/
├── app/
│   ├── config.py              # Configuration loading
│   ├── views.py               # Webhook endpoints
│   ├── services/
│   │   └── openai_service.py  # OpenAI integration
│   └── utils/
│       └── whatsapp_utils.py  # WhatsApp message handling
├── start/
│   ├── setup_assistant.py     # Assistant creation script
│   └── assistants_quickstart.py # Example usage
├── .env                       # Your environment variables
├── run.py                     # Flask app entry point
└── requirements.txt           # Python dependencies
```

## Customization

### Custom Assistant Instructions
Update `ASSISTANT_INSTRUCTIONS` in your `.env` file to customize your bot's personality and behavior.

### Knowledge Base
Upload files to your assistant for domain-specific knowledge:
1. Run `python start/setup_assistant.py`
2. Choose to upload a file when prompted
3. The assistant will use this knowledge to answer questions

### Message Processing
Modify `process_whatsapp_message()` in `app/utils/whatsapp_utils.py` to add custom logic before/after AI responses.

## Support

- **WhatsApp API Docs**: [developers.facebook.com/docs/whatsapp](https://developers.facebook.com/docs/whatsapp)
- **OpenAI API Docs**: [platform.openai.com/docs](https://platform.openai.com/docs)
- **Meta Developer Community**: [developers.facebook.com/community](https://developers.facebook.com/community) 