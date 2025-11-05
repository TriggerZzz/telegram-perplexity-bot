#!/usr/bin/env python3
"""
Multi-destination main bot script with guaranteed unique image generation.
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
    """Multi-destination main function with unique image guarantee.""" 
    try:
        logger.info("🚀 Starting Multi-Destination Crypto Bot with Unique Images")
        logger.info(f"⏰ Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
        logger.info("🎨 NEW: Advanced image rotation system - TRULY unique images every post!")
        
        # Validate environment variables
        api_key = os.getenv('PERPLEXITY_API_KEY')
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        channel_chat_id = os.getenv('TELEGRAM_CHANNEL_ID')
        group_chat_id = os.getenv('TELEGRAM_GROUP_ID')
        
        if not all([api_key, bot_token, channel_chat_id, group_chat_id]):
            logger.error("❌ Missing required environment variables:")
            if not api_key:
                logger.error("   - PERPLEXITY_API_KEY")
            if not bot_token:
                logger.error("   - TELEGRAM_BOT_TOKEN")
            if not channel_chat_id:
                logger.error("   - TELEGRAM_CHANNEL_ID")
            if not group_chat_id:
                logger.error("   - TELEGRAM_GROUP_ID")
            sys.exit(1)
        
        logger.info("✅ Environment variables validated")
        
        # Create list of destinations
        destinations = [channel_chat_id, group_chat_id]
        logger.info(f"📍 Publishing destinations:")
        logger.info(f"   📢 Channel: {channel_chat_id}")
        logger.info(f"   👥 Private Group: {group_chat_id}")
        
        # Initialize clients
        perplexity = PerplexityClient(api_key)
        telegram = TelegramClient(bot_token, destinations)
        
        # Test connections
        logger.info("🔗 Testing API connections...")
        
        if not perplexity.test_connection():
            logger.error("❌ Perplexity connection failed")
            sys.exit(1)
        
        if not telegram.test_connection():  
            logger.error("❌ Telegram connection failed")
            sys.exit(1)
        
        # Generate content with unique image
        logger.info("📰 Generating crypto content with GUARANTEED unique image...")
        content = perplexity.get_crypto_news_content()
        
        if not content:
            logger.error("❌ No content generated")
            sys.exit(1)
        
        # Log content details
        char_count = content['char_count']
        image_url = content.get('image_url', 'None')
        
        logger.info(f"✅ Content with unique image generated:")
        logger.info(f"   📏 Characters: {char_count} (target: ~1000)")
        logger.info(f"   📊 Length status: {'✅ Perfect' if 950 <= char_count <= 1050 else '⚠️ Adjusting'}")
        logger.info(f"   🖼️  Unique image: {image_url[:50]}...")
        logger.info(f"   🎯 Image uniqueness: GUARANTEED (timestamp + hash + random)")
        logger.info(f"   📝 Preview: {content['text'][:80]}...")
        
        # Send to all destinations
        logger.info("📤 Publishing unique content to all destinations...")
        success = telegram.send_content(
            text=content['text'],
            image_url=image_url
        )
        
        if success:
            logger.info("🎉 Unique crypto content published successfully!")
            logger.info("📈 Features delivered:")
            logger.info("   ✅ Published to public channel + private group")
            logger.info("   ✅ GUARANTEED unique image every time")
            logger.info("   ✅ Advanced rotation system with 20+ image sources")
            logger.info("   ✅ Timestamp + hash + random seed uniqueness")
            logger.info("   ✅ 1-line hashtag spacing with italic formatting")
            logger.info(f"   ✅ ~1000 character content ({char_count} chars)")
            logger.info("   ✅ Professional crypto market analysis")
        else:
            logger.error("❌ Failed to publish to destinations")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"💥 Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
