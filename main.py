# -*- coding: utf-8 -*-

import re
from multiprocessing import Pool
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from lxml import html

import dbcon


class MyParser(object):
    def __init__(self, *url):
            options = webdriver.ChromeOptions()
            # чтобы не открывалось окно браузера
            options.add_argument("--headless")
            self.driver = webdriver.Chrome(chrome_options=options, executable_path='C:\Program Files\chromedriver.exe')
            try:
                self.driver.set_page_load_timeout(30)
                self.driver.get(url[0])
            except TimeoutException as ex:
                print("\nСайт не отвечает.\n" + str(ex))
                self.driver.close()
                self.driver.quit()

    def service(self, start_date, end_date, level, region):
        # TODO - Сделать еще фильтров
        print("Выставление параметров     ", end='', flush=True)
        # Очищаем форму начальной даты и вставляем необходимые параметры
        # не стоит вводить дату ранее 2 сентября 2007 года (тогда был другой вид отчета)
        start_date_element = self.driver.find_element_by_id("start_date")
        start_date_element.clear()
        start_date_element.send_keys(start_date)
        end_date_element = self.driver.find_element_by_id("end_date")
        end_date_element.clear()
        end_date_element.send_keys(end_date)
        # Выбираем субъект РФ
        select_subject = Select(self.driver.find_element_by_name('actual_regions_subjcode'))
        select_subject.select_by_value(region)
        # Выбираем уровень выборов
        select_level = str("javascript:document.getElementById('urovproved').value={};").format(level)
        self.driver.execute_script(select_level)
        sleep(1)
        # Тут мы кликаем "Искать" по выставленным параметрам
        ok_element = self.driver.find_element_by_name("ok")
        ok_element.submit()
        print("OK")
        # "Протыкав" js элементы на выходе мы получаем нужный нам html
        return self.driver.page_source

    def service2(self):
        s = self.driver.page_source
        try:
            # Нажимаем кнопочку искать, чтобы вывести полный список кандидатов
            self.driver.execute_script("javascript:document.forms['search'].submit();")
            sleep(1)
            vib_url = self.driver.current_url
            vib_date = re.search(r'\d\d\.\d\d\.\d{4}', s).group()
            vib_name = self.driver.find_elements_by_class_name('w2')
            # Не используем переменную s так как html поменялся.
            tree = html.fromstring(self.driver.page_source)
            quantity = re.search(r'\s{8,}\d+', s).group()
            # Для нестандартного шаблона вывода списка кандидатов
            dif_pattern = re.search(r'отказе в регистрации,', s)
            iterator = int(quantity)
            cand_info = get_info(tree, dif_pattern)
            cand_info2 = Soup(self.driver.page_source).soup3()
            db = dbcon.DbAdmin()
            # Передаем нули в vib_type и vib_region т.к. установлен
            # триггер на insert, который потом вставит нужные данные из
            # временной таблицы. Сделано для избежания глобальных переменных.
            db.vibory_insert(vib_url, vib_date, vib_name[1].text, 0, 0)
            for i in range(iterator):
                db.candidates_insert(vib_url,
                                     cand_info2[i][0],
                                     cand_info2[i][1],
                                     cand_info.birth_date[i],
                                     cand_info.party[i],
                                     cand_info.vidvizh[i],
                                     cand_info.registr[i],
                                     cand_info.izbr[i])
            db.close()
            return print('OK')
        finally:
            self.driver.quit()


# Ищем в html данные кандидатов
def get_info(data, dif_pattern):
    class Candidate(object):
        def __init__(self, birth_date, party, vidvizh, registr, izbr):
            self.birth_date = birth_date
            self.party = party
            self.vidvizh = vidvizh
            self.registr = registr
            self.izbr = izbr
    # Парсим данные кандидата по xpath
    length = len(data.xpath('//*[@id="test"]/tr[1]/td'))
    birth_date = data.xpath('//*[@id="test"]/tr/td[3]/text()')
    party = data.xpath('//*[@id="test"]/tr/td[4]/text()')
    if dif_pattern is not None:
        # На парламентских выборах шаблон немного другой.
        vidvizh = data.xpath('//*[@id="test"]/tr/td[' + str(length - 4) + ']/text()')
        regisrt = data.xpath('//*[@id="test"]/tr/td[' + str(length - 3) + ']/text()')
        izbir = data.xpath('//*[@id="test"]/tr/td[' + str(length) + ']/text()')
    else:
        vidvizh = data.xpath('//*[@id="test"]/tr/td[' + str(length - 2) + ']/text()')
        regisrt = data.xpath('//*[@id="test"]/tr/td[' + str(length - 1) + ']/text()')
        izbir = data.xpath('//*[@id="test"]/tr/td[' + str(length) + ']/text()')
    candidate = Candidate(birth_date, party, vidvizh, regisrt, izbir)
    return candidate


# Первая функция, в которую задаем нужные нам параметры поиска
def begin():
    start_date = input('Укажите начальную дату (пример: 01.01.2018)\n ')
    end_date = input("Укажите конечную дату (пример: 31.12.2018)\n ")
    level = input('Укажите уровень выборов:\n '
                  '"1" - Федеральный,\n '
                  '"2" - Региональный,\n '
                  '"3" - Административный центр,\n '
                  '"4" - Местное самоуправление.\n '
                  )
    print("HINT: Узнать код региона: https://calcus.ru/kody-regionov")
    region = input("Укажите код региона РФ:\n ")
    db = dbcon.DbAdmin()
    db.temp_table(int(level), int(region))
    db.close()
    values = [start_date, end_date, level, region]
    return values


class Soup(object):
    def __init__(self, html):
        self.blank = BeautifulSoup(html, "html.parser")

    def soup1(self):
        # В этом цикле BS возвращает список ссылок найденых выборов. Это еще не те ссылки, что нам нужны.
        vib_name = []
        for tmp in self.blank.find_all('a'):
            link = tmp.get('href')
            # Отфильтровываем ненужные ссылки по длине
            if len(link) < 50:
                pass
            else:
                # Формируем словарь с выборами, по укзананным параметрам и ссылками к ним
                vib_name.append(link)
        return vib_name

    def soup2(self):
        raw_cand_info_links = []
        # Формируем список с ссылками, которые приведут к списку кандидатов
        for tmp in self.blank.find_all('a'):
            link = tmp.get('href')
            if '=220' in link or '=221' in link:
                raw_cand_info_links.append(link)
            else:
                # TODO - пока пропускаем другие ссылки (так как там другой формат (до 02.09.2007))
                pass
        return raw_cand_info_links

    def soup3(self):
        # Ищем ссылки на личные странички кандидатов
        cand_name_and_links = []
        for tmp in self.blank.find_all('a'):
            link = tmp.get('href')
            name = tmp.text
            if len(link) < 104:
                pass
            else:
                cand_name_and_links.append([link, name])
        return cand_name_and_links


def req():
    url = "http://www.vybory.izbirkom.ru/region/izbirkom"
    # REMINDER - первая функция в которую задаем параметры поиска
    params = begin()
    # Вставляем параметры поиска выборов в автоматизированный браузер (вернет html со списком выборов)
    target_page = MyParser(url).service(params[0], params[1], params[2], params[3])
    # Далее полученный html обрабатываем BS и получаем список ссылок с выборами
    link = Soup(target_page).soup1()
    link2 = []
    for i in range(len(link)):
        # Переходим по ссылкам из списка выборов
        response = requests.get(link[i])
        # Получаем список ссылок через, которые попадем на страницу со списком кандидатов
        link2_raw = Soup(response.text).soup2()
        link2.append(link2_raw[0])
    return link2


# Оборачиваем для p.map()
def req2(url):
    return MyParser(url).service2()


def req3():
    link = req()
    with Pool(5) as p:
        p.map(req2, link)


if __name__ == '__main__':
    req3()
