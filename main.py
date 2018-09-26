# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import requests
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from time import sleep
import re
from multiprocessing import Pool
import dbcon


class MyParser(object):
    def __init__(self, *url):
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  # чтобы не открывалось окно браузера
            self.driver = webdriver.Chrome(chrome_options=options, executable_path='C:\Program Files\chromedriver.exe')
            try:
                self.driver.set_page_load_timeout(30)
                self.driver.get(url[0])
            except TimeoutException as ex:
                print("\nСайт не отвечает.\n" + str(ex))
                self.driver.close()
                self.driver.quit()


    def service(self, start_date, end_date, level, region):
        # TODO - Разбить на отдельные методы - метод service и сделать там try except.
        # TODO - Сделать еще фильтров,
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
        sleep(1)  # Можно закомментить, если инет шустрый и браузер не тупит.
        # Тут мы кликаем "Искать" по выставленным параметрам
        ok_element = self.driver.find_element_by_name("ok")
        ok_element.submit()
        print("OK")
        return self.driver.page_source

    def service2(self):
        try:
            s = self.driver.page_source
            # на 221 заканчиваются ссылки, где в форме поиска отсутствует возможность выбора "выдвижения"
            if '=221' in s:
                # TODO - тут не доделано
                result = re.findall(r'table-[1-2]', s)
                element = self.driver.find_element_by_id(result[0])
                print(element)
                db = dbcon.DbAdmin()
                db.set_func()
                db.start_func(1, '23.06.2005', reg_exp1(element)[0], 'sfd')
                db.close()
                return print('OK')
            elif '=220' in s:
                input_element = self.driver.find_element_by_id("csearch_vidvig")
                input_element.send_keys("в")
                input_element.submit()
                result1 = re.findall(r'table-[1-2]', s)
                element = self.driver.find_element_by_id(result1[0])
                db = dbcon.DbAdmin()
                db.set_func()
                db.start_func(2, '22.06.2005', reg_exp1(element)[0], 'sfddf')
                db.close()
                return print('OK')  # вызываем функцию поиска кандидатов
        finally:
            self.driver.quit()


# Ищем по шаблону в html кандидатов
def reg_exp1(data):
    # TODO - сейчас не парсит если кандидат без отчества
    pattern = r"\d+\s[А-Яа-я\-?]+\s[А-Яа-я]+\s[А-Яа-я?]+\s\d{2}\.\d{2}\.\d{4}.*"
    result2 = re.findall(pattern, data.text)
    return result2


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
    values = [start_date, end_date, level, region]
    return values


class Soup(object):
    def __init__(self, html):
        self.blank = BeautifulSoup(html, "html.parser")

    def soup1(self):
        # В этом цикле BS возвращает список найденых выборов и ссылок (Это еще не те ссылки, что нам нужны.
        # Хотя список найденых выборов нам уже будет нужен для конечного отчета.
        vib_name = []
        for link in self.blank.find_all('a'):
            tmp = link.get('href')
            tmp2 = link.get_text()
            if len(tmp) < 50:
                pass
            else:
                vib_name.append([tmp2, tmp])  # Формируем словарь с выборами, по укзананным параметрам и ссылками к ним
        return vib_name

    def soup2(self):
        vib_name = []
        for link in self.blank.find_all('a'):
            tmp = link.get('href')
            if '=220' in tmp or '=221' in tmp:
                vib_name.append(tmp)
            else:
                pass
        return vib_name


def req():
    url = "http://www.vybory.izbirkom.ru/region/izbirkom"
    params = begin()
    link = Soup(MyParser(url).service(params[0], params[1], params[2], params[3])).soup1()  # Этот кошмар надо упростить
    link2 = []
    for i in range(len(link)):  # Получаем ссылки через, которые попадем на страницу со списком кандидатов
        response = requests.get(link[i][1])
        link2_raw = Soup(response.text).soup2()
        link2.append(link2_raw[0])
    return link2


def req2(url):
    return MyParser(url).service2()


def req3():
    link = req()
    # for i in range(len(link)):
    with Pool(5) as p:
        p.map(req2, link)


if __name__ == '__main__':
    req3()
