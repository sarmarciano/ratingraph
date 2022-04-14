from config import NA

class TvShow:
    """ This class represents a tv show. """
    def __init__(self, rank, title, start_year, end_year, genres, nb_seasons, nb_episodes, writers, directors,
                 actors, synopsis, imdb_rating):
        self.title = title.title().replace('"', "'")
        self.rank = int(rank)
        self.genres = genres
        self.nb_seasons = int(nb_seasons)
        self.nb_episodes = int(nb_episodes)
        self.start_year = int(start_year)
        self.end_year = int(end_year) if end_year.isdigit() else 0
        self.writers = writers if writers else []
        self.directors = directors if directors else []
        self.actors = actors if actors else []
        self.synopsis = synopsis.capitalize() if synopsis != NA else ''
        self.synopsis = self.synopsis.replace('"', "'")
        self.imdb_rating = -1.0 if imdb_rating == NA else float(imdb_rating)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        # return str(self.__dict__)
        return str(self.__dict__)
