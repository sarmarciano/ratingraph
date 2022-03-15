# Data Mining Project ratingraph

![alt text](https://i.imgur.com/6zM7JBq.png)

## Installation steps:
1. clone the repository
2. install in the working directory `pip install -r requirements.txt`.
3. execute in terminal `python ratingraph.py`

The ratingraph website provides ranking and information about tv shows and their directors and writers.

Our scraper takes most of the information from the top 250 tv shows and details about their directors and writers.

#### Note
The running time for the totality of the 250 top TV shows is approximately 5 minutes at the moment.

### Parsing with arguments
Our scraper also allows to scrape only certain data based on the arguments entered in the terminal:

**--tv_shows_range:** enter this command followed by the start range and the end range, and only the tv shows between this range will be scrapped.

**--tv_show_rank:** enter this command followed by a rank between 1 and 250 included and only the tv show of this specific rank will be scrapped.

**--title:** enter this command followed by a tv show title (in format "title"), and all the information about this tv show will be scrapped. _Warning: if the tv show is not in the top 250 tv shows, we can't scrap the information._