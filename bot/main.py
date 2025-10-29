#!/usr/bin/env python3
"""
Main bot script - SIMPLIFIED WORKING VERSION
"""

import os
import sys
import logging

from perplexity_client import PerplexityClient
from telegram_client import TelegramClient

# Simple logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main function - simplified and working."""
    try:
        logger.info("🚀 Starting Crypto Bot...")
        
        # Check environment
        api_key = os.getenv('PERPLEXITY_API_KEY')
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not all([api_key, bot_token, chat_id]):
            logger.error("❌ Missing environment variables")
            sys.exit(1)
        
        # Initialize clients
        perplexity = PerplexityClient(api_key)
        telegram = TelegramClient(bot_token, chat_id)
        
        # Test connections
        if not perplexity.test_connection():
            logger.error("❌ Perplexity connection failed")
            sys.exit(1)
        
        if not telegram.test_connection():
            logger.error("❌ Telegram connection failed")
            sys.exit(1)
        
        # Get content
        logger.info("📰 Getting crypto content...")
        content = perplexity.get_crypto_news_content()
        
        if not content:
            logger.error("❌ No content generated")
            sys.exit(1)
        
        # Send to Telegram
        logger.info("📤 Sending to Telegram...")
        success = telegram.send_content(
            text=content['text'],
            image_url=content.get('image_url')
        )
        
        if success:
            logger.info("🎉 SUCCESS! Content sent!")
        else:
            logger.error("❌ Failed to send")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"💥 Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
