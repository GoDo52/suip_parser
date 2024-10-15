from bot.setup import bot

import telebot.types
from threading import Thread

from handlers.markups import *

from database.db import Domain, get_all_domains, get_all_domains_list, Proxy

from scripts.tools_executor import get_subdomains

from config import ADMIN_ID_LIST


# ======================================================================================================================


def split_messages(text, max_length=4090):
    lines = text.split('\n')
    messages = []
    current_message = ""

    for line in lines:
        if len(current_message) + len(line) + 1 > max_length:
            messages.append(current_message)
            current_message = line
        else:
            current_message += ('\n' + line if current_message else line)

    if current_message:
        messages.append(current_message)

    return messages


def bot_message(message, markup, inline: bool = False):
    markup_reply, markup_text = markup
    text_length = len(markup_text)
    if inline and text_length <= 4090:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=markup_text,
            reply_markup=markup_reply,
            parse_mode='html',
            disable_web_page_preview=True
        )
    else:
        if text_length > 4090:
            text_chunks = split_messages(text=markup_text)
            for i, chunk in enumerate(text_chunks):
                if i == len(text_chunks) - 1:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text=chunk,
                        reply_markup=markup_reply,
                        parse_mode='html',
                        disable_web_page_preview=True
                    )
                else:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text=chunk,
                        reply_markup=None,
                        parse_mode='html',
                        disable_web_page_preview=True
                    )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text=markup_text,
                reply_markup=markup_reply,
                parse_mode='html',
                disable_web_page_preview=True
            )


# ======================================================================================================================


def check_domains():
    print('Checking domains')
    domains = get_all_domains(notification_true=True)
    for domain_name in domains:
        domain = Domain(domain=domain_name[0])
        subdomains_list = get_subdomains(url=domain.domain)
        subdomains_update_status, new_subdomains = domain.add_subdomains(subdomains=subdomains_list)
        print(f"{domain.domain}: new - {subdomains_update_status}, new_subdomains - {new_subdomains}")
        if subdomains_update_status:
            markup_reply, markup_text = subdomains_menu_markup(domain_name=domain.domain,
                                                               subdomains_list=new_subdomains, new=True)
            for admin in ADMIN_ID_LIST:
                try:
                    bot.send_message(
                        chat_id=admin,
                        text=markup_text,
                        reply_markup=markup_reply,
                        parse_mode='html',
                        disable_web_page_preview=True
                    )
                except Exception as e:
                    print(f"Not able to reach Admin (blocked the bot, or not known: {e}")
        else:
            print(f"No difference in subdomains for {domain.domain}")


# ======================================================================================================================


def start_menu_logic(message, inline: bool = False):
    bot_message(message, start_menu_markup(), inline)


def domains_menu_logic(message, section: int = 1, inline: bool = False):
    domains_list, forward, first_page = get_all_domains(section=int(section))
    bot_message(
        message,
        domains_menu_markup(domains_list=domains_list, forward=forward, first_page=first_page, section=int(section)),
        inline
    )


def all_domains_menu_logic(message, inline: bool = False):
    domains_list = get_all_domains_list()
    bot_message(
        message,
        all_domains_menu_markup(domains_list=domains_list),
        inline
    )


def subdomains_menu_logic(message, domain_name: str, inline: bool = False):
    domain = Domain(domain=domain_name)
    subdomains_list = get_subdomains(url=domain.domain)
    subdomains_update_status, new_subdomains = domain.add_subdomains(subdomains_list)
    bot_message(message, subdomains_menu_markup(domain_name=domain.domain, subdomains_list=subdomains_list), inline)
    if subdomains_update_status:
        bot_message(
            message,
            subdomains_menu_markup(domain_name=domain.domain, subdomains_list=new_subdomains, new=True),
            inline=False
        )


# ======================================================================================================================


def add_domain_text_logic(message, inline: bool = False):
    bot_message(message, add_domain_text_markup(), inline)
    bot.register_next_step_handler(message, add_domain)


def add_domain(message, inline: bool = False):
    domain_name = message.text.removeprefix('https://').removeprefix('http://')
    domain = Domain(domain_name)
    bot_message(message, add_domain_markup(domain_name=domain.domain), inline)
    bot_message(message, start_menu_markup(), inline)


def delete_domain_logic(message, domain_name: str, inline: bool = True):
    domain = Domain(domain_name)
    domain.delete_domain()
    domains_menu_logic(message, inline=inline)


def update_domain_status_logic(message,domain_name: str,  section: int = 1, inline: bool = True):
    domain = Domain(domain_name)
    domain.change_domain_status()
    domains_menu_logic(message, section=section, inline=inline)


# ======================================================================================================================


def proxies_menu_logic(message, inline: bool = False):
    bot_message(message, proxies_menu_markup(), inline)


def add_proxy_text_logic(message, inline: bool = False):
    bot_message(message, add_proxy_text_markup(), inline)
    bot.register_next_step_handler(message, add_proxy)


def add_proxy(message, inline: bool = False):
    proxy_list = message.text.split('\n')
    proxy = Proxy()
    proxy.add_proxy(proxy=proxy_list)
    bot_message(message, add_proxy_markup(), inline)
    bot_message(message, start_menu_markup(), inline)


def delete_proxy_logic(message, proxy_name: str, inline: bool = False):
    proxy = Proxy()
    proxy.delete_proxy(proxy=proxy_name)
    proxies_menu_logic(message, inline)
