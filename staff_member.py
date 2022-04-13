class StaffMember:
    """ This class represent a member of a tv show staff member """
    def __init__(self, role, name, rank, nb_tv_shows):
        self.role = role.title()
        self.name = name.title()
        self.rank = int(rank.split("/")[0].replace(",", ""))
        self.nb_tv_shows = int(nb_tv_shows)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'
