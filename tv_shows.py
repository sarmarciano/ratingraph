class TvShow:
    """ This class represent a tv show. """
    def __init__(self, rank, title, start_year, end_year, genres, number_of_seasons, number_of_episodes, writers, directors):
        self.title = title
        self.rank = rank
        self.genres = genres
        self.number_of_seasons = number_of_seasons
        self.number_of_episodes = number_of_episodes
        self.start_year = start_year
        self.end_year = end_year
        self.writers = writers
        self.directors = directors

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        # return str(self.__dict__)
        return str(self.__dict__)
