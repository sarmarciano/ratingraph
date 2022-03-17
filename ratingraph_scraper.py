"""
Assignment name - Data Mining project.
Authors - Sarah Marciano, Alon Gabay.
"""
import grequests
import requests
from staff_member import StaffMember
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pprint import pprint
from selenium import webdriver
from bs4 import BeautifulSoup
from tv_shows import TvShow
import chromedriver_autoinstaller
from time import sleep
from datetime import datetime
import argparse
from tqdm import tqdm

TWO_HUNDRED_FIFTY = 250
TWO_HUNDRED_FIFTY_INDEX = 4
SLEEP = 2
URL = 'https://www.ratingraph.com/tv-shows'

staff_member_instance_dict = {}


def get_headless_driver():
    """ Returns a headless selenium chrome driver. """
    chromedriver_autoinstaller.install()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_staff_member_details(soup, staff_role):
    """
    Given a BeautifulSoup object that represent the staff member web pag (soup), and the role of the staff member
    returns the staff member rank and the number of tv shows he/she worked on as a tuple (rank,tv_show).
    """
    details_dict = {'Rank': 0, 'TV shows': 0}
    staff_details = soup.find_all('table', class_=staff_role)[0]
    for row in staff_details.find_all('tr'):
        detail = row.th.text
        if detail in details_dict.keys():
            details_dict[detail] = row.td.text
    details_dict['TV shows'] = int(details_dict['TV shows'])
    return details_dict['Rank'], details_dict['TV shows']


def get_tv_show_staff_members(role, names, urls):
    """
    Given a role of a staff member, list of their names and their url pages
    returns a list of StaffMember objects.
    """
    staff_member_list = []
    relevant_names = []
    relevant_urls = []
    for name, url in zip(names, urls):
        key = (name, role)
        if key in staff_member_instance_dict:
            staff_member_list.append(staff_member_instance_dict[key])
        else:
            relevant_names.append(name)
            relevant_urls.append(url)

    responses = get_grequests_responses(relevant_urls)
    for name, url, res in zip(relevant_names, relevant_urls, responses):
        key = (name, role)
        html_text = res.text
        soup = BeautifulSoup(html_text, 'html.parser')
        rank, number_of_tv_shows = get_staff_member_details(soup, role)
        staff_member = StaffMember(role, name, rank, number_of_tv_shows)
        staff_member_instance_dict[key] = staff_member
        staff_member_list.append(staff_member_instance_dict[key])
    return staff_member_list


def get_staff_members(tv_soup, role):
    """
    Given a BeautifulSoup object of a specific tv-show and a roll, returns list of the staff members
    with a specific role that participate this specific show as a list of StaffMember objects.
    """
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

    staff_members = get_tv_show_staff_members(staff_member_tuple[1], staff_member_names, staff_member_urls)
    return staff_members


def select_250_entries(driver):
    """ Given a selenium driver, selects the 250 entries option. """
    options_div = driver.find_elements(By.TAG_NAME, 'select')[-1]
    options_list = options_div.find_elements(By.TAG_NAME, 'option')
    options_list[TWO_HUNDRED_FIFTY_INDEX].click()
    sleep(SLEEP)


def get_rank_index_by_title(tv_shows_details, title):
    """ Returns the rank index of a specific tv-show title. """
    titles = [details[1].lower() for details in tv_shows_details if int(details[0].replace(",", "")) <= TWO_HUNDRED_FIFTY]
    if title not in titles:
        return -1
    return titles.index(title)


def get_grequests_responses(urls):
    """ Given list of urls return their http responses list. """
    my_requests = (grequests.get(u) for u in urls)
    responses = grequests.map(my_requests)
    return responses


def get_tv_shows_details_and_urls(driver, url):
    """ Given a selenium driver and an url, returns a tuple of tv-shows details list and their page urls. """
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


def get_tv_show_list(tv_shows_urls, start, end, home_page_tv_shows_details, batch_size):
    """
    Given urls of tv-shows, range to scrape (start, end), tv-shows details and batch size, returns list of tv-shows
    objects.
    """
    tv_shows_list = []
    for index in range(start, end, batch_size):
        responses = get_grequests_responses(tv_shows_urls[index:index + batch_size])
        for i in range(batch_size):
            tv_show_details, tv_show_url = home_page_tv_shows_details[index + i], tv_shows_urls[index + i]
            res = responses[i]
            tv_soup = BeautifulSoup(res.text, 'html.parser')
            writers = get_staff_members(tv_soup, "writer")
            directors = get_staff_members(tv_soup, "director")
            tv_show = TvShow(*tv_show_details, writers, directors)
            print(tv_show)
            tv_shows_list.append(tv_show)
    return tv_shows_list


def scrape_ratingraph_parts(ranks=None, title=None):
    """
    Given ranks range as a list (ranks=[starting_rank - 1, ending_rank]) or tv show title return a list of tv-shows
    objects.
    """
    start = datetime.now()
    driver = get_headless_driver()
    home_page_tv_shows_details, tv_shows_page_urls = get_tv_shows_details_and_urls(driver, URL)
    tv_shows_list = []
    if not ranks and not title:
        return tv_shows_list
    if ranks:
        first_rank = ranks[0]
        last_rank = ranks[1]
        home_page_tv_shows_details = home_page_tv_shows_details[first_rank:last_rank]
        tv_shows_page_urls = tv_shows_page_urls[first_rank:last_rank]
    elif title:
        titles = [details[1].lower() for details in home_page_tv_shows_details if int(details[0].replace(",", "")) <= TWO_HUNDRED_FIFTY]
        if title.lower() not in titles:
            return []
        rank_index = titles.index(title.lower())
        home_page_tv_shows_details = [home_page_tv_shows_details[rank_index]]
        tv_shows_page_urls = [tv_shows_page_urls[rank_index]]
    ranks_list = tv_shows_page_urls
    batch_size = min(len(ranks_list), 125)
    remainder = len(ranks_list) % batch_size
    remainder = remainder if remainder else batch_size
    whole = len(ranks_list) - remainder
    whole_list = get_tv_show_list(tv_shows_page_urls, 0, whole, home_page_tv_shows_details, batch_size)
    remainder_list = get_tv_show_list(tv_shows_page_urls, whole, len(ranks_list), home_page_tv_shows_details, remainder)

    tv_shows_list = whole_list + remainder_list

    driver.close()
    end = datetime.now()
    print(f"Data mining project checkpoint #1 took {end - start}")
    return tv_shows_list


def cli_main():
    parser = argparse.ArgumentParser(description='ratingraph-scraper.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--tv_shows_range', type=int, metavar=('start', 'end'), nargs=2, help='tv shows rank range 1-250')
    group.add_argument('--tv_show_rank', type=int, metavar='rank', help='tv show rank 1-250]')
    group.add_argument('--title', type=str, metavar='movie_title', help='tv show title needs to be in format "title"')
    # group.add_argument('--staff_member', type=int, metavar='staff member', help='staff member information')

    args = parser.parse_args()
    if args.tv_shows_range:
        ranks = args.tv_shows_range
        ranks[0] = ranks[0] - 1
        ranks[1] = ranks[1]
        scrape_ratingraph_parts(ranks=ranks)
    elif args.tv_show_rank:
        scrape_ratingraph_parts(ranks=[args.tv_show_rank - 1, args.tv_show_rank])
    elif args.title:
        if not scrape_ratingraph_parts(title=args.title):
            print(f'The tv show {args.title} is not in the top 250 tv shows of ratingraph.')
    # if args.w:
    #     print("good morning :)")


def main():
    return scrape_ratingraph_parts(ranks=[0, 250])


if __name__ == '__main__':
    cli_main()
    # main()
