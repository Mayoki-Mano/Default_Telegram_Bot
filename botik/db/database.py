import os
import sqlite3

from botik.structures.player import Player
from botik.structures.team import Team


class Database:
    def __init__(self, dir_path, db_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.db_tables_creation()

    def __del__(self):
        self.conn.close()

    def db_tables_creation(self):
        sql_query_Team_creating = """
        CREATE TABLE IF NOT EXISTS Team (
            TeamName VARCHAR(255) NOT NULL,
            TeamScore INTEGER DEFAULT 0,
            CreationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            MembersCount INT
        );
        """
        sql_query_TeamMember_creating = """
        CREATE TABLE IF NOT EXISTS TeamMember (
            MemberName VARCHAR(255),
            MemberPassword VARCHAR(255),
            MemberAge INT,
            Score INTEGER DEFAULT 0,
            TeamName VARCHAR(255),
            FOREIGN KEY (TeamName) REFERENCES Team(TeamName),
            FOREIGN KEY (MemberName) REFERENCES States(MemberName)
        );
        """
        sql_query_States_creating = """
        CREATE TABLE IF NOT EXISTS States (
        chat_id INTEGER PRIMARY KEY,
        MemberName VARCHAR(255),
        state INT
        );
        """
        sql_query_TeamInvites_creating = """
        CREATE TABLE IF NOT EXISTS TeamInvites (
        MemberName VARCHAR(255),
        TeamName VARCHAR(255),
        FOREIGN KEY (TeamName) REFERENCES Team(TeamName),
        FOREIGN KEY (MemberName) REFERENCES TeamMember(MemberName)
        );
        """
        self.cursor.execute(sql_query_Team_creating)
        self.cursor.execute(sql_query_States_creating)
        self.cursor.execute(sql_query_TeamMember_creating)
        self.cursor.execute(sql_query_TeamInvites_creating)

    def get_state_from_database(self, message):
        self.cursor.execute('SELECT state FROM States WHERE chat_id = ?', (message.chat.id,))
        return self.cursor.fetchone()

    def set_state_to_database(self, chat_id, state):
        self.cursor.execute(
            'INSERT INTO States (chat_id, state) VALUES (?, ?) '
            'ON CONFLICT(chat_id) DO UPDATE SET state =?',
            (chat_id, state, state))
        self.conn.commit()

    def set_member_name_into_states_table(self, chat_id, member_name):
        self.cursor.execute(
            'INSERT INTO States (chat_id, MemberName) VALUES (?, ?) '
            'ON CONFLICT(chat_id) DO UPDATE SET MemberName =?',
            (chat_id, member_name, member_name))
        self.conn.commit()

    def delete_chat_id_from_database(self, chat_id):
        self.cursor.execute('DELETE FROM States WHERE chat_id = ?', (chat_id,))
        self.conn.commit()

    def user_exits_in_db(self, member_name):
        self.cursor.execute('SELECT * FROM TeamMember WHERE MemberName =?', (member_name,))
        return self.cursor.fetchone()

    def set_member_to_db(self, member_name, member_age, score, member_passwd, team_name):
        self.cursor.execute("""INSERT OR REPLACE INTO TeamMember                           
            (MemberName,MemberAge,Score,MemberPassword,TeamName) 
            VALUES(?,?,?,?,?)""", (member_name, member_age, score, member_passwd, team_name))
        self.conn.commit()

    def get_membername_by_id(self, chat_id):
        self.cursor.execute('SELECT MemberName FROM States WHERE chat_id =?', (chat_id,))
        return self.cursor.fetchone()[0]

    def update_member_age_to_db(self, member_name, member_age):
        self.cursor.execute("""UPDATE TeamMember SET MemberAge =? WHERE MemberName = ?""", (member_age, member_name))
        self.conn.commit()

    def update_member_password_to_db(self, member_name, member_passwd):
        self.cursor.execute("""UPDATE TeamMember SET MemberPassword =? WHERE MemberName = ?""",
                            (member_passwd, member_name))
        self.conn.commit()

    def up_score_into_db(self, chat_id, score):
        member_name = self.get_membername_by_id(chat_id)
        team_name = self.get_member_team_from_db(member_name)
        self.cursor.execute("""UPDATE TeamMember 
        SET TeamMember.Score=TeamMember.Score+? 
        WHERE TeamMember.MemberName = ?""", (score, member_name))
        self.cursor.execute("""UPDATE Team SET Team.TeamScore=Team.TeamScore+? WHERE TeamName=?""",
                            (score, team_name))
        self.conn.commit()

    def get_age_by_id(self, member_name):
        self.cursor.execute('SELECT MemberAge FROM TeamMember WHERE MemberName =?', (member_name,))
        return self.cursor.fetchone()[0]

    def try_login_to_db(self, member_name, member_passwd):
        self.cursor.execute('SELECT * FROM TeamMember WHERE MemberName =? AND MemberPassword=?',
                            (member_name, member_passwd))
        return self.cursor.fetchone()

    def get_top_players_from_database(self):
        self.cursor.execute(
            """SELECT * FROM TeamMember ORDER BY score LIMIT 10""")
        data_array_of_players = self.cursor.fetchall()
        players = []
        for data_player in data_array_of_players:
            players.append(Player(*data_player))
        return players

    def get_profile_from_database(self, chat_id):
        self.cursor.execute("""SELECT TeamMember.* FROM States 
                    LEFT JOIN TeamMember ON TeamMember.MemberName = States.MemberName 
                    WHERE States.chat_id = ?""", (chat_id,))
        return Player(*self.cursor.fetchone())

    def get_top_teams_from_database(self):
        self.cursor.execute("""SELECT * FROM Team ORDER BY TeamScore LIMIT 10""")
        data_array_of_teams = self.cursor.fetchall()
        teams = []
        for data_team in data_array_of_teams:
            teams.append(Team(*data_team))
        return teams

    def team_exits_in_db(self, team_name):
        self.cursor.execute('SELECT * FROM Team WHERE TeamName =?', (team_name,))
        return self.cursor.fetchone()

    def add_team_to_db(self, team_name):
        self.cursor.execute("""INSERT INTO Team (TeamName) VALUES (?)""", (team_name,))
        self.conn.commit()

    def add_player_into_team(self, chat_id, team_name):
        member_name = self.get_membername_by_id(chat_id)
        self.cursor.execute("""UPDATE TeamMember SET TeamName = ? WHERE MemberName = ?""", (team_name, member_name))
        self.cursor.execute("""UPDATE Team SET MembersCount = MembersCount+1 WHERE TeamName = ?""", (team_name,))
        self.conn.commit()

    def delete_player_from_team(self, chat_id):
        member_name = self.get_membername_by_id(chat_id)
        team_name = self.get_member_team_from_db(member_name)
        self.cursor.execute("""UPDATE TeamMember SET TeamName = NULL WHERE MemberName = ?""", (member_name,))
        self.cursor.execute("""UPDATE Team SET MembersCount = MembersCount-1 WHERE TeamName = ?""", (team_name,))
        self.cursor.execute("""DELETE FROM Team WHERE MembersCount =0""")
        self.conn.commit()

    def get_member_team_from_db(self, member_name):
        self.cursor.execute("""SELECT TeamName FROM TeamMember WHERE MemberName = ?""", (member_name,))
        return self.cursor.fetchone()[0]

    def get_team_invites(self, chat_id):
        member_name = self.get_membername_by_id(chat_id)
        self.cursor.execute("""SELECT TeamName FROM TeamInvites WHERE MemberName = ?""", (member_name,))
        team_names = []
        for data in self.cursor.fetchall():
            team_names.append(data[0])
        self.cursor.execute("""SELECT * FROM Team WHERE TeamName IN (:team_names)""")
        teams = []
        for data_team in self.cursor.fetchall():
            teams.append(Team(*data_team))
        return teams

    def invite_player_into_team(self, chat_id, player_name):
        member_name = self.get_membername_by_id(chat_id)
        team_name = self.get_member_team_from_db(member_name)
        self.cursor.execute("""INSERT INTO TeamInvites (MemberName, TeamName) VALUES (?,?)""",
                            (player_name, team_name))
        self.conn.commit()
