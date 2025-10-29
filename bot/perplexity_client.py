"""
Perplexity API client for fetching daily content.
"""

import requests
import json
import logging
import re
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class PerplexityClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
    def get_daily_content(self, topic: str) -> Optional[Dict]:
        """
        Get daily content from Perplexity API.
        Returns dict with 'text' and optionally 'image_url'.
        """
        try:
            # Create a focused prompt that encourages both text and image suggestions
            prompt = f"""Write an engaging, informative post about {topic}. 
            
            Requirements:
            - Maximum 900 characters (including spaces)
            - Include interesting facts or recent developments
            - Suggest a relevant image search term at the end in format: [IMAGE: search_term]
            - Make it engaging and shareable
            - Use emojis sparingly but effectively
            
            Topic: {topic}"""
            
            payload = {
                "model": "sonar-pro",  # Using PRO model
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a content creator who writes engaging, factual posts with image suggestions."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.7,
                "stream": False
            }
            
            logger.info("Making request to Perplexity API...")
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            if 'choices' not in data or not data['choices']:
                logger.error("No choices in Perplexity response")
                return None
                
            content = data['choices']['message']['content']
            logger.info(f"Received content from Perplexity ({len(content)} chars)")
            
            # Extract image suggestion if present
            image_search_term = self._extract_image_suggestion(content)
            
            # Clean content by removing image suggestion
            clean_content = re.sub(r'\[IMAGE:.*?\]', '', content).strip()
            
            result = {
                'text': clean_content,
                'image_search_term': image_search_term
            }
            
            # If we have an image search term, try to get an image URL
            if image_search_term:
                image_url = self._get_image_url(image_search_term)
                if image_url:
                    result['image_url'] = image_url
                    
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in Perplexity client: {str(e)}")
            return None
            
    def _extract_image_suggestion(self, content: str) -> Optional[str]:
        """Extract image search term from content."""
        match = re.search(r'\[IMAGE:\s*([^\]]+)\]', content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None
        
    def _get_image_url(self, search_term: str) -> Optional[str]:
        """
        Get a relevant image URL for the search term.
        Using a simple approach with Unsplash API (free tier).
        """
        try:
            # Using Unsplash for free stock photos
            unsplash_url = "https://source.unsplash.com/800x600/"
            # Clean search term for URL
            clean_term = search_term.replace(' ', '+').replace(',', '')
            image_url = f"{unsplash_url}?{clean_term}"
            
            # Verify the URL returns an image
            response = requests.head(image_url, timeout=10)
            if response.status_code == 200:
                logger.info(f"Found image for: {search_term}")
                return image_url
                
        except Exception as e:
            logger.warning(f"Could not get image for '{search_term}': {str(e)}")
            
        return None
