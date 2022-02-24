"""
Assignment name - Data Mining project.
Authors - Sarah Marciano, Alon Gabay.
"""
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pprint import pprint
from selenium import webdriver
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
import grequests
from time import sleep


TEN = 0
TWENTY_FIVE = 1
FIFTY = 2
HUNDRED = 3
TWO_HUNDRED_FIFTY = 4
SLEEP = 5

URL = 'https://www.ratingraph.com/tv-shows/'


def get_headless_driver():
    """ Returns a headless selenium chrome driver. """
    chromedriver_autoinstaller.install()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def main():
    driver = get_headless_driver()
    driver.get(URL)
    # print(html_text)
    num_of_entries = TEN
    options_div = driver.find_element(By.ID, 'toplist_length')
    options_list = options_div.find_elements(By.TAG_NAME, 'option')
    options_dict = {TEN: options_list[TEN], TWENTY_FIVE: options_list[TWENTY_FIVE], FIFTY: options_list[FIFTY],
                    HUNDRED: options_list[HUNDRED], TWO_HUNDRED_FIFTY: options_list[TWO_HUNDRED_FIFTY]}

    options_dict[num_of_entries].click()
    sleep(SLEEP)

    html_text = driver.page_source
    soup = BeautifulSoup(html_text, 'html.parser')
    table_list = soup.find_all("div", class_="dataTables_scrollBody")
    # print(soup)
    if not table_list:
        return
    table = table_list[0]
    tv_page_urls = []
    home_page_table = []
    for i, row in enumerate(table.findAll('tr')):
        home_page_table.append([])
        for cell in row.findAll('td'):
            children = cell.findChildren("a", recursive=False)
            if children:
                tv_page = children[0]['href']
                tv_page_urls.append(tv_page)
            home_page_table[i].append(cell.text)
    pprint(home_page_table)
    print(tv_page_urls)
    print(len(home_page_table))


if __name__ == '__main__':
    main()
