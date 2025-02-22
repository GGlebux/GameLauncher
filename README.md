# Idea
Наш проект представляет лаунчер миниигр.

Пользователь стартует с главного меню:
1) Запуск желаемой игры
2) Настройки (программы и игровых процессов) 
3) Пользовательская учетная(для сохранения и отслеживания рекордов в каждой из мини игр через sqlite)

Из миниигр планируется: 
1) Стандартный тетрис
2) Гоночная игра (автомобиль)
3) Висельник (в стиле хоррор)
4) Другие

Пока точного списка игр нету.
Идея удобна тем, что каждый из нас может отдельно создать миниигру, потом просто интегрировать ее в лаунчер!


# Техническое задание (ТЗ) для проекта "Лаунчер миниигр"

## 1. Назначение проекта
Проект "Лаунчер миниигр" предназначен для создания удобной платформы, на которой пользователи смогут запускать различные миниигры. Основные цели:
- Обеспечить пользователям простой и интуитивно понятный интерфейс для доступа к играм.
- Позволить пользователям сохранять свои достижения и отслеживать рекорды в каждой миниигре.
- Обеспечить возможность разработчикам легко интегрировать новые миниигры в лаунчер.

## 2. Пользовательские группы
- **Игроки**: пользователи, которые хотят развлекаться, играя в миниигры.
- **Разработчики**: лица, создающие и интегрирующие новые миниигры в лаунчер.
- **Администраторы**: лица, ответственные за управление и обновление лаунчера и миниигр.

## 3. Обзор содержания
### Функции лаунчера:
1. **Главное меню**:
   - Запуск желаемой игры.
   - Доступ к настройкам программы и игровых процессов.
   - Управление пользовательской учетной записью для сохранения и отслеживания рекордов.
   
2. **Миниигры**:
   - Стандартный тетрис.
   - Гоночная игра (автомобиль).
   - Висельник (в стиле хоррор).
   - Возможность добавления других миниигр.

### Сценарии использования:
- Пользователь запускает лаунчер и видит главное меню.
- Пользователь выбирает игру из списка доступных миниигр и запускает её.
- Пользователь настраивает параметры игры через меню настроек.
- Пользователь создает учетную запись или входит в существующую для сохранения рекордов.

## 4. Взаимодействие с другими компонентами
- Интеграция с базой данных SQLite для хранения пользовательских данных и рекордов.
- Возможная интеграция с внешними API для получения дополнительных данных (например, рейтингов).

## 5. Обзор интерфейса
- Главное меню должно быть простым и интуитивно понятным, с четкой навигацией между пунктами.
- Дизайн должен соответствовать современным стандартам UX/UI (надеемся).
- Все миниигры должны иметь похожий по тематике интерфейс.

## 6. Безопасность
- Реализация системы аутентификации пользователей для защиты учетных записей.
- Использование шифрования для хранения паролей и личных данных пользователей.
- Внедрение механизмов защиты от SQL-инъекций при работе с базой данных.

## 7. Разработка
- Язык разработки: Python.
- Использование фреймворков: pyGame.

## 8. Системное окружение

  - Операционная система: Windows.
  - Минимальные требования: 2 ГБ ОЗУ, 1 ядро CPU, 500 МБ свободного места на диске.

---
