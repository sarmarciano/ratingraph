CREATE DATABASE IF NOT EXISTS ratingraph;
USE ratingraph;
CREATE TABLE IF NOT EXISTS tvshow (tv_show_rank INT NOT NULL, title VARCHAR(150) PRIMARY KEY, nb_seasons INT NOT NULL, nb_episodes INT NOT NULL, start_year INT NOT NULL, end_year INT);
CREATE TABLE IF NOT EXISTS tvshow_genre (tvshow_title VARCHAR(150), genre VARCHAR(150) NOT NULL, PRIMARY KEY (tvshow_title, genre), FOREIGN KEY (tvshow_title) REFERENCES tvshow(title));
CREATE TABLE IF NOT EXISTS staff_member (name VARCHAR(150) NOT NULL, role VARCHAR(150) NOT NULL, staff_member_rank INT NOT NULL, nb_tv_shows INT NOT NULL, PRIMARY KEY (name, role));
CREATE TABLE IF NOT EXISTS tvshow_staff (name VARCHAR(150) NOT NULL, role VARCHAR(150) NOT NULL, tvshow_title VARCHAR(150), PRIMARY KEY (name, role, tvshow_title), FOREIGN KEY fk1 (name, role) REFERENCES staff_member(name, role), FOREIGN KEY (tvshow_title) REFERENCES tvshow(title));