"""
Enhanced Telegram client with improved formatting support.
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
        """Send enhanced formatted content to Telegram."""
        try:
            # Format text for Telegram with proper parsing
            formatted_text = self._format_for_telegram(text)
            
            if image_url:
                return self._send_photo(formatted_text, image_url)
            else:
                return self._send_message(formatted_text)
                
        except Exception as e:
            logger.error(f"💥 Send error: {str(e)}")
            return False
    
    def _format_for_telegram(self, text: str) -> str:
        """Format text with Telegram-specific formatting."""
        try:
            # Convert markdown-style formatting to Telegram format
            formatted = text
            
            # Handle bold text (keep existing **)
            # Handle bullet points (already using •)
            # Handle dates and titles (keep existing formatting)
            
            # Ensure proper line spacing for hashtags
            lines = formatted.split('\n')
            
            # Find hashtags and ensure proper spacing
            hashtag_index = -1
            for i, line in enumerate(lines):
                if line.strip().startswith('#'):
                    hashtag_index = i
                    break
            
            if hashtag_index > 0:
                # Ensure two empty lines before hashtags
                while hashtag_index > 0 and lines[hashtag_index - 1].strip() == "":
                    hashtag_index -= 1
                
                # Insert proper spacing
                lines.insert(hashtag_index, "")
                lines.insert(hashtag_index, "")
            
            return '\n'.join(lines)
            
        except Exception as e:
            logger.error(f"💥 Format error: {str(e)}")
            return text
    
    def _send_photo(self, caption: str, image_url: str) -> bool:
        """Send photo with formatted caption."""
        try:
            url = f"{self.base_url}/sendPhoto"
            data = {
                'chat_id': self.chat_id,
                'photo': image_url,
                'caption': caption,
                'parse_mode': 'Markdown'  # Enable Markdown parsing
            }
            
            logger.info("📤 Sending photo with enhanced formatting...")
            response = requests.post(url, data=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    logger.info("✅ Enhanced photo sent successfully")
                    return True
                else:
                    logger.warning(f"⚠️ Photo API returned: {result}")
            
            logger.warning("⚠️ Photo failed, trying text only")
            return self._send_message(caption)
            
        except Exception as e:
            logger.error(f"💥 Photo error: {str(e)}")
            return self._send_message(caption)
    
    def _send_message(self, text: str) -> bool:
        """Send formatted text message."""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': 'Markdown'  # Enable Markdown parsing
            }
            
            logger.info("📤 Sending enhanced text message...")
            response = requests.post(url, data=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    logger.info("✅ Enhanced message sent successfully")
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
