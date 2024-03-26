import os
import sqlite3


class Database:
    def __init__(self, dir_path, db_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.db_tables_creation()

    def __del__(self):
        self.conn.close()

    def db_tables_creation(self):
        sql_query_Team_creating = """
        CREATE TABLE IF NOT EXISTS Team (
            TeamID INTEGER PRIMARY KEY AUTOINCREMENT,
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
            TeamID INT,
            Score INTEGER DEFAULT 0,
            FOREIGN KEY (TeamID) REFERENCES Team(TeamID),
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
        self.cursor.execute(sql_query_Team_creating)
        self.cursor.execute(sql_query_States_creating)
        self.cursor.execute(sql_query_TeamMember_creating)

    def get_profile_from_database(self, chat_id):
        self.cursor.execute("""
                    SELECT TeamMember.MemberName, TeamMember.MemberAge,TeamMember.Score, Team.TeamName
                        FROM States 
                        LEFT JOIN TeamMember ON TeamMember.MemberName = States.MemberName
                        LEFT JOIN Team ON Team.TeamID = TeamMember.TeamID 
                        WHERE States.chat_id = ?
                        """, (chat_id,))
        return self.cursor.fetchone()

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

    def set_member_to_db(self, member_name, member_age, score, member_passwd, team_id):
        self.cursor.execute("""INSERT OR REPLACE INTO TeamMember                           
            (MemberName,MemberAge,Score,MemberPassword,TeamID) 
            VALUES(?,?,?,?,?)""", (member_name, member_age,score, member_passwd, team_id))
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
    def up_score_to_db(self, member_name, score):
        self.cursor.execute("""UPDATE TeamMember SET Score=Score+? WHERE MemberName = ?""",(score, member_name))
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
            """SELECT TeamMember.MemberName, TeamMember.MemberAge,TeamMember.Score, Team.TeamName
            FROM TeamMember JOIN Team ON Team.TeamID = TeamMember.TeamID ORDER BY score LIMIT 10""")
        return self.cursor.fetchall()

    def get_top_teams_from_database(self):
        self.cursor.execute(
            """SELECT Team.TeamName, Team.TeamScore, Team.MembersCount
            FROM Team ORDER BY TeamScore LIMIT 10""")
        return self.cursor.fetchall()
