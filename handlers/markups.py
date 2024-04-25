import telebot.types

from database.db import Domain

from scripts.parser import status_code_checker


# ======================================================================================================================


def start_menu_markup():
    text = "Текст приветствия"

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Домены", callback_data='domains_menu'))
    markup.add(telebot.types.InlineKeyboardButton("Добавить домен", callback_data='add_domain'))

    return markup, text


def domains_menu_markup(domains_list: list = None):
    text = ""
    markup = telebot.types.InlineKeyboardMarkup()
    if domains_list:
        for i in domains_list:
            text += f"http://{i[0]} \n"
        for i in domains_list:
            markup.add(
                telebot.types.InlineKeyboardButton(f"{i[0]}", callback_data=f'show_subdomains_{i[0]}'),
                telebot.types.InlineKeyboardButton(f"{i[1]}", callback_data=f'change_status_{i[0]}'),
                telebot.types.InlineKeyboardButton(f"-", callback_data=f'delete_domain_{i[0]}')
            )
    else:
        text = "Домены"

    markup.add(telebot.types.InlineKeyboardButton("Назад", callback_data='back_to_start_menu'))
    return markup, text


# TODO: show statuses
def subdomains_menu_markup(domain_name: str, subdomains_list: list | set, new: bool = False):
    text = f"Сабдомены {domain_name}:\n"
    markup = telebot.types.InlineKeyboardMarkup()

    if new:
        text = f"Появились новые сабдомены для {domain_name}:\n"

    if subdomains_list:
        for i in subdomains_list:
            status_code = status_code_checker(domain=i)
            text += f"http://{i} | {status_code} \n"

    markup.add(telebot.types.InlineKeyboardButton("Назад", callback_data='domains_menu'))
    return markup, text


def add_domain_text_markup():
    text = "Напишите домейн в ответ на это сообщение"
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text="Назад", callback_data='back_to_start_menu'))
    return markup, text


def add_domain_markup(domain_name: str = None, error: bool = False):
    text = f"Домейн {domain_name} был добавлен"
    markup = telebot.types.InlineKeyboardMarkup()
    if error:
        text = "Неправильный формат домейна"
    return markup, text
