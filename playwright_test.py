import os
import time 
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv


def login_to_website():
    with sync_playwright() as p:
        # Launch a browser (securely disable headless mode for debugging)
        browser = p.chromium.launch(headless=False)  # Use headless=False for debugging
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the login page
        page.goto("https://canvas.ucsd.edu/courses/59004/external_tools/5826")

        # Load environment variables from .env file
        load_dotenv()

        # Get the username from the environment variable
        username = os.getenv('CANVAS_USERNAME')
        password = os.getenv('CANVAS_PASSWORD')
        print(username, password)
        # Fill in the username textbox
        page.fill('input[type="username"]', username)
        page.fill('input[type="password"]', password)
        # Click the submit button
        page.click('button[type="submit"]')
        
        # page.wait_for_timeout(timeout=10000)
        # page.wait_for_selector() # apparently this function is discouraged: https://playwright.dev/python/docs/api/class-page
        # page.wait_for_url('https://canvas.ucsd.edu/courses/59004/external_tools/5826)')

        page.wait_for_selector('h1#header-text:has-text("Check for a Duo Push")', timeout=15000)  # Wait for Duo Push prompt

        start_time = time.time()
        while time.time() - start_time < 30:  # Timeout after 30 seconds
            current_title = page.title()
            print("hello")
            if current_title == "Media Gallery":
                print("Title is 'Media Gallery'")
                break
            time.sleep(1)  # Check every second

        if time.time() - start_time >= 30:
            print("Timeout: Title was not 'Media Gallery' within 30 seconds.")
        
        print("Login successful!")

        # Take a screenshot
        page.screenshot(path="screenshot.png")

        # Close the browser
        browser.close()

if __name__ == "__main__":
    login_to_website()
