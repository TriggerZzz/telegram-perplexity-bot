"""
Perplexity API client for fetching daily crypto content with image generation.
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
        """
        try:
            # Get today's date for context
            today = datetime.now().strftime("%B %d, %Y")
            
            # Optimized prompt for crypto news with strict character limit
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
                "model": "sonar-pro",  # Using PRO model for real-time data
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
                "max_tokens": 400,  # Reduced to ensure concise response
                "temperature": 0.3,  # Lower for more factual content
                "stream": False
            }
            
            logger.info("Making request to Perplexity API for crypto news...")
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=45  # Increased timeout for real-time data
            )
            
            # Log response details for debugging
            logger.info(f"Response status code: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"API request failed with status {response.status_code}")
                logger.error(f"Response text: {response.text}")
                return None
            
            # Parse JSON response with comprehensive error handling
            try:
                data = response.json()
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.error(f"Raw response text: {response.text}")
                return None
            
            # Validate response structure step by step
            if not isinstance(data, dict):
                logger.error(f"Expected dict, got {type(data)}")
                return None
                
            if 'choices' not in data:
                logger.error(f"No 'choices' field in response. Available keys: {list(data.keys())}")
                return None
                
            if not isinstance(data['choices'], list) or not data['choices']:
                logger.error(f"'choices' is not a valid list: {data['choices']}")
                return None
            
            # Get the first choice - CORRECTED: choices is a list, get first element
            choice = data['choices']  # This is the dict we want
            logger.info(f"Choice structure: {choice}")  # Now logging the correct object
            
            # The choice is a dict, extract message
            if not isinstance(choice, dict):
                logger.error(f"Choice is not a dict: {type(choice)}")
                return None
                
            if 'message' not in choice:
                logger.error(f"No 'message' field in choice. Available keys: {list(choice.keys())}")
                return None
                
            message = choice['message']
            logger.info(f"Message structure: {message}")
            
            if not isinstance(message, dict):
                logger.error(f"Message is not a dict: {type(message)}")
                return None
                
            if 'content' not in message:
                logger.error(f"No 'content' field in message. Available keys: {list(message.keys())}")
                return None
                
            content = message['content']
            
            if not isinstance(content, str):
                logger.error(f"Content is not a string: {type(content)}")
                return None
                
            logger.info(f"Successfully extracted content ({len(content)} characters)")
            
            # Clean and validate content
            clean_content = content.strip()
            
            # Remove any citation numbers like  that might appear
            clean_content = re.sub(r'\[\d+\]', '', clean_content)
            
            # Ensure content ends with the required hashtags
            required_tags = "#CryptoNews #MarketOverview"
            if not clean_content.endswith(required_tags):
                # Remove any existing hashtags and add the required ones
                clean_content = re.sub(r'#\w+\s*#\w+\s*$', '', clean_content).strip()
                if not clean_content.endswith(required_tags):
                    clean_content = f"{clean_content.rstrip()} {required_tags}"
            
            # Validate character limit (1000 max, targeting 950)
            if len(clean_content) > 1000:
                logger.warning(f"Content too long ({len(clean_content)} chars), truncating...")
                # Truncate while preserving hashtags
                max_content_length = 1000 - len(required_tags) - 1  # -1 for space
                truncated = clean_content[:max_content_length].rsplit(' ', 1)
                clean_content = f"{truncated} {required_tags}"
            
            # Generate crypto-themed image
            logger.info("Generating crypto-themed image...")
            image_url = self._generate_crypto_image()
            
            result = {
                'text': clean_content,
                'image_url': image_url,
                'char_count': len(clean_content)
            }
            
            logger.info(f"✅ Content processed successfully!")
            logger.info(f"Final character count: {len(clean_content)}")
            logger.info(f"Has image: {'Yes' if image_url else 'No'}")
            logger.info(f"Content preview: {clean_content[:100]}...")
            
            return result
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            if e.response:
                logger.error(f"Response text: {e.response.text}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in Perplexity client: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None
    
    def _generate_crypto_image(self) -> Optional[str]:
        """
        Generate a cryptocurrency-themed image URL.
        Uses multiple fallback methods for reliability.
        """
        try:
            # Method 1: Unsplash with crypto-specific terms
            crypto_terms = [
                "cryptocurrency+trading+charts",
                "bitcoin+financial+market",
                "blockchain+technology+finance", 
                "crypto+market+analysis",
                "digital+currency+exchange",
                "financial+trading+screen"
            ]
            
            # Try each term until we find a working image
            for term in crypto_terms:
                try:
                    image_url = f"https://source.unsplash.com/1200x800/?{term}"
                    
                    # Test if image is accessible
                    response = requests.head(image_url, timeout=10, allow_redirects=True)
                    if response.status_code == 200:
                        logger.info(f"✅ Generated crypto image with term: {term}")
                        return image_url
                        
                except requests.RequestException as e:
                    logger.debug(f"Failed to get image for term {term}: {e}")
                    continue
            
            # Method 2: Fallback to Picsum (Lorem Picsum) with fixed image
            fallback_urls = [
                "https://picsum.photos/1200/800?random=crypto1",
                "https://picsum.photos/1200/800?random=finance1", 
                "https://picsum.photos/1200/800?random=market1"
            ]
            
            for url in fallback_urls:
                try:
                    response = requests.head(url, timeout=10)
                    if response.status_code == 200:
                        logger.info(f"✅ Using fallback image: {url}")
                        return url
                except requests.RequestException as e:
                    logger.debug(f"Failed fallback image {url}: {e}")
                    continue
                    
            # Method 3: Static crypto-themed image (most reliable)
            static_crypto_image = "https://images.unsplash.com/photo-1640340434855-6084b1f4901c?w=1200&h=800&fit=crop"
            
            try:
                response = requests.head(static_crypto_image, timeout=10)
                if response.status_code == 200:
                    logger.info("✅ Using static crypto image")
                    return static_crypto_image
            except requests.RequestException as e:
                logger.debug(f"Failed static image: {e}")
                pass
                
        except Exception as e:
            logger.warning(f"Error generating crypto image: {str(e)}")
            
        # If all methods fail, return None (bot will send text-only)
        logger.warning("⚠️  All image generation methods failed, sending text-only")
        return None
        
    def test_connection(self) -> bool:
        """Test the API connection and key validity."""
        try:
            payload = {
                "model": "sonar-pro",
                "messages": [
                    {
                        "role": "user",
                        "content": "Test connection - respond with 'OK'"
                    }
                ],
                "max_tokens": 10
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            logger.info(f"Test connection status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'choices' in data and data['choices']:
                    logger.info("Perplexity API connection successful")
                    return True
            
            logger.error(f"Test connection failed: {response.text}")
            return False
            
        except Exception as e:
            logger.error(f"Test connection error: {str(e)}")
            return False
            
    def get_daily_content(self, topic: str) -> Optional[Dict]:
        """
        Compatibility method for existing code.
        Routes to crypto news function for consistent behavior.
        """
        logger.info(f"Routing topic '{topic}' to crypto news generation")
        return self.get_crypto_news_content()
