import pymysql
import pymysql.cursors

import ratingraph_scraper

SQL_INIT_FILEPATH = 'ratingraph_init.sql'


def insert_into_tvshow_table(cursor, show):
    """ Insert into data of a specific tv-show 'show', into tvshow table. """
    tvshow_template = """
    INSERT INTO tvshow (title, tv_show_rank, nb_seasons, nb_episodes, start_year, end_year) 
    VALUES ("{0}", {1} ,{2} ,{3}, {4}, {5})
    ON DUPLICATE KEY UPDATE tv_show_rank={1}, nb_seasons={2}, nb_episodes={3}, start_year={4}, end_year={5};
    """
    query = tvshow_template.format(show.title, show.rank, show.nb_seasons, show.nb_episodes, show.start_year,
                                   show.end_year)
    cursor.execute(query)


def insert_into_tvshow_genre_table(cursor, show):
    """ Insert genres of a specific tv-show into tvshow_genre table. """
    tvshow_genre_template = """
    INSERT INTO tvshow_genre (tvshow_title, genre) 
    VALUES ("{0}", "{1}")
    ON DUPLICATE KEY UPDATE tvshow_title="{0}", genre="{1}";
    """
    for genre in show.genres:
        query = tvshow_genre_template.format(show.title, genre)
        cursor.execute(query)


def insert_into_staff_member_table(cursor, s_member):
    """ Insert data of a specific staff member s_member into staff_member table. """
    tvshow_genre_template = """
    INSERT INTO staff_member (name, role, staff_member_rank, nb_tv_shows) 
    VALUES ("{0}", "{1}", {2}, {3})
    ON DUPLICATE KEY UPDATE staff_member_rank={2}, nb_tv_shows={3};
    """
    query = tvshow_genre_template.format(s_member.name, s_member.role, s_member.rank, s_member.nb_tv_shows)
    cursor.execute(query)


def insert_into_tvshow_staff_table(cursor, s_member, show):
    """ Insert data into tvshow_staff table. """
    tvshow_genre_template = """
    INSERT INTO tvshow_staff (name, role, tvshow_title) 
    VALUES ("{0}", "{1}", "{2}")
    ON DUPLICATE KEY UPDATE name="{0}", role="{1}", tvshow_title="{2}";
    """
    # role, name, rank, nb_tv_shows
    query = tvshow_genre_template.format(s_member.name, s_member.role, show.title)
    cursor.execute(query)


def insert_staff_members_of_a_tvshow(cursor, show):
    """ Insert data of staff members that are part of a specific tv show into tables staff_member and tvshow_staff.  """
    for director in show.directors:
        insert_into_staff_member_table(cursor, director)
        insert_into_tvshow_staff_table(cursor, director, show)
    for writer in show.writers:
        insert_into_staff_member_table(cursor, writer)
        insert_into_tvshow_staff_table(cursor, writer, show)


def create_ratingraph_db():
    """ Creating mysql database named 'ratingraph' if it is not already existing. """
    initialize_script = ''
    with open(SQL_INIT_FILEPATH, 'r') as f:
        initialize_script = f.read()
        query_list = initialize_script.split('\n')
        query_list = [query for query in query_list if query]
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 database='',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            for query in query_list:
                cursor.execute(query)
        connection.commit()


def main():
    """
    Creating a mysql database named 'ratingraph' and fill it with data from
    the website https://www.ratingraph.com/tv-shows/ .
    """
    create_ratingraph_db()
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 database='ratingraph',
                                 cursorclass=pymysql.cursors.DictCursor)
    # tv_shows = ratingraph_scraper.scrape_ratingraph_parts(ranks=[0, 1])
    tv_shows = ratingraph_scraper.main()
    print(len(tv_shows))
    with connection:
        with connection.cursor() as cursor:
            for show in tv_shows:
                insert_into_tvshow_table(cursor, show)
                insert_into_tvshow_genre_table(cursor, show)
                insert_staff_members_of_a_tvshow(cursor, show)
        connection.commit()


if __name__ == '__main__':
    main()
