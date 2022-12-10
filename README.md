# **api_yamdb**

**YaMDb** ***спроектирован при совместном взаимодействии***

[***Орлов Сергей***](https://github.com/sergio7523)

[***Воробьёв Илья***](https://github.com/iliya12321)

[***Чендева Анна***](https://github.com/Owlachno)

___ 

### *Технологии*
- Python 3.7
- Django 2.2.19
- DjangoRestFramework 3.12.4
- SQLite
- Pytest

___

## *Описание проекта*

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором.

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка.

Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

## *Пользовательские роли*

**Аноним** — может просматривать описания произведений, читать отзывы и комментарии.

**Аутентифицированный пользователь (user)** — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.

**Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.

**Администратор (admin)** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

**Суперюзер Django** должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

## *Самостоятельная регистрация новых пользователей*
- Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт /api/v1/auth/signup/.
- Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
- В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом.
- После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт /api/v1/users/me/ и заполнить поля в своём профайле (описание полей — в документации).

## *Создание пользователя администратором*
- Пользователя может создать администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт api/v1/users/ (описание полей запроса для этого случая — в документации).
- В этот момент письмо с кодом подтверждения пользователю отправлять не нужно.
- После этого пользователь должен самостоятельно отправить свой email и username на эндпоинт /api/v1/auth/signup/ , в ответ ему должно прийти письмо с кодом подтверждения.
- Далее пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен), как и при самостоятельной регистрации.

## *Запуск проекта в dev-режиме*

+ *Клонируем репозиторий*
```
git clone git@github.com:Owlachno/api_yamdb.git
```
+ *Переходим в репозиторий*
```
cd api_yamdb
```
+ *Создаём виртуальное окружение*
```
python -m venv venv
```
+ *Активируем виртуально окружение*
```
source venv/Script/activate
```
+ *Обновляем pip*
```
python -m pip install --upgrade pip
```
+ *Установка зависимостей*
```
pip install -r requirements.txt
```
+ *Выполняем миграции*
```
python manage.py migrate
```
+ Запустить проект:
```
python3 manage.py runserver
```
*На маке и линуксе вместо команды "python" использовать "python3"*

___
после запуска проекта, по адресу http://127.0.0.1:8000/redoc/ будет доступна документация для API Yatube.В ней описаны возможные запросы к API и структура ожидаемых ответов. Для каждого запроса указаны уровни прав доступа: пользовательские роли, которым разрешён запрос.

___

+ заполнить  тестовые данные:
```
python manage.py importcsv
```
___
***Вид на количество проделанной работы***

![красивая фотография](https://million-wallpapers.ru/wallpapers/6/7/492940876511675/zhivopisnyj-pejzazh-krasivaya-priroda.jpg)
