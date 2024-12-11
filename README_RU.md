🇺🇸 [English README](https://github.com/YourLov3r/TinyVerseBot/blob/master/README.md)

# TinyVerse Bot 🌌

Скрипт для автоматизации тапалки TinyVerse

## Требования

[![Python](https://img.shields.io/badge/python-%3E%3D3.10-3670A0?style=flat&logo=python&logoColor=ffdd54)](https://www.python.org/)

## Возможности

<table>
  <thead>
    <tr>
      <th>Функция</th>
      <th>Поддержка</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Супер-Мега-Крутое интро с капибарой</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Предстартовые проверки безопасности</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Сбор пыли</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Добавление звезд в галактику</td>
      <td><img src="https://img.shields.io/badge/Work_in_Progress-orange?style=flat-square"></td>
    </tr>
    <tr>
      <td>Применение бустов</td>
      <td><img src="https://img.shields.io/badge/Work_in_Progress-orange?style=flat-square"></td>
    </tr>
    <tr>
      <td>Скрипт в .exe</td>
      <td><img src="https://img.shields.io/badge/Work_in_Progress-orange?style=flat-square"></td>
    </tr>
    <tr>
      <td>Ночной режим</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Привязка прокси к сессии</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Привязка User-Agent к сессии</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Автообнаружение новых .session</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Асинхронная работа</td>
      <td>✅</td>
    </tr>
  </tbody>
</table>

## Почему мы лучше других публичных скриптов?

### ✨ Интро с капибарой (имба, киллер-фича)

![Интро с капибарой](https://github.com/YourLov3r/TinyVerseBot/blob/master/assets/Capybara_Intro.gif)

### 👥 Дружелюбное сообщество

Мы создали дружественное сообщество, где вы можете задавать вопросы и получать помощь.

### 🔗 Ясное использование реферальной системы

Если вы измените ref id на свой в настройках, то так оно и будет. Наш скрипт не препятствует этому, в отличие от некоторых публичных скриптов.

### 🚀 Регулярные обновления

Мы осуществляем регулярные обновления скрипта в зависимости от изменений в игре.

## [Настройки](https://github.com/YourLov3r/TinyVerseBot/blob/master/.env-example)

<table>
  <thead>
    <tr>
      <th>Настройка</th>
      <th>Описание</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>API_ID / API_HASH</td>
      <td>Учетные данные API для Telegram API</td>
    </tr>
    <tr>
      <td>PLAY_INTRO</td>
      <td>True/False воспроизведение интро при запуске скрипта (НЕ СМЕЙ ЭТО ВЫКЛЮЧАТЬ)</td>
    </tr>
    <tr>
      <td>INITIAL_START_DELAY_SECONDS</td>
      <td>Диапазон задержки в секундах для случайной задержки при запуске сессии</td>
    </tr>
    <tr>
      <td>ITERATION_SLEEP_MINUTES</td>
      <td>Как долго скрипт будет ждать перед началом следующей итерации скрипта (клейм, добавление звезд и т.д.)</td>
    </tr>
    <tr>
      <td>USE_REF</td>
      <td>True/False использование рефералки для запуска бота</td>
    </tr>
    <tr>
      <td>REF_ID</td>
      <td>Реферер ID</td>
    </tr>
    <tr>
      <td>SLEEP_AT_NIGHT</td>
      <td>True/False спать ночью</td>
    </tr>
    <tr>
      <td>NIGHT_START_HOURS</td>
      <td>Диапазон начальных часов ночи</td>
    </tr>
    <tr>
      <td>NIGHT_END_HOURS</td>
      <td>Диапазон конечных часов ночи</td>
    </tr>
    <tr>
      <td>ADDITIONAL_NIGHT_SLEEP_MINUTES</td>
      <td>Дополнительный диапазон минут для сна ночью</td>
    </tr>
    <tr>
      <td>CHECK_BOT_STATE</td>
      <td>True/False проверка состояния бота (остановлен ли он админами или нет)</td>
    </tr>
    <tr>
      <td>CLAIM_DUST</td>
      <td>True/False автоматический сбор пыли</td>
    </tr>
  </tbody>
</table>

## Как установить 📚

Прежде чем начать, убедитесь, что вы соблюдаете [требования](#требования). Это очень ВАЖНО, без этого вы не сможете запустить наш скрипт.

### Получение ключей API

1. Перейдите на my.telegram.org и войдите, используя свой номер телефона.
2. Выберите "API development tools" и заполните форму для регистрации нового приложения.
3. Запишите полученные API_ID и API_HASH после регистрации вашего приложения в файл .env.

Иногда при создании нового приложения может отображаться ошибка. До сих пор не ясно, что является причиной, но вы можете попробовать решения, описанные на [stackoverflow](https://stackoverflow.com/questions/68965496/my-telegram-org-sends-an-error-when-i-want-to-create-an-api-id-hash-in-api-devel).

### Ручная установка на Linux

```shell
git clone https://github.com/YourLov3r/TinyVerseBot.git
cd TinyVerseBot
python3 -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install --only main
cp .env-example .env
nano .env 
# Укажите ваши API_ID и API_HASH, остальное берётся по умолчанию
# Чтобы выйти из nano нажмите Ctrl + O (будет предложено сохранить, соглашайтесь) и затем Ctrl + X
```

### Ручная установка на Windows

```shell
git clone https://github.com/YourLov3r/TinyVerseBot.git
cd YinyVerseBot
python -m venv .venv
.venv\Scripts\activate
pip install poetry
poetry install --only main
copy .env-example .env
# Затем откройте .env в любом текстовом редакторе и укажите ваши API_ID и API_HASH, остальное берётся по умолчанию
```

### Запуск скрипта

![TinyVerse интро](https://github.com/YourLov3r/TinyVerseBot/blob/master/assets/TinyVerse_Intro.gif)

#### Используя start.bat

Вы можете запустить скрипт используя start.bat скрипт, просто запустите его.

#### Вручную

Перед запуском скрипта вам ВСЕГДА нужно активировать виртуальное окружение и проверять на обновления.

```shell
# Linux
source .venv\bin\activate
# Windows
.venv\Scripts\activate

# Linux/Windows
git pull
```

Для запуска скрипта используйте `python3 main.py` на Linux или `python main.py` на Windows.

Также вы можете использовать флаг `--action` или `-a` для быстрого запуска скрипта с указанным действием.

```shell
# Linux
python3 main.py --action [1/2]
# Windows
python main.py --action [1/2]

# Или

# Linux
python3 main.py -a [1/2]
# Windows
python main.py -a [1/2]
```

Где [1/2] это:

    1 - Создаёт сессию
    2 - Запускает бота

Например, если вы хотите создать сессию, вы можете выполнить эту команду:

```shell
# Linux
python3 main.py --action 1
# Windows
python main.py --action 1

# Или

# Linux
python3 main.py -a 1
# Windows
python main.py -a 1
```

## Контакты

Если у вас есть вопросы или предложения, не стесняйтесь обращаться к нам в комментариях.

[![Capybara Society](https://img.shields.io/badge/Capybara%20Society-Присоединиться-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/capybara_society_ru)