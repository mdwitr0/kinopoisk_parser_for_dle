# Парсер из кинопоиска для DLE

Автоматический бот-парсер фильмов для сайтов на DLE из api kinopoisk.dev
Публикуйте прямо из телеграма фильмы на сайт!
Бот умеет искать фильмы по id кинопоиска и по названию фильма.
А также предлагает добавить свое описание для фильма или опубликовать фильм с тем отписанием, что на кинопоиске.

Для того чтобы скачать все зависимости необходимо в терминале написать `pip install -r requirements.txt`

Так же для работы постера нужен браузер Firefox или Chrome.
Firefox используется по умолчанию, но если у вас нет браузера Firefox то нужно сделать следующее:

1. Зайти в файл browser/send_movie.py
2. Закомментировать строку в самом верху **from selenium.webdriver.firefox.options import Options**
3. И **driver = webdriver.Firefox(firefox_options=options)**
4. Раскомментировать **from selenium.webdriver.chrome.options import Options**
5. И **driver = webdriver.Chrome(options=options)**

Могут быть ошибки связанные с версией браузера. Сейчас драйвера ориентированы на работу с _Firefox 75.0_ и _Chrome 81_.

## Конфигурация бота

**Для работы парсера необходимо заполнить файл _config.py_:**

API*TOKEN - это токен из [api кинопоиска](https://kinopoisk.dev/ "апи кинопоиска") получить его можно бесплатно.  
BOT_TOKEN - необходим токен вашего бота в телеграме. Создать бота можно в *@BotFather\_

**Для того чтобы постинг работал, необходимо указать данные для авторизации на сайте:**  
URL_DLE_SITES: http://site.online (без слеша в конце)  
DLE_LOGIN: логин пользователя с доступом к публикациям на сайте  
DLE_PASSWORD: пароль от этого аккаунта

## Запуск

Чтобы бот запустился нужно запустить файл **app.py** c помощью консоли python или IDE  
Либо в терминале `python app.py`

## Настройка сайта

Чтобы бот знал что ему заполнять, нужно немного настроить ваш сайт, добавив туда категории и дополнительные поля

**Категории которые проставляет парсер:**  
Так как бот работает по api кинопоиска, он умеет проставлять следующие категории:

| Категории       |
| --------------- |
| Документальный  |
| Драма           |
| Комедия         |
| Мультфильм      |
| Музыка          |
| Короткометражка |
| Фэнтези         |
| Детектив        |
| Мелодрама       |
| Триллер         |
| Семейный        |
| Биография       |
| Ужасы           |
| Криминал        |
| Боевик          |
| Фантастика      |
| Детский         |
| Спорт           |
| Приключения     |
| Аниме           |
| История         |
| Военный         |
| Вестерн         |
| Реальное ТВ     |
| Мюзикл          |
| Для взрослых    |
| Фильм-нуар      |
| Новости         |
| Концерт         |
| Игра            |
| Ток - шоу       |
| Церемония       |
| Фильмы          |
| Сериалы         |
| 2020 год        |
| 2019 год        |
| 2018 год        |
| 2017 год        |
| 2016 год        |
| 2015 год        |

**Дополнительные поля**  
Бот выполняет поиск по доп. полям и заполняет данные.
Доп. поля вашего сайта хранятся в файле engine/data/xfields.txt Если они не совпадают с теми, что ниже,
то стоит либо поменять их, либо переделать бота под ваши поля

Конфигурация полей находится в файле browser/send_movie.py и переменной mover_data

Нужно добавить в этот файл следующий текст:

```
name_foreign|Международное название||text||1|0|0|0|||0|0|||||||||
year|Год||text||1|1|0|0|||0|0||||||||||
slogan|Слоган||text||1|0|0|0|||0|0|||||||||
actors|Актеры||text||1|0|0|0|||0|0|||||||||
film_editor|Монтаж||text||1|0|0|0|||0|0|||||||||
painter|Художник||text||1|0|0|0|||0|0|||||||||
composer|Композитор||text||1|0|0|0|||0|0|||||||||
operator|Оператор||text||1|0|0|0|||0|0|||||||||
producer|Продюсер||text||1|0|0|0|||0|0|||||||||
director|Режисер||text||1|0|0|0|||0|0|||||||||
screenwriters|Сценаристы||text||1|0|0|0|||0|0|||||||||
studio|Киностудии||text||1|0|0|0|||0|0|||||||||
country|Страны||text||1|1|0|0|||0|0||||||||||
genre|Жанры||text||1|0|0|0|||0|0|||||||||
movie_type|Тип||text||1|0|0|0|||0|0|||||||||
age|Возрастная группа||text||1|0|0|0|||0|0|||||||||
poster|Постер||text||1|0|0|0|||0|0|||||||||
screen|Скриншоты||text||1|1|0|0|||0|0|||||||||
youtube_iframe|Трейлер||text||1|0|0|0|||0|0|||||||||
budget|Бюджет||text||1|0|0|0|||0|0|||||||||
kinopoisk_id|ID Кинопосика||text||1|0|0|0|||0|0|||||||||
imdb_id|ID IMDB||text||1|0|0|0|||0|0|||||||||
rating|Рейтинг Кинопоиск||text||1|0|0|0|||0|0|||||||||
rating_num|Голоса Кинопоиск||text||1|0|0|0|||0|0|||||||||
imdb|Рейтинг IMDB||text||1|0|0|0|||0|0|||||||||
imdb_num|Голоса IMDB||text||1|0|0|0|||0|0|||||||||
premiere_russia|Премьера в России||text||1|0|0|0|||0|0|||||||||
premiere_world|Премьера в мире||text||1|0|0|0|||0|0|||||||||
audience|Аудитория||text||1|0|0|0|||0|0|||||||||
fees_in_russia|Сборы в России||text||1|0|0|0|||0|0|||||||||
fees_in_world|Сборы в мире||text||1|0|0|0|||0|0|||||||||
```
