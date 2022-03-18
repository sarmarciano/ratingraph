class StaffMember:
    """ This class represent a member of a tv show staff member """
    def __init__(self, role, name, rank, nb_tv_shows):
        self.role = role
        self.name = name
        self.rank = int(rank.split("/")[0].replace(",", ""))
        self.nb_tv_shows = int(nb_tv_shows)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return f'role - {self.role}, name {self.name}'
