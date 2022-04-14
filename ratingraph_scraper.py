"""
Assignment name - Data Mining project.
Authors - Sarah Marciano, Alon Gabay.
"""
import grequests

from staff_member import StaffMember
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from tv_shows import TvShow
import chromedriver_autoinstaller
from time import sleep
from datetime import datetime
import argparse
import sys
from config import *
import json
import logging
from database import update_tvshows, update_staff_member

# Global variables
staff_member_instance_dict = dict()


def set_logging():
    """ Set logging basic config to INFO level and to write the output to a file. """
    logging.basicConfig(filename=FILE_NAME, format=FORMAT, level=logging.INFO)


def get_headless_driver():
    """ Returns a headless selenium chrome driver. """
    chromedriver_autoinstaller.install()
    chrome_options = Options()
    chrome_options.add_argument(HEADLESS)
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_staff_member_details(soup, staff_role):
    """
    Given a BeautifulSoup object that represent the staff member web pag (soup), and the role of the staff member
    returns the staff member rank and the number of tv shows he/she worked on as a tuple (rank,tv_show).
    """
    details_dict = {RANK: 0, SHOWS: 0}
    staff_details = soup.find_all('table', class_=staff_role)[0]
    for row in staff_details.find_all('tr'):
        detail = row.th.text
        if detail in details_dict.keys():
            details_dict[detail] = row.td.text
    details_dict[SHOWS] = int(details_dict[SHOWS])
    return details_dict[RANK], details_dict[SHOWS]


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
        if res is None or res.status_code != OK:
            logging.error(f"Did not get a successful response "
                          f"for {name}/{role}.")
            continue
        html_text = res.text
        soup = BeautifulSoup(html_text, PARSER)
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
    staff_member_tuple = STAFF_MEMBER_DICT[role]
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
        staff_member_names.append(a_tag.text.title())
    staff_members = get_tv_show_staff_members(staff_member_tuple[1], staff_member_names, staff_member_urls)
    return staff_members


def select_250_entries(driver):
    """ Given a selenium driver, selects the 250 entries option. """
    options_div = driver.find_elements(By.TAG_NAME, 'select')[-1]
    options_list = options_div.find_elements(By.TAG_NAME, 'option')
    options_list[TWO_HUNDRED_FIFTY_INDEX].click()
    sleep(SLEEP)


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
    soup = BeautifulSoup(html_text, PARSER)
    table_list = soup.find_all("div", class_="dataTables_scrollBody")
    table = table_list[-1]
    tv_series_page_urls = []
    tv_shows_details = []
    for i, row in enumerate(table.findAll('tr')[1:]):
        tv_show_args = []
        for index, cell in enumerate(row.findAll('td')):
            children = cell.findChildren("a", recursive=False)
            if children:
                tv_page_url = children[0]['href']
                tv_series_page_urls.append(tv_page_url)
            tv_show_args.append(cell.text.title())
        tv_show_args = [tv_show_args[j] for j in range(len(tv_show_args)) if j in IMPORTANT_INDICES]
        tv_show_args[GENRE_INDEX] = tv_show_args[GENRE_INDEX].split(', ')

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
            if res is None or res.status_code != OK:
                logging.error(f"Did not get a successful response "
                              f"for {tv_show_details[RANK_INDEX]} - {tv_show_details[TITLE_INDEX]}.")
                continue
            tv_soup = BeautifulSoup(res.text, PARSER)
            writers = get_staff_members(tv_soup, WRITER)
            directors = get_staff_members(tv_soup, DIRECTOR)
            logging.info(f'{tv_show_details[RANK_INDEX]}-"{tv_show_details[TITLE_INDEX]}"'
                         f'was successfully scraped from ratingraph.')
            actors, synopsis, imdb_rating = get_api_data(tv_show_details[TITLE_INDEX])
            if (actors, synopsis, imdb_rating) == NO_API_RESULTS:
                logging.error(f"{tv_show_details[RANK_INDEX]}-'{tv_show_details[TITLE_INDEX]}' wasn't scrape from API.")
            else:
                logging.info(f'{tv_show_details[RANK_INDEX]}-"{tv_show_details[TITLE_INDEX]}" scraped from API.')
            tv_show = TvShow(*tv_show_details, writers, directors, actors, synopsis, imdb_rating)
            print(tv_show)
            print()
            tv_shows_list.append(tv_show)
    return tv_shows_list


def get_staff_member_url_list(name):
    """
    Given a name search in the search bar and returns the url list of the staff member that it represent.
    Returns an empty list in case of more than 2 results or in case of 0 results.
    """
    driver = get_headless_driver()
    driver.get(URL)
    search_div = driver.find_elements(By.CLASS_NAME, "search")[0]
    search_input = search_div.find_element(By.TAG_NAME, "input")
    search_input.clear()
    search_input.send_keys(name)
    sleep(SLEEP)
    div_with_a_tags = search_div.find_element(By.TAG_NAME, "div")
    a_tags = div_with_a_tags.find_elements(By.TAG_NAME, "a")
    a_tags = a_tags[:-1]
    if not a_tags:
        print(f'staff member {name} does not exist in ratingraph website.')
        return []
    elif len(a_tags) > UNIQUE_THRESHOLD:
        print(f'staff member {name} is not a unique staff member, please be more specific in your search.')
        return []
    urls = [a_elem.get_attribute('href') for a_elem in a_tags]
    driver.close()
    return urls


def get_staff_member_info(name):
    """ Given a staff member name prints information about him/her and the tv-shows he/she has been part of.
    For now the staff member can be writer/director or both and the resulting output will refer to him/her in all
    his/hers roles. """
    start = datetime.now()
    driver = get_headless_driver()
    urls = get_staff_member_url_list(name)
    s_members = []
    worked_on_top_250 = False
    for url in urls:
        role = DIRECTOR if url.find("directors") != -1 else WRITER
        s_member = get_tv_show_staff_members(role, [name], [url])[0]
        s_members.append(s_member)
        print(s_member)
        tv_shows_details, tv_series_page_urls = get_tv_shows_details_and_urls(driver, url)
        tv_shows_ranks_titles = [[int(details[RANK_INDEX].replace(',', '')), details[TITLE_INDEX]] for details
                                 in tv_shows_details]
        relevant_tv_shows_ranks_titles = [[ranks_titles[RANK_INDEX], ranks_titles[TITLE_INDEX]] for ranks_titles in
                                          tv_shows_ranks_titles if ranks_titles[RANK_INDEX] <= UPPER_BOUND]
        relevant_tv_shows_ranks_titles = sorted(relevant_tv_shows_ranks_titles, key=lambda x: x[RANK_INDEX])
        if relevant_tv_shows_ranks_titles:
            worked_on_top_250 = True
            print('\n' + role)
            for rank, title in relevant_tv_shows_ranks_titles:
                print(f'rank: {rank}, title: {title}')
    driver.close()
    print(f"Data mining project checkpoint #2 took {datetime.now() - start}")
    if not worked_on_top_250:
        print(f'{name} is not a staff member in any of the top 250 tv shows.')
        return []
    return s_members


def scrape_ratingraph_parts(ranks=None, title=None):
    """ Given a range of ranks ([starting_rank - 1, ending_rank]) or tv show title return a list of tv-shows objects."""
    start = datetime.now()
    driver = get_headless_driver()
    try:
        home_page_tv_shows_details, tv_shows_page_urls = get_tv_shows_details_and_urls(driver, URL)
    except Exception as e:
        logging.critical(f"Could not access {URL}.\n{e}")
        return []
    tv_shows_list = []
    if not ranks and not title:
        return tv_shows_list
    if ranks:
        home_page_tv_shows_details = home_page_tv_shows_details[ranks[0]:ranks[1]]
        tv_shows_page_urls = tv_shows_page_urls[ranks[0]:ranks[1]]
    elif title:
        titles = [details[TITLE_INDEX].title() for details in home_page_tv_shows_details
                  if int(details[RANK_INDEX].replace(",", "")) <= UPPER_BOUND]
        if title.title() not in titles:
            return []
        rank_index = titles.index(title.title())
        home_page_tv_shows_details = [home_page_tv_shows_details[rank_index]]
        tv_shows_page_urls = [tv_shows_page_urls[rank_index]]
    ranks_list = tv_shows_page_urls
    batch_size = min(len(ranks_list), UPPER_BOUND // 2)
    remainder = len(ranks_list) % batch_size if len(ranks_list) % batch_size else batch_size
    whole = len(ranks_list) - remainder
    whole_list = get_tv_show_list(tv_shows_page_urls, 0, whole, home_page_tv_shows_details, batch_size)
    remainder_list = get_tv_show_list(tv_shows_page_urls, whole, len(ranks_list), home_page_tv_shows_details, remainder)
    tv_shows_list = whole_list + remainder_list
    driver.close()
    print(f"Data mining project checkpoint #1 took {datetime.now() - start}")
    logging.info(f"Data mining project checkpoint #1 took {datetime.now() - start}")
    return tv_shows_list


def get_api_data(title):
    """ This function gets some additional data on a specific tvshow using API query on the omdb API."""
    title = title.replace(' ', '+')
    query = API_BASE_URL + title + API_KEY
    res_list = get_grequests_responses([query])
    res = res_list[0]
    if not res or res.status_code != OK:
        print(f'Could not request omdbapi website - status code - {res.status_code}')
        return NO_API_RESULTS
    details = json.loads(res_list[0].text)
    if not details.get(ACTORS):
        return NO_API_RESULTS
    actor_list = details[ACTORS].split(', ')
    return actor_list, details[SYNOPSIS], details[IMDB_RATING]


def cli_main():
    """ Cli option for checkpoint 2 can scrap data by terms as explain in -h help command. """
    start = datetime.now()
    parser = argparse.ArgumentParser(description='ratingraph-scraper.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--tv_shows_range', type=int, metavar=('start', 'end'), nargs=2,
                       help=f'tv shows rank range 1-{UPPER_BOUND}')
    group.add_argument('--tv_show_rank', type=int, metavar='rank', help=f'tv show rank 1-{UPPER_BOUND}')
    group.add_argument('--title', type=str, metavar='tvshow_title', help='tv show title needs to be in format "title"')
    group.add_argument('--staff_member', type=str, metavar='name',
                       help='staff member information can be writer/director or both')
    args = parser.parse_args()
    if args.tv_shows_range:
        ranks = args.tv_shows_range
        if (ranks[1] > ranks[0]) and (1 <= ranks[0] < UPPER_BOUND) and (1 < ranks[1] <= UPPER_BOUND):
            return scrape_ratingraph_parts(ranks=[ranks[0] - 1, ranks[1]])
        else:
            print("The ranks must be in this format: [a, b] where b > a and they are both in the segment [1,250]")
            return []
    elif args.tv_show_rank:
        if not (1 <= args.tv_show_rank <= UPPER_BOUND):
            print("The tv-show rank must be in the segment [1,250]")
        return scrape_ratingraph_parts(ranks=[args.tv_show_rank - 1, args.tv_show_rank])
    elif args.title:
        result = scrape_ratingraph_parts(title=args.title.title())
        if not result:
            print(f'The tv show {args.title} is not in the top {UPPER_BOUND} tv shows of ratingraph.')
        return result
    elif args.staff_member:
        return get_staff_member_info(args.staff_member.title())
    print(f"Data mining project checkpoint #2 took {datetime.now() - start}")
    logging.info(f"Data mining project checkpoint #2 took {datetime.now() - start}")


def main():
    """
    Scraping up to the predetermined upper bound (default: 250) tv shows from https://www.ratingraph.com/tv-shows/ .
    """
    return scrape_ratingraph_parts(ranks=[0, UPPER_BOUND])


if __name__ == '__main__':
    # All update functions are part of the third checkpoint.
    set_logging()
    if len(sys.argv) == 1:
        # First checkpoint
        tv_shows = main()
        update_tvshows(tv_shows=tv_shows)
    else:
        # Second checkpoint
        info = cli_main()
        if info:
            if isinstance(info[0], TvShow):
                tv_shows = info
                update_tvshows(tv_shows)
                pass
            elif isinstance(info[0], StaffMember):
                for st_member in info:
                    update_staff_member(st_member)
