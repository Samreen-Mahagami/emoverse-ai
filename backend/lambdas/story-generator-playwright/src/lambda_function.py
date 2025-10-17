import json
import logging
import asyncio
from playwright.async_api import async_playwright
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

EDUCATIONAL_WEBSITES = {
    'emotions': [
        {'name': 'Scholastic Emotions', 'url': 'https://www.scholastic.com/teachers/books-and-authors/', 'selectors': ['h3', '.title', '.book-title', 'a[href*="book"]']},
        {'name': 'PBS Kids Stories', 'url': 'https://pbskids.org/games/stories/', 'selectors': ['.game-title', 'h2', '.activity-title', '.story-title']}
    ],
    'friendship': [
        {'name': 'Reading Rockets', 'url': 'https://www.readingrockets.org/books-and-authors/books/', 'selectors': ['.book-title', 'h3', '.title', 'a[title*="friend"]']},
        {'name': 'Common Sense Media', 'url': 'https://www.commonsensemedia.org/lists/books-that-build-character', 'selectors': ['h3', '.content-title', '.book-title']}
    ]
}

async def scrape_single_site(site, theme, grade_level):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(site['url'], timeout=15000, wait_until='domcontentloaded')
            await asyncio.sleep(1)

            story_titles = []
            for selector in site['selectors']:
                elements = await page.query_selector_all(selector)
                for element in elements[:8]:
                    text = (await element.inner_text()).strip()
                    if len(text) > 5:
                        story_titles.append(text)
                if len(story_titles) >= 3:
                    break

            await context.close()
            await browser.close()

            return {'website': site['name'], 'url': site['url'], 'stories': list(dict.fromkeys(story_titles))[:3], 'theme': theme, 'grade_level': grade_level}

    except Exception as e:
        logger.warning(f"Failed to scrape {site['name']}: {e}")
        return {'website': site['name'], 'url': site['url'], 'stories': [], 'theme': theme, 'grade_level': grade_level}

async def scrape_educational_stories_async(theme, grade_level):
    websites = EDUCATIONAL_WEBSITES.get(theme, EDUCATIONAL_WEBSITES['emotions'])
    tasks = [scrape_single_site(site, theme, grade_level) for site in websites]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return [r for r in results if isinstance(r, dict) and r.get('stories')]

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}')) if 'body' in event else event
        story_theme = body.get('story_theme', 'emotions')
        grade_level = body.get('grade_level', 'Grade 5')

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        live_stories = loop.run_until_complete(scrape_educational_stories_async(story_theme, grade_level))
        loop.close()

        if not live_stories:
            live_stories = [{'website': 'Fallback', 'url': '#', 'stories': ['Story 1', 'Story 2'], 'theme': story_theme, 'grade_level': grade_level}]

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'success': True, 'live_stories': live_stories, 'scraped_count': len(live_stories)})
        }

    except Exception as e:
        logger.error(f"Playwright Lambda error: {e}")
        return {'statusCode': 500, 'body': json.dumps({'success': False, 'error': str(e), 'live_stories': []})}
