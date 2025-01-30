import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

URL = "https://www.gsk.com/en-gb/"
async def main():
    browser_conf = BrowserConfig(headless=True)  # or False to see the browser
    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS
    )
    async with AsyncWebCrawler(config=browser_conf) as crawler:
        result = await crawler.arun(
            url= URL,
            config=run_conf
        )
        print(result.cleaned_html)

if __name__ == "__main__":
    asyncio.run(main=main())
