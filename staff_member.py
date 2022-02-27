class StaffMember:
    """ This class represent a member of a tv show staff member """
    def __init__(self, role, name, url_page, rank, trend, number_of_tv_shows, average_rating):
        self.role = role
        self.name = name
        self.url_page = url_page
        self.rank = rank
        self.trend = trend
        self.number_of_tv_shows = number_of_tv_shows
        self.average_rating = average_rating
        self.tv_shows = []

    def __str__(self):
        return f'role - {self.role}, name {self.name}'

    def __repr__(self):
        return f'role - {self.role}, name {self.name}'
