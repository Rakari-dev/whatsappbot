# 🤖 WhatsApp Job Board Bot

An automated WhatsApp chatbot that connects job seekers with employers through real-time job matching and notifications.

## ✨ Features

- **Job Seeker Registration**: Users can register their preferred role and location
- **Job Posting**: Employers can post job openings instantly
- **Smart Matching**: Automatic matching between job seekers and relevant opportunities
- **Real-time Alerts**: Instant WhatsApp notifications when matching jobs are posted
- **Command-based Interface**: Simple, intuitive commands for all interactions

## 🏗️ Architecture

```
WhatsappBot/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── bot/
│   │   ├── message_handler.py   # Webhook & message processing
│   │   ├── commands.py          # Command parsing & validation
│   │   └── notifications.py     # Alert sending logic
│   ├── models/
│   │   ├── user.py             # Job seeker model
│   │   └── job.py              # Job posting model
│   └── services/
│       ├── twilio_service.py   # WhatsApp messaging via Twilio
│       └── matcher_service.py  # Job matching logic
├── config/
│   └── config.py               # Configuration management
├── tests/
│   └── test_bot.py            # Unit tests
├── requirements.txt           # Python dependencies
└── run.py                    # Application entry point
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Twilio account with WhatsApp Sandbox access
- ngrok (for local development)

### 1. Clone & Setup

```bash
git clone <repository-url>
cd Whatsappbot
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your Twilio credentials:

```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+14155238886
SECRET_KEY=your-secret-key
DEBUG=True
```

### 3. Run the Application

```bash
python run.py
```

The server will start on `http://localhost:5000`

### 4. Setup Webhook (Local Development)

1. Install and run ngrok:
```bash
ngrok http 5000
```

2. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

3. In Twilio Console:
   - Go to WhatsApp Sandbox Settings
   - Set webhook URL to: `https://abc123.ngrok.io/webhook`
   - Set HTTP method to `POST`

## 📱 Usage

### For Job Seekers

**Register for job alerts:**
```
register developer london
```

**Update preferences:**
```
register designer paris
```

### For Employers

**Post a job:**
```
post developer london
```

### General Commands

**Get help:**
```
help
```

## 🔧 API Endpoints

- `POST /webhook` - Main WhatsApp webhook endpoint
- `GET /status` - Health check and statistics

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

Or run specific tests:

```bash
python -m unittest tests.test_bot.TestCommandParser
```

## 📊 Example Workflow

1. **Job Seeker Registration:**
   ```
   User: "register developer london"
   Bot: "✅ Registration Successful! You're now registered for Developer in London"
   ```

2. **Job Posting:**
   ```
   Employer: "post developer london"
   Bot: "✅ Job Posted Successfully! 3 job seekers have been notified!"
   ```

3. **Automatic Alert:**
   ```
   Bot → Job Seekers: "🎯 New Job Alert!
   Role: Developer
   Location: London
   Posted: 2024-01-15 14:30"
   ```

## 🚀 Deployment

### Option 1: Render

1. Connect your GitHub repository to Render
2. Set environment variables in Render dashboard
3. Deploy as a Web Service

### Option 2: Heroku

```bash
heroku create your-app-name
heroku config:set TWILIO_ACCOUNT_SID=your_sid
heroku config:set TWILIO_AUTH_TOKEN=your_token
heroku config:set TWILIO_PHONE_NUMBER=your_number
git push heroku main
```

### Option 3: Railway

1. Connect repository to Railway
2. Set environment variables
3. Deploy automatically

## 🔒 Security Considerations

- Never commit `.env` file to version control
- Use strong secret keys in production
- Validate all incoming webhook requests
- Implement rate limiting for production use
- Consider adding user authentication for sensitive operations

## 📈 Scaling Considerations

For production use, consider:

- **Database**: Replace in-memory storage with PostgreSQL/MongoDB
- **Caching**: Add Redis for session management
- **Queue System**: Use Celery for background job processing
- **Monitoring**: Add logging and error tracking (Sentry)
- **Load Balancing**: Use multiple server instances

## 🛠️ Development

### Adding New Commands

1. Add parsing logic in `app/bot/commands.py`
2. Add handler in `app/bot/message_handler.py`
3. Add tests in `tests/test_bot.py`

### Adding New Features

1. Create new models in `app/models/`
2. Add business logic in `app/services/`
3. Update message handlers as needed
4. Add comprehensive tests

## 🐛 Troubleshooting

### Common Issues

**Webhook not receiving messages:**
- Check ngrok is running and URL is correct
- Verify Twilio webhook configuration
- Check server logs for errors

**Messages not sending:**
- Verify Twilio credentials
- Check account balance
- Ensure phone numbers are in correct format

**Bot not responding:**
- Check command format (case-insensitive)
- Verify server is running
- Check application logs

### Debugging

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review Twilio WhatsApp documentation
- Open an issue on GitHub

---

**Built with ❤️ using Flask, Twilio, and Python** 