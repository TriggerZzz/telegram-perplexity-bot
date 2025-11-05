"""
Refined Telegram client with updated formatting support for italic hashtags.
"""

import requests
import logging

logger = logging.getLogger(__name__)

class TelegramClient:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        
    def send_content(self, text: str, image_url: str = None) -> bool:
        """Send refined formatted content to Telegram."""
        try:
            # Format text for Telegram with proper parsing
            formatted_text = self._format_for_telegram_refined(text)
            
            if image_url:
                return self._send_photo(formatted_text, image_url)
            else:
                return self._send_message(formatted_text)
                
        except Exception as e:
            logger.error(f"💥 Send error: {str(e)}")
            return False
    
    def _format_for_telegram_refined(self, text: str) -> str:
        """Format text with refined Telegram-specific formatting."""
        try:
            # The text already has the correct formatting with italic hashtags
            formatted = text
            
            # Ensure proper line spacing (already handled in perplexity_client)
            lines = formatted.split('\n')
            
            # Verify hashtags are properly formatted as italic
            for i, line in enumerate(lines):
                if line.strip().startswith('*#') and line.strip().endswith('*'):
                    # Hashtags are already in italic format
                    continue
                elif line.strip().startswith('#'):
                    # Convert regular hashtags to italic
                    lines[i] = f"*{line.strip()}*"
            
            return '\n'.join(lines)
            
        except Exception as e:
            logger.error(f"💥 Format error: {str(e)}")
            return text
    
    def _send_photo(self, caption: str, image_url: str) -> bool:
        """Send photo with refined formatted caption."""
        try:
            url = f"{self.base_url}/sendPhoto"
            data = {
                'chat_id': self.chat_id,
                'photo': image_url,
                'caption': caption,
                'parse_mode': 'Markdown'  # Enable Markdown parsing for italic hashtags
            }
            
            logger.info("📤 Sending photo with refined formatting...")
            response = requests.post(url, data=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    logger.info("✅ Refined photo sent successfully")
                    return True
                else:
                    logger.warning(f"⚠️ Photo API returned: {result}")
            
            logger.warning("⚠️ Photo failed, trying text only")
            return self._send_message(caption)
            
        except Exception as e:
            logger.error(f"💥 Photo error: {str(e)}")
            return self._send_message(caption)
    
    def _send_message(self, text: str) -> bool:
        """Send refined formatted text message."""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': 'Markdown'  # Enable Markdown parsing for italic hashtags
            }
            
            logger.info("📤 Sending refined text message...")
            response = requests.post(url, data=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    logger.info("✅ Refined message sent successfully")
                    return True
                else:
                    logger.warning(f"⚠️ Message API returned: {result}")
            
            logger.error(f"❌ Message failed: {response.text}")
            return False
            
        except Exception as e:
            logger.error(f"💥 Message error: {str(e)}")
            return False
    
    def test_connection(self) -> bool:
        """Test bot connection."""
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    bot_info = result['result']
                    logger.info(f"✅ Bot connected: {bot_info['first_name']} (@{bot_info.get('username', 'N/A')})")
                    return True
            
            logger.error(f"❌ Bot test failed: {response.text}")
            return False
            
        except Exception as e:
            logger.error(f"💥 Bot test error: {str(e)}")
            return False
