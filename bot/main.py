from config import ADMIN_ID_LIST

from setup import bot

from handlers.botlogic import *


# --------------- bot -------------------


@bot.message_handler(commands=['start'])
def start_menu(message):
    if message.chat.id not in ADMIN_ID_LIST:
        return ''
    start_menu_logic(message=message)


@bot.callback_query_handler(func=lambda call: True)
def callback_logic(call):
    if call.message.chat.id not in ADMIN_ID_LIST:
        return ''
    if call.data == 'list_of_all_domains_menu':
        all_domains_menu_logic(message=call.message, inline=True)
    if call.data == 'back_to_start_menu':
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        start_menu_logic(message=call.message, inline=True)
    elif call.data == 'domains_menu':
        domains_menu_logic(message=call.message, inline=True)
    elif call.data.startswith('domains_menu_previous_page_'):
        section = call.data.split('_')[-1]
        domains_menu_logic(message=call.message, section=section, inline=True)
    elif call.data.startswith('domains_menu_next_page_'):
        section = call.data.split('_')[-1]
        domains_menu_logic(message=call.message, section=section, inline=True)
    elif call.data.startswith("show_subdomains_"):
        bot.answer_callback_query(callback_query_id=call.id, text='Парсинг и проверка статус кодов...')
        domain_name = call.data.split('_')[-1]
        subdomains_menu_logic(message=call.message, domain_name=domain_name, inline=True)
    elif call.data.startswith("delete_domain_"):
        domain_name = call.data.split('_')[-1]
        delete_domain_logic(message=call.message, domain_name=domain_name, inline=True)
    elif call.data.startswith("change_status_"):
        domain_name = call.data.split('_')[-1]
        section = call.data.split('_')[-2]
        update_domain_status_logic(message=call.message, section=section, domain_name=domain_name, inline=True)
    elif call.data == 'add_domain':
        add_domain_text_logic(message=call.message, inline=True)
    elif call.data == 'proxies':
        proxies_menu_logic(message=call.message, inline=True)
    elif call.data == 'add_proxy':
        add_proxy_text_logic(message=call.message, inline=True)
    elif call.data.startswith("delete_proxy_"):
        proxy_name = call.data.split('_')[-1]
        delete_proxy_logic(message=call.message, proxy_name=proxy_name, inline=True)


# --------------- main name -------------------


if __name__ == '__main__':
    bot.infinity_polling()
