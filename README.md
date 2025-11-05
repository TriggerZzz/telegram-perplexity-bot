🚀 Crypto News Bot - Automated Daily Market Analysis
GitHub Actions
Telegram Bot
Perplexity API
Python 3.11
License: MIT

Professional cryptocurrency market analysis delivered automatically to your Telegram channel every weekday at 17:00 UTC

📈 Features
🤖 Fully Automated: Runs daily via GitHub Actions - no manual intervention required

📊 Real-time Analysis: Powered by Perplexity PRO API with live market data

🎯 Professional Format: Structured content with title, date, bullet points, and hashtags

📱 Telegram Integration: Direct publishing to your Telegram channel

🖼️ Dynamic Images: Unique crypto-themed images for every post

⏰ Scheduled Posts: Daily execution Monday-Friday at 17:00 UTC

🔧 Zero Maintenance: Set it and forget it - runs automatically forever

📋 Content Structure
Each daily post includes:

text
📈 **Crypto Market Analysis**
📅 *November 06, 2025*

• Bitcoin demonstrates resilience above $67,000 with institutional accumulation patterns
• Ethereum shows network strength at $2,600 with increasing Layer 2 adoption
• Major altcoins including BNB, XRP, SOL display mixed signals across sectors
• Market sentiment remains cautiously optimistic with balanced Fear & Greed Index
• DeFi protocols report increased TVL while AI tokens attract institutional interest
• Technical analysis reveals key support levels holding firm for consolidation

*#CryptoNews #MarketOverview*
🚀 Quick Start
Prerequisites
GitHub account (free)

Telegram bot token from @BotFather

Perplexity PRO subscription with API access

Telegram channel to publish content

1. Fork This Repository
Click the Fork button at the top of this repository to create your own copy.

2. Get Your API Keys
Perplexity API Key:

Sign up for Perplexity PRO

Go to Settings → API → Create API Key

Copy your API key (format: pplx-...)

Telegram Bot Token:

Message @BotFather on Telegram

Create a new bot with /newbot

Copy your bot token (format: 123456789:ABC...)

Telegram Chat ID:

Add your bot to your channel as an administrator

Send a test message in your channel

Visit: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates

Find your chat ID in the response (format: -1001234567890)

3. Configure GitHub Secrets
In your forked repository:

Go to Settings → Secrets and variables → Actions

Click New repository secret and add:

Secret Name	Description	Example
PERPLEXITY_API_KEY	Your Perplexity PRO API key	pplx-abc123...
TELEGRAM_BOT_TOKEN	Your Telegram bot token	123456789:ABC...
TELEGRAM_CHAT_ID	Your channel/chat ID	-1001234567890
4. Enable GitHub Actions
Go to the Actions tab in your repository

Click Enable workflows

The bot will automatically run Monday-Friday at 17:00 UTC

5. Test Your Setup
Click Actions → Daily Telegram Bot → Run workflow to test immediately.

🛠️ Configuration
Customize Schedule
Edit .github/workflows/daily-bot.yml:

text
schedule:
  - cron: '0 17 * * 1-5'  # 17:00 UTC, Monday-Friday
Modify Content Style
Edit bot/perplexity_client.py to customize:

Content length (currently ~1000 characters)

Bullet point structure

Market focus areas

Hashtags

Change Posting Format
Edit formatting in bot/telegram_client.py:

Markdown styles

Image handling

Error messaging

📊 Architecture
text
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub Actions │────│  Perplexity API │────│  Telegram Bot   │
│   (Scheduler)    │    │ (Content Gen)   │    │  (Publisher)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
   Runs at 17:00 UTC        Generates Analysis       Posts to Channel
   Monday - Friday          1000 chars + Image       Professional Format
Core Components
bot/main.py: Main orchestration script

bot/perplexity_client.py: Perplexity API integration

bot/telegram_client.py: Telegram bot functionality

bot/utils.py: Utility functions

.github/workflows/daily-bot.yml: GitHub Actions workflow

📈 Sample Output
The bot generates professional crypto market analysis with:

Comprehensive Coverage: Bitcoin, Ethereum, altcoins, DeFi, market sentiment

Technical Analysis: Support/resistance levels, indicators, price targets

Institutional Insights: Regulatory updates, adoption news, ETF flows

Visual Appeal: Crypto-themed images, professional formatting

Engagement Ready: Optimized for Telegram with hashtags and emojis

🔧 Troubleshooting
Bot Not Posting
Check GitHub Actions: Go to Actions tab, verify workflow runs

Verify Secrets: Ensure all three secrets are properly set

Bot Permissions: Confirm bot is admin in your channel

API Credits: Check Perplexity account has available credits

Content Issues
Character Limit: Posts are capped at 1000 characters

Image Loading: Uses multiple fallback image sources

API Limits: Perplexity has rate limits on API calls

Common Fixes
bash
# Test bot locally (optional)
python bot/main.py

# Check API connectivity
curl -H "Authorization: Bearer YOUR_API_KEY" https://api.perplexity.ai/chat/completions
💰 Cost Breakdown
GitHub Actions: Free tier includes 2000 minutes/month

Perplexity PRO: $20/month (includes API access)

Telegram Bot: Free

Total Monthly Cost: ~$20 (just Perplexity PRO)

🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🌟 Acknowledgments
Perplexity AI - Real-time market data and analysis

Telegram Bot API - Messaging platform

GitHub Actions - Free automation platform

Unsplash - High-quality crypto images

📞 Support
Issues: GitHub Issues

Discussions: GitHub Discussions

<div align="center">
Made with ❤️ for the crypto community

⭐ Star this repo • 🐛 Report Bug • ✨ Request Feature

</div>
