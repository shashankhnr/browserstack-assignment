# browserstack_test.py
import os
import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions, FirefoxOptions, SafariOptions

# -------- BrowserStack Credentials --------
BS_USER = os.getenv("BROWSERSTACK_USERNAME") or "shashankganeshna_aZwFo8"
BS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY") or "oCVyDtkEpxeghs54sVHN"
if not BS_USER or not BS_KEY:
    print("BrowserStack credentials not found!")
    raise SystemExit(1)

HUB = f"https://{BS_USER}:{BS_KEY}@hub-cloud.browserstack.com/wd/hub"

# -------- BrowserStack Capabilities --------
CAPS = [
    {"browserName": "Chrome", "browserVersion": "latest",
     "bstack:options": {"os": "Windows", "osVersion": "11", "sessionName": "Test-1"}},
    {"browserName": "Firefox", "browserVersion": "latest",
     "bstack:options": {"os": "Windows", "osVersion": "11", "sessionName": "Test-2"}},
    {"browserName": "Safari", "browserVersion": "16.0",
     "bstack:options": {"os": "OS X", "osVersion": "Ventura", "sessionName": "Test-3"}},
    {"browserName": "Chrome", "browserVersion": "latest",
     "bstack:options": {"deviceName": "Samsung Galaxy S23", "realMobile": "true", "sessionName": "Test-4"}},
    {"browserName": "Safari", "browserVersion": "latest",
     "bstack:options": {"deviceName": "iPhone 14", "realMobile": "true", "sessionName": "Test-5"}},
]

# -------- Helper to get proper options per browser --------
def get_options(browser_name):
    browser_name = browser_name.lower()
    if browser_name == "chrome":
        return ChromeOptions()
    elif browser_name == "firefox":
        return FirefoxOptions()
    elif browser_name == "safari":
        return SafariOptions()
    else:
        return ChromeOptions()  # fallback

# -------- Run one session --------
def run_one(cap):
    session_name = cap.get("bstack:options", {}).get("sessionName")
    print(f"[START] session: {session_name}")

    options = get_options(cap["browserName"])
    for key, value in cap.items():
        options.set_capability(key, value)

    driver = webdriver.Remote(command_executor=HUB, options=options)
    sid = driver.session_id
    print(f"Session id: {sid}")

    try:
        driver.get("https://elpais.com/opinion/")
        time.sleep(4)

        try:
            el = driver.find_element(By.TAG_NAME, "article")
            sample = el.text[:140]
        except Exception:
            sample = "N/A"

        print(sid, "sample:", sample)

        # Mark session as passed on BrowserStack
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed","reason":"Smoke check passed"}}'
        )

    except Exception as e:
        print("Error during run:", e)
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed","reason":"Exception occurred"}}'
        )

    finally:
        driver.quit()
    return sid

# -------- Run all sessions in parallel --------
if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(run_one, CAPS))
    print("All sessions done:", results)
