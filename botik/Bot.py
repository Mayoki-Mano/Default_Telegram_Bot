from enum import Enum

import telebot

from botik.db.Database import Database


class State(Enum):
    UNREGISTERED = 0
    REGISTERED = 1
    IN_TEAM = 2
    REG_NAME = 3
    REG_AGE = 4
    REG_PASSWD = 5
    LOG_NAME = 6
    LOG_PASSWD = 7
    INV_NAME = 8
    CHECK_INV = 9
    CHECK_INV_NAME = 10


class Bot(telebot.TeleBot):

    def __init__(self, token, dir_path, db_path):
        super().__init__(token)
        self.DB = Database(dir_path, db_path)
        self.dict = {}
        self.register_message_handler(self.start_message, commands=['start'])
        self.register_message_handler(self.get_help, commands=['help'])
        self.register_message_handler(self.get_logout, commands=['logout'])
        self.register_message_handler(self.get_profile, commands=['profile'])
        self.register_message_handler(self.get_top_players, commands=['top_players'])
        self.register_message_handler(self.get_top_teams, commands=['top_teams'])
        self.register_message_handler(self.get_text, content_types=['text'])

    def get_top_teams(self, message):
        team_info = self.DB.get_top_teams_from_database()
        for i in range(len(team_info)):
            self.send_message(message.chat.id,
                              str(i + 1) + ".     TeamName:  " + team_info[i][0] + "  Score:  " + str(
                                  team_info[i][1]) + "  MembersCount:  " + str(
                                  team_info[i][2]))

    def get_top_players(self, message):
        profile_info = self.DB.get_top_players_from_database()
        for i in range(len(profile_info)):
            self.send_message(message.chat.id,
                              str(i + 1) + ".     Nickname:  " + profile_info[i][0] + "  Age:  " + str(
                                  profile_info[i][1]) + "  Score:  " + str(
                                  profile_info[i][2]) + "  Team:  " + str(
                                  profile_info[i][3]))

    def get_profile(self, message):
        state = self.load_state_from_database(message)
        if state == State.UNREGISTERED:
            self.send_message(message.chat.id, 'Вы не зарегистрированы, вам доступны команды start/reg/login/help')
        else:
            profile_info = self.DB.get_profile_from_database(message.chat.id)
            self.send_message(message.chat.id,
                              "Nickname: " + profile_info[0] + "\nAge: " + str(profile_info[1]) + "\nScore: " +
                              str(profile_info[2]) + "\nTeam: " + str(profile_info[3]))

    def load_state_from_database(self, message):
        result = self.DB.get_state_from_database(message)
        return State(0) if result is None else State(result[0])

    def insert_into_states_table(self, chat_id, state, member_name):
        self.DB.set_state_to_database(chat_id, state.value)
        if member_name is not None:
            self.DB.set_member_name_into_states_table(chat_id, member_name)

    def start_message(self, message):
        state = self.load_state_from_database(message)
        match state:
            case State.UNREGISTERED:
                self.send_message(message.chat.id, 'Вы не зарегистрированы, вам доступны команды start/reg/login/help')
            case State.REGISTERED:
                self.send_message(message.chat.id,
                                  'Вы зарегистрированы, вам доступны команды start/logout/help/profile')
            case State.REG_NAME | State.REG_AGE:
                self.send_message(message.chat.id, 'Введите ваш возраст')
            case State.REG_PASSWD | State.LOG_PASSWD:
                self.send_message(message.chat.id, 'Введите ваш пароль')
            case State.LOG_NAME:
                self.send_message(message.chat.id, 'Введите ваше имя')
            case _:
                self.send_message(message.chat.id, 'Start_message error, case didn\'t find')

    def get_logout(self, message):
        state = self.load_state_from_database(message)
        if state == State.UNREGISTERED:
            self.send_message(message.chat.id, 'Вы и так не авторизованы')
        else:
            self.DB.delete_chat_id_from_database(message.chat.id)
            self.send_message(message.chat.id, 'Успешная деавторизация')
            self.insert_into_states_table(message.chat.id, State.UNREGISTERED, None)  # useless
            if self.dict.__contains__(message.chat.id):
                self.dict.pop(message.chat.id)

    def get_help(self, message):
        self.send_message(message.chat.id,
                          "Это так называемый ботик для Степана, можно взаимодействовать через Привет/reg/help/start")

    def get_text(self, message):
        text = message.text
        state = self.load_state_from_database(message)
        if text == "Привет":
            self.send_message(message.from_user.id, "Привет))")
            return
        match state:
            case State.UNREGISTERED:
                match text:
                    case "/reg":
                        self.insert_into_states_table(message.chat.id, State.REG_NAME, None)
                        self.send_message(message.from_user.id, "Введите своё имя")
                    case "/login":
                        self.insert_into_states_table(message.chat.id, State.LOG_NAME, None)
                        self.send_message(message.from_user.id, "Введите своё имя")
                    case _:
                        self.send_message(message.from_user.id, "Пошёл нахуй")
            case State.REGISTERED:
                match text:
                    case "/reg":
                        self.send_message(message.from_user.id, "Вы уже авторизованы, рега не будет")
                    case "/login":
                        self.send_message(message.from_user.id, "Вы уже авторизованы")
                    case _:
                        self.send_message(message.from_user.id, "Пошёл нахуй")
            case State.REG_NAME:
                self.dict[message.chat.id] = (message.text,)
                if not self.DB.user_exits_in_db(message.text):
                    self.insert_into_states_table(message.chat.id, State.REG_AGE, message.text)
                    self.DB.set_member_to_db(message.text, -1, 0, None, -1)
                    self.send_message(message.from_user.id, "Введите свой возраст")
                else:
                    self.insert_into_states_table(message.chat.id, State.UNREGISTERED, None)
                    self.send_message(message.from_user.id, "Пользователь с таким именем уже существует")
            case State.REG_AGE:
                try:
                    text = int(message.text)
                    if text <= 0:
                        self.send_message(message.from_user.id, "Некорректный возраст, попробуйте снова")
                        return
                except ValueError:
                    self.send_message(message.from_user.id, "Желательно цифрами")
                    return
                if not self.dict.__contains__(message.chat.id):
                    self.dict[message.chat.id] = (self.DB.get_membername_by_id(message.chat.id),)
                self.dict[message.chat.id] = (self.dict[message.chat.id][0], text)
                self.DB.update_member_age_to_db(self.dict[message.chat.id][0], text)
                self.insert_into_states_table(message.chat.id, State.REG_PASSWD, None)
                self.send_message(message.from_user.id, "Введите ваш пароль")
            case State.REG_PASSWD:
                if not self.dict.__contains__(message.chat.id):
                    self.dict[message.chat.id] = (self.DB.get_membername_by_id(message.chat.id),)
                    self.dict[message.chat.id] = (self.DB.get_membername_by_id(message.chat.id),
                                                  self.DB.get_age_by_id(self.dict[message.chat.id][0]),)
                self.dict[message.chat.id] = (
                    self.dict[message.chat.id][0], self.dict[message.chat.id][1], message.text,)
                self.insert_into_states_table(message.chat.id, State.REGISTERED, self.dict[message.chat.id][0])
                self.DB.update_member_password_to_db(self.dict[message.chat.id][0], message.text)
                self.send_message(message.from_user.id, "Успешная регистрация")
            case State.LOG_NAME:
                self.dict[message.chat.id] = (message.text,)
                if self.DB.user_exits_in_db(message.text):
                    self.insert_into_states_table(message.chat.id, State.LOG_PASSWD, message.text)
                    self.send_message(message.from_user.id, "Введите ваш пароль")
                else:
                    self.send_message(message.from_user.id, "Пользователя с данным именем не существует")
                    self.insert_into_states_table(message.chat.id, State.UNREGISTERED, None)
            case State.LOG_PASSWD:
                if not self.dict.__contains__(message.chat.id):
                    self.dict[message.chat.id] = (self.DB.get_membername_by_id(
                        message.chat.id),)
                self.dict[message.chat.id] = (self.dict[message.chat.id][0], message.text,)

                if self.DB.try_login_to_db(self.dict[message.chat.id][0], message.text):
                    self.insert_into_states_table(message.chat.id, State.REGISTERED, self.dict[message.chat.id][0])
                    self.send_message(message.from_user.id, "Успешная авторизация")
                else:
                    self.insert_into_states_table(message.chat.id, State.UNREGISTERED, None)
                    self.send_message(message.from_user.id, "Неправильный пароль")
            case _:
                self.insert_into_states_table(message.chat.id, State.UNREGISTERED, None)
                self.send_message(message.from_user.id, "get_text case error")
