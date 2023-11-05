# SMART МОНИТОРИНГ БАЗЫ ДАННЫХ POSTGRESQL ЧЕРЕЗ БОТА В TELEGRAM

## Ссылки
* [Ссылки на бота](https://t.me/smart_monitoring_fsp_bot)

## 🖥️ Команда

| Имя             | Фамилия       |
|------------------|--------------|
| Айсен           | Слепцов      |
| Эрхан            | Семенов      |
| Алексей         | Алексей      |
| Максим         | Харитонов    |
| Айтал           | Попов        |


# **Документация к Telegram-боту для работы с базой данных**

## **Введение**

Данный Telegram-бот представляет собой инструмент для взаимодействия с базой данных PostgreSQL. Он обеспечивает авторизацию пользователей, управление базой данных и предоставляет различные функциональности для работы с данными.

## **Основные функции**

### **1. Авторизация**

Бот позволяет пользователям авторизоваться, требуя ввода логина и пароля. После успешной авторизации пользователь получает доступ к функционалу бота.

### Процесс авторизации

1. Пользователь вводит логин.
2. Пользователь вводит пароль.
3. Если логин и пароль верные, пользователь авторизован. В противном случае выводится сообщение об ошибке.

### **2. Основное меню**

После авторизации пользователь имеет доступ к основному меню бота, где он может выбирать различные опции:

- **Создание резервной копии данных:** Бот позволяет создавать резервные копии данных в различных форматах.
- **Экспорт схемы базы данных:** Пользователь может экспортировать схему базы данных в отдельный файл.
- **Сохранение данных:** Бот позволяет сохранить данные в базе данных.
- **Поддержка различных форматов:** Пользователь может выбирать формат для сохранения данных.
- **Восстановление данных:** Бот поддерживает восстановление данных из резервных копий.

### **3. Метрики и журналы**

Бот предоставляет информацию о производительности базы данных, включая:

- **Продолжительность самой долгой транзакции**
- **Количество активных сессий**
- **Загруженность процессора**
- **Объем свободного места на диске**

Бот также ведет журнал проверок связи с базой данных, отображая успешные и неудачные попытки.

## **Как использовать**

1. **Авторизация:**
    - Пользователь вводит команду **`/start`**, бот запрашивает логин и пароль.
    - После успешной авторизации пользователь получает доступ к основному меню.
2. **Основное меню:**
    - Пользователь выбирает опцию из основного меню, взаимодействуя с кнопками.
    - Бот выполняет выбранное действие и возвращает результат пользователю.
3. **Метрики и журналы:**
    - Пользователь выбирает опцию "Метрика" из меню базы данных.
    - Бот выводит текущие метрики производительности и журналы проверок связи с базой данных.
4. **Выход:**
    - Пользователь вводит команду **`/exit`** или выбирает "Выйти из системы" из меню.
    - Пользователь выходит из системы и закрывает соединение с базой данных.

## **Помощь и поддержка**

Если у вас возникли вопросы или проблемы при использовании бота, обратитесь к администратору для получения поддержки.

---

## Устновка

```
pip install -r requirements.txt
```

```
py main.py
```
