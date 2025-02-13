import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def close_popups():
    """
    Closes popups on LinkedIn like weekly limit warnings, email verifications,
    and "Got it" network popups.
    """
    try:
        weekly_popup = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'artdeco-button--tertiary')]")
        ))
        driver.execute_script("arguments[0].click();", weekly_popup)
        print("Weekly limit warning popup closed.")
    except Exception:
        pass

    try:
        verify_popup = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Dismiss') or contains(text(),'Close')]"
        )
        driver.execute_script("arguments[0].click();", verify_popup)
        print("Email verification popup closed.")
    except Exception:
        pass

    try:
        got_it_button = driver.find_element(By.XPATH, "//button[@aria-label='Got it']")
        driver.execute_script("arguments[0].click();", got_it_button)
        print("Clicked 'Got it' button for network popup.")
    except Exception:
        pass

def linkedin_login():
    """
    Logs into LinkedIn by waiting for the necessary elements,
    clicking the "Keep me logged in" checkbox (via its label),
    and then clicking the sign-in button.
    """
    driver.get("https://www.linkedin.com/login")
    
    # Enter email
    email_field = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    email_field.clear()
    email_field.send_keys(LINKEDIN_EMAIL)

    # Enter password
    password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    password_field.clear()
    password_field.send_keys(LINKEDIN_PASSWORD)

    # Click the "Keep me logged in" checkbox via its label
    try:
        label = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='rememberMeOptIn-checkbox']")))
        driver.execute_script("arguments[0].click();", label)
        print("Keep me logged in checkbox clicked.")
    except Exception as e:
        print("Failed to click the 'Keep me logged in' checkbox:", e)

    # Click the sign in button
    sign_in_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    driver.execute_script("arguments[0].click();", sign_in_btn)
    print("Attempted to sign in automatically.")

    input("Press Enter once you're fully logged in (either manually or automatically) to continue with connection requests...")

def send_connection_requests():
    """
    Processes the LinkedIn search results for people matching SEARCH_QUERY,
    sending connection requests on each page. Even if no "Connect" buttons are found,
    it clicks the Next page button to proceed. This loop runs until MAX_PAGES is reached.
    """
    base_search_url = f"https://www.linkedin.com/search/results/people/?keywords={SEARCH_QUERY}"
    driver.get(base_search_url)
    
    for current_page in range(1, MAX_PAGES + 1):
        print(f"\nProcessing page {current_page}...")
        
        # Wait for the search results container to load
        try:
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//ul[contains(@class, 'reusable-search__entity-result-list')]")
            ))
        except Exception:
            print(f"Search results container not found on page {current_page}.")
        
        # Scroll down to load all search results
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Find all Connect buttons
        try:
            connect_buttons = driver.find_elements(By.XPATH, "//span[text()='Connect']/ancestor::button")
        except Exception:
            connect_buttons = []
        
        if connect_buttons:
            print(f"Found {len(connect_buttons)} 'Connect' buttons on page {current_page}.")
            for button in connect_buttons:
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                    driver.execute_script("arguments[0].click();", button)
                    
                    # Try clicking "Send without a note" first, then "Done"
                    try:
                        send_btn = wait.until(EC.element_to_be_clickable(
                            (By.XPATH, "//button[@aria-label='Send without a note']")
                        ))
                        driver.execute_script("arguments[0].click();", send_btn)
                        print("Connection request sent.")
                    except Exception:
                        try:
                            done_btn = wait.until(EC.element_to_be_clickable(
                                (By.XPATH, "//button[contains(text(),'Done')]")
                            ))
                            driver.execute_script("arguments[0].click();", done_btn)
                            print("Connection request sent (via Done button).")
                        except Exception:
                            print("Send/Done button not found. Skipping this connection.")
                            try:
                                dismiss_btn = wait.until(EC.element_to_be_clickable(
                                    (By.XPATH, "//button[@aria-label='Dismiss']")
                                ))
                                driver.execute_script("arguments[0].click();", dismiss_btn)
                            except Exception:
                                pass
                    
                    close_popups()
                except Exception as e:
                    print("Error during connection request:", e)
                    continue
        else:
            print(f"No 'Connect' buttons found on page {current_page}.")
        
        # Click the Next page button to proceed
        try:
            next_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@aria-label, 'Next')]")
            ))
            driver.execute_script("arguments[0].click();", next_button)
            print("Moving to next page...")
        except Exception as e:
            print("Next page button not found, ending process.")
            break


# ====== User Configurable Variables ======
LINKEDIN_EMAIL = "@gmail.com"
LINKEDIN_PASSWORD = ""
SEARCH_QUERY = "Recruiter"    # Modify as needed
WAIT_TIME = 10                # Increase if your network is slow
MAX_PAGES = 100               # Process up to 100 pages
# =========================================

current_dir = os.getcwd()
chromedriver_path = os.path.join(current_dir, "chromedriver")

options = webdriver.ChromeOptions()
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()
wait = WebDriverWait(driver, WAIT_TIME)


if __name__ == "__main__":
    start_time = time.time()  
    linkedin_login()
    send_connection_requests()
    print("\nScript complete. Closing browser.")
    driver.quit()
    end_time = time.time() 
    elapsed = end_time - start_time
    minutes = round(elapsed / 60, 2)
    print(f"====> You have saved approximately {minutes} minute(s) by automating this code!")


