"""
Telegram bot client for sending messages and photos.
"""

import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class TelegramClient:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        
    def send_content(self, text: str, image_url: Optional[str] = None) -> bool:
        """
        Send content to Telegram channel.
        If image_url is provided, sends photo with caption, otherwise sends text message.
        """
        try:
            if image_url:
                return self._send_photo(text, image_url)
            else:
                return self._send_message(text)
                
        except Exception as e:
            logger.error(f"Error sending content: {str(e)}")
            return False
            
    def _send_photo(self, caption: str, image_url: str) -> bool:
        """Send photo with caption to Telegram."""
        try:
            url = f"{self.base_url}/sendPhoto"
            
            payload = {
                'chat_id': self.chat_id,
                'photo': image_url,
                'caption': caption,
                'parse_mode': 'HTML'  # Enable HTML formatting
            }
            
            logger.info("Sending photo to Telegram...")
            response = requests.post(url, data=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if result.get('ok'):
                logger.info("Photo sent successfully")
                return True
            else:
                logger.error(f"Telegram API error: {result}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error sending photo: {str(e)}")
            # Fallback to text message
            logger.info("Falling back to text message...")
            return self._send_message(caption)
        except Exception as e:
            logger.error(f"Unexpected error sending photo: {str(e)}")
            return False
            
    def _send_message(self, text: str) -> bool:
        """Send text message to Telegram."""
        try:
            url = f"{self.base_url}/sendMessage"
            
            payload = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': 'HTML'  # Enable HTML formatting
            }
            
            logger.info("Sending text message to Telegram...")
            response = requests.post(url, data=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if result.get('ok'):
                logger.info("Message sent successfully")
                return True
            else:
                logger.error(f"Telegram API error: {result}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error sending message: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending message: {str(e)}")
            return False
            
    def test_connection(self) -> bool:
        """Test bot connection and permissions."""
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get('ok'):
                bot_info = result['result']
                logger.info(f"Bot connected: {bot_info['first_name']} (@{bot_info['username']})")
                return True
            else:
                logger.error(f"Bot connection failed: {result}")
                return False
                
        except Exception as e:
            logger.error(f"Error testing bot connection: {str(e)}")
            return False
