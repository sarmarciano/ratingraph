"""
Assignment name - Data Mining project.
Authors - Sarah Marciano, Alon Gabay.
"""
from staff_member import StaffMember
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pprint import pprint
from selenium import webdriver
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
# import grequests
import requests
from time import sleep



TEN = 0
TWENTY_FIVE = 1
FIFTY = 2
HUNDRED = 3
TWO_HUNDRED_FIFTY = 4
SLEEP = 5

URL = 'https://www.ratingraph.com/tv-shows'


def get_headless_driver():
    """ Returns a headless selenium chrome driver. """
    chromedriver_autoinstaller.install()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_staff_member_details(url, staff_role):
    details_dict = {'Rank': 0, 'Trend': 0, 'TV shows': 0, 'Average rating': 0}
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    staff_details = soup.find_all('table', class_=staff_role)[0]
    for row in staff_details.find_all('tr'):
        detail = row.th.text
        if detail in details_dict.keys():
            details_dict[detail] = row.td.text
    details_dict['Trend'] = int(details_dict['Trend'].replace(',', ''))
    details_dict['TV shows'] = int(details_dict['TV shows'])
    return details_dict['Rank'], details_dict['Trend'], details_dict['TV shows'], details_dict['Average rating']


def get_staff_member_list(role, names, urls):
    staff_member_list = []
    for name, url in zip(names, urls):
        rank, trend, number_of_tv_shows, average_rating = get_staff_member_details(url, role)
        staff_member_list.append(StaffMember(role, name, url, rank, trend, number_of_tv_shows, average_rating))
    return staff_member_list


def main():
    driver = get_headless_driver()
    driver.get(URL)

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

    if not table_list:
        return
    table = table_list[0]
    tv_series_page_urls = []
    # This variable stores the data table from the home page.
    home_page_table = []
    for i, row in enumerate(table.findAll('tr')):
        home_page_table.append([])
        for cell in row.findAll('td'):
            children = cell.findChildren("a", recursive=False)
            if children:
                tv_page = children[0]['href']
                tv_series_page_urls.append(tv_page)
            home_page_table[i].append(cell.text)
    # pprint(home_page_table)
    # print(tv_series_page_urls)
    # print(len(home_page_table))

    res = requests.get(tv_series_page_urls[1])
    tv_soup = BeautifulSoup(res.text, 'html.parser')
    director_tag = tv_soup.find(text='Directors:').parent
    writer_tag = tv_soup.find(text='Writers:').parent
    directors_a_elements = director_tag.find_next_siblings('a')
    writer_a_elements = writer_tag.find_next_siblings('a')
    director_names = []
    director_urls = []
    writer_names = []
    writer_urls = []
    for a_tag in directors_a_elements:
        url = '/'.join(URL.split('/')[:-1])
        director_urls.append(url + a_tag['href'])
        director_names.append(a_tag.text)

    for a_tag in writer_a_elements:
        url = '/'.join(URL.split('/')[:-1])
        writer_urls.append(url + a_tag['href'])
        writer_names.append(a_tag.text)
    directors = []
    writers = []
    roles = ['director', 'writer']

    directors = get_staff_member_list('director', director_names, director_urls)
    writers = get_staff_member_list('writer', writer_names, writer_urls)

    pprint(directors)
    pprint(writers)

    driver.close()


if __name__ == '__main__':
    main()
    # html = requests.get("https://www.ratingraph.com/tv-shows/")
    # print(html)
