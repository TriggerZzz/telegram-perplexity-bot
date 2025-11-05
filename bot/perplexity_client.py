"""
Refined Perplexity API client with updated formatting and expanded content length.
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
        """Get crypto market news with refined formatting and expanded content."""
        try:
            today = datetime.now()
            formatted_date = today.strftime("%B %d, %Y")
            
            # Enhanced prompt for longer, more detailed content
            prompt = f"""Write a comprehensive crypto market analysis for {formatted_date}. Structure it as follows:
            
            1. Start with a compelling title about today's crypto market
            2. Write 5-6 detailed bullet points covering:
               - Bitcoin price analysis with technical indicators and percentage changes
               - Ethereum performance, network developments, and market dynamics
               - Top 3-5 altcoin performances with specific price movements
               - Market sentiment analysis and fear/greed indicators
               - Regulatory developments, institutional news, or market catalysts
               - Technical analysis insights and key support/resistance levels
            
            Make each bullet point substantial with specific data, percentages, and insights.
            Target total length around 950-980 characters including spaces.
            Use engaging, professional financial language with specific metrics.
            End with: #CryptoNews #MarketOverview"""

            payload = {
                "model": "sonar-pro",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a senior crypto market analyst. Write detailed, data-rich market summaries with specific prices, percentages, and technical analysis. Focus on comprehensive market coverage with actionable insights. Be thorough and professional."
                    },
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 450,  # Increased for longer content
                "temperature": 0.4,
                "stream": False
            }
            
            logger.info("📡 Requesting refined crypto news from Perplexity...")
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=35)
            
            if response.status_code != 200:
                logger.error(f"❌ API failed: {response.status_code}")
                return self._create_refined_fallback_content(formatted_date)
            
            try:
                data = response.json()
            except:
                logger.error("❌ JSON parse failed")
                return self._create_refined_fallback_content(formatted_date)
            
            # Extract content
            content = self._extract_content_simple(data)
            
            if not content:
                logger.warning("⚠️ No content extracted, using fallback")
                return self._create_refined_fallback_content(formatted_date)
            
            # Format content with refined structure
            formatted_content = self._format_content_refined(content, formatted_date)
            
            # Generate unique image for this content
            image_url = self._generate_unique_crypto_image(formatted_content)
            
            result = {
                'text': formatted_content,
                'image_url': image_url,
                'char_count': len(formatted_content)
            }
            
            logger.info(f"✅ Refined content ready: {len(formatted_content)} chars")
            return result
            
        except Exception as e:
            logger.error(f"💥 Error: {str(e)}")
            today_str = datetime.now().strftime("%B %d, %Y")
            return self._create_refined_fallback_content(today_str)
    
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
                if isinstance(obj, str) and len(obj) > 50:
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
    
    def _format_content_refined(self, content: str, date: str) -> str:
        """Format content with refined structure - 1 line spacing and italic hashtags."""
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
                if len(first_line) < 120 and not first_line.startswith('•') and not first_line.startswith('-'):
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
            
            # Convert content to detailed bullet points
            bullet_content = self._convert_to_detailed_bullets(body_content)
            formatted_lines.extend(bullet_content)
            
            # Add refined spacing before hashtags (1 line instead of 2)
            formatted_lines.extend([
                "",  # Single empty line
                "*#CryptoNews #MarketOverview*"  # Italic hashtags
            ])
            
            result = '\n'.join(formatted_lines)
            
            # Ensure around 1000 characters
            target_length = 1000
            if len(result) > target_length:
                # Truncate bullet points while keeping structure
                header_size = len(formatted_lines) + len(formatted_lines) + len(formatted_lines) + 6  # +6 for newlines
                footer_size = 35  # For spacing and italic hashtags
                available_space = target_length - header_size - footer_size
                
                truncated_bullets = self._truncate_bullets_refined(bullet_content, available_space)
                
                result_lines = formatted_lines[:3] + truncated_bullets + ["", "*#CryptoNews #MarketOverview*"]
                result = '\n'.join(result_lines)
            
            elif len(result) < 900:
                # Expand content if too short
                expanded_bullets = self._expand_bullets(bullet_content, target_length - len(result))
                result_lines = formatted_lines[:3] + expanded_bullets + ["", "*#CryptoNews #MarketOverview*"]
                result = '\n'.join(result_lines)
            
            return result
            
        except Exception as e:
            logger.error(f"💥 Format error: {str(e)}")
            return f"📈 **Crypto Market Update**\n📅 *{date}*\n\n• Comprehensive market analysis in progress\n\n*#CryptoNews #MarketOverview*"
    
    def _convert_to_detailed_bullets(self, content: str) -> list:
        """Convert content to detailed bullet point format for ~1000 character target."""
        try:
            # Remove existing hashtags
            content = re.sub(r'#\w+\s*#\w+\s*$', '', content).strip()
            
            # Split into sentences and create detailed bullets
            sentences = []
            for sentence in content.replace('.', '.|').replace('!', '!|').replace('?', '?|').split('|'):
                sentence = sentence.strip()
                if sentence and len(sentence) > 15:
                    sentences.append(sentence)
            
            bullets = []
            for sentence in sentences:
                if sentence:
                    # Clean and enhance sentence
                    sentence = sentence.rstrip('.!?').strip()
                    if sentence:
                        # Make bullets more substantial
                        if len(sentence) < 60:
                            # Try to combine short sentences or expand them
                            sentence = self._enhance_short_bullet(sentence)
                        bullets.append(f"• {sentence}")
            
            # Ensure we have 4-6 substantial bullet points
            if len(bullets) < 4:
                bullets = self._generate_comprehensive_bullets()
            elif len(bullets) > 6:
                bullets = bullets[:6]  # Limit to 6 bullets max
            
            return bullets
            
        except Exception as e:
            logger.error(f"💥 Bullet conversion error: {str(e)}")
            return self._generate_comprehensive_bullets()
    
    def _enhance_short_bullet(self, bullet: str) -> str:
        """Enhance short bullets with more detail."""
        try:
            # Add context to common short phrases
            enhancements = {
                "bitcoin": "Bitcoin continues its market leadership with institutional interest",
                "ethereum": "Ethereum shows network strength amid ongoing development",
                "market": "Market dynamics reflect broader economic sentiment",
                "price": "Price action indicates key technical levels",
                "trading": "Trading volumes suggest increased market participation"
            }
            
            bullet_lower = bullet.lower()
            for key, enhancement in enhancements.items():
                if key in bullet_lower and len(bullet) < 50:
                    return enhancement
            
            return bullet
            
        except:
            return bullet
    
    def _generate_comprehensive_bullets(self) -> list:
        """Generate comprehensive fallback bullets for detailed analysis."""
        return [
            "• Bitcoin maintains consolidation above key support levels with institutional accumulation patterns emerging",
            "• Ethereum demonstrates network resilience with increasing validator participation and Layer 2 adoption growth", 
            "• Top altcoins including BNB, XRP, and SOL show divergent performance reflecting sector-specific developments",
            "• Market sentiment indicators suggest cautious optimism amid ongoing regulatory clarity initiatives",
            "• DeFi and AI token sectors attract renewed interest following recent technological breakthroughs",
            "• Technical analysis reveals critical support and resistance zones shaping near-term price trajectories"
        ]
    
    def _truncate_bullets_refined(self, bullets: list, max_chars: int) -> list:
        """Truncate bullets to fit within character limit while maintaining quality."""
        result = []
        current_length = 0
        
        for bullet in bullets:
            bullet_length = len(bullet) + 1  # +1 for newline
            if current_length + bullet_length <= max_chars:
                result.append(bullet)
                current_length += bullet_length
            else:
                # Try to fit a shortened version of the bullet
                available_chars = max_chars - current_length - 4  # -4 for "..." and newline
                if available_chars > 30:  # Only if meaningful content can fit
                    shortened = bullet[:available_chars] + "..."
                    result.append(shortened)
                break
        
        # Ensure at least 3 bullets
        if len(result) < 3 and bullets:
            result = bullets[:3]
        
        return result
    
    def _expand_bullets(self, bullets: list, additional_chars_needed: int) -> list:
        """Expand bullets if content is too short."""
        if additional_chars_needed < 50:
            return bullets
        
        # Add more comprehensive bullets if we have space
        comprehensive_bullets = self._generate_comprehensive_bullets()
        
        # Combine existing with comprehensive, avoiding duplicates
        expanded = bullets[:]
        for comp_bullet in comprehensive_bullets:
            if len('\n'.join(expanded + [comp_bullet])) < 800:  # Leave room for header/footer
                if not any(comp_bullet[2:20] in existing[2:20] for existing in expanded):
                    expanded.append(comp_bullet)
        
        return expanded
    
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
    
    def _create_refined_fallback_content(self, date: str) -> Dict:
        """Create refined fallback content with proper formatting and ~1000 characters."""
        fallback_bullets = [
            "• Bitcoin demonstrates resilience above $67,000 with institutional accumulation continuing despite market volatility",
            "• Ethereum network shows strength at $2,600 level with increasing validator participation and Layer 2 adoption expanding",
            "• Major altcoins including BNB, XRP, SOL, and ADA display mixed signals reflecting individual project developments",
            "• Market sentiment remains cautiously optimistic with Fear & Greed Index indicating balanced investor psychology",
            "• DeFi protocols report increased total value locked while AI and gaming tokens attract renewed institutional interest",
            "• Technical indicators suggest key support levels holding firm with potential for continued consolidation phase"
        ]
        
        formatted_content = f"""📈 **Crypto Market Analysis**
📅 *{date}*

{chr(10).join(fallback_bullets)}

*#CryptoNews #MarketOverview*"""
        
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
