#!/usr/bin/env python3
"""
Main bot script - BULLETPROOF VERSION
"""

import os
import sys
import logging
import traceback
from datetime import datetime

from perplexity_client import PerplexityClient
from telegram_client import TelegramClient
from utils import validate_content_length, format_for_telegram

# Enhanced logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    """BULLETPROOF main function."""
    try:
        logger.info("🚀 STARTING BULLETPROOF CRYPTO BOT")
        logger.info(f"⏰ Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
        
        # Validate environment variables
        required_vars = ['PERPLEXITY_API_KEY', 'TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.error(f"❌ Missing environment variables: {missing_vars}")
            sys.exit(1)
        
        logger.info("✅ All environment variables present")
        
        # Initialize clients with error handling
        try:
            perplexity = PerplexityClient(os.getenv('PERPLEXITY_API_KEY'))
            logger.info("✅ Perplexity client initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Perplexity client: {e}")
            sys.exit(1)
        
        try:
            telegram = TelegramClient(os.getenv('TELEGRAM_BOT_TOKEN'), os.getenv('TELEGRAM_CHAT_ID'))
            logger.info("✅ Telegram client initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Telegram client: {e}")
            sys.exit(1)
        
        # Test connections
        logger.info("🔗 Testing API connections...")
        
        if not perplexity.test_connection():
            logger.error("❌ Perplexity API connection failed")
            sys.exit(1)
        logger.info("✅ Perplexity API connection successful")
        
        if not telegram.test_connection():
            logger.error("❌ Telegram bot connection failed")
            sys.exit(1)
        logger.info("✅ Telegram bot connection successful")
        
        # Generate content
        logger.info("📰 Generating crypto market content...")
        content_data = perplexity.get_crypto_news_content()
        
        if not content_data:
            logger.error("❌ Failed to generate crypto content")
            sys.exit(1)
        
        # Validate content
        text = content_data.get('text', '')
        if not text:
            logger.error("❌ Generated content is empty")
            sys.exit(1)
        
        if not validate_content_length(text):
            logger.error(f"❌ Content exceeds limit: {len(text)} characters")
            sys.exit(1)
        
        logger.info(f"✅ Content validation passed: {len(text)} characters")
        
        # Format and send
        formatted_text = format_for_telegram(text)
        image_url = content_data.get('image_url')
        
        logger.info("📤 Sending content to Telegram...")
        success = telegram.send_content(text=formatted_text, image_url=image_url)
        
        if success:
            logger.info("🎉 SUCCESS! Crypto content sent to Telegram!")
            logger.info(f"📊 Final stats:")
            logger.info(f"   - Character count: {len(formatted_text)}")
            logger.info(f"   - Has image: {'Yes' if image_url else 'No'}")
            logger.info(f"   - Preview: {formatted_text[:50]}...")
        else:
            logger.error("❌ Failed to send content to Telegram")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("👋 Bot execution interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"💥 CRITICAL ERROR: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    main()
