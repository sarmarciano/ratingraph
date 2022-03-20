import pymysql
import pymysql.cursors
import ratingraph_scraper
from config import *


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
    INSERT INTO tvshow_genre (tvshow_title, genre, start_year) 
    VALUES ("{0}", "{1}", {2})
    ON DUPLICATE KEY UPDATE tvshow_title="{0}", genre="{1}", start_year={2};
    """
    for genre in show.genres:
        query = tvshow_genre_template.format(show.title, genre, show.start_year)
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
    INSERT INTO tvshow_staff (name, role, tvshow_title, start_year) 
    VALUES ("{0}", "{1}", "{2}", {3})
    ON DUPLICATE KEY UPDATE name="{0}", role="{1}", tvshow_title="{2}", start_year={3};
    """
    # role, name, rank, nb_tv_shows, start_year
    query = tvshow_genre_template.format(s_member.name, s_member.role, show.title, show.start_year)
    cursor.execute(query)


def insert_staff_members_of_a_tvshow(cursor, show):
    """ Insert data of staff members that are part of a specific tv show into tables staff_member and tvshow_staff.  """
    for director in show.directors:
        insert_into_staff_member_table(cursor, director)
        insert_into_tvshow_staff_table(cursor, director, show)
    for writer in show.writers:
        insert_into_staff_member_table(cursor, writer)
        insert_into_tvshow_staff_table(cursor, writer, show)

def delete_from_tvshow_genre_table(cursor, title, start_year):
    """ Delete genres of a specific tv-show into tvshow_genre table. """
    tvshow_delete_template = """
    DELETE FROM tvshow_genre WHERE tvshow_title = "{0}" and start_year = {1};
    """
    query = tvshow_delete_template.format(title, start_year)
    cursor.execute(query)

def delete_from_tvshow_staff_table(cursor, title, start_year):
    """  """
    tvshow_delete_template = """
    DELETE FROM tvshow_staff WHERE tvshow_title = "{0}" and start_year = {1};
    """
    query = tvshow_delete_template.format(title, start_year)
    cursor.execute(query)


def delete_from_staff_member_table(cursor, name, role):
    """  """
    tvshow_delete_template = """
    DELETE FROM staff_member WHERE name = "{0}" and role = "{1}";
    """
    query = tvshow_delete_template.format(name, role)
    cursor.execute(query)

def delete_from_tvshow_table(cursor, title, start_year):
    """  """
    tvshow_delete_template = """
    DELETE FROM tvshow WHERE title = "{0}" and start_year = "{1}";
    """
    query = tvshow_delete_template.format(title, start_year)
    cursor.execute(query)


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


def main():
    """
    Creating a mysql database named 'ratingraph' and fill it with data from
    the website https://www.ratingraph.com/tv-shows/ .
    """

    create_ratingraph_db()
    connection = pymysql.connect(host=HOST,
                                 user=USERNAME,
                                 password=PASSWORD,
                                 database=DB_NAME,
                                 cursorclass=pymysql.cursors.DictCursor)
    existing_titles = "SELECT title, start_year FROM tvshow;"
    existing_staff_member = "SELECT name, role FROM tvshow_staff;"

    tv_shows = ratingraph_scraper.main()

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(existing_titles)
            old_results_tvshows = cursor.fetchall()

            old_results_tvshows = {(record['title'], record['start_year']) for record in old_results_tvshows}
            new_results_tvshows = {(show.title, show.start_year) for show in tv_shows}
            not_in_top_250 = list(old_results_tvshows - new_results_tvshows)
            cursor.execute(existing_staff_member)
            remaining_results_tvshow_staff = cursor.fetchall()

            for title_start_year in not_in_top_250:
                # genre, tvshow_staff, staff_member - order is important
                delete_from_tvshow_genre_table(cursor, title_start_year[0], title_start_year[1])
                delete_from_tvshow_staff_table(cursor, title_start_year[0], title_start_year[1])
            connection.commit()

            new_results_tvshow_staff = list()
            remaining_results_tvshow_staff = {(record['name'], record['role']) for record in remaining_results_tvshow_staff}

            for show in tv_shows:
                for director in show.directors:
                    new_results_tvshow_staff.append((director.name, director.role))
                for writer in show.writers:
                    new_results_tvshow_staff.append((writer.name, writer.role))
            new_results_tvshow_staff = set(new_results_tvshow_staff)
            not_in_top_250_s_members = list(remaining_results_tvshow_staff - new_results_tvshow_staff)

            for name_role in not_in_top_250_s_members:
                delete_from_staff_member_table(cursor, name_role[0], name_role[1])
            connection.commit()

            for title_start_year in not_in_top_250:
                delete_from_tvshow_table(cursor, title_start_year[0], title_start_year[1])
            connection.commit()

            for show in tv_shows:
                insert_into_tvshow_table(cursor, show)
                insert_into_tvshow_genre_table(cursor, show)
                insert_staff_members_of_a_tvshow(cursor, show)
        connection.commit()


if __name__ == '__main__':
    main()
