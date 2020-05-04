import requests
from browser.send_movie import SendMovie
from config import API_TOKEN


class FinderId(object):
    """
    Выполняет поиск по id в базе
    """

    def __init__(self, id_kp, send):
        self.id_kp = id_kp
        self.send = send

    def get_movie(self):
        """
        :return: Возвращает данные о фильме по id кинопоиска
        """

        if self.id_kp.isdecimal():
            # запрос к базе фильмов
            url = f'https://api.kinopoisk.cloud/movies/{self.id_kp}/token/{API_TOKEN}'
            re = requests.get(url)
            if re.status_code != 200:
                url = f'https://api.kinopoisk.cloud/tv-series/{self.id_kp}/token/{API_TOKEN}'
                re = requests.get(url)
                if re.status_code != 200:
                    return "Это чо еще такое а? Id пришли"
            re = re.json()
            info = f'Фильм который вы искали: {re["title"]} \r\nОписание: {re["description"]} ' \
                   f'\r\nТрейлер: {re["trailer"]} \r\nПостер: {re["poster"]}'
            if self.send:
                return SendMovie(re, None).run_sender()
            else:
                return re
        else:
            return "Это чо еще такое а? Id пришли"


class FinderPage(object):
    """
    Выполняет поиск по плагинации
    """

    def __init__(self, page, index):
        self.page = page
        self.index = index

    def get_list_movie(self):
        """
        Возвращает фильм в соответствии с индексом page
        """
        if self.page:
            url = f'https://api.kinopoisk.cloud/movies/all/page/{self.page}/token/{API_TOKEN}'
            re = requests.get(url)
            re = re.json()["movies"]
            movie_list = []
            for movie in re:
                movie_list.append(movie["title"])
            return movie_list
        else:
            return "Это чо еще такое а?"