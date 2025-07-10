
from faker import Faker  # Import the Faker library
import asyncio
from playwright.async_api import async_playwright  # Use async_playwright instead of sync_playwright
import nest_asyncio

nest_asyncio.apply()

# Flag to indicate whether the script is running
running = True

async def start(name, user, wait_time, meetingcode, passcode):
    print(f"{name} started!")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--use-fake-device-for-media-stream', '--use-fake-ui-for-media-stream'])
        context = await browser.new_context(permissions=['microphone'])
        page = await context.new_page()
        await page.goto(f'https://zoom.us/wc/join/{meetingcode}', timeout=60000)

        try:
            await page.click('//button[@id="onetrust-accept-btn-handler"]', timeout=5000)
        except:
            pass

        try:
            await page.click('//button[@id="wc_agree1"]', timeout=5000)
        except:
            pass

        try:
            await page.wait_for_selector('input[type="text"]', timeout=10000)
            await page.fill('input[type="text"]', user)
            await page.fill('input[type="password"]', passcode)
            join_button = await page.wait_for_selector('button.preview-join-button', timeout=10000)
            await join_button.click()
        except:
            pass

        try:
            query = '//button[text()="Join Audio by Computer"]'
            await asyncio.sleep(3)
            mic_button_locator = await page.wait_for_selector(query, timeout=10000)
            await asyncio.sleep(2)
            await mic_button_locator.evaluate_handle('node => node.click()')
            print(f"{name} mic aayenge.")
        except Exception as e:
            print(f"{name} mic nahe aayenge. ", e)

        print(f"{name} sleep for {wait_time} seconds ...")
        while running and wait_time > 0:
            await asyncio.sleep(1)
            wait_time -= 1
        print(f"{name} ended!")

        await browser.close()

async def main():
    global running
    number = int(input("Enter number of Users: "))
    meetingcode = input("Enter meeting code (No Space): ")
    passcode = input("Enter Password (No Space): ")

    sec = 90
    wait_time = sec * 60

    tasks = []
    fake = Faker('en_US')
    for i in range(number):
        user = fake.name()
        task = start(f'[Thread{i}]', user, wait_time, meetingcode, passcode)
        tasks.append(task)

    await asyncio.gather(*tasks)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
