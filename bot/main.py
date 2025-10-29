#!/usr/bin/env python3
"""
Main bot script that orchestrates the daily crypto content generation and sending.
"""

import os
import sys
import logging
import traceback
from datetime import datetime

from perplexity_client import PerplexityClient
from telegram_client import TelegramClient
from utils import validate_content_length, format_for_telegram

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the daily crypto bot."""
    try:
        # Validate environment variables
        required_env_vars = [
            'PERPLEXITY_API_KEY',
            'TELEGRAM_BOT_TOKEN', 
            'TELEGRAM_CHAT_ID'
        ]
        
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            logger.error(f"Missing required environment variables: {missing_vars}")
            sys.exit(1)
            
        logger.info("Starting daily crypto bot execution...")
        logger.info(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
        
        # Initialize clients
        perplexity = PerplexityClient(os.getenv('PERPLEXITY_API_KEY'))
        telegram = TelegramClient(
            os.getenv('TELEGRAM_BOT_TOKEN'),
            os.getenv('TELEGRAM_CHAT_ID')
        )
        
        # Test connections first
        logger.info("Testing API connections...")
        
        if not perplexity.test_connection():
            logger.error("Perplexity API connection failed")
            sys.exit(1)
        logger.info("✅ Perplexity API connection successful")
        
        if not telegram.test_connection():
            logger.error("Telegram bot connection failed")
            sys.exit(1)
        logger.info("✅ Telegram bot connection successful")
        
        # Get crypto market content
        logger.info("Fetching crypto market content from Perplexity...")
        content_data = perplexity.get_crypto_news_content()
        
        if not content_data:
            logger.error("Failed to get crypto content from Perplexity")
            sys.exit(1)
            
        # Log content details
        logger.info(f"Content generated successfully:")
        logger.info(f"- Character count: {content_data.get('char_count', 'unknown')}")
        logger.info(f"- Has image: {'Yes' if content_data.get('image_url') else 'No'}")
        logger.info(f"- Content preview: {content_data['text'][:100]}...")
        
        # Validate content length (max 1000 characters)
        if not validate_content_length(content_data['text']):
            logger.error(f"Content exceeds 1000 character limit: {len(content_data['text'])} chars")
            sys.exit(1)
            
        # Format content for Telegram
        formatted_text = format_for_telegram(content_data['text'])
        
        # Send to Telegram
        logger.info("Sending crypto content to Telegram...")
        success = telegram.send_content(
            text=formatted_text,
            image_url=content_data.get('image_url')
        )
        
        if success:
            logger.info("🎉 Crypto content sent successfully!")
            logger.info(f"Final message length: {len(formatted_text)} characters")
        else:
            logger.error("❌ Failed to send content to Telegram")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
