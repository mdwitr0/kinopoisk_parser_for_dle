import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from config import URL_DLE_SITES, DLE_LOGIN, DLE_PASSWORD


def chose_genres(driver, genres):
    """
    Обрабатывает ошибки связанные с регистром категорий

    :param driver: драйвер selenium
    :param genres: список категорий из api
    :return:
    """
    for genre in genres:
        driver.find_element_by_xpath("//div[@id='category_chosen']/ul/li/input").click()
        try:
            driver.find_elements_by_xpath(f"//li[contains(text(), '{genre}')]")[0].click()
        except IndexError:
            driver.find_elements_by_xpath(f"//li[contains(text(), '{genre.capitalize()}')]")[0].click()


def check_exists_by_xpath(driver, xpath):
    """
    Проверяет наличие элемента на странице по xpath

    :param driver: драйвер selenium
    :param xpath: элемент по которому осуществляется проверка
    :return: Bool Вернет True если элемент найден на странице и False если нет
    """
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def enter_text(driver, xpath, value):
    """
    Функция выполняет роль синтаксического сахара и упрощает ввод текста на сайте

    :param driver: драйвер selenium
    :param xpath: путь к элементу
    :param value: значение которое необходимо ввести
    :return:
    """
    driver.find_element_by_xpath(xpath).send_keys(value)


def authorization(driver):
    """
    Проходит этап авторизации на сайте
    """
    enter_text(driver, "//input[@name='username']", DLE_LOGIN)
    enter_text(driver, "//input[@name='password']", DLE_PASSWORD)
    driver.find_element_by_xpath("//button/i").click()


class SendMovie(object):
    """
    Модуль SendMovie публикует выбранный фильм на сайте
    """

    def __init__(self, json, description):
        self.json = json
        self.description = description

    def run_sender(self):
        """
        Определяет webdriwer и проходит авторизацию на сайте
        """
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(firefox_options=options)
        driver.get(f'{URL_DLE_SITES}/admin.php')
        if check_exists_by_xpath(driver, "//input[@name='username']"):
            authorization(driver)
        self.add_news(driver)
        url = driver.find_element_by_xpath("//div[@class='text-center']/a[4]").get_attribute('href')
        driver.quit()
        return url

    def add_news(self, driver):
        """
        Заходит на страницу добавления новости и заполняет все доп поля
        :param driver: драйвер selenium
        :return:
        """
        driver.find_element_by_xpath("//a[contains(@href, '?mod=addnews&action=addnews')]").click()
        description = self.description if self.description else self.json["description"]

        # Массив в котором сопоставляются доп поля с данными из api
        mover_data = [
            ["//input[@id='title']", self.json["title"]],
            ["//textarea[@id='short_story']", description],
            ["//textarea[@id='full_story']", description],
            ["//input[@id='xf_name_foreign']", self.json["title_alternative"]],
            ["//input[@id='xf_slogan']", self.json["tagline"]],
            ["//input[@id='xf_actors']", self.json["actors"]],
            ["//input[@id='xf_director']", self.json["directors"]],
            ["//input[@id='xf_country-tokenfield']", self.json["countries"]],
            ["//input[@id='xf_genre']", self.json["genres"]],
            ["//input[@id='xf_movie_type']", self.type_movie()],
            ["//input[@id='xf_age']", self.json["age"]],
            ["//input[@id='xf_poster']", self.json["poster"]],
            ["//input[@id='xf_year-tokenfield']", self.json["year"]],
            ["//input[@id='xf_budget']", self.json["budget"]],
            ["//input[@id='xf_kinopoisk_id']", self.json["id_kinopoisk"]],
            ["//input[@id='xf_rating']", self.json["rating_kinopoisk"]],
            ["//input[@id='xf_rating_num']", self.json["kinopoisk_votes"]],
            ["//input[@id='xf_imdb']", self.json["rating_imdb"]],
            ["//input[@id='xf_imdb_num']", self.json["imdb_votes"]],
            ["//input[@id='xf_youtube_iframe']", self.json["trailer"]],
            ["//input[@id='xf_premiere_russia']", self.json["premiere_world"]],
            ["//input[@id='xf_premiere_world']", self.json["premiere_russia"]],
            ["//input[@id='xf_fees_in_russia']", self.json["fees_world"]],
            ["//input[@id='xf_film_editor']", self.json["editors"]],
            ["//input[@id='xf_painter']", self.json["painters"]],
            ["//input[@id='xf_composer']", self.json["composers"]],
            ["//input[@id='xf_operator']", self.json["operators"]],
            ["//input[@id='xf_producer']", self.json["producers"]],
            ["//input[@id='xf_screenwriters']", self.json["screenwriters"]],
            ["//input[@id='xf_fees_in_world']", self.json["fees_world"]],
        ]

        for data in mover_data:
            current_data = data[1]
            if current_data:
                if isinstance(current_data, float):
                    current_data = str(current_data)
                if isinstance(current_data, list):
                    current_data = ', '.join(current_data)
                enter_text(driver, data[0], current_data)

        genres = self.add_genres()
        chose_genres(driver, genres)
        driver.find_element_by_xpath("//button[@type='submit']").click()

    def type_movie(self):
        """
        Определяет конкретный тип картины
        :return: [фильм], [мультфильм], [сериал], [мультсериал]
        """
        type_movie = self.json["type"]
        genres = self.json["genres"]
        if type_movie == 'movie':
            type_movie = 'мультфильм' if 'мультфильм' in genres else 'фильм'
        else:
            type_movie = 'мультсериал' if 'мультфильм' in genres else 'сериал'
        return type_movie

    def add_genres(self):
        """
        Добавляет к категориям из API дополнительные категории
        :return: Обновленный список категорий
        """
        genre = self.json["genres"]
        type_movie = self.type_movie()
        if "Мультфильм" not in genre:
            if type_movie == "фильм":
                type_movie = "Фильмы"
            elif type_movie == "Cериал":
                type_movie = "Сериалы"
            else:
                type_movie = None
        else:
            type_movie = None
        year = self.json["year"]
        if year in range(2015, 2021):
            genre.append(f"{year} год")

        if type_movie:
            genre.append(type_movie)

        return genre
