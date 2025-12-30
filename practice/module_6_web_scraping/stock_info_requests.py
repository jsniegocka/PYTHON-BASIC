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

BASE_URL = "https://finance.yahoo.com/"
SEARCH_URL = "https://finance.yahoo.com/markets/stocks/most-active/"
IS_COMPANIES_LIMIT  = False # introduce limit of scraped companies
COMPANIES_NUMBER_LIMIT = 10 # limit number of scraped companies

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

import requests
from bs4 import BeautifulSoup
import yfinance as yf
from time import time


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

def get_specific_urls(base_url, company_code):
    """Getting specific urls"""
    company_profiles_url = f"{base_url}quote/{company_code}/profile/"
    company_statistics_url = f"{base_url}quote/{company_code}/key-statistics/"
    company_holders_url = f"{base_url}quote/{company_code}/holders"
    return company_profiles_url, company_statistics_url, company_holders_url

def collect_data_first_and_second_sheet(sym, info_dict, sheet_1, sheet_2):
    """Collecting data for first sheet and second sheet"""
    # Collect data
    name = info_dict.get("longName", "")

    officers = info_dict.get("companyOfficers", [])
    ceo_name = None
    ceo_year = None

    for officer in officers:
        title = officer.get("title", "").lower()
        if "ceo" in title or "chief executive officer" in title:
            ceo_name = officer.get("name")
            ceo_year = officer.get("yearBorn")
            break

    employees = info_dict.get("fullTimeEmployees", None)
    country = info_dict.get("country", None)

    # Creating data for sheet 2
    change = info_dict.get("52WeekChange", None)
    cash = info_dict.get("totalCash", None)

    # Add data
    sheet_1.append({
        "Name": name,
        "Code": sym,
        "Country": country,
        "Employees": employees,
        "CEO Name": ceo_name,
        "CEO Year Born": ceo_year
    })

    sheet_2.append({
        "Name": name,
        "Code": sym,
        "52-Week Change": change,
        "Total Cash": cash
    })
    return name

def collect_data_third_sheet(sym, name, holders, sheet_3):
    """Collecting data for third sheet"""
    if holders is None or holders.empty:
        return

    blackrock = holders[holders['Holder'].str.contains("blackrock", case=False, na=False)]

    if blackrock.empty:
        return

    row = blackrock.iloc[0]

    # Add data
    sheet_3.append({
        "Name": name,
        "Code": sym,
        "Shares": row.get("Shares", 0),
        "Date Reported": row.get("Date Reported"),
        "% Out": row.get("pctHeld", 0.0),
        "Value": row.get("Value", 0)
    })

def collect_data_all_sheets(search_url):
    """Collecting data for all sheets"""
    # Download dynamically codes and names of all active companies
    start = 0
    count = 100
    companies_codes = []
    companies_names = []

    while True:
        url = f"{search_url}?start={start}&count={count}"
        print(f"Downloading: {url}")

        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            break

        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Get table with company details
        companies_table = soup.find(class_="yf-1uayyp1 bd")
        if not companies_table:
            break

        # Get info from companies_table
        page_codes, page_names = get_info_from_companies_table(companies_table)
        if not page_codes:
            break

        # Collect info from one page
        companies_codes.extend(page_codes)
        companies_names.extend(page_names)
        start += count

    return companies_codes, companies_names

def remove_empty_rows(sheet_dict_list, key):
    """Remove empty rows for sorting"""
    sheet_dict_list_filtered = [
        row for row in sheet_dict_list
        if (row.get(key) is not None) and (row.get(key) != "")
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
    # Collect data for all sheets
    symbols, names = collect_data_all_sheets(SEARCH_URL)

    # Print web scraping information
    print(f"Number of companies: {len(symbols)}")
    print(symbols)
    print(names)

    # Create empty data sheets
    sheet_1, sheet_2, sheet_3 = [], [], []

    # Limit number of scraped companies
    if IS_COMPANIES_LIMIT:
        symbols = symbols[:COMPANIES_NUMBER_LIMIT]

    # Collect data for all sheets
    for i, sym in enumerate(symbols):
        print(f"Collecting data for the company {sym} ({i + 1}/{len(symbols)})...")
        print(get_specific_urls(BASE_URL, sym))

        # Getting information
        ticker = yf.Ticker(sym)
        info_dict = dict(ticker.info)

        # Collecting and adding data for sheet 1 and 2
        name = collect_data_first_and_second_sheet(sym, info_dict, sheet_1, sheet_2)

        # Collecting and adding data for sheet 3
        holders = ticker.institutional_holders
        collect_data_third_sheet(sym, name, holders, sheet_3)

    # Creating a list of sheets
    sheet_dict_lists = [sheet_1, sheet_2, sheet_3]

    # Setting parameters
    keys = ["CEO Year Born", "52-Week Change", "Value"] # sort keys for sheets
    reversing = [False, True, True] # sort sheets in reverse order
    row_numbers = [5, 10, 10]  # number of companies in each sheet
    sheet_titles = ["5 stocks with most youngest CEOs", "10 stocks with best 52-Week Change",
                    "10 largest holds of Blackrock Inc."]

    # Process data and print sheets
    for i, sheet in enumerate(sheet_dict_lists):
        # Remove empty rows
        sheet_dict_lists[i] = remove_empty_rows(sheet_dict_lists[i], keys[i])
        # Sort data
        sheet_dict_lists[i] = sort_sheet_dict_list(sheet_dict_lists[i], keys[i], reversing[i])
        # Limit number of rows
        sheet_dict_lists[i] = sheet_dict_lists[i][0:row_numbers[i]]

    # Custom changes to sheets

    # Change None to "--" in missing data
    for sheet in sheet_dict_lists:
        for row in sheet:
            for key in row.keys():
                if row[key] is None:
                    row[key] = "--"

    for row in sheet_dict_lists[0]:
        row["Employees"] = f"{row["Employees"]:,}"

    for row in sheet_dict_lists[1]:
        row["52-Week Change"] = f"{round(row["52-Week Change"]*100,2)}%"
        if isinstance(row.get("Total Cash"), (int, float)): row["Total Cash"] = f"{row['Total Cash']:,}"

    for row in sheet_dict_lists[2]:
        row["Date Reported"] = row["Date Reported"].strftime("%Y-%m-%d")
        if isinstance(row.get("Shares"), (int, float)): row["Shares"] = f"{row['Shares']:,}"
        row["% Out"] = f"{round(row["% Out"]*100, 2)}%"
        row["Value"] = f"{row["Value"]:,}"
        if isinstance(row.get("Value"), (int, float)): row["Value"] = f"{row['Value']:,}"

    # Print sheets
    for i, sheet in enumerate(sheet_dict_lists):
        print_sheet(sheet_titles[i], sheet_dict_lists[i][0].keys(), sheet_dict_lists[i])

if __name__ == "__main__":
    start_time = time()
    get_stock_info()
    end_time = time()
    execution_time = end_time - start_time
    print(f"Function executed in {execution_time:.6f} seconds")