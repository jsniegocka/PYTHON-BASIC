"""
There is a list of most active Stocks on Yahoo Finance https://finance.yahoo.com/most-active.
You need to compose several sheets based on data about companies from this list.
To fetch data from webpage you can use requests lib. To parse html you can use beautiful soup lib or lxml.
Sheets which are needed:
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.


Example for the first sheet (you need to use same sheet format):
==================================== 5 stocks with most youngest CEOs ===================================
| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |
---------------------------------------------------------------------------------------------------------
| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |
...

About sheet format:
- sheet title should be aligned to center
- all columns should be aligned to the left
- empty line after sheet

Write at least 2 tests on your choose.
Links:
    - requests docs: https://docs.python-requests.org/en/latest/
    - beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - lxml docs: https://lxml.de/
"""

IS_COMPANIES_LIMIT  = False # introduce limit of scraped companies
COMPANIES_NUMBER_LIMIT = 10 # limit number of scraped companies

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep, time
import random

def set_web_scraping_urls():
    """Setting up web scraping urls"""
    start_url = "https://finance.yahoo.com/most-active/"
    search_url = "https://finance.yahoo.com/markets/stocks/most-active/"
    base_url = "https://finance.yahoo.com/"
    return start_url, search_url, base_url

def set_up_selenium_options():
    """Setting up Selenium options"""
    options = Options()
    options.page_load_strategy = 'eager'
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    return options

def set_up_selenium(options):
    """Setting up Selenium"""
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)
    return driver, wait

def accept_cookies(wait):
    """Accepting cookies (optionally)"""
    try:
        agree = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Accept')]")
            )
        )
        agree.click()
    except:
        pass

def get_beautiful_soup(driver, parser="html.parser"):
    """Getting page source and parse with BeautifulSoup"""
    html = driver.page_source
    soup = BeautifulSoup(html, parser)
    return soup

def get_info_from_companies_table(companies_table):
    """Getting info from companies table"""
    # Get company codes from table
    page_codes = [c.text.strip() for c in companies_table.find_all(class_="symbol yf-1pdfbgz")]

    # Get company names from table
    page_names = [
        n.text.strip()
        for n in companies_table.find_all(
            class_="leftAlignHeader companyName yf-362rys enableMaxWidth"
        )
    ]
    return page_codes, page_names


def collect_data_all_sheets(search_url, driver):
    """Collecting data for all sheets"""
    # Download dynamically codes nad names of all active companies
    start = 0
    count = 100
    companies_codes = []
    companies_names = []

    while True:
        url = f"{search_url}?start={start}&count={count}"
        print(f"Downloading: {url}")
        driver.get(url)
        # sleep(random.uniform(0.01, 0.03))

        # Get page source and parse with BeautifulSoup
        soup = get_beautiful_soup(driver, "html.parser")

        # Get table with company details
        companies_table = soup.find(class_="yf-1uayyp1 bd")
        if not companies_table: break

        # Get info from companies_table
        page_codes, page_names = get_info_from_companies_table(companies_table)
        if not page_codes: break

        # Collect info from one page
        companies_codes.extend(page_codes)
        companies_names.extend(page_names)
        start += count

    return companies_codes, companies_names

def get_specific_urls(base_url, companies_codes):
    """Getting specific urls"""
    companies_profiles_urls = [f"{base_url}quote/{company_code}/profile/" for company_code in companies_codes]
    companies_statistics_urls = [f"{base_url}quote/{company_code}/key-statistics/" for company_code in companies_codes]
    companies_holders_urls = [f"{base_url}quote/{company_code}/holders" for company_code in companies_codes]
    return companies_profiles_urls, companies_statistics_urls, companies_holders_urls

def restart_driver(driver, start_url, chrome_options):
    """Restarting driver"""
    print("Restarting driver...")
    driver.quit()
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)
    driver.get(start_url)

    # Accept cookies if needed
    accept_cookies(wait)

    return driver

def handle_error(driver, start_url, url, chrome_options):
    """Handling too many requests errors"""
    print("Block detected - restarting")
    driver = restart_driver(driver, start_url, chrome_options)
    return driver

def collect_data_first_sheet(soup, first_sheet_dict):
    """Collecting data for first sheet"""
    # Collect CEO data
    executives_table = soup.find("table")

    try:
        ceo_name = list(executives_table.find_all("td", string=lambda text: text and (
                "ceo" in text.lower() or "chief executive officer" in text.lower()))[0].parent)[0].text.strip()
    except:
        ceo_name = ""
    first_sheet_dict["CEO Name"] = ceo_name

    try:
        ceo_year_born = list(executives_table.find_all("td", string=lambda text: text and (
                "ceo" in text.lower() or "chief executive officer" in text.lower()))[0].parent)[4].text.strip()
        ceo_year_born = int(ceo_year_born)
    except:
        ceo_year_born = None
    first_sheet_dict["CEO Year Born"] = ceo_year_born

    # Collect employee data
    try:
        employee_number = list(
            soup.find("dt", class_="yf-kh0hf0", string=lambda text: text and ("employees" in text.lower())).parent)[
            2].text.strip()
        employee_number = int(employee_number.replace(",", ""))
    except:
        employee_number = None
    first_sheet_dict["Employees"] = employee_number

    # Collect address data
    try:
        country = soup.find(class_="address yf-kh0hf0").find_all("div")[-1].text.strip()
    except:
        country = ""
    first_sheet_dict["Country"] = country

    return first_sheet_dict

def collect_data_second_sheet(soup, second_sheet_dict):
    """Collecting data for second sheet"""
    # Collect cash data
    try:
        cash = soup.find("td", string=lambda text: text and (
                    "total cash" in text.lower() and "per share" not in text.lower())).parent.find("td",
                                                                                                   class_="value yf-vaowmx").text.strip()
    except:
        cash = ""
    second_sheet_dict["Total Cash"] = cash

    # Collect 52 Week Change
    try:
        week_change = soup.find(string=lambda text: "52 week change" in text.lower()).parent.parent.find("td",
                                                                                                         class_="value yf-vaowmx").text.strip()
        week_change = float(week_change.replace("%", ""))
    except:
        week_change = None
    second_sheet_dict["52-Week Change"] = week_change

    return second_sheet_dict

def collect_data_third_sheet(soup, third_sheet_dict):
    """Collecting data for third sheet"""
    # Collecting Blackrock data
    try:
        blackr_shares_list = list(soup.find("td", string=lambda text: "blackrock inc." in text.lower()).parent)
        shares = blackr_shares_list[1].text.strip()
        date = blackr_shares_list[2].text.strip()
        out = blackr_shares_list[3].text.strip()
        value = int(blackr_shares_list[4].text.strip().replace(",", ""))
    except:
        shares = ""
        date = ""
        out = ""
        value = None

    third_sheet_dict["Shares"] = shares
    third_sheet_dict["Date Reported"] = date
    third_sheet_dict["% Out"] = out
    third_sheet_dict["Value"] = value

    return third_sheet_dict

def collect_data_for_sheet(sheet_tag, urls, start_url, driver, chrome_options, number_per_session, companies_names, companies_codes):
    """Collecting data for one sheet"""
    sheet_dict_list = []
    for i, url in enumerate(urls):
        print(f"Collecting data for the {sheet_tag} sheet. Company {i + 1}/{len(urls)}")
        print(url)

        if i > 0 and i % number_per_session == 0:
            print("Restarting driver to avoid MaxRetryError...")
            driver = restart_driver(driver, start_url, chrome_options)
            driver.get(url)

        sheet_dict = {}
        driver.get(url)

        sheet_dict["Name"] = companies_names[i]
        sheet_dict["Code"] = companies_codes[i]

        # Handling too many requests errors
        current_url = driver.current_url.lower()
        if "404" in current_url and "err" in current_url:
            driver = handle_error(driver, start_url, url, chrome_options)
            driver.get(url)

        # Parsing html with Beautiful Soup
        soup = get_beautiful_soup(driver, "html.parser")

        # Choosing web scraping pattern
        match sheet_tag:
            case "first":
                sheet_dict = collect_data_first_sheet(soup, sheet_dict)
            case "second":
                sheet_dict = collect_data_second_sheet(soup, sheet_dict)
            case "third":
                sheet_dict = collect_data_third_sheet(soup, sheet_dict)

        sheet_dict_list.append(sheet_dict)

    return sheet_dict_list

def remove_empty_rows(sheet_dict_list, key):
    """Remove empty rows for sorting"""
    sheet_dict_list_filtered = [
        row for row in sheet_dict_list
        if row.get(key) is not None
    ]
    return sheet_dict_list_filtered

def sort_sheet_dict_list(sheet_dict_list, key, reverse=False):
    """Sort sheet information"""
    sheet_dict_list_sorted = sorted(
        sheet_dict_list,
        key=lambda row: row[key],
        reverse=reverse
    )
    return sheet_dict_list_sorted

def remove_duplicates(rows, columns):
    """Remove duplicate rows based on specified columns"""
    seen = set()
    unique_rows = []
    for row in rows:
        row_tuple = tuple(row.get(col, "") for col in columns)
        if row_tuple not in seen:
            seen.add(row_tuple)
            unique_rows.append(row)
    return unique_rows

def print_sheet(title, columns, rows):
    """Print sheet information"""
    # Remove duplicates
    rows = remove_duplicates(rows, columns)

    # Setting columns widths: max(title, data)
    col_widths = {}
    for col in columns:
        col_widths[col] = max(
            len(col),
            max(len(str(row.get(col, ""))) for row in rows)
        )

    # Setting table width
    table_width = (
            sum(col_widths[col] for col in columns)
            + 3 * len(columns) + 1
    )

    # Title
    print(title.center(table_width, "="))

    # Header
    header = "| " + " | ".join(
        col.ljust(col_widths[col]) for col in columns
    ) + " |"
    print(header)

    # Separator
    print("-" * table_width)

    # Rows
    for row in rows:
        line = "| " + " | ".join(
            str(row.get(col, "")).ljust(col_widths[col])
            for col in columns
        ) + " |"
        print(line)

    print()

def get_stock_info():

    # Set up web scraping urls
    start_url, search_url, base_url = set_web_scraping_urls()

    # Set up Selenium
    chrome_options = set_up_selenium_options()
    driver, wait = set_up_selenium(chrome_options)
    driver.get(start_url)

    # Accept cookies if needed
    accept_cookies(wait)

    # Collect data for all sheets
    companies_codes, companies_names = collect_data_all_sheets(search_url, driver)

    # Get specific urls
    companies_profiles_urls, companies_statistics_urls, companies_holders_urls = get_specific_urls(base_url, companies_codes)

    # Print web scraping information
    print(f"Number of companies: {len(companies_profiles_urls)}")
    print(companies_codes)
    print(companies_names)
    print(companies_profiles_urls)
    print(companies_statistics_urls)
    print(companies_holders_urls)

    # Prepare for data collecting and processing
    first_sheet_dict_list, second_sheet_dict_list, third_sheet_dict_list = [], [], []
    sheet_dict_lists = [first_sheet_dict_list, second_sheet_dict_list, third_sheet_dict_list]
    sheet_tags = ["first", "second", "third"]
    sheet_urls = [companies_profiles_urls, companies_statistics_urls, companies_holders_urls]
    keys = ["CEO Year Born", "52-Week Change", "Value"]
    reversing = [False, True, True]
    row_numbers = [5, 10, 10] # number of companies in each sheet
    sheet_titles = ["5 stocks with most youngest CEOs", "10 stocks with best 52-Week Change", "10 largest holds of Blackrock Inc."]
    companies_number_limit_bool = IS_COMPANIES_LIMIT # introduce limit of scraped companies
    companies_number_limit = COMPANIES_NUMBER_LIMIT # limit number of scraped companies
    number_per_session = 160 # limit number of companies per session

    # Collect data from dynamically created html for all sheets
    if companies_number_limit_bool:
        for i, sheet in enumerate(sheet_dict_lists):
            # Restart session
            driver = restart_driver(driver, start_url, chrome_options)
            # Collect data
            sheet_dict_lists[i] = collect_data_for_sheet(sheet_tags[i], sheet_urls[i][0:companies_number_limit], start_url, driver, chrome_options, number_per_session, companies_names, companies_codes)
    else:
        for i, sheet in enumerate(sheet_dict_lists):
            # Restart session
            driver = restart_driver(driver, start_url, chrome_options)
            sheet_dict_lists[i] = collect_data_for_sheet(sheet_tags[i], sheet_urls[i], start_url, driver, chrome_options, number_per_session, companies_names, companies_codes)

    driver.quit()

    # Process data and print sheets
    for i, sheet in enumerate(sheet_dict_lists):
        # Remove empty rows
        sheet_dict_lists[i] = remove_empty_rows(sheet_dict_lists[i], keys[i])
        # Sort data
        sheet_dict_lists[i] = sort_sheet_dict_list(sheet_dict_lists[i], keys[i], reversing[i])
        # Limit number of rows
        sheet_dict_lists[i] = sheet_dict_lists[i][0:row_numbers[i]]

    # Custom changes to sheets
    for row in sheet_dict_lists[0]:
        row["Employees"] = f"{row["Employees"]:,}"

    for row in sheet_dict_lists[1]:
        row["52-Week Change"] = f"{row["52-Week Change"]}%"

    for row in sheet_dict_lists[2]:
        row["Value"] = f"{row["Value"]:,}"

    # Print sheets
    for i, sheet in enumerate(sheet_dict_lists):
        print_sheet(sheet_titles[i], sheet_dict_lists[i][0].keys(), sheet_dict_lists[i])

if __name__ == "__main__":
    start_time = time()
    get_stock_info()
    end_time = time()
    execution_time = end_time - start_time
    print(f"Function executed in {execution_time:.6f} seconds")