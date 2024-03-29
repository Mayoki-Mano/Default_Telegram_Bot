class Team:
    def __init__(self, team_name=None, team_score=None, creation_date=None, members_count=0):
        self.name = team_name
        self.score = team_score
        self.members_count = members_count
        self.creation_date = creation_date

    def print_info(self, i=-1):
        if i == -1:
            return f"""Name: {self.name}, Score: {self.score}, Members count: {self.members_count}, 
            Creation time: {self.creation_date}"""
        else:
            return f"""{i+1}. Name: {self.name}, Score: {self.score}, Members count: {self.members_count}, 
                    Creation time: {self.creation_date}"""
