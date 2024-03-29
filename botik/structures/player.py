class Player:
    def __init__(self, name=None, password=None, age=None, score=0, team_name=None):
        self.name = name
        self.password = password
        self.age = age
        self.score = score
        self.team_name = team_name

    def print_info(self, i=-1):
        if i == -1:
            return f"""Name: {self.name}, Age: {self.age}, Score: {self.score}, Team: {self.team_name}"""
        else:
            return f"""{i+1}. Name: {self.name}, Age: {self.age}, Score: {self.score}, Team: {self.team_name}"""
