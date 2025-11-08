# 🚀 Crypto News Bot - Automated Daily Market News

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-blue)](https://github.com/features/actions)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue)](https://core.telegram.org/bots)
[![Perplexity API](https://img.shields.io/badge/Perplexity-API-green)](https://perplexity.ai)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Professional cryptocurrency news summaries delivered automatically to your Telegram channel every weekday at 17:00 UTC**

## 📈 Features

- **🤖 Fully Automated**: Runs daily via GitHub Actions - no manual intervention required
- **📰 Real-time News**: Powered by Perplexity PRO API with live global market data
- **🎯 Professional Format**: Structured content with title, date, bullet points, and hashtags
- **📱 Telegram Integration**: Direct publishing to your Telegram channel
- **🖼️ Dynamic Images**: Unique crypto-themed images for every post
- **⏰ Scheduled Posts**: Daily execution Monday-Friday at 17:00 UTC
- **🔧 Zero Maintenance**: Set it and forget it - runs automatically forever
- **📊 Factual Reporting**: News summaries without market predictions or investment guidance

## 📋 Content Structure

Each daily post includes:

```
📈 **Crypto Market Update**
📅 *November 08, 2025*

• Bitcoin ETF sees $200M inflows as institutional adoption accelerates
• Federal Reserve maintains interest rates affecting crypto market sentiment
• Ethereum Dencun upgrade scheduled for next week with major scaling improvements
• SEC approves spot crypto ETF applications from major financial institutions
• Major global banks announce blockchain integration for cross-border payments
• Upcoming industry conference set to unveil new Layer 2 scaling solutions

*#CryptoNews #MarketOverview*
```

## 🎯 Content Focus

The bot provides **factual news summaries** including:

- **📰 Today's top global crypto news** - What happened in the market today
- **🌍 Major global economic events** - Central bank decisions, regulatory updates, institutional moves
- **📅 Breaking news about near future events** - Upcoming launches, upgrades, conferences, policy changes
- **❌ NO market predictions** - Purely factual reporting without trend guidance or investment advice

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

### Modify Content Focus

Edit `bot/perplexity_client.py` to customize:
- News focus areas (currently: global crypto news + economic events)
- Content length (currently ~800 characters raw content)
- Bullet point structure
- Hashtags

**Current Prompt:**
> "Summarize today's top global news about crypto market. Include major global economic events, and highlight any breaking news about near future events. Make an article no more than 800 characters (with spaces). Don't provide any guidance for the market trend."

### Change Posting Format

Edit formatting in `bot/telegram_client.py`:
- Markdown styles
- Image handling
- Error messaging

## 📊 Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub Actions │────│  Perplexity API │────│  Telegram Bot   │
│   (Scheduler)    │    │  (News Summary) │    │  (Publisher)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
   Runs at 17:00 UTC      Generates News        Posts to Channel
   Monday - Friday        ~1000 chars + Image    Professional Format
```

### Core Components

- **`bot/main.py`**: Main orchestration script
- **`bot/perplexity_client.py`**: Perplexity API integration with news-focused prompt
- **`bot/telegram_client.py`**: Telegram bot functionality with Markdown formatting
- **`bot/utils.py`**: Utility functions for content processing
- **`.github/workflows/daily-bot.yml`**: GitHub Actions workflow scheduler

## 📈 Sample Output

The bot generates professional crypto news summaries with:

- **📰 Factual News Coverage**: What happened today in global crypto markets
- **🌍 Economic Context**: Federal Reserve decisions, regulatory updates, institutional moves
- **📅 Future Events**: Upcoming protocol upgrades, product launches, industry conferences
- **🎨 Visual Appeal**: Crypto-themed images with professional formatting
- **📱 Mobile Optimized**: Perfect formatting for Telegram with hashtags and emojis
- **❌ No Predictions**: Pure news reporting without market trend guidance

## 🔧 Troubleshooting

### Bot Not Posting

1. **Check GitHub Actions**: Go to Actions tab, verify workflow runs without errors
2. **Verify Secrets**: Ensure all three secrets are properly set in repository settings
3. **Bot Permissions**: Confirm bot is administrator in your Telegram channel
4. **API Credits**: Check Perplexity account has available API credits

### Content Issues

1. **Character Limit**: Raw content is 800 chars, final formatted output ~1000 chars
2. **Image Loading**: Uses multiple fallback image sources for reliability
3. **API Limits**: Perplexity has rate limits - bot runs once per day to stay within limits

### Common Fixes

```bash
# Test bot locally (requires environment variables)
export PERPLEXITY_API_KEY="your_key"
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_chat_id"
python bot/main.py

# Check API connectivity
curl -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model":"sonar-pro","messages":[{"role":"user","content":"Test"}],"max_tokens":10}' \
     https://api.perplexity.ai/chat/completions
```

### Logs and Debugging

- Check **Actions** tab for detailed execution logs
- Look for API response codes (200 = success)
- Verify content generation and Telegram delivery steps
- Common issues: expired API keys, bot removed from channel, incorrect chat ID

## 💰 Cost Breakdown

- **GitHub Actions**: Free tier includes 2000 minutes/month (plenty for daily bot)
- **Perplexity PRO**: $20/month (includes API access + search capabilities)
- **Telegram Bot**: 100% Free (no limits for bot API)
- **Total Monthly Cost**: **~$20** (only Perplexity PRO subscription)

**Cost Efficiency**: Running 5 days/week, ~20 posts/month = **$1 per post** for professional crypto news summaries!

## 🌟 Use Cases

Perfect for:

- **📢 Crypto News Channels**: Keep your community informed with daily news
- **👥 Investment Groups**: Share factual market updates without bias
- **📱 Personal Updates**: Stay informed with automated daily summaries
- **🏢 Business Intelligence**: Monitor crypto market events for decision-making
- **🎓 Educational Content**: Learn about crypto markets through daily news
- **🔍 Research Projects**: Archive daily crypto news for analysis

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Ideas for Contributions:**
- Additional news sources or APIs
- Multi-language support
- Custom filtering options
- Advanced scheduling features
- Analytics and tracking
- Alternative messaging platforms

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- [Perplexity AI](https://perplexity.ai) - Real-time global news and market data
- [Telegram Bot API](https://core.telegram.org/bots/api) - Free messaging platform
- [GitHub Actions](https://github.com/features/actions) - Free automation and scheduling
- [Unsplash](https://unsplash.com) - High-quality crypto-themed images
- [Python](https://python.org) - Reliable programming language

## 📞 Support & Community

- **Issues**: [GitHub Issues](https://github.com/TriggerZzz/telegram-perplexity-bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/TriggerZzz/telegram-perplexity-bot/discussions)
- **Telegram**: See the bot in action daily!

## 🔄 Recent Updates

**November 2025:**
- ✅ Updated prompt to focus on news summaries (no market predictions)
- ✅ Emphasized global economic events and near-future breaking news
- ✅ Maintained professional formatting with title, date, bullets, hashtags
- ✅ Content optimized for ~1000 characters total (800 raw + formatting)
- ✅ Enhanced factual reporting without investment guidance

## 🚀 Getting Started in 5 Minutes

1. **Fork** this repository ⚡
2. **Add** three secrets (API keys) 🔑
3. **Enable** GitHub Actions ▶️
4. **Run** manual test workflow ✅
5. **Enjoy** daily crypto news! 🎉

---

<div align="center">

**Made with ❤️ for the Binance Angel Dev crypto community**

[⭐ Star this repo](https://github.com/TriggerZzz/telegram-perplexity-bot) • [🐛 Report Bug](https://github.com/TriggerZzz/telegram-perplexity-bot/issues) • [✨ Request Feature](https://github.com/TriggerZzz/telegram-perplexity-bot/issues)

**Delivering factual crypto news since 2025**

</div>
