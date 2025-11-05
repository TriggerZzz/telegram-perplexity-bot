#!/usr/bin/env python3
"""
Enhanced main bot script with improved logging and error handling.
"""

import os
import sys
import logging
from datetime import datetime

from perplexity_client import PerplexityClient
from telegram_client import TelegramClient

# Enhanced logging configuration
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def main():
    """Enhanced main function with better formatting support.""" 
    try:
        logger.info("🚀 Starting Enhanced Crypto News Bot")
        logger.info(f"⏰ Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
        logger.info("📋 New features: Enhanced formatting, unique images, 17:00 UTC schedule")
        
        # Validate environment
        api_key = os.getenv('PERPLEXITY_API_KEY')
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not all([api_key, bot_token, chat_id]):
            logger.error("❌ Missing environment variables")
            sys.exit(1)
        
        logger.info("✅ Environment variables validated")
        
        # Initialize enhanced clients
        perplexity = PerplexityClient(api_key)
        telegram = TelegramClient(bot_token, chat_id)
        
        # Test connections
        logger.info("🔗 Testing enhanced API connections...")
        
        if not perplexity.test_connection():
            logger.error("❌ Perplexity connection failed")
            sys.exit(1)
        
        if not telegram.test_connection():  
            logger.error("❌ Telegram connection failed")
            sys.exit(1)
        
        # Generate enhanced content
        logger.info("📰 Generating enhanced crypto content...")
        content = perplexity.get_crypto_news_content()
        
        if not content:
            logger.error("❌ No enhanced content generated")
            sys.exit(1)
        
        # Log content details
        logger.info(f"✅ Enhanced content generated:")
        logger.info(f"   📏 Characters: {content['char_count']}")
        logger.info(f"   🖼️  Has image: {'Yes' if content.get('image_url') else 'No'}")
        logger.info(f"   📝 Preview: {content['text'][:80]}...")
        
        # Send enhanced content
        logger.info("📤 Sending enhanced content to Telegram...")
        success = telegram.send_content(
            text=content['text'],
            image_url=content.get('image_url')
        )
        
        if success:
            logger.info("🎉 Enhanced crypto content sent successfully!")
            logger.info("📈 Features delivered:")
            logger.info("   ✅ Structured title with date")
            logger.info("   ✅ Bullet point format")
            logger.info("   ✅ Proper hashtag spacing")
            logger.info("   ✅ Unique image generation")
            logger.info("   ✅ 17:00 UTC scheduling")
        else:
            logger.error("❌ Failed to send enhanced content")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"💥 Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
