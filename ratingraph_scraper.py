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
from tv_shows import TvShow
import chromedriver_autoinstaller
import requests
from time import sleep
from datetime import datetime
# import grequests


TWO_HUNDRED_FIFTY = 250
TWO_HUNDRED_FIFTY_INDEX = 4
SLEEP = 2
URL = 'https://www.ratingraph.com/tv-shows'


def get_headless_driver():
    """ Returns a headless selenium chrome driver. """
    chromedriver_autoinstaller.install()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_staff_member_details(staff_member_url, staff_role):
    details_dict = {'Rank': 0, 'TV shows': 0}
    html_text = requests.get(staff_member_url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    staff_details = soup.find_all('table', class_=staff_role)[0]
    for row in staff_details.find_all('tr'):
        detail = row.th.text
        if detail in details_dict.keys():
            details_dict[detail] = row.td.text
    details_dict['TV shows'] = int(details_dict['TV shows'])
    return details_dict['Rank'], details_dict['TV shows']


def get_staff_member_list(driver, role, names, urls):
    staff_member_list = []
    for name, url in zip(names, urls):
        rank, number_of_tv_shows = get_staff_member_details(url, role)
        titles = get_tv_shows_titles(driver, url)
        staff_member_list.append(StaffMember(role, name, url, rank, number_of_tv_shows, titles))
    return staff_member_list


def get_staff_members(driver, tv_soup, role):
    staff_member_dict = {'writer': ('Writers:', 'writer'), 'director': ('Directors:', 'director')}
    staff_member_tuple = staff_member_dict[role]
    staff_member_child = tv_soup.find(text=staff_member_tuple[0])
    if not staff_member_child:
        return None
    staff_member_tag = staff_member_child.parent
    staff_member_a_elements = staff_member_tag.find_next_siblings('a')
    staff_member_urls = []
    staff_member_names = []
    for a_tag in staff_member_a_elements:
        url = '/'.join(URL.split('/')[:-1])
        staff_member_urls.append(url + a_tag['href'])
        staff_member_names.append(a_tag.text)

    staff_members = get_staff_member_list(driver, staff_member_tuple[1], staff_member_names, staff_member_urls)
    return staff_members


def select_250_entries(driver):
    # toplist_length -> was id
    options_div = driver.find_elements(By.TAG_NAME, 'select')[-1]
    options_list = options_div.find_elements(By.TAG_NAME, 'option')
    options_list[TWO_HUNDRED_FIFTY_INDEX].click()
    sleep(SLEEP)


def get_tv_shows_titles(driver, url):
    tv_shows_details, urls = get_tv_shows_details_and_urls(driver, url)
    # index 1 is the title index.
    return [details[1] for details in tv_shows_details if int(details[0].replace(",", "")) <= TWO_HUNDRED_FIFTY]


def get_tv_shows_details_and_urls(driver, url):
    driver.get(url)
    select_250_entries(driver)
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, 'html.parser')
    table_list = soup.find_all("div", class_="dataTables_scrollBody")
    table = table_list[0]
    tv_series_page_urls = []
    tv_shows_details = []
    important_indices = {0, 2, 3, 4, 5, 6, 7}
    for i, row in enumerate(table.findAll('tr')[1:]):
        tv_show_args = []
        for index, cell in enumerate(row.findAll('td')):
            children = cell.findChildren("a", recursive=False)
            if children:
                tv_page_url = children[0]['href']
                tv_series_page_urls.append(tv_page_url)
            tv_show_args.append(cell.text)
        tv_show_args = [tv_show_args[j] for j in range(len(tv_show_args)) if j in important_indices]
        tv_show_args[4] = tv_show_args[4].split(', ')

        tv_shows_details.append(tv_show_args)
    return tv_shows_details, tv_series_page_urls


def main():
    start = datetime.now()
    driver = get_headless_driver()
    home_page_tv_shows_details, tv_shows_page_urls = get_tv_shows_details_and_urls(driver, URL)
    tv_shows_list = []
    for tv_show_details, tv_show_url in zip(home_page_tv_shows_details, tv_shows_page_urls):
        res = requests.get(tv_show_url)
        tv_soup = BeautifulSoup(res.text, 'html.parser')
        writers = get_staff_members(driver, tv_soup, "writer")
        directors = get_staff_members(driver, tv_soup, "director")
        tv_show = TvShow(*tv_show_details, writers, directors)
        print(tv_show)
        tv_shows_list.append(tv_show)

    driver.close()
    end = datetime.now()
    print(f"Data mining project checkpoint #1 took {end - start}")


if __name__ == '__main__':
    main()
    # html = requests.get("https://www.ratingraph.com/tv-shows/")
    # print(html)
