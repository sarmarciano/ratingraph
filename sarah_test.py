# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from pprint import pprint
# from selenium import webdriver
# from bs4 import BeautifulSoup
# import chromedriver_autoinstaller
# import grequests
# from time import sleep
import requests
# import grequests



URL = 'https://www.ratingraph.com/tv-shows/'

page = requests.get(URL)
print(page)
