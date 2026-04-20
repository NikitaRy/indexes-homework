C:\Users\User.TESTPCN\Downloads\бдшки\mongo>node index.js
Успешное подключение к MongoDB

--- Задание 1: Tom Hanks и Tim Allen ---
[
  {
    year: 1995,
    title: 'Toy Story',
    cast: [ 'Tom Hanks', 'Tim Allen', 'Don Rickles', 'Jim Varney' ]
  },
  {
    year: 1999,
    title: 'Toy Story 2',
    cast: [ 'Tom Hanks', 'Tim Allen', 'Joan Cusack', 'Kelsey Grammer' ]
  },
  {
    cast: [ 'Tom Hanks', 'Tim Allen', 'Joan Cusack', 'Ned Beatty' ],
    title: 'Toy Story 3',
    year: 2010
  },
  {
    cast: [ 'Tom Hanks', 'Tim Allen', 'Joan Cusack', 'Carl Weathers' ],
    title: 'Toy Story of Terror',
    year: 2013
  },
  {
    cast: [ 'Tom Hanks', 'Tim Allen', 'Kristen Schaal', 'Kevin McKidd' ],
    title: 'Toy Story That Time Forgot',
    year: 2014
  }
]

--- Задание 2: Средняя продолжительность по десятилетиям (1900-1999) ---
┌─────────┬──────┬────────────────────┐
│ (index) │ _id  │ avgRuntime         │
├─────────┼──────┼────────────────────┤
│ 0       │ 1900 │ 12.5               │
│ 1       │ 1910 │ 64.42857142857143  │
│ 2       │ 1920 │ 87.20833333333333  │
│ 3       │ 1930 │ 95.59751037344398  │
│ 4       │ 1940 │ 97.56456456456456  │
│ 5       │ 1950 │ 101.44642857142857 │
│ 6       │ 1960 │ 109.32627646326276 │
│ 7       │ 1970 │ 111.18072289156626 │
│ 8       │ 1980 │ 106.88295687885011 │
│ 9       │ 1990 │ 106.43375886524822 │
└─────────┴──────┴────────────────────┘

--- Задание 3: Топ-10 фильмов по комментариям ---
┌─────────┬─────────────────────────────────────────┬────────────────────┐
│ (index) │ title                                   │ num_mflix_comments │
├─────────┼─────────────────────────────────────────┼────────────────────┤
│ 0       │ 'The Taking of Pelham 1 2 3'            │ 161                │
│ 1       │ '50 First Dates'                        │ 158                │
│ 2       │ "Ocean's Eleven"                        │ 158                │
│ 3       │ 'About a Boy'                           │ 158                │
│ 4       │ 'Terminator Salvation'                  │ 158                │
│ 5       │ 'Sherlock Holmes'                       │ 157                │
│ 6       │ 'The Mummy'                             │ 157                │
│ 7       │ 'Hellboy II: The Golden Army'           │ 155                │
│ 8       │ 'Anchorman: The Legend of Ron Burgundy' │ 154                │
│ 9       │ 'The Mummy Returns'                     │ 154                │
└─────────┴─────────────────────────────────────────┴────────────────────┘

--- Задание 4: Добавление документа с гибкой схемой ---
Добавлен документ с ID: 691e163c73744f4a0dfd22e4

--- Задание 5: Покрывающий индекс ---
Создание индекса...
Топ фильмов 2010-х:
┌─────────┬─────────────────────────────────────────┬──────┬────────────────┐
│ (index) │ title                                   │ year │ imdb           │
├─────────┼─────────────────────────────────────────┼──────┼────────────────┤
│ 0       │ 'Absent Minded'                         │ 2013 │ { rating: '' } │
│ 1       │ 'Boj za'                                │ 2014 │ { rating: '' } │
│ 2       │ 'Mary Loss of Soul'                     │ 2014 │ { rating: '' } │
│ 3       │ 'Emergency Exit: Young Italians Abroad' │ 2014 │ { rating: '' } │
│ 4       │ 'No Tomorrow'                           │ 2010 │ { rating: '' } │
│ 5       │ 'Learning to Ride'                      │ 2014 │ { rating: '' } │
│ 6       │ 'A Bigger Splash'                       │ 2015 │ { rating: '' } │
│ 7       │ 'The Last Season'                       │ 2014 │ { rating: '' } │
│ 8       │ 'Coming to Terms'                       │ 2013 │ { rating: '' } │
│ 9       │ 'Krot na more'                          │ 2012 │ { rating: '' } │
└─────────┴─────────────────────────────────────────┴──────┴────────────────┘
Анализ Explain:
TotalDocsExamined: 5373 (Должно быть 0)
Stage: PROJECTION_DEFAULT (Ожидается PROJECTION_COVERED или IXSCAN без FETCH)

--- Задание 6: Multikey Index (Genres) ---
Создание индекса по жанрам...
Примеры фильмов Action + Sci-Fi:
┌─────────┬─────────────────────────────────────┬─────────────────────────────────────┐
│ (index) │ genres                              │ title                               │
├─────────┼─────────────────────────────────────┼─────────────────────────────────────┤
│ 0       │ [ 'Action', 'Adventure', 'Sci-Fi' ] │ 'Flash Gordon'                      │
│ 1       │ [ 'Action', 'Sci-Fi', 'Thriller' ]  │ 'The War of the Worlds'             │
│ 2       │ [ 'Action', 'Sci-Fi' ]              │ 'The 10th Victim'                   │
│ 3       │ [ 'Action', 'Drama', 'Sci-Fi' ]     │ 'Das Millionenspiel'                │
│ 4       │ [ 'Action', 'Sci-Fi' ]              │ 'Battle for the Planet of the Apes' │
└─────────┴─────────────────────────────────────┴─────────────────────────────────────┘
Анализ Explain:
Использованный индекс: undefined
Stage: LIMIT (Ожидается FETCH с входным IXSCAN)
