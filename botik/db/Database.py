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
            CreationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            MembersCount INT
        );
        """
        sql_query_TeamMember_creating = """
        CREATE TABLE IF NOT EXISTS TeamMember (
            MemberID INTEGER PRIMARY KEY AUTOINCREMENT,
            MemberName VARCHAR(255) NOT NULL,
            MemberPassword VARCHAR(255),
            MemberAge INT,
            TeamID INT,
            FOREIGN KEY (TeamID) REFERENCES Team(TeamID),
            FOREIGN KEY (MemberID) REFERENCES States(MemberID)
        );
        """
        sql_query_States_creating = """
        CREATE TABLE IF NOT EXISTS States (
        chat_id INTEGER PRIMARY KEY,
        MemberID INTEGER,
        state INT
        );
        """
        self.cursor.execute(sql_query_Team_creating)
        self.cursor.execute(sql_query_States_creating)
        self.cursor.execute(sql_query_TeamMember_creating)
