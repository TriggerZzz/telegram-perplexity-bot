"""
Telegram client - SIMPLIFIED WORKING VERSION
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
        """Send content to Telegram."""
        try:
            if image_url:
                return self._send_photo(text, image_url)
            else:
                return self._send_message(text)
        except Exception as e:
            logger.error(f"💥 Send error: {str(e)}")
            return False
    
    def _send_photo(self, caption: str, image_url: str) -> bool:
        """Send photo with caption."""
        try:
            url = f"{self.base_url}/sendPhoto"
            data = {
                'chat_id': self.chat_id,
                'photo': image_url,
                'caption': caption
            }
            
            response = requests.post(url, data=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    logger.info("✅ Photo sent successfully")
                    return True
            
            logger.warning("⚠️ Photo failed, trying text only")
            return self._send_message(caption)
            
        except Exception as e:
            logger.error(f"💥 Photo error: {str(e)}")
            return self._send_message(caption)
    
    def _send_message(self, text: str) -> bool:
        """Send text message."""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': text
            }
            
            response = requests.post(url, data=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    logger.info("✅ Message sent successfully")
                    return True
            
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
                    logger.info(f"✅ Bot connected: {result['result']['first_name']}")
                    return True
            
            logger.error(f"❌ Bot test failed: {response.text}")
            return False
            
        except Exception as e:
            logger.error(f"💥 Bot test error: {str(e)}")
            return False
