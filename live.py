from playwright.sync_api import sync_playwright
import time

def get_video_transcript_and_track_time():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Launch Chrome
        context = browser.new_context()
        page = context.new_page()
        
        # Open the webpage
        page.goto("https://podcast.ucsd.edu/watch/fa24/cse158_a00/16")  # Replace with the correct URL
        
        # Wait for the video player to load (adjust selectors based on the actual page)
        page.wait_for_selector("iframe#kaltura_player_ifp")

        # Interact with the iframe to access the player
        frame = page.frame(name="kaltura_player_ifp")
        time_element = page.query_selector('body > div.mwPlayerContainer.kdark.ua-mouse.ua-win.ua-chrome.size-large.pause-state > div.controlBarContainer.hover.open > div.controlsContainer > div.timers.comp.currentTimeLabel.display-high')
        if not frame:
            print("Video iframe not found.")
            return
        
        # Get the transcript if available
        try:
            transcript = frame.query_selector("div.transcript-text")  # Adjust selector if needed
            if transcript:
                print("Transcript:")
                print(transcript.inner_text())
            else:
                print("Transcript not found.")
        except Exception as e:
            print(f"Error fetching transcript: {e}")
        
        # Start tracking video time
        print("Tracking video time...")
        try:
            while True:
                print('...')
                #current_time = frame.evaluate("() => document.querySelector('video').currentTime")
                if time_element:
                    current_time = float(time_element.inner_text())
                    print(f"Current video time: {current_time:.2f} seconds")
                else:
                    print("Time element not found.")
                    time_element = page.locator('xpath=/html/body/div[1]/div[4]/div[2]/div[2]')

                time.sleep(1)  # Poll every second
        except KeyboardInterrupt:
            print("Stopped tracking video time.")
        finally:
            browser.close()

if __name__ == "__main__":
    get_video_transcript_and_track_time()
