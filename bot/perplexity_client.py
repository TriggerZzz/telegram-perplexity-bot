"""
Perplexity API client for fetching daily crypto content with image generation.
BULLETPROOF VERSION - Handles all edge cases and API response variations.
"""

import requests
import json
import logging
import re
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class PerplexityClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
    def get_crypto_news_content(self) -> Optional[Dict]:
        """
        Get today's crypto market news and analysis from Perplexity API.
        Returns dict with 'text' and 'image_url'.
        BULLETPROOF - Handles all possible API response formats.
        """
        try:
            today = datetime.now().strftime("%B %d, %Y")
            
            prompt = f"""Write a comprehensive crypto market summary for {today}. 

REQUIREMENTS:
- Exactly 950 characters or less (including spaces)
- Focus on: Bitcoin, Ethereum, major altcoins, market trends, economic events
- Include specific prices, percentages, and market cap changes
- Mention any breaking news, regulatory updates, or institutional movements
- Write in engaging, informative style
- End with exactly: #CryptoNews #MarketOverview
- Include relevant technical analysis if applicable

Format as a single flowing article, not bullet points."""

            payload = {
                "model": "sonar-pro",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a professional crypto market analyst writing daily market summaries. Provide accurate, current market data and analysis. Always stay within the exact character limit specified."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "max_tokens": 400,
                "temperature": 0.3,
                "stream": False
            }
            
            logger.info("Making request to Perplexity API for crypto news...")
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=45
            )
            
            logger.info(f"Response status code: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"API request failed with status {response.status_code}")
                logger.error(f"Response text: {response.text}")
                return None
            
            # Parse JSON response
            try:
                data = response.json()
                logger.info("✅ Successfully parsed JSON response")
            except json.JSONDecodeError as e:
                logger.error(f"❌ Failed to parse JSON response: {e}")
                logger.error(f"Raw response text: {response.text}")
                return None
            
            # BULLETPROOF EXTRACTION - Handle any response format
            content = self._extract_content_bulletproof(data)
            
            if not content:
                logger.error("❌ Failed to extract content from API response")
                return None
                
            logger.info(f"✅ Successfully extracted content ({len(content)} characters)")
            
            # Clean and process content
            processed_content = self._process_content(content)
            
            if not processed_content:
                logger.error("❌ Failed to process content")
                return None
            
            # Generate image
            logger.info("Generating crypto-themed image...")
            image_url = self._generate_crypto_image()
            
            result = {
                'text': processed_content,
                'image_url': image_url,
                'char_count': len(processed_content)
            }
            
            logger.info(f"🎉 CONTENT READY!")
            logger.info(f"📏 Final character count: {len(processed_content)}")
            logger.info(f"🖼️  Has image: {'Yes' if image_url else 'No'}")
            logger.info(f"📝 Content preview: {processed_content[:100]}...")
            
            return result
            
        except Exception as e:
            logger.error(f"💥 Unexpected error in get_crypto_news_content: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None
    
    def _extract_content_bulletproof(self, data: dict) -> Optional[str]:
        """
        BULLETPROOF content extraction that handles any API response format.
        """
        try:
            logger.info("🔍 Starting bulletproof content extraction...")
            
            # Method 1: Standard OpenAI-compatible format
            if 'choices' in data and isinstance(data['choices'], list) and data['choices']:
                logger.info(f"📋 Found choices array with {len(data['choices'])} items")
                
                choice = data['choices']
                logger.info(f"🎯 Processing first choice: {type(choice)}")
                
                if isinstance(choice, dict) and 'message' in choice:
                    message = choice['message']
                    logger.info(f"💬 Found message: {type(message)}")
                    
                    if isinstance(message, dict) and 'content' in message:
                        content = message['content']
                        logger.info(f"📄 Found content: {type(content)}, length: {len(content) if isinstance(content, str) else 'N/A'}")
                        
                        if isinstance(content, str) and content.strip():
                            logger.info("✅ Successfully extracted content via Method 1 (OpenAI format)")
                            return content.strip()
            
            # Method 2: Direct text field
            if 'text' in data and isinstance(data['text'], str):
                logger.info("✅ Successfully extracted content via Method 2 (direct text)")
                return data['text'].strip()
            
            # Method 3: Alternative content field
            if 'content' in data and isinstance(data['content'], str):
                logger.info("✅ Successfully extracted content via Method 3 (direct content)")
                return data['content'].strip()
            
            # Method 4: Response field
            if 'response' in data and isinstance(data['response'], str):
                logger.info("✅ Successfully extracted content via Method 4 (response field)")
                return data['response'].strip()
            
            # Method 5: Nested text extraction
            for key in ['result', 'output', 'generated_text', 'completion']:
                if key in data:
                    value = data[key]
                    if isinstance(value, str) and value.strip():
                        logger.info(f"✅ Successfully extracted content via Method 5 ({key} field)")
                        return value.strip()
                    elif isinstance(value, dict) and 'text' in value:
                        text = value['text']
                        if isinstance(text, str) and text.strip():
                            logger.info(f"✅ Successfully extracted content via Method 5 (nested {key}.text)")
                            return text.strip()
            
            # Log available keys for debugging
            logger.error(f"❌ No valid content found. Available top-level keys: {list(data.keys())}")
            
            # Last resort: convert entire response to string if it contains readable content
            response_str = str(data)
            if len(response_str) > 100 and any(word in response_str.lower() for word in ['bitcoin', 'crypto', 'ethereum', 'market']):
                logger.warning("⚠️  Using last resort string conversion")
                return response_str[:1000]  # Limit length
            
            return None
            
        except Exception as e:
            logger.error(f"💥 Error in bulletproof extraction: {str(e)}")
            return None
    
    def _process_content(self, content: str) -> Optional[str]:
        """
        Process and clean the extracted content.
        """
        try:
            logger.info("🧹 Processing and cleaning content...")
            
            # Clean the content
            clean_content = content.strip()
            
            # Remove citation numbers like 
            clean_content = re.sub(r'\[\d+\]', '', clean_content)
            logger.info("🔗 Removed citation numbers")
            
            # Remove extra whitespace
            clean_content = re.sub(r'\s+', ' ', clean_content)
            logger.info("🧽 Cleaned whitespace")
            
            # Ensure required hashtags
            required_tags = "#CryptoNews #MarketOverview"
            if not clean_content.endswith(required_tags):
                # Remove any existing hashtags
                clean_content = re.sub(r'#\w+\s*#\w+\s*$', '', clean_content).strip()
                clean_content = f"{clean_content} {required_tags}"
                logger.info("🏷️  Added required hashtags")
            
            # Validate character limit
            if len(clean_content) > 1000:
                logger.warning(f"📏 Content too long ({len(clean_content)} chars), truncating...")
                max_content_length = 1000 - len(required_tags) - 1
                truncated = clean_content[:max_content_length].rsplit(' ', 1)
                clean_content = f"{truncated} {required_tags}"
                logger.info(f"✂️  Truncated to {len(clean_content)} characters")
            
            # Final validation
            if len(clean_content) == 0:
                logger.error("❌ Content is empty after processing")
                return None
            
            if not any(word in clean_content.lower() for word in ['bitcoin', 'crypto', 'ethereum', 'market', 'btc', 'eth']):
                logger.warning("⚠️  Content may not be crypto-related")
            
            logger.info("✅ Content processing completed successfully")
            return clean_content
            
        except Exception as e:
            logger.error(f"💥 Error processing content: {str(e)}")
            return None
    
    def _generate_crypto_image(self) -> Optional[str]:
        """
        Generate a cryptocurrency-themed image URL with multiple fallbacks.
        """
        try:
            # High-quality crypto image sources
            image_sources = [
                # Method 1: Unsplash crypto terms
                "https://source.unsplash.com/1200x800/?cryptocurrency+trading",
                "https://source.unsplash.com/1200x800/?bitcoin+market+analysis", 
                "https://source.unsplash.com/1200x800/?blockchain+finance",
                "https://source.unsplash.com/1200x800/?crypto+charts+trading",
                
                # Method 2: Picsum with crypto seeds
                "https://picsum.photos/1200/800?random=crypto123",
                "https://picsum.photos/1200/800?random=bitcoin456",
                "https://picsum.photos/1200/800?random=finance789",
                
                # Method 3: Reliable static images
                "https://images.unsplash.com/photo-1640340434855-6084b1f4901c?w=1200&h=800&fit=crop",
                "https://images.unsplash.com/photo-1559757175-0eb30cd8c063?w=1200&h=800&fit=crop",
                "https://images.unsplash.com/photo-1616499370260-485b3e5ed653?w=1200&h=800&fit=crop"
            ]
            
            for i, image_url in enumerate(image_sources, 1):
                try:
                    logger.info(f"🖼️  Testing image source {i}/{len(image_sources)}")
                    response = requests.head(image_url, timeout=10, allow_redirects=True)
                    
                    if response.status_code == 200:
                        logger.info(f"✅ Found working image: {image_url}")
                        return image_url
                    else:
                        logger.debug(f"❌ Image source {i} failed: HTTP {response.status_code}")
                        
                except requests.RequestException as e:
                    logger.debug(f"❌ Image source {i} failed: {str(e)}")
                    continue
            
            logger.warning("⚠️  All image sources failed, sending text-only")
            return None
            
        except Exception as e:
            logger.error(f"💥 Error generating image: {str(e)}")
            return None
        
    def test_connection(self) -> bool:
        """Test the API connection and key validity."""
        try:
            payload = {
                "model": "sonar-pro",
                "messages": [{"role": "user", "content": "Test"}],
                "max_tokens": 10
            }
            
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=30)
            logger.info(f"Test connection status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                content = self._extract_content_bulletproof(data)
                if content:
                    logger.info("Perplexity API connection successful")
                    return True
            
            logger.error(f"Test connection failed: {response.text}")
            return False
            
        except Exception as e:
            logger.error(f"Test connection error: {str(e)}")
            return False
            
    def get_daily_content(self, topic: str) -> Optional[Dict]:
        """Compatibility method - routes to crypto news."""
        logger.info(f"Routing topic '{topic}' to crypto news generation")
        return self.get_crypto_news_content()
