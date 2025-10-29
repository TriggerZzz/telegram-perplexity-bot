"""
Utility functions for the bot.
"""

import random
from datetime import datetime
from typing import List

def generate_daily_topic() -> str:
    """Generate a topic for today's content based on day of week and trends."""
    
    # Topic categories with engaging subjects
    topics = {
        'monday': [
            "Summarize today's top global news about crypto market. Include major economic events, and highlight any breaking news about future events, at the end of the article include these two hashtags #CryptoNews #MarketOverview" 
        ],
        'tuesday': [
            "Summarize today's top global news about crypto market. Include major economic events, and highlight any breaking news about future events, at the end of the article include these two hashtags #CryptoNews #MarketOverview"
        ],
        'wednesday': [
            "Summarize today's top global news about crypto market. Include major economic events, and highlight any breaking news about future events, at the end of the article include these two hashtags #CryptoNews #MarketOverview"
        ],
        'thursday': [
            "Summarize today's top global news about crypto market. Include major economic events, and highlight any breaking news about future events, at the end of the article include these two hashtags #CryptoNews #MarketOverview"
        ],
        'friday': [
            "Summarize today's top global news about crypto market. Include major economic events, and highlight any breaking news about future events, at the end of the article include these two hashtags #CryptoNews #MarketOverview"
        ]
    }
    
    # Get current day
    current_day = datetime.now().strftime('%A').lower()
    
    # Default to general topics if day not found
    if current_day not in topics:
        current_day = 'monday'
        
    # Select random topic for the day
    selected_topic = random.choice(topics[current_day])
    
    return selected_topic

def validate_content_length(text: str, max_length: int = 1000) -> bool:
    """Validate that content is within character limit."""
    return len(text) <= max_length

def truncate_text(text: str, max_length: int = 1000) -> str:
    """Truncate text to fit within character limit while preserving word boundaries."""
    if len(text) <= max_length:
        return text
        
    # Find the last space before the limit
    truncated = text[:max_length]
    last_space = truncated.rfind(' ')
    
    if last_space > 0:
        truncated = truncated[:last_space]
        
    return truncated + "..."

def format_for_telegram(text: str) -> str:
    """Format text for Telegram with basic HTML formatting."""
    # Add some basic formatting
    # This is a simple implementation - you can expand it
    formatted = text
    
    # Make first line bold if it looks like a title
    lines = formatted.split('\n')
    if lines and len(lines) < 100:
        lines = f"<b>{lines}</b>"
        formatted = '\n'.join(lines)
    
    return formatted
