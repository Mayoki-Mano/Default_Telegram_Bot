import random
from enum import Enum

import telebot

from botik.db.database import Database


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
    CREATE_TEAM_NAME = 11
    HAVE_TEAM = 12


class Bot(telebot.TeleBot):

    def __init__(self, token, dir_path, db_path):
        super().__init__(token, threaded=False)
        self.DB = Database(dir_path, db_path)
        self.dict = {}
        self.register_message_handler(self.start_message, commands=['start'])
        self.register_message_handler(self.get_help, commands=['help'])
        self.register_message_handler(self.get_logout, commands=['logout'])
        self.register_message_handler(self.get_profile, commands=['profile'])
        self.register_message_handler(self.get_top_players, commands=['top_players'])
        self.register_message_handler(self.get_top_teams, commands=['top_teams'])
        self.register_message_handler(self.get_text, content_types=['text'])

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.DB:
            self.DB.__del__()
        if self.threaded:
            for i in range(self.worker_pool.num_threads):
                self.worker_pool.workers[i].stop()
                self.worker_pool.workers[i].clear_exceptions()
            self.worker_pool.workers.clear()
            self.worker_pool.clear_exceptions()
            self.worker_pool.close()

    def __enter__(self):
        return self

    def get_top_teams(self, message):
        top_teams = self.DB.get_top_teams_from_database()
        for i in range(len(top_teams)):
            self.send_message(message.chat.id, top_teams[i].print_info(i))

    def get_top_players(self, message):
        top_players = self.DB.get_top_players_from_database()
        for i in range(len(top_players)):
            self.send_message(message.chat.id, top_players[i].print_info(i))

    def get_profile(self, message):
        state = self.load_state_from_database(message)
        if state == State.UNREGISTERED:
            self.send_message(message.chat.id, 'Вы не зарегистрированы, вам доступны команды start/reg/login/help')
        else:
            player = self.DB.get_profile_from_database(message.chat.id)
            self.send_message(message.chat.id, player.print_info())

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
            case State.CREATE_TEAM_NAME:
                self.send_message(message.chat.id, 'Введите имя вашей команды')
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
                    case "/create_team":
                        self.insert_into_states_table(message.chat.id, State.CREATE_TEAM_NAME, None)
                        self.send_message(message.from_user.id, "Введите имя вашей новой команды")
                    case _:
                        self.send_message(message.from_user.id, "Пошёл нахуй")
            case State.REG_NAME:
                self.dict[message.chat.id] = (message.text,)
                if not self.DB.user_exits_in_db(message.text):
                    self.insert_into_states_table(message.chat.id, State.REG_AGE, message.text)
                    self.DB.set_member_to_db(message.text, -1, 0, None, None)
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
                    if self.DB.get_team_by_member_name(self.dict[message.chat.id][0]):
                        self.insert_into_states_table(message.chat.id, State.HAVE_TEAM, self.dict[message.chat.id][0])
                    else:
                        self.insert_into_states_table(message.chat.id, State.REGISTERED, self.dict[message.chat.id][0])
                    self.send_message(message.from_user.id, "Успешная авторизация")
                else:
                    self.insert_into_states_table(message.chat.id, State.UNREGISTERED, None)
                    self.send_message(message.from_user.id, "Неправильный пароль")
            case State.CREATE_TEAM_NAME:
                self.dict[message.chat.id] = (message.text,)
                if not self.DB.team_exits_in_db(message.text):
                    self.insert_into_states_table(message.chat.id, State.HAVE_TEAM, None)
                    self.DB.add_team_to_db(message.text)
                    self.DB.add_player_into_team(message.chat.id, message.text)
                    self.send_message(message.chat.id, "Успешная регистрация команды")
            case State.HAVE_TEAM:
                match text:
                    case "/invite_to_team":
                        self.send_message(message.chat.id, "Введите имя приглашаемого друга")
                        self.insert_into_states_table(message.chat.id, State.INV_NAME, None)
                    case "/leave_from_team":
                        self.insert_into_states_table(message.chat.id, State.REGISTERED, None)
                        self.send_message(message.chat.id, "Вы успешно вышли из команды")
                    case "/check_invites_to_team":
                        inv_teams = self.DB.get_team_invites(message.chat.id)
                        if inv_teams:
                            for inv_team in inv_teams:
                                self.send_message(message.chat.id, inv_team.print_info())
                            self.insert_into_states_table(message.chat.id, State.CHECK_INV_NAME, None)
                            self.send_message(message.chat.id, "Введите имя предпочитаемой команды")
                        else:
                            self.send_message(message.chat.id, "Вас ещё никто не пригласил :(")
                    case "/play_CTF":
                        score_up = random.randint(0, 1000)
                        self.send_message(message.chat.id,
                                          f"Как всегда красавчик, ты заработал {score_up} баллов для своей команды")

                        self.DB.up_score_into_db(message.chat.id, score_up)
                    case _:
                        self.send_message(message.chat.id, "Пошёл нахуй, и команду свою прихвати")
            case State.CHECK_INV_NAME:
                team_name = message.text
                inv_teams = self.DB.get_team_invites(message.chat.id)
                inv_team_names = [inv_team.name for inv_team in inv_teams]
                if team_name in inv_team_names:
                    self.insert_into_states_table(message.chat.id, State.HAVE_TEAM, None)
                    self.DB.delete_player_from_team(message.chat.id)
                    self.DB.add_player_into_team(message.chat.id, team_name)
                    self.send_message(message.chat.id, f"Вы успешно добавлены в команду {team_name}")
                else:
                    self.send_message(message.chat.id, "В предложенном списке нет такой команды :(")
                    if self.DB.get_team_by_member_name(self.DB.get_membername_by_id(message.chat.id)):
                        self.insert_into_states_table(message.chat.id, State.HAVE_TEAM, None)
                    else:
                        self.insert_into_states_table(message.chat.id, State.REGISTERED, None)

            case State.INV_NAME:
                name = message.text
                if self.DB.user_exits_in_db(name):
                    self.DB.invite_player_into_team(message.chat.id, name)
                    self.send_message(message.from_user.id, "Игрок успешно приглашён")
                else:
                    self.insert_into_states_table(message.chat.id, State.HAVE_TEAM, None)
                    self.send_message(message.from_user.id, "Пользователя с таким именем не существует")
            case _:
                self.insert_into_states_table(message.chat.id, State.UNREGISTERED, None)
                self.send_message(message.from_user.id, "get_text case error")
