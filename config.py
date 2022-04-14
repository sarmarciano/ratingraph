# ratingraph_scraper constants
UPPER_BOUND = 250
TWO_HUNDRED_FIFTY_INDEX = 4
SLEEP = 2
URL = 'https://www.ratingraph.com/tv-shows'
RANK = 'Rank'
SHOWS = 'TV shows'
HEADLESS = '--headless'
PARSER = 'html.parser'
WRITER = 'writer'
DIRECTOR = 'director'
STAFF_MEMBER_DICT = {WRITER: ('Writers:', WRITER), DIRECTOR: ('Directors:', DIRECTOR)}
IMPORTANT_INDICES = {0, 2, 3, 4, 5, 6, 7}
GENRE_INDEX = 4
UNIQUE_THRESHOLD = 2
OK = 200
API_BASE_URL = 'http://www.omdbapi.com/?t='
RANK_INDEX = 0
TITLE_INDEX = 1

FORMAT = '%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s'
FILE_NAME = 'ratingraph_logging.log'

# TODO sign up for omdbapi and put your one key.
# API_KEY = "&apikey=YOUR_KEY"
# my_key = f8ff4bf5
# sarah's_key = 9dbc638c
API_KEY = '&apikey=9dbc638c'

# database constants
SQL_INIT_FILEPATH = 'ratingraph_init.sql'
HOST = 'localhost'
DB_NAME = 'ratingraph'
USERNAME = 'root'  # TODO please update with your personal username
PASSWORD = 'root'  # TODO please update with your personal password
