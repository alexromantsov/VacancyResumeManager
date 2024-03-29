# VacancyResumeManager

## Описание
VacancyResumeManager - это Python приложение для управления базами данных вакансий и резюме. Оно позволяет добавлять, просматривать, удалять и автоматически генерировать записи вакансий и резюме с использованием OpenAI GPT.

## Установка
Для работы приложения требуется Python 3.7 или выше. Также необходимо установить зависимости, указанные в `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Конфигурация
Перед использованием убедитесь, что вы указали свой API ключ OpenAI в main.py. Замените значение переменной API_KEY на свой личный ключ:
```
API_KEY = 'ваш ключ от OpenAI'
```

## Запуск

Для запуска приложения выполните:
```bash
python main.py
```

После запуска откроется консольное меню, где можно выбрать одно из доступных действий.

## Функции

* Просмотр всех вакансий и резюме.
* Добавление новых вакансий и резюме.
* Удаление вакансий и резюме по id.
* Автоматическая генерация вакансий и резюме с помощью GPT.