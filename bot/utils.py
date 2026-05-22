"""
Utility functions - SIMPLIFIED VERSION
"""

def validate_content_length(text: str, max_length: int = 1000) -> bool:
    """Validate content length."""
    return len(text) <= max_length

def format_for_telegram(text: str) -> str:
    """Format text for Telegram."""
    return text.strip()
