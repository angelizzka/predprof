import requests
from bs4 import BeautifulSoup

import db

# список букв, которые часто заменяют на похожие
LETTERS = {
        "a":["@"],
        "b":["6"],
        "v":["в", "w"],
        "g":["9"],
        "u":["v", "w"],
        "i":["1", "l", "f"],
        "l":["1", "i", "t", "f"],
        "m":["n"],
        "n":["m"],
        "o":["0"],
        "0":["o"],
        "s":["c"],
        "t":["l"],
        "y":["u"],
        "f":["1", "l"],
    }

# страницы соцсетей, которые не проверяются на оригинальность
# (для уменьшения времени работы скрипта)
SOCIALS = [
    'vk',
    'ok',
    'instagram',
    'youtube',
    'facebook',
    'plus.google',
    'twitter',
    'zen.yandex',
    't.me',
]



def delete_tags(s, *args):
    for i in args:
        s = s.replace(i, '')
    return s


# парсинг сайта ЦБ и добавление всех банков, с неотозванной лицензией в БД
def update_bank_list():
    num = 0
    url = "https://www.cbr.ru/banking_sector/credit/FullCoList/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    f = soup.find('div', class_='table-wrapper table').find('tbody')
    for i in f:
        # bank = delete_tags(str(i), '<td>', '<tr>', '</td>', '</tr>', )
        bank = delete_tags(str(i), '<tr>', '</td>', '</tr>', '\n').split('<td>')
        if bank != ['']:
            num += 1
            info = bank[5]
            bank_id = info.split('id=')[1][:9]
            bank_name = info.split('>')[1][:-3]
            if 'ОТЗ' in bank:
                db.add_bank(bank_name, bank_id, False)
            else:
                db.add_bank(bank_name, bank_id, True)


# обновление БД новыми потенциально опасными адресами сайтов
# побочно создается таблица в БД с официальными сайтами
def update_fake_site_list():
    for i in db.select_banks_data():
        site_counter = 0
        fake_site_counter = 0
        bank_cb_active = list(i)[2]
        if bank_cb_active:
            bank_name = list(i)[0]
            bank_cb_id = list(i)[1]
            bank_url_cb = "https://www.cbr.ru/banking_sector/credit/coinfo/?id=" + str(bank_cb_id)
            r = requests.get(bank_url_cb)

            bank_soup = BeautifulSoup(r.text, 'html.parser')
            raw_data = bank_soup.findAll('a', class_='tab')
            temp_list = [] # for only unique sites
            for line in raw_data:
                flag = True
                link = delete_tags(line['href'], 'http://', 'https://', 'www.', '.ru', '.com', '.org', 'su')
                if link in temp_list: break
                else: temp_list.append(link)
                for social in SOCIALS: # check social network link
                    if social in link:
                        flag = False
                        break
                if flag:
                    db.add_site(bank_name + '_' + str(site_counter), link)
                    site_counter += 1
                    for letter in link:
                        if letter in LETTERS:
                            for symbol in LETTERS[letter]:
                                db.add_fake_site(bank_name + '_' + str(fake_site_counter), str(link).replace(letter, symbol))
                                fake_site_counter += 1


# проверка потенциально вредных адресов сайтов на работу
def check_fishing_sites():
    for i in db.select_fake_site_data():
        for domen in ['.ru',]: #  '.com', 'su'
            site = 'https://' + list(i)[1] + domen
            try:
                response = requests.get(site, timeout=0.5)
                print(f'Сайт "{site}" потенциально опасен')
            except:
                pass


# проверка работы официальных сайтов
def check_official_sites():
    for i in db.select_official_site_data():
        for domen in ['.ru',]: #  '.com', 'su'
            site = 'https://' + list(i)[1] + domen
            try:
                response = requests.get(site,)
            except:
                print(f'На сайт "{site}" нельзя перейти')


while 1:
    print(
        """Список комманд: '
        1) Обновить список банков
        2) Обновить список потенциально фишинговых сайтов
        3) Проверить наличие фишинговых сайтов
        4) Проверка официальных сайтов"""
        )
    command = input('Введите номер команды ')
    if command == '1':
        update_bank_list()
        print('Операция завершена')
        print('-'*30)
    elif command == '2':
        update_fake_site_list()
        print('Операция завершена')
        print('-'*30)
    elif command == '3':
        check_fishing_sites()
        print('Операция завершена')
        print('-'*30)
    elif command == '4':
        check_official_sites()
        print('Операция завершена')
        print('-'*30)
    else:
        print('Неверный ввод')