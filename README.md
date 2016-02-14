# Коллективный блог
Этот репозиторий содержит исходный код коллективного блога, разрабатываемого в рамках проектной работы. Основная планируемая его функциональность следующая:

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

### Использеумые технологии
Django

### Протип
В папке Prototype размещен примерный планируемый интерфейс
