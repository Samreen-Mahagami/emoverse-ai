"""
Playwright Agent for browsing external story websites
Activated when student dislikes regenerated stories
"""
from playwright.sync_api import sync_playwright, Page
from typing import List, Dict, Optional
import json


class StoryBrowserAgent:
    """AgentCore agent that uses Playwright to find stories on external sites"""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.story_sources = [
            {
                'name': 'Storyline Online',
                'url': 'https://www.storylineonline.net/',
                'selector': '.story-card'
            },
            {
                'name': 'International Children\'s Digital Library',
                'url': 'http://en.childrenslibrary.org/',
                'selector': '.book-item'
            }
        ]
    
    def search_external_stories(
        self, 
        topic: str, 
        grade_level: int,
        emotional_theme: Optional[str] = None
    ) -> List[Dict]:
        """
        Browse external story websites and return relevant stories
        
        Args:
            topic: Main topic from extracted text
            grade_level: Student's grade level
            emotional_theme: SEL theme (e.g., 'empathy', 'resilience')
        
        Returns:
            List of story recommendations with titles, URLs, and descriptions
        """
        stories = []
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context()
            page = context.new_page()
            
            for source in self.story_sources:
                try:
                    print(f"Searching {source['name']}...")
                    source_stories = self._search_source(
                        page, 
                        source, 
                        topic, 
                        grade_level,
                        emotional_theme
                    )
                    stories.extend(source_stories)
                except Exception as e:
                    print(f"Error searching {source['name']}: {e}")
            
            browser.close()
        
        return stories[:5]  # Return top 5 stories
    
    def _search_source(
        self, 
        page: Page, 
        source: Dict, 
        topic: str,
        grade_level: int,
        emotional_theme: Optional[str]
    ) -> List[Dict]:
        """Search a specific story source"""
        stories = []
        
        try:
            page.goto(source['url'], timeout=10000)
            page.wait_for_load_state('networkidle')
            
            # Search for topic if search box exists
            search_selectors = ['input[type="search"]', '#search', '.search-input']
            for selector in search_selectors:
                if page.locator(selector).count() > 0:
                    search_query = f"{topic} {emotional_theme or ''} grade {grade_level}"
                    page.fill(selector, search_query)
                    page.press(selector, 'Enter')
                    page.wait_for_load_state('networkidle')
                    break
            
            # Extract story information
            story_elements = page.locator(source['selector']).all()[:5]
            
            for element in story_elements:
                try:
                    title = element.locator('h2, h3, .title').first.inner_text()
                    link = element.locator('a').first.get_attribute('href')
                    
                    # Get description if available
                    description = ""
                    desc_selectors = ['.description', '.summary', 'p']
                    for desc_sel in desc_selectors:
                        if element.locator(desc_sel).count() > 0:
                            description = element.locator(desc_sel).first.inner_text()
                            break
                    
                    # Make URL absolute
                    if link and not link.startswith('http'):
                        from urllib.parse import urljoin
                        link = urljoin(source['url'], link)
                    
                    stories.append({
                        'title': title,
                        'url': link,
                        'description': description,
                        'source': source['name'],
                        'grade_level': grade_level,
                        'topic': topic
                    })
                except Exception as e:
                    print(f"Error extracting story element: {e}")
                    continue
        
        except Exception as e:
            print(f"Error in _search_source: {e}")
        
        return stories
    
    def get_story_content(self, url: str) -> Optional[str]:
        """Fetch full story content from a URL"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                page = browser.new_page()
                page.goto(url, timeout=10000)
                page.wait_for_load_state('networkidle')
                
                # Try to find main content
                content_selectors = [
                    'article',
                    '.story-content',
                    '.content',
                    'main',
                    '#content'
                ]
                
                for selector in content_selectors:
                    if page.locator(selector).count() > 0:
                        content = page.locator(selector).first.inner_text()
                        browser.close()
                        return content
                
                # Fallback to body
                content = page.locator('body').inner_text()
                browser.close()
                return content
        
        except Exception as e:
            print(f"Error fetching story content: {e}")
            return None
