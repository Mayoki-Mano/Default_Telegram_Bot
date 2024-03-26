import traceback

import telebot

from botik.Database import Database


class Bot(telebot.TeleBot):
    def __init__(self, token, dir_path, db_path):
        super().__init__(token)
        self.DB = Database(dir_path, db_path)
        self.dict = {}
        self.register_message_handler(self.start_message, commands=['start'])
        self.register_message_handler(self.get_help, commands=['help'])
        self.register_message_handler(self.get_logout, commands=['logout'])
        self.register_message_handler(self.get_profile, commands=['profile'])
        self.register_message_handler(self.get_text, content_types=['text'])

    def get_profile(self, message):
        state = self.load_state_from_database(message.chat.id)
        if state == 0:
            self.send_message(message.chat.id, 'Вы не зарегистрированы, вам доступны команды start/reg/login/help')
        else:
            self.DB.cursor.execute("""
            SELECT TeamMember.MemberName, Team.TeamName
                FROM TeamMember 
                JOIN Team ON TeamMember.TeamID = Team.TeamID
                WHERE TeamMember.MemberID = ?""", (message.chat.id,))
            self.send_message(message.chat.id, self.DB.cursor.fetchone())

    def load_state_from_database(self, chat_id):
        self.DB.cursor.execute('SELECT state FROM States WHERE chat_id = ?', (chat_id,))
        result = self.DB.cursor.fetchone()
        return 0 if result is None else result[0]

    def save_state_to_database(self, chat_id, state):
        self.DB.cursor.execute('INSERT INTO States (chat_id, state, MemberID) VALUES (?, ?, ?) ON DUPLICATE KEY UPDATE chat_id=chat_id, state=state', (chat_id, state,-1))
        self.DB.conn.commit()

    def start_message(self, message):
        state = self.load_state_from_database(message.chat.id)
        match state:
            case 0:
                self.send_message(message.chat.id, 'Вы не зарегистрированы, вам доступны команды start/reg/login/help')
            case 1:
                self.send_message(message.chat.id,
                                  'Вы зарегистрированы, вам доступны команды start/logout/help/profile')
            case 3 | 4:
                self.send_message(message.chat.id, 'Введите ваш возраст')
            case 5 | 7:
                self.send_message(message.chat.id, 'Введите ваш пароль')
            case 6:
                self.send_message(message.chat.id, 'Введите ваше имя')
            case _:
                self.send_message(message.chat.id, 'Start_message error, case didn\'t find')

    def get_logout(self, message):
        state = self.load_state_from_database(message.chat.id)
        if state == 0:
            self.send_message(message.chat.id, 'Вы и так не авторизованы')
        else:
            self.send_message(message.chat.id, 'Успешная деавторизация')
            self.save_state_to_database(message.chat.id, 0)

    def get_help(self, message):
        self.send_message(message.chat.id,
                          "Это так называемый ботик для Степана, можно взаимодействовать через Привет/reg/help/start")

    def get_text(self, message):
        text = message.text
        state = self.load_state_from_database(message.chat.id)
        if text == "Привет":
            self.send_message(message.from_user.id, "Привет))")
            return
        match state:
            case 0:
                match text:
                    case "/reg":
                        self.save_state_to_database(message.chat.id, 3)
                        self.send_message(message.from_user.id, "Введите своё имя")
                    case "/login":
                        self.save_state_to_database(message.chat.id, 6)
                        self.send_message(message.from_user.id, "Введите своё имя")
                    case _:
                        self.send_message(message.from_user.id, "Пошёл нахуй")
            case 1:
                match text:
                    case "/reg":
                        self.send_message(message.from_user.id, "Вы уже авторизованы, рега не будет")
                    case "/login":
                        self.send_message(message.from_user.id, "Вы уже авторизованы")
                    case _:
                        self.send_message(message.from_user.id, "Пошёл нахуй")
            case 3:
                self.dict[message.chat.id] = (message.text,)
                self.DB.cursor.execute('SELECT * FROM TeamMember WHERE MemberName =?', (message.text,))
                if not self.DB.cursor.fetchone():
                    self.save_state_to_database(message.chat.id, 4)
                    self.DB.cursor.execute("""INSERT OR REPLACE INTO TeamMember
                                           (MemberID,MemberName,MemberAge,MemberPassword,TeamID) 
                                           VALUES(?,?,?,?,?)""", (message.chat.id, message.text, None, -1))
                    self.DB.conn.commit()
                    self.send_message(message.from_user.id, "Введите свой возраст")
                else:
                    self.save_state_to_database(message.chat.id, 0)
                    self.send_message(message.from_user.id, "Пользователь с таким именем уже существует")
            case 4:
                text = message.text
                try:
                    text = int(message.text)
                    if text <= 0:
                        self.send_message(message.from_user.id, "Некорректный возраст, попробуйте снова")
                except IOError:
                    print("get_text, case 4 IOError", traceback)
                self.dict[message.chat.id] = (self.dict[message.chat.id][0], text)
                self.DB.cursor.execute("""INSERT OR REPLACE INTO TeamMember (MemberID,MemberName,MemberAge,
                MemberPassword,TeamID) VALUES (?,?,?,?,?)""",
                                       (message.chat.id, self.dict[message.chat.id][0],
                                        self.dict[message.chat.id][1]), None, -1)
                self.DB.conn.commit()
                self.save_state_to_database(message.chat.id, 5)
                self.send_message(message.from_user.id, "Введите ваш пароль")
            case 5:
                self.dict[message.chat.id] = (
                    self.dict[message.chat.id][0], self.dict[message.chat.id][1], message.text,)
                self.save_state_to_database(message.chat.id, 1)
                self.DB.cursor.execute("""INSERT OR REPLACE INTO TeamMember (MemberID,MemberName,MemberAge,
                MemberPassword,TeamID) VALUES (?,?,?,?,?) """,
                                       (message.chat.id, self.dict[message.chat.id][0], self.dict[message.chat.id][1],
                                        self.dict[message.chat.id][2], -1))
                self.DB.conn.commit()
                self.send_message(message.from_user.id, "Успешная регистрация")
            case 6:
                self.dict[message.chat.id] = (message.text,)
                self.DB.cursor.execute('SELECT * FROM TeamMember WHERE MemberID =?', (message.chat.id,))
                if self.DB.cursor.fetchone():
                    self.save_state_to_database(message.chat.id, 7)
                    self.send_message(message.from_user.id, "Введите ваш пароль")
                else:
                    self.send_message(message.from_user.id, "Пользователя с данным именем не существует")
            case 7:
                self.dict[message.chat.id] = (self.dict[message.chat.id][0], message.text,)
                self.save_state_to_database(message.chat.id, 1)
                self.DB.cursor.execute('SELECT * FROM TeamMember WHERE MemberID =? AND MemberPassword=?',
                                       (message.chat.id, self.dict[1]))
                if self.DB.cursor.fetchone():
                    self.send_message(message.from_user.id, "Успешная авторизация")
                else:
                    self.send_message(message.from_user.id, "Неправильный пароль")
            case _:
                self.send_message(message.from_user.id, "get_text case error")
