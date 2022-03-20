# Data Mining Project ratingraph

![alt text](https://i.imgur.com/6zM7JBq.png)

Prerequisite of the project:
- have mysql on the computer

## Installation steps:
1. clone the repository
2. install in the working directory `pip install -r requirements.txt`.
3. enter in config.py and take actions from the #TODO (update username and password)
4. execute in terminal `python ratingraph.py`

The ratingraph website provides ranking and information about tv shows and their directors and writers.

Our scraper takes most of the information from the top 250 tv shows and details about their directors and writers.

#### Note
The running time for the totality of the 250 top TV shows is approximately 5 minutes at the moment.

Our scraper also allows to scrape only certain data based on the arguments entered in the terminal:

**--tv_shows_range:** enter this command followed by the start range and the end range, and only the tv shows between this range will be scrapped.

**--tv_show_rank:** enter this command followed by a rank between 1 and 250 included and only the tv show of this specific rank will be scrapped.

**--title:** enter this command followed by a tv show title (in format "title"), and all the information about this tv show will be scrapped. _Warning: if the tv show is not in the top 250 tv shows, we can't scrap the information._

### Database

ERD of the database:
The database is composed of 4 tables:

**1. tvshow table:** the table of all the tv show and its details.

The title is the primary key.
  - title: title of the tvshow
  - rank: rank of the tvshow
  - nb_seasons: the number of seasons of the tvshow
  - nb_episodes: the number of episodes of the tvshow
  - start_year: the starting year of the tvshow
  - end_year: the ending year of the tvshow if any. If no end year, the end year will be 0 by default.

**2. tvshow_genre table:** the table that matches the tv show to the genre it belong to.

Both fields are primary keys.
  - genre: genre of the tvshow
  - tvshow_title: title of the tvshow.

**3. staff_member:** this table provide details on a staff member. 

Primary keys are the name and the role.
   - name: the staff member name
   - role: the role of the staff member, can be either writer either director
   - staff_member_rank: the rank of the staff member among its category (either writer or director)
   - nb_tv_shows: the number of tvshows the staff member worked with this role

**4. tvshow_staff:** this is the table that matches a staff member to the tv show he/she worked on.

The 3 fields are the primary keys.
   - name: the staff member name
   - role: the role of the staff member, can be either writer either director.
   - tvshow_title: the title of the show he worked on.

