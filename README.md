﻿# Коллективный блог
Этот репозиторий содержит исходный код коллективного блога, разрабатываемого в рамках проектной работы. <br>
Автор: Поляков Павел, 146

### 1. Тема блога
Развлекательно-познавательный ресурс

### 2. Описание проекта
На сайте есть несколько блогов, в которых пишут пользователи. Можно просматривать и/или комментировать записи конкретного блога или пользователя, а также просматривать общую ленту на главной странице. Существует возможность подписки на пользователя или блог. На сайте имеется система рейтингов: можно положительно или отрицательно голосовать за посты и комментарии. Комментарии располагаются иерархично.

### 3. Функциональность
Основной набор возможностей следующий:
<ol>
<li>Можно регистрироваться, делать посты в блоги, комментировать записи</li>
<li>Есть система рейтингов, с которой можно взаимодействовать без перезагрузки страницы</li>
<li>Посты в ленте подгружаются без перезагрузки страницы в фоновом режиме</li>
<li>Комментарии отображаются иерархично, сортируются по рейтингу/дате</li>
<li>Система прав пользователей: кто-то может быть администратором блога и редактировать список участников, участники могут не иметь прав на просмотр определенного блога, если не состоят в нем или имеют рейтинг ниже значения, заданного администратором</li>
<li>Можно осуществлять поиск по тегам</li>
<li>Форматирование постов с использованием WYSIWYG-редактора</li>
<li>Приложение защищено от инъекций к базе, XSS-атак, регистрации ботов</li>
</ol>

### 4. Технические средства
Django 1.9 <br>
Данный список будет пополнятся/изменяться по мере необходимости

### 5. План работ
См. <a>http://hack.supply</a>

### 6. Прочее
В папке specs/design размещен макет примерного планируемого интерфейса <br>
Адрес в интернете: http://ppavel96.pythonanywhere.com/

