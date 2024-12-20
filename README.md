# libraryConsoleApp
 Консольное приложение для управления библиотекой книг.
 
 Написано с помощью: Python 3.12

## Описание функционала:
С помощью программы библиотекарь может управлять базой книг.
А именно:
- ### Просматривать все книги, добавленные в библиотеку.
- ### Добавлять новые книги, вводя название, автора и год издания книги.
- ### Искать книги по названию, автору или году, или все вместе...
  В приложении реализована масштабная система поиска с помощью регулярных выражений. Есть возможность найти книги автора по годам, книги по частям названия, автора или года. Возможны самые разные варианты поиска.
- ### Удалять книги по их id
- ### Менять статус книги с "в наличии" на "выдана" и обратно


## Работа с приложением
Приложение представляет собой простую версию программы администратора библиотеки.
- ### Выбор языка приложения
  При запуске приложение предложит выбрать язык. После ввода RU или EN. Весь интерфейс будет на выбранном языке.
- ### Меню управления
  После выбора языка у вас откроется меню управления с описанием доступных функций. Здесь вы можете ввести команду, необходимую в данный момент.
  - /all - команда выводит в консоль все книги, которые на данный момент присутствуют в базе данных.
  - /add - команда добавления новой книги. При ее выборе запускается процесс опроса пользователя для получения всех необходимых данных для формирования новой записи в базе данных
  - /delete - команда, которая запускает процесс удаления. После нее программа запросит у пользователя id книги, которую он хочет удалить. Есть возможность массового удаления. Для этого пользователь должен ввести несколько id через запятую.
  - /search - команда, которая дает пользователю доступ к системе поиска в базе данных. Программа попросит пользователя ввести запрос, по которому начнется поиск. Правила формирования запроса очень просты. Для поиска по нескольким значениям, например перечисление нескольких авторов или перечисление авторов и книг, не связанных с указанными авторами, необходимо элементы отделять друг от друга точкой с запятой. Например: Толстой;Пушкин;Властелин Колец. Для точного поиска, например всех книг автора определенного года, необходимо разделять элементы точного запроса символами &&&, а независимые элементы все также точкой с запятой. Например: Пушкин;Роулинг&&&1999;Роулинг&&&2003;Есенин;19
  - /change-status - команда смены статуса книги, приложение запросит id книги, статус которой нужно поменять, а после всех проверок - предложит ввести новый статус.
  - /exit - команда выхода из приложения
- ### Дополнительные функции
  Для данного проекта пришлось реализовать несколько дополнительных инструментов
  - pretty_tables - утилита для преобразования списка словарей, которые программа получает из базы данных в красивую таблицу в консоли. Работает по принципу заполнения матрицы, где каждое поле - это определнный символ в строке, которая в свою очередь находится в списке строк.
  - colouring - утилита для добавления цветов в текст, который выводится в консоль
 
