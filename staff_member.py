class StaffMember:
    """ This class represent a member of a tv show staff member """
    def __init__(self, role, name, rank, number_of_tv_shows):
        self.role = role
        self.name = name
        self.rank = rank
        self.number_of_tv_shows = number_of_tv_shows

    def __str__(self):
        return f'role - {self.role}, name {self.name}'

    def __repr__(self):
        return f'role - {self.role}, name {self.name}'
