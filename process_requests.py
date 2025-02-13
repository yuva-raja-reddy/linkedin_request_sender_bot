import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# ====== User Configurable Variables ======
LINKEDIN_EMAIL = "@gmail.com"
LINKEDIN_PASSWORD = ""
SEARCH_QUERY = "Recruiter"    # Modify to search for other types of people if needed
WAIT_TIME = 6                # General wait time in seconds
# =========================================

current_dir = os.getcwd()
chromedriver_path = os.path.join(current_dir, "chromedriver")

options = webdriver.ChromeOptions()
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()
wait = WebDriverWait(driver, WAIT_TIME)

def close_popups():
    """
    Close popups such as:
    - Weekly limit warnings
    - Email verification dialogs
    - 'Got it' network growth popups
    """
    # 1. Weekly limit or other artdeco-button--tertiary popups
    try:
        weekly_popup = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'artdeco-button--tertiary')]"))
        )
        weekly_popup.click()
        print("Weekly limit warning popup closed.")
    except Exception:
        pass

    # 2. Email verification or dismiss/close popups
    try:
        verify_popup = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Dismiss') or contains(text(),'Close')]"
        )
        verify_popup.click()
        print("Email verification popup closed.")
    except Exception:
        pass

    # 3. "Got it" popups for "You're growing your network!"
    try:
        got_it_button = driver.find_element(By.XPATH, "//button[@aria-label='Got it']")
        got_it_button.click()
        print("Clicked 'Got it' button for network popup.")
    except Exception:
        pass

def check_weekly_limit():
    """
    Checks if the EXACT element:
      <h2 id="ip-fuse-limit-alert__header">You’ve reached the weekly invitation limit</h2>
    is present. Returns True if found.
    """
    try:
        limit_message = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//h2[@id='ip-fuse-limit-alert__header' and normalize-space(text())=\"You’ve reached the weekly invitation limit\"]")
            )
        )
        if limit_message:
            return True
    except Exception:
        return False
    return False

def exit_if_weekly_limit():
    """
    If the weekly limit popup is detected, print details, close the browser,
    and exit the script.
    """
    if check_weekly_limit():
        print("Weekly invitation limit reached. Halting further requests.")
        try:
            limit_details = driver.find_element(By.XPATH, "//h2[@id='ip-fuse-limit-alert__header']").text
            print("Popup details:", limit_details)
        except Exception as ex:
            print("Could not retrieve popup details:", ex)
        driver.quit()
        sys.exit(0)

def linkedin_login():
    """
    Navigates to the LinkedIn login page, waits for the user to solve any captcha,
    then automatically fills in email/password. User can click 'Sign in' manually
    or let the script click the submit button.
    """
    driver.get("https://www.linkedin.com/login")
    time.sleep(3)

    input("If there's a 'Verify you're not a bot' or any challenge, solve it now in the browser. Then press Enter here to continue...")

    # Fill in email
    email_field = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    email_field.clear()
    email_field.send_keys(LINKEDIN_EMAIL)

    # Fill in password
    password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    password_field.clear()
    password_field.send_keys(LINKEDIN_PASSWORD)

    # Optionally auto-click "Sign in"
    # Click on the "Keep me logged in" checkbox
    try:
        label = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='rememberMeOptIn-checkbox']")))
        label.click()
        print("Keep me logged in Checkbox clicked")
    except Exception as e:
        print("Failed to click the Checkbox:", e)

    sign_in_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))) 
    sign_in_btn.click()
    print("Attempted to sign in automatically.")

    input("Press Enter once you're fully logged in (either manually or automatically) to continue with connection requests...")

def send_connection_requests():
    """
    Continuously processes LinkedIn People search results
    and sends connection requests until the weekly limit is reached
    or the "Next" button cannot be found.
    """
    base_search_url = f"https://www.linkedin.com/search/results/people/?keywords={SEARCH_QUERY}"
    driver.get(base_search_url)
    time.sleep(5)  # Allow search results to load

    while True:
        print("Processing current page...")
        time.sleep(2)

        # Scroll down to load all search results on the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # Find all "Connect" buttons on the page
        connect_buttons = driver.find_elements(By.XPATH, "//span[text()='Connect']/ancestor::button")
        print(f"Found {len(connect_buttons)} 'Connect' buttons on this page.")

        for button in connect_buttons:
            # Check if we've hit the weekly limit BEFORE clicking
            exit_if_weekly_limit()

            try:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                time.sleep(1)
                button.click()
                time.sleep(2)

                # Check again AFTER clicking, in case the popup appears immediately
                exit_if_weekly_limit()

                # Look for the "Send without a note" button
                try:
                    send_btn = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//button[@aria-label='Send without a note']")
                    ))
                    send_btn.click()
                    print("Connection request sent.")
                except Exception:
                    # If we can't find "Send without a note", try "Done" or dismiss
                    try:
                        done_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Done')]")
                        done_btn.click()
                        print("Connection request sent (via Done button).")
                    except Exception:
                        print("Send/Done button not found. Skipping this connection.")
                        try:
                            dismiss_btn = driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                            dismiss_btn.click()
                        except Exception:
                            pass

                time.sleep(3)
                close_popups()
            except Exception as e:
                print(f"Error during connection request: {e}")
                # Print the current page text for debugging
                print("============this is in page ===============")
                try:
                    body_text = driver.find_element(By.TAG_NAME, "body").text
                    print(body_text)
                except Exception as ex:
                    print(f"Could not retrieve page text: {ex}")
                continue

        # Attempt to click the "Next" button to load more results
        try:
            next_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[@aria-label='Next']")
            ))
            next_button.click()
            print("Navigating to next page...")
            time.sleep(5)
        except Exception as e:
            print("Next button not found. Ending process.")
            print("============this is in page ===============")
            try:
                body_text = driver.find_element(By.TAG_NAME, "body").text
                print(body_text)
            except Exception as ex:
                print(f"Could not retrieve page text: {ex}")
            break

if __name__ == "__main__":
    start_time = time.time()  # Track script start time

    linkedin_login()
    send_connection_requests()

    end_time = time.time()    # Track script end time
    elapsed = end_time - start_time
    minutes = round(elapsed / 60, 2)
    print("================================================================")
    print("Script complete. Closing browser.")
    driver.quit()

    print(f"====> You have saved approximately {minutes} minute(s) by automating this code!")