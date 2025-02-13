LinkedIn Connection Request Bot

This is a simple Python-based bot that automates sending LinkedIn connection requests based on a search query. The script logs into your LinkedIn account, navigates through search results, clicks on "Connect" buttons, and sends connection requests using the "Send without a note" or "Done" button. It then clicks the Next page button to process up to a specified number of pages.

> **Disclaimer:**  
> Use this script at your own risk. Automated actions on LinkedIn may violate their terms of service and can result in account restrictions. This project is for educational purposes only.

## Features

- **Automated Login:** Logs into LinkedIn using your credentials.
- **Search and Connect:** Searches for people matching a specified query and sends connection requests.
- **Pagination:** Navigates through search results by clicking the Next page button.
- **Pop-up Handling:** Closes common pop-ups (e.g., "Got it", email verification, etc.) automatically.
- **Optimized Interactions:** Uses JavaScript clicks with explicit waits to speed up the process without sacrificing reliability.

## Prerequisites

- **Python 3.x**
- **Selenium:** Install via pip:
  ```bash
  pip install selenium
  ```
- **Chrome WebDriver:**  
  Download the correct version of ChromeDriver for your version of Chrome from [ChromeDriver Downloads](https://sites.google.com/chromium.org/driver/). Place the executable in the same directory as the script or add it to your system PATH.
- **Google Chrome Browser**

## Setup

1. **Clone or Download the Repository:**  
   Download the repository or copy the script file to your local machine.

2. **Configure Your Credentials and Settings:**  
   Edit the script to update the following variables:
   - `LINKEDIN_EMAIL`: Your LinkedIn email address.
   - `LINKEDIN_PASSWORD`: Your LinkedIn password.
   - `SEARCH_QUERY`: The query to search for people (e.g., "Recruiter").
   - `MAX_PAGES`: Maximum number of pages to process (default is 100).
   - `WAIT_TIME`: Wait time for elements to load (adjust if your network is slow).

## How to Run

1. Open your terminal or command prompt.
2. Navigate to the directory containing the script and ChromeDriver.
3. Run the script:
   ```bash
   python process_requests_main.py
   ```
4. A Chrome browser window will open and navigate to LinkedIn's login page.
5. The script will automatically enter your credentials and click the "Keep me logged in" checkbox.
6. **Important:** If there are any challenges or captchas, solve them manually.
7. Once you're fully logged in, return to the terminal and press **Enter** to start processing connection requests.
8. The bot will then process each page and click the Next page button until it reaches the set maximum number of pages.

## Troubleshooting

- **Element Not Found / Timeout Errors:**  
  Ensure that your ChromeDriver version matches your Chrome browser version. If pages load slowly, consider increasing the `WAIT_TIME` variable.
  
- **Account Restrictions:**  
  LinkedIn may flag automated behavior. Use the script responsibly and consider implementing additional delays or randomness if needed.

## License

This project is for educational purposes only. There is no warranty provided. Use at your own risk.

## Disclaimer

By using this script, you acknowledge that you are responsible for complying with LinkedIn's terms of service. The author is not liable for any consequences resulting from the use of this script.
