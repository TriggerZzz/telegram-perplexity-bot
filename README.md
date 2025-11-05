# 🚀 Crypto News Bot - Automated Daily Market Analysis

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-blue)](https://github.com/features/actions)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue)](https://core.telegram.org/bots)
[![Perplexity API](https://img.shields.io/badge/Perplexity-API-green)](https://perplexity.ai)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Professional cryptocurrency market analysis delivered automatically to your Telegram channel every weekday at 17:00 UTC**

## 📈 Features

- **🤖 Fully Automated**: Runs daily via GitHub Actions - no manual intervention required
- **📊 Real-time Analysis**: Powered by Perplexity PRO API with live market data
- **🎯 Professional Format**: Structured content with title, date, bullet points, and hashtags
- **📱 Telegram Integration**: Direct publishing to your Telegram channel
- **🖼️ Dynamic Images**: Unique crypto-themed images for every post
- **⏰ Scheduled Posts**: Daily execution Monday-Friday at 17:00 UTC
- **🔧 Zero Maintenance**: Set it and forget it - runs automatically forever

## 📋 Content Structure

Each daily post includes:

```
📈 **Crypto Market Analysis**
📅 *November 06, 2025*

• Bitcoin demonstrates resilience above $67,000 with institutional accumulation patterns
• Ethereum shows network strength at $2,600 with increasing Layer 2 adoption
• Major altcoins including BNB, XRP, SOL display mixed signals across sectors
• Market sentiment remains cautiously optimistic with balanced Fear & Greed Index
• DeFi protocols report increased TVL while AI tokens attract institutional interest
• Technical analysis reveals key support levels holding firm for consolidation

*#CryptoNews #MarketOverview*
```

## 🚀 Quick Start

### Prerequisites

- GitHub account (free)
- Telegram bot token from [@BotFather](https://t.me/BotFather)
- Perplexity PRO subscription with API access
- Telegram channel to publish content

### 1. Fork This Repository

Click the **Fork** button at the top of this repository to create your own copy.

### 2. Get Your API Keys

**Perplexity API Key:**
1. Sign up for [Perplexity PRO](https://perplexity.ai)
2. Go to Settings → API → Create API Key
3. Copy your API key (format: `pplx-...`)

**Telegram Bot Token:**
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Create a new bot with `/newbot`
3. Copy your bot token (format: `123456789:ABC...`)

**Telegram Chat ID:**
1. Add your bot to your channel as an administrator
2. Send a test message in your channel
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Find your chat ID in the response (format: `-1001234567890`)

### 3. Configure GitHub Secrets

In your forked repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** and add:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `PERPLEXITY_API_KEY` | Your Perplexity PRO API key | `pplx-abc123...` |
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token | `123456789:ABC...` |
| `TELEGRAM_CHAT_ID` | Your channel/chat ID | `-1001234567890` |

### 4. Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. Click **Enable workflows**
3. The bot will automatically run Monday-Friday at 17:00 UTC

### 5. Test Your Setup

Click **Actions** → **Daily Telegram Bot** → **Run workflow** to test immediately.

## 🛠️ Configuration

### Customize Schedule

Edit `.github/workflows/daily-bot.yml`:

```yaml
schedule:
  - cron: '0 17 * * 1-5'  # 17:00 UTC, Monday-Friday
```

### Modify Content Style

Edit `bot/perplexity_client.py` to customize:
- Content length (currently ~1000 characters)
- Bullet point structure
- Market focus areas
- Hashtags

### Change Posting Format

Edit formatting in `bot/telegram_client.py`:
- Markdown styles
- Image handling
- Error messaging

## 📊 Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub Actions │────│  Perplexity API │────│  Telegram Bot   │
│   (Scheduler)    │    │ (Content Gen)   │    │  (Publisher)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
   Runs at 17:00 UTC        Generates Analysis       Posts to Channel
   Monday - Friday          1000 chars + Image       Professional Format
```

### Core Components

- **`bot/main.py`**: Main orchestration script
- **`bot/perplexity_client.py`**: Perplexity API integration
- **`bot/telegram_client.py`**: Telegram bot functionality
- **`bot/utils.py`**: Utility functions
- **`.github/workflows/daily-bot.yml`**: GitHub Actions workflow

## 📈 Sample Output

The bot generates professional crypto market analysis with:

- **Comprehensive Coverage**: Bitcoin, Ethereum, altcoins, DeFi, market sentiment
- **Technical Analysis**: Support/resistance levels, indicators, price targets
- **Institutional Insights**: Regulatory updates, adoption news, ETF flows
- **Visual Appeal**: Crypto-themed images, professional formatting
- **Engagement Ready**: Optimized for Telegram with hashtags and emojis

## 🔧 Troubleshooting

### Bot Not Posting

1. **Check GitHub Actions**: Go to Actions tab, verify workflow runs
2. **Verify Secrets**: Ensure all three secrets are properly set
3. **Bot Permissions**: Confirm bot is admin in your channel
4. **API Credits**: Check Perplexity account has available credits

### Content Issues

1. **Character Limit**: Posts are capped at 1000 characters
2. **Image Loading**: Uses multiple fallback image sources
3. **API Limits**: Perplexity has rate limits on API calls

### Common Fixes

```bash
# Test bot locally (optional)
python bot/main.py

# Check API connectivity
curl -H "Authorization: Bearer YOUR_API_KEY" https://api.perplexity.ai/chat/completions
```

## 💰 Cost Breakdown

- **GitHub Actions**: Free tier includes 2000 minutes/month
- **Perplexity PRO**: $20/month (includes API access)
- **Telegram Bot**: Free
- **Total Monthly Cost**: ~$20 (just Perplexity PRO)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- [Perplexity AI](https://perplexity.ai) - Real-time market data and analysis
- [Telegram Bot API](https://core.telegram.org/bots/api) - Messaging platform
- [GitHub Actions](https://github.com/features/actions) - Free automation platform
- [Unsplash](https://unsplash.com) - High-quality crypto images

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/TriggerZzz/crypto-news-bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/TriggerZzz/crypto-news-bot/discussions)
- **Telegram**: [@channel1700UTC](https://t.me/channel1700UTC) - See the bot in action!

---

<div align="center">

**Made with ❤️ for the crypto community**

[⭐ Star this repo](https://github.com/TriggerZzz/crypto-news-bot) • [🐛 Report Bug](https://github.com/TriggerZzz/crypto-news-bot/issues) • [✨ Request Feature](https://github.com/TriggerZzz/crypto-news-bot/issues)

</div>