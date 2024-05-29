# Публикация комиксов
Данный скрипт скачивает случайные комиксы и их описание с сайта [xkcd](https://xkcd.com), и публикует в сообщество социальной сети [Вконтакте](https://vk.com)
### Что понадобится?
#### Предварительные требования
Скачайте или склонируйте репозиторий на свой компьютер.
Python3 должен быть уже установлен. 
#### Установка зависимостей
Используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
#### Доплнительные требования
Создать в социальной сети [Вконтакте](https://vk.com) сообщество и приложение. Получить access_token через процедуру [Implicit Flow](https://dev.vk.com/ru/api/access-token/implicit-flow-user?ref=old_portal)
#### Переменные окружения
Создайте файл ```.env``` в вашей директории проекта, откройте его в любом текстовом редакторе. Вам понадобятся следующие переменные окружения:
```
VK_TOKEN=Ваш access_token
GROUP_ID= ID вашего сообщества
```
### Как запустить?
Данный скрипт запускается командой:
```bush
python script.py
```
После запуска скачается картинка в директорию с кодом, опубликуется на стене в сообществе и удалиться из директории.
### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).