"""
Utility functions for the crypto bot.
"""

import re
from datetime import datetime
from typing import List

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
    """Format text for Telegram with enhanced formatting for crypto content."""
    formatted = text.strip()
    
    # Enhanced formatting for crypto content
    # Bold currency symbols and prices
    formatted = re.sub(r'\$([0-9,]+\.?[0-9]*)', r'<b>$\1</b>', formatted)
    formatted = re.sub(r'(Bitcoin|BTC|Ethereum|ETH|Binance|BNB)', r'<b>\1</b>', formatted)
    
    # Format percentages
    formatted = re.sub(r'([+-]?[0-9]+\.?[0-9]*%)', r'<i>\1</i>', formatted)
    
    # Make hashtags stand out (though they should already be at the end)
    formatted = re.sub(r'(#\w+)', r'<b>\1</b>', formatted)
    
    return formatted

def get_crypto_terms() -> List[str]:
    """Get list of crypto-related terms for image generation."""
    return [
        "cryptocurrency market analysis",
        "bitcoin trading charts", 
        "blockchain technology finance",
        "crypto exchange dashboard",
        "digital currency trends",
        "financial market data",
        "trading indicators crypto",
        "bitcoin price chart",
        "ethereum market analysis",
        "crypto market overview"
    ]

def clean_api_response(text: str) -> str:
    """Clean API response text for better formatting."""
    # Remove markdown formatting that might interfere
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Remove bold markdown
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Remove italic markdown
    
    # Ensure single spacing
    text = re.sub(r'\s+', ' ', text)
    
    # Clean up any extra punctuation
    text = re.sub(r'\.{2,}', '.', text)
    
    return text.strip()

def validate_crypto_content(content: str) -> bool:
    """Validate that content contains relevant crypto information."""
    crypto_keywords = [
        'bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'cryptocurrency', 
        'blockchain', 'market', 'price', 'trading', 'exchange', 'digital currency'
    ]
    
    content_lower = content.lower()
    return any(keyword in content_lower for keyword in crypto_keywords)

def get_current_date_context() -> str:
    """Get current date context for crypto news."""
    now = datetime.now()
    return f"{now.strftime('%B %d, %Y')} ({now.strftime('%A')})"
