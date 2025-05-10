'''pip install playwright
   playwright install
'''

from playwright.sync_api import sync_playwright

def scrape_hacker_news():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Go to Hacker News homepage
        page.goto("https://news.ycombinator.com/")

        # Get all the story titles
        titles = page.locator(".titleline > a").all_text_contents()

        # Print the titles
        print("Top Hacker News Stories:")
        for title in (titles):
            print(f"{title}")

        # Close browser
        browser.close()

if __name__ == "__main__":
    scrape_hacker_news()
