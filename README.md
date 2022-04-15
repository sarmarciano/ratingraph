# Data Mining Project ratingraph

![alt text](https://i.imgur.com/6zM7JBq.png)

Prerequisite of the project:
- have mysql on the computer
- sign up to the omdb API and get a key

## Installation steps:

I. Sign up to omdb API:
1. enter this website: http://www.omdbapi.com/
2. click on API Key
3. create a FREE account: you'll get an email with your key (please check your spams)
4. enter the key you received in the config file in API_KEY

####Note : the free version of the scraper allows to scrap with a limit of 1000 tries a day.

II. Get the scraper files:
1. clone the repository
2. install in the working directory `pip install -r requirements.txt`.
3. enter in config.py and take actions from the #TODO (update username and password)
4. execute in terminal `python ratingraph.py`

The ratingraph website provides ranking and information about tvshows and their directors and writers, and the API
provides information about the main actors, about the imdb rating and a synopsis of the tvshow.

Our scraper takes most of the information from the top 250 tvshows rated in the Ratingraph website.

#### Note
The running time for the totality of the 250 top TVshows is approximately 5 minutes at the moment.

Our scraper also allows scraping only certain data based on the arguments entered in the terminal:

**--tv_shows_range:** enter this command followed by the start range and the end range, and only the tv shows between this range will be scrapped.

**--tv_show_rank:** enter this command followed by a rank between 1 and 250 included and only the tv show of this specific rank will be scrapped.

**--title:** enter this command followed by a tv show title (in format "title"), and all the information about this tv show will be scrapped. _Warning: if the tv show is not in the top 250 tv shows, we can't scrap the information._

**--staff_member:** enter this command followed by a staff member name (in format "title"), and all the information about him and the tvshows he worked on will be scraped. _Warning: if the tv show is not in the top 250 tv shows, we can't scrap the information._


### Database

ERD of the database:
The database is composed of 7 tables:

**1. tvshow table:** the table of all the tv show and its details.

The title is the primary key.
  - title: title of the tvshow
  - nb_seasons: the number of seasons of the tvshow
  - nb_episodes: the number of episodes of the tvshow
  - start_year: the starting year of the tvshow
  - end_year: the ending year of the tvshow if any. If no end year, the end year will be 0 by default
  - imdb_rating: rating of the tvshow on imdb
  - synopsis: a short description of the tvshow

**2. genre table:** the table with the existing genres and their id.

The genre_id is the primary key.
- genre_id: id of the genre of the tvshow, generated automatically when creating a genre.
- genre_name: name of the genre.

**3. tvshow_genre table:** the table that matches the tv show to the genre it belongs to.

Both fields are primary keys.
  - genre_id: id of the genre of the tvshow
  - tvshow_id: id of the tvshow.

**4. staff_member:** this table provides details on a staff member. 

The staff_member_id is the primary key.
   - staff_member_id: id generated automatically when creating the staff member
   - name: the staff member name
   - role: the role of the staff member, can be either writer either director
   - staff_member_rank: the rank of the staff member among its category (either writer or director)
   - nb_tv_shows: the number of tvshows the staff member worked with this role

**5. tvshow_staff:** this is the table that matches a staff member to the tv show he/she worked on.

The 2 fields are the primary keys.
   - staff_member_id: the id of the staff member
   - tvshow_id: the id of the tvshow he worked on.


**6. tvshow_actor:** this is the table that matches an actor to the tv show he/she worked on.

The id field is the primary key.
- actor_id: the id of the actor, generated automatically when creating the actor.
- actor_name: the name of the actor.

**7. actor:** this is the table that lists all the actors and their ids.

The 2 fields are the primary keys.
- actor_id: the id of the actor.
- tvshow_id: the id of the tvshow he worked on.
