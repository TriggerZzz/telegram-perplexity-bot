"""
Enhanced Perplexity API client with improved formatting and dynamic image generation.
"""

import requests
import json
import logging
import re
import hashlib
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
        """Get crypto market news with enhanced formatting."""
        try:
            today = datetime.now()
            formatted_date = today.strftime("%B %d, %Y")
            
            # Enhanced prompt for better structure
            prompt = f"""Write a crypto market analysis for {formatted_date}. Structure it as follows:
            
            1. Start with a compelling title about today's crypto market
            2. Write 3-4 bullet points covering:
               - Bitcoin and Ethereum price movements with percentages
               - Major altcoin performance and trends
               - Market sentiment and key economic factors
               - Any breaking news or regulatory updates
            
            Keep total length under 850 characters including spaces.
            Use engaging, professional financial language.
            End with: #CryptoNews #MarketOverview"""

            payload = {
                "model": "sonar-pro",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a professional crypto market analyst. Write concise, engaging market summaries with specific data and percentages. Focus on actionable insights."
                    },
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 350,
                "temperature": 0.4,
                "stream": False
            }
            
            logger.info("📡 Requesting enhanced crypto news from Perplexity...")
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code != 200:
                logger.error(f"❌ API failed: {response.status_code}")
                return self._create_enhanced_fallback_content(formatted_date)
            
            try:
                data = response.json()
            except:
                logger.error("❌ JSON parse failed")
                return self._create_enhanced_fallback_content(formatted_date)
            
            # Extract content
            content = self._extract_content_simple(data)
            
            if not content:
                logger.warning("⚠️ No content extracted, using fallback")
                return self._create_enhanced_fallback_content(formatted_date)
            
            # Format content with new structure
            formatted_content = self._format_content_enhanced(content, formatted_date)
            
            # Generate unique image for this content
            image_url = self._generate_unique_crypto_image(formatted_content)
            
            result = {
                'text': formatted_content,
                'image_url': image_url,
                'char_count': len(formatted_content)
            }
            
            logger.info(f"✅ Enhanced content ready: {len(formatted_content)} chars")
            return result
            
        except Exception as e:
            logger.error(f"💥 Error: {str(e)}")
            today_str = datetime.now().strftime("%B %d, %Y")
            return self._create_enhanced_fallback_content(today_str)
    
    def _extract_content_simple(self, data: dict) -> str:
        """Simple content extraction that works with any format."""
        try:
            # Method 1: Standard format
            if 'choices' in data and data['choices']:
                choice = data['choices']
                
                if isinstance(choice, dict):
                    if 'message' in choice and 'content' in choice['message']:
                        content = choice['message']['content']
                        if isinstance(content, str) and content.strip():
                            logger.info("✅ Found content in standard format")
                            return content.strip()
                
                elif isinstance(choice, list) and choice:
                    for item in choice:
                        if isinstance(item, dict):
                            if 'message' in item and 'content' in item['message']:
                                content = item['message']['content']
                                if isinstance(content, str) and content.strip():
                                    logger.info("✅ Found content in list format")
                                    return content.strip()
            
            # Recursive search fallback
            def find_content(obj):
                if isinstance(obj, str) and len(obj) > 20:
                    return obj
                elif isinstance(obj, dict):
                    for key, value in obj.items():
                        if key == 'content' and isinstance(value, str):
                            return value
                        result = find_content(value)
                        if result:
                            return result
                elif isinstance(obj, list):
                    for item in obj:
                        result = find_content(item)
                        if result:
                            return result
                return None
            
            content = find_content(data)
            if content:
                logger.info("✅ Found content via recursive search")
                return content.strip()
            
            return ""
            
        except Exception as e:
            logger.error(f"💥 Extract error: {str(e)}")
            return ""
    
    def _format_content_enhanced(self, content: str, date: str) -> str:
        """Format content with title, bullet points, and proper spacing."""
        try:
            # Clean citations and extra formatting
            clean_content = re.sub(r'\[\d+\]', '', content)
            clean_content = re.sub(r'\*\*(.*?)\*\*', r'\1', clean_content)
            clean_content = re.sub(r'\*(.*?)\*', r'\1', clean_content)
            clean_content = re.sub(r'\s+', ' ', clean_content).strip()
            
            # Extract title if present or create one
            lines = clean_content.split('\n')
            title = ""
            body_content = clean_content
            
            # Check if first line looks like a title
            if lines and len(lines) > 1:
                first_line = lines.strip()
                if len(first_line) < 100 and not first_line.startswith('•') and not first_line.startswith('-'):
                    title = first_line
                    body_content = '\n'.join(lines[1:]).strip()
            
            # If no title found, create one
            if not title:
                title = f"🚀 Crypto Market Update"
            
            # Create formatted structure
            formatted_lines = [
                f"📈 **{title}**",
                f"📅 *{date}*",
                "",  # Empty line after header
            ]
            
            # Convert content to bullet points
            bullet_content = self._convert_to_bullets(body_content)
            formatted_lines.extend(bullet_content)
            
            # Add spacing before hashtags
            formatted_lines.extend([
                "",  # Empty line
                "",  # Second empty line
                "#CryptoNews #MarketOverview"
            ])
            
            result = '\n'.join(formatted_lines)
            
            # Ensure under character limit
            if len(result) > 1000:
                # Truncate bullet points while keeping structure
                header_size = len(formatted_lines) + len(formatted_lines) + len(formatted_lines) + 6  # +6 for newlines
                footer_size = 50  # For spacing and hashtags
                available_space = 1000 - header_size - footer_size
                
                truncated_bullets = self._truncate_bullets(bullet_content, available_space)
                
                result_lines = formatted_lines[:3] + truncated_bullets + ["", "", "#CryptoNews #MarketOverview"]
                result = '\n'.join(result_lines)
            
            return result
            
        except Exception as e:
            logger.error(f"💥 Format error: {str(e)}")
            return f"📈 **Crypto Market Update**\n📅 *{date}*\n\n• Market analysis unavailable\n\n\n#CryptoNews #MarketOverview"
    
    def _convert_to_bullets(self, content: str) -> list:
        """Convert content to bullet point format."""
        try:
            # Remove existing hashtags
            content = re.sub(r'#\w+\s*#\w+\s*$', '', content).strip()
            
            # Split into sentences and create bullets
            sentences = [s.strip() for s in content.replace('.', '.|').split('|') if s.strip()]
            
            bullets = []
            for sentence in sentences:
                if sentence and len(sentence) > 10:
                    # Clean sentence
                    sentence = sentence.rstrip('.').strip()
                    if sentence:
                        bullets.append(f"• {sentence}")
            
            # Ensure we have at least 2-3 bullet points
            if len(bullets) < 2:
                bullets = [
                    "• Bitcoin and Ethereum show mixed trading signals",
                    "• Altcoin markets display varied performance patterns", 
                    "• Market sentiment remains cautious amid economic developments"
                ]
            
            return bullets
            
        except Exception as e:
            logger.error(f"💥 Bullet conversion error: {str(e)}")
            return ["• Crypto market analysis in progress"]
    
    def _truncate_bullets(self, bullets: list, max_chars: int) -> list:
        """Truncate bullets to fit within character limit."""
        result = []
        current_length = 0
        
        for bullet in bullets:
            if current_length + len(bullet) + 1 <= max_chars:  # +1 for newline
                result.append(bullet)
                current_length += len(bullet) + 1
            else:
                break
        
        # Ensure at least one bullet
        if not result and bullets:
            result = [bullets[:max_chars-3] + "..."]
        
        return result
    
    def _generate_unique_crypto_image(self, content: str) -> str:
        """Generate a unique crypto image based on content hash."""
        try:
            # Create hash from content for uniqueness
            content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
            
            # Multiple image sources with rotation based on content
            crypto_images = [
                f"https://source.unsplash.com/1200x800/?cryptocurrency,trading,{content_hash}",
                f"https://source.unsplash.com/1200x800/?bitcoin,market,analysis",
                f"https://source.unsplash.com/1200x800/?blockchain,finance,charts",
                f"https://picsum.photos/1200/800?random={content_hash}",
                "https://images.unsplash.com/photo-1640340434855-6084b1f4901c?w=1200&h=800&fit=crop",
                "https://images.unsplash.com/photo-1559757175-0eb30cd8c063?w=1200&h=800&fit=crop",
                "https://images.unsplash.com/photo-1616499370260-485b3e5ed653?w=1200&h=800&fit=crop"
            ]
            
            # Select image based on hash to ensure different images
            hash_int = int(content_hash, 16)
            selected_image = crypto_images[hash_int % len(crypto_images)]
            
            # Test image availability
            try:
                response = requests.head(selected_image, timeout=10)
                if response.status_code == 200:
                    logger.info(f"✅ Generated unique image: {selected_image}")
                    return selected_image
            except:
                pass
            
            # Fallback to reliable static image
            return "https://images.unsplash.com/photo-1640340434855-6084b1f4901c?w=1200&h=800&fit=crop"
            
        except Exception as e:
            logger.error(f"💥 Image generation error: {str(e)}")
            return "https://images.unsplash.com/photo-1640340434855-6084b1f4901c?w=1200&h=800&fit=crop"
    
    def _create_enhanced_fallback_content(self, date: str) -> Dict:
        """Create enhanced fallback content with proper formatting."""
        fallback_bullets = [
            "• Bitcoin continues consolidation in key resistance zones",
            "• Ethereum shows resilience amid network development progress", 
            "• Altcoin sectors display mixed performance across categories",
            "• Market participants monitor regulatory developments closely"
        ]
        
        formatted_content = f"""📈 **Crypto Market Analysis**
📅 *{date}*

{chr(10).join(fallback_bullets)}


#CryptoNews #MarketOverview"""
        
        return {
            'text': formatted_content,
            'image_url': self._generate_unique_crypto_image(formatted_content),
            'char_count': len(formatted_content)
        }
    
    def test_connection(self) -> bool:
        """Simple connection test."""
        try:
            payload = {
                "model": "sonar-pro",
                "messages": [{"role": "user", "content": "Test"}],
                "max_tokens": 10
            }
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=20)
            
            if response.status_code == 200:
                logger.info("✅ Perplexity API connection successful")
                return True
            return False
            
        except Exception as e:
            logger.error(f"💥 Test error: {str(e)}")
            return False
    
    def get_daily_content(self, topic: str) -> Optional[Dict]:
        """Compatibility method."""
        return self.get_crypto_news_content()
