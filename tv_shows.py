class TvShow:
    """ This class represent a tv show. """
    def __init__(self, rank, title, start_year, end_year, genres, nb_seasons, nb_episodes, writers, directors):
        self.title = title
        self.rank = int(rank)
        self.genres = genres
        self.nb_seasons = int(nb_seasons)
        self.nb_episodes = int(nb_episodes)
        self.start_year = int(start_year)
        self.end_year = int(end_year) if end_year.isdigit() else 0
        self.writers = writers if writers else []
        self.directors = directors if directors else []

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        # return str(self.__dict__)
        return str(self.__dict__)
