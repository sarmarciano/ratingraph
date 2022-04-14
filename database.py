import logging
import pymysql
import pymysql.cursors
from config import *
from datetime import datetime


def insert_into_actor_table(cursor, show):
    """ Insert genres into genre table. """
    sql_check = """ 
    SELECT COUNT(*) as count FROM actor WHERE actor_name = "{0}";
    """
    tvshow_actor_template = """
    INSERT INTO actor (actor_name) VALUES ("{0}");
    """
    for actor_name in show.actors:
        check_query = sql_check.format(actor_name)
        cursor.execute(check_query)
        result = cursor.fetchone()
        if result['count'] == 0:
            query = tvshow_actor_template.format(actor_name)
            cursor.execute(query)


def insert_into_tvshow_actor_table(cursor, show):
    """ Insert genres of a specific tv-show into tvshow_genre table. """
    sql_check = """ 
    SELECT actor_id, tvshow_id
    FROM actor, tvshow 
    WHERE actor_name = "{0}" and title = "{1}" and start_year = {2};
    """
    tvshow_actor_template = """
    INSERT INTO tvshow_actor (actor_id, tvshow_id) 
    VALUES ({0}, {1})
    ON DUPLICATE KEY UPDATE actor_id={0}, tvshow_id={1};
    """
    for actor in show.actors:
        check_query = sql_check.format(actor, show.title, show.start_year)
        cursor.execute(check_query)
        result = cursor.fetchone()
        actor_id, tvshow_id = result['actor_id'], result['tvshow_id']
        query = tvshow_actor_template.format(actor_id, tvshow_id)
        cursor.execute(query)


def insert_into_tvshow_rank_table(cursor, show):
    """ Insert data of a specific tv-show 'show', into tvshow table. """
    sql_get_id = """ 
    SELECT tvshow_id 
    FROM tvshow
    WHERE title = "{0}" and start_year = {1};
    """
    tvshow_template = """
    INSERT INTO tvshow_rank (tvshow_id, tvshow_rank, rank_date) 
    VALUES ({0}, {1} ,"{2}")
    ON DUPLICATE KEY UPDATE rank_date="{2}";
    """
    get_query = sql_get_id.format(show.title, show.start_year)
    cursor.execute(get_query)
    result = cursor.fetchone()
    today_str = datetime.today().strftime('%Y-%m-%d')
    query = tvshow_template.format(result['tvshow_id'], show.rank, today_str)
    cursor.execute(query)


def insert_into_tvshow_table(cursor, show):
    """ Insert data of a specific tv-show 'show', into tvshow table. """
    sql_check = """ 
    SELECT COUNT(*) as count 
    FROM tvshow 
    WHERE title = "{0}" and start_year = {1};
    """
    tvshow_template = """
    INSERT INTO tvshow (title, nb_seasons, nb_episodes, start_year, end_year, imdb_rating, synopsis) 
    VALUES ("{0}", {1} ,{2}, {3}, {4}, {5}, "{6}");
    """
    tvshow_update = """
    UPDATE tvshow
    SET nb_seasons={2}, nb_episodes={3}, end_year={4}, imdb_rating={5}, synopsis="{6}"
    WHERE title = "{0}" and start_year = {1};
    """
    check_query = sql_check.format(show.title, show.start_year)
    cursor.execute(check_query)
    result = cursor.fetchone()
    query = ''
    if result['count'] == 0:
        query = tvshow_template.format(show.title, show.nb_seasons, show.nb_episodes, show.start_year, show.end_year,
                                       show.imdb_rating, show.synopsis)
    else:
        query = tvshow_update.format(show.title, show.start_year, show.nb_seasons, show.nb_episodes, show.end_year,
                                     show.imdb_rating, show.synopsis)
    cursor.execute(query)


def insert_into_genre_table(cursor, show):
    """ Insert genres into genre table. """
    sql_check = """ 
    SELECT COUNT(*) as count FROM genre WHERE genre_name="{0}";
    """
    tvshow_genre_template = """
    INSERT INTO genre (genre_name) VALUES ("{0}");
    """
    for genre_name in show.genres:
        check_query = sql_check.format(genre_name)
        cursor.execute(check_query)
        result = cursor.fetchone()
        if result['count'] == 0:
            query = tvshow_genre_template.format(genre_name)
            cursor.execute(query)


def insert_into_tvshow_genre_table(cursor, show):
    """ Insert genres of a specific tv-show into tvshow_genre table. """
    sql_check = """ 
    SELECT genre_id, tvshow_id
    FROM genre, tvshow 
    WHERE genre_name = "{0}" and title = "{1}" and start_year = {2};
    """
    tvshow_genre_template = """
    INSERT INTO tvshow_genre (genre_id, tvshow_id) 
    VALUES ({0}, {1})
    ON DUPLICATE KEY UPDATE genre_id={0}, tvshow_id={1};
    """
    for genre in show.genres:
        check_query = sql_check.format(genre, show.title, show.start_year)
        cursor.execute(check_query)
        result = cursor.fetchone()
        genre_id, tvshow_id = result['genre_id'], result['tvshow_id']
        query = tvshow_genre_template.format(genre_id, tvshow_id)
        cursor.execute(query)


def insert_into_staff_member_table(cursor, s_member):
    """ Insert data of a specific staff member s_member into staff_member table. """
    sql_check = """ 
     SELECT COUNT(*) as count
     FROM staff_member 
     WHERE name = "{0}" and role = "{1}";
     """
    staff_member_template = """
    INSERT INTO staff_member (name, role, staff_member_rank, nb_tv_shows) 
    VALUES ("{0}", "{1}", {2}, {3});
    """
    staff_member_update = """
    UPDATE staff_member
    SET staff_member_rank={2}, nb_tv_shows={3}
    WHERE name="{0}" and role="{1}";
    """
    check_query = sql_check.format(s_member.name, s_member.role)
    cursor.execute(check_query)
    result = cursor.fetchone()
    if result['count'] == 0:
        query = staff_member_template.format(s_member.name, s_member.role, s_member.rank, s_member.nb_tv_shows)
    else:
        query = staff_member_update.format(s_member.name, s_member.role, s_member.rank, s_member.nb_tv_shows)
    cursor.execute(query)


def insert_into_tvshow_staff_table(cursor, s_member, show):
    """ Insert data into tvshow_staff table. """
    sql_check = """ 
    SELECT staff_member_id, tvshow_id
    FROM staff_member, tvshow 
    WHERE name = "{0}" and role ="{1}" and title = "{2}" and start_year = {3};
    """
    tvshow_staff_template = """
    INSERT INTO tvshow_staff (staff_member_id, tvshow_id) 
    VALUES ({0}, {1})
    ON DUPLICATE KEY UPDATE staff_member_id={0}, tvshow_id={1};
    """
    # role, name, rank, nb_tv_shows, start_year
    check_query = sql_check.format(s_member.name, s_member.role, show.title, show.start_year)
    cursor.execute(check_query)
    result = cursor.fetchone()
    staff_member_id, tvshow_id = result['staff_member_id'], result['tvshow_id']
    query = tvshow_staff_template.format(staff_member_id, tvshow_id)
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

    connection = pymysql.connect(host=HOST,
                                 # port=3306,
                                 user=USERNAME,
                                 password=PASSWORD,
                                 database='',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            for query in query_list:
                cursor.execute(query)
        connection.commit()
    connection = pymysql.connect(host=HOST,
                                 user=USERNAME,
                                 password=PASSWORD,
                                 database=DB_NAME,
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def update_staff_member(s_member):
    connection = create_ratingraph_db()
    with connection:
        with connection.cursor() as cursor:
            insert_into_staff_member_table(cursor, s_member)
        connection.commit()


def update_tvshows(tv_shows):
    """
    Creating a mysql database named 'ratingraph' and fill it with data from
    the website https://www.ratingraph.com/tv-shows/ .
    """
    connection = create_ratingraph_db()
    if not tv_shows:
        return
    with connection:
        with connection.cursor() as cursor:
            for show in tv_shows:
                insert_into_tvshow_table(cursor, show)
                insert_into_tvshow_rank_table(cursor, show)
                insert_into_genre_table(cursor, show)
                insert_into_tvshow_genre_table(cursor, show)
                insert_staff_members_of_a_tvshow(cursor, show)
                insert_into_actor_table(cursor, show)
                insert_into_tvshow_actor_table(cursor, show)
                logging.info(f'Details about {show.title} inserted successfully to all the relevant tables.')
        connection.commit()
        logging.info("Data mining project checkpoint #3, updating database finished successfully")
        print(f"Data mining project checkpoint #3, updating database finished successfully")
