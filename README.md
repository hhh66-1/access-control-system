# Система управления доступом "Стражник"

## Описание
Система "Стражник" предназначена для контроля доступа пользователей к данным учащихся и работников образовательной организации. Система обеспечивает безопасное хранение и обработку персональных данных с использованием многоуровневой системы авторизации.

## Роли пользователей

### 👤 Администратор доступа
- Управление доступом пользователей
- Добавление новых сотрудников
- Управление данными пользователей

### 🛡️ Сотрудник службы безопасности
- Оформление заявок на пропуск
- Управление гостевым доступом
- Контроль посещений

## Тестовые учетные данные

### 👤 Администратор доступа
- Логин: `guardianskk`
- Пароль: `Admin@123`
- Секретное слово: `key1`

### 🛡️ Сотрудник службы безопасности
- Логин: `defendservice`
- Пароль: `Secure@456`
- Секретное слово: `key2`

## Функциональность

### 1. Авторизация пользователей
- Двухуровневая система ролей
- Трехуровневая аутентификация (логин, пароль, секретное слово)
- Требования к паролю:
  - Минимум 8 символов
  - Верхний и нижний регистр
  - Специальные символы
  - Цифры
  - Хранение в зашифрованном виде
- Отображение ФИО авторизованного пользователя

### 2. Панель администратора
- Управление данными пользователей:
  - ФИО
  - Пол
  - Должность
  - Фотография (требования):
    - Соотношение сторон 3x4
    - Вертикальная ориентация
    - Максимальный размер 2 МБ
    - Форматы: JPG или PNG
- Автоматическое сохранение данных
- Очистка формы после сохранения
- Система уведомлений

### 3. Заявка на пропуск
#### Индивидуальное посещение
- Информация для пропуска:
  - Срок действия (1-15 дней)
  - Подразделение
  - ФИО принимающего сотрудника
- Данные посетителя:
  - ФИО (обязательно)
  - Телефон (маска: +7 (###) ###-##-##)
  - Email (с валидацией)
  - Организация
  - Примечание
  - Дата рождения (от 14 лет)
  - Паспортные данные
  - Фотография (опционально)
- Документы:
  - Скан паспорта (JPG)

#### Групповое посещение
- Аналогичные поля с отличиями:
  - Возраст от 16 лет
  - Упрощенная форма

### 4. Эмулятор посещения
- Случайный выбор из реестра
- Моделирование прихода/ухода
- Валидация данных гостей
- Реалтайм-логирование
- Сохранение истории
- Управление через интерфейс

## Структура проекта
- `main.py` - основной файл приложения
- `auth.py` - модуль авторизации
- `admin_panel.py` - панель администратора
- `guest_request.py` - форма запроса гостевого доступа
- `emulator.py` - эмулятор системы
- `data/` - директория с данными:
  - `users.json` - база сотрудников
  - `requests.json` - заявки на пропуск
  - `log.json` - журнал посещений

## Требования
- Python 3.x
- PyQt5

## Установка
1. Убедитесь, что у вас установлен Python 3.x
2. Установите необходимые зависимости:
```bash
pip install PyQt5
```

## Запуск
Для запуска приложения выполните:
```bash
python main.py
```

## Разработка
Проект разработан с использованием:
- PyQt5 для создания графического интерфейса
- Модульной архитектуры для удобства поддержки
- JSON для хранения данных
- Системы валидации данных
- Многоуровневой системы безопасности 