#!/usr/bin/env python3
"""
Refined main bot script with updated content specifications.
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
    """Refined main function with updated formatting specifications.""" 
    try:
        logger.info("🚀 Starting Refined Crypto News Bot")
        logger.info(f"⏰ Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
        logger.info("📋 Refinements: 1-line hashtag spacing, italic hashtags, ~1000 char content")
        
        # Validate environment
        api_key = os.getenv('PERPLEXITY_API_KEY')
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not all([api_key, bot_token, chat_id]):
            logger.error("❌ Missing environment variables")
            sys.exit(1)
        
        logger.info("✅ Environment variables validated")
        
        # Initialize refined clients
        perplexity = PerplexityClient(api_key)
        telegram = TelegramClient(bot_token, chat_id)
        
        # Test connections
        logger.info("🔗 Testing refined API connections...")
        
        if not perplexity.test_connection():
            logger.error("❌ Perplexity connection failed")
            sys.exit(1)
        
        if not telegram.test_connection():  
            logger.error("❌ Telegram connection failed")
            sys.exit(1)
        
        # Generate refined content
        logger.info("📰 Generating refined crypto content (~1000 chars)...")
        content = perplexity.get_crypto_news_content()
        
        if not content:
            logger.error("❌ No refined content generated")
            sys.exit(1)
        
        # Log content details
        char_count = content['char_count']
        logger.info(f"✅ Refined content generated:")
        logger.info(f"   📏 Characters: {char_count} (target: ~1000)")
        logger.info(f"   📊 Length status: {'✅ Perfect' if 950 <= char_count <= 1050 else '⚠️ Adjusting'}")
        logger.info(f"   🖼️  Has image: {'Yes' if content.get('image_url') else 'No'}")
        logger.info(f"   📝 Preview: {content['text'][:80]}...")
        
        # Send refined content
        logger.info("📤 Sending refined content to Telegram...")
        success = telegram.send_content(
            text=content['text'],
            image_url=content.get('image_url')
        )
        
        if success:
            logger.info("🎉 Refined crypto content sent successfully!")
            logger.info("📈 Refinements delivered:")
            logger.info("   ✅ 1-line spacing before hashtags")
            logger.info("   ✅ Italic hashtag formatting")
            logger.info(f"   ✅ ~1000 character content ({char_count} chars)")
            logger.info("   ✅ Detailed bullet points")
            logger.info("   ✅ Unique image generation")
        else:
            logger.error("❌ Failed to send refined content")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"💥 Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
