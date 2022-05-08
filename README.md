# agrosmart - умная ферма

Проект для автоматизированного управления фермой Raspberry Pi + Python (Flask) + Nextion

**sudo python3 server.py** - запуск демона обновления данных и веб-сервера

**sudo python3 display.py** - запуск демона взаимодействия с дисплеем

Обновление данных датчиков раз в 3 секунды (ограничение китайских датчиков с запасом). Фронтенд обновляется long-polling'ом. Дисплей работает на событийной модели обновления данных. Дисплей не будет работать без демона обновления данных!

#

Управление через браузер (видео)

[![Посмотрите видео](https://img.youtube.com/vi/YpPX43LzU2A/maxresdefault.jpg)](https://youtu.be/YpPX43LzU2A)

Управление через сенсорный экран (фото)

<img src="https://user-images.githubusercontent.com/37335292/167301134-e38a5b37-e3bd-49b6-b822-33b41144e856.jpg" width="330" height="250"> <img src="https://user-images.githubusercontent.com/37335292/167301154-a9baca4f-4e78-4d49-86e7-edba527eea8f.jpg" width="330" height="250"> <img src="https://user-images.githubusercontent.com/37335292/167301155-7a9e2263-c569-4a1a-ab6f-0ca68871521f.jpg" width="330" height="250">

*При первоначальной настройке нужно установить все зависимости, активировать аппаратный COM-порт и привести настройки путей и пинов в актуальное состояние*
