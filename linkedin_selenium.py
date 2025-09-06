# linkedin_selenium.py
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from state import State

def post_to_linkedin_selenium(state: State) -> State:
    post_text = state.get("post_draft", "")
    cert_image = state.get("cert_image_path")

    if not post_text:
        return {"slack_response": {"ok": False, "error": "No post draft to publish"}}

    try:
        linkedin_user = os.getenv("LINKEDIN_USERNAME")
        linkedin_pass = os.getenv("LINKEDIN_PASSWORD")
        if not linkedin_user or not linkedin_pass:
            return {"slack_response": {"ok": False, "error": "LinkedIn credentials not set"}}

        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        wait = WebDriverWait(driver, 15)

        # Login
        driver.get("https://www.linkedin.com/login")
        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        username.send_keys(linkedin_user)
        password.send_keys(linkedin_pass)
        password.send_keys(Keys.RETURN)
        time.sleep(5)

        # Open post dialog
        driver.get("https://www.linkedin.com/feed/")
        post_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Start a post')]")))
        post_box.click()
        time.sleep(2)

        # Add text
        text_area = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ql-editor")))
        text_area.send_keys(post_text)
        time.sleep(1)

        # Upload image if available
        if cert_image and os.path.exists(cert_image):
            add_media_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Add media']")))
            add_media_btn.click()
            time.sleep(1)

            file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            file_input.send_keys(cert_image)
            time.sleep(3)

            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next']")))
            next_button.click()
            time.sleep(2)

        # Publish
        post_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label,'Post')]")))
        post_button.click()
        time.sleep(3)

        driver.quit()
        return {"slack_response": {"ok": True, "status": "LinkedIn post published via Selenium"}}

    except Exception as e:
        try:
            driver.quit()
        except:
            pass
        return {"slack_response": {"ok": False, "error": str(e)}}
