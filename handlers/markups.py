import telebot.types

from scripts.parser import status_code_checker, check_proxies


# ======================================================================================================================


def start_menu_markup():
    text = "<u><b><i>Привет</i></b></u>"

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton("Домены", callback_data='domains_menu'),
        telebot.types.InlineKeyboardButton("Добавить Домен", callback_data='add_domain')
    )
    markup.add(
        telebot.types.InlineKeyboardButton("Прокси", callback_data='proxies'),
        telebot.types.InlineKeyboardButton("Добавить Прокси", callback_data='add_proxy')
    )

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


def subdomains_menu_markup(domain_name: str, subdomains_list: list | set, new: bool = False):
    text = f"<i>Сабдомены {domain_name}:</i>\n"
    markup = telebot.types.InlineKeyboardMarkup()

    if new:
        text = f"Появились новые сабдомены для <i>{domain_name}:</i>\n"

    if subdomains_list:
        for i in subdomains_list:
            status_code = status_code_checker(domain=i)
            text += f"http://{i} | {status_code} \n"

    markup.add(telebot.types.InlineKeyboardButton("Назад", callback_data='domains_menu'))
    return markup, text


def add_domain_text_markup():
    text = "Напишите <i>Название Домена</i> в ответ на это сообщение"
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text="Назад", callback_data='back_to_start_menu'))
    return markup, text


def add_domain_markup(domain_name: str = None, error: bool = False):
    text = f"Домен {domain_name} был добавлен"
    markup = telebot.types.InlineKeyboardMarkup()
    if error:
        text = "Неправильный формат домена"
    return markup, text


# ======================================================================================================================


def proxies_menu_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    proxies_good, proxies_bad = check_proxies()
    text = f"Исправных: <b>{len(proxies_good)}</b> | Неисправных: <b>{len(proxies_bad)}</b>\n"
    for count, i in enumerate(proxies_good):
        text += f"{count + 1}: <code>{i}</code>\n"
        markup.add(
            telebot.types.InlineKeyboardButton(f"{count + 1}", callback_data='none_data'),
            telebot.types.InlineKeyboardButton(f"✅", callback_data='none_data'),
            telebot.types.InlineKeyboardButton(f"-", callback_data=f'delete_proxy_{i}')
        )
    for count, i in enumerate(proxies_bad):
        text += f"{count + 1}: <code>{i}</code>\n"
        markup.add(
            telebot.types.InlineKeyboardButton(f"{count + 1}", callback_data='none_data'),
            telebot.types.InlineKeyboardButton(f"❌", callback_data='none_data'),
            telebot.types.InlineKeyboardButton(f"-", callback_data=f'delete_proxy_{i}')
        )

    markup.add(telebot.types.InlineKeyboardButton("Назад", callback_data='back_to_start_menu'))
    return markup, text


def add_proxy_text_markup():
    text = "Напишите <i>Прокси</i> или <i>Список Прокси</i> в ответ на это сообщение"
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text="Назад", callback_data='back_to_start_menu'))
    return markup, text


def add_proxy_markup():
    text = f"Прокси были добавлены"
    markup = telebot.types.InlineKeyboardMarkup()
    return markup, text
