#!/usr/bin/env python3
"""
Main bot script that orchestrates the daily content generation and sending.
"""

import os
import sys
import logging
import traceback
from datetime import datetime

from perplexity_client import PerplexityClient
from telegram_client import TelegramClient
from utils import generate_daily_topic, validate_content_length

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the daily bot."""
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
            
        logger.info("Starting daily bot execution...")
        
        # Initialize clients
        perplexity = PerplexityClient(os.getenv('PERPLEXITY_API_KEY'))
        telegram = TelegramClient(
            os.getenv('TELEGRAM_BOT_TOKEN'),
            os.getenv('TELEGRAM_CHAT_ID')
        )
        
        # Generate today's topic
        topic = generate_daily_topic()
        logger.info(f"Generated topic: {topic}")
        
        # Get content from Perplexity
        logger.info("Fetching content from Perplexity...")
        content_data = perplexity.get_daily_content(topic)
        
        if not content_data:
            logger.error("Failed to get content from Perplexity")
            sys.exit(1)
            
        # Validate content length (max 1000 characters)
        if not validate_content_length(content_data['text']):
            logger.error("Content exceeds 1000 character limit")
            sys.exit(1)
            
        # Send to Telegram
        logger.info("Sending content to Telegram...")
        success = telegram.send_content(
            text=content_data['text'],
            image_url=content_data.get('image_url')
        )
        
        if success:
            logger.info("Content sent successfully!")
        else:
            logger.error("Failed to send content to Telegram")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
