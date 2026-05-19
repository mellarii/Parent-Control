# ParentControl

Родительский контроль для Windows. Ограничение времени за компьютером и блокировка сайтов через Windows Firewall.

## Возможности

- **Таймер** — отсчёт времени сессии с настраиваемым лимитом
- **Блокировка сайтов** — добавление доменов в чёрный список, блокировка через `New-NetFirewallRule`
- **Статистика** — учёт времени на посещённых сайтах (Chrome, Firefox, Edge)
- **Темы** — Pink, White, Dark
- **Профили** — имена родителя и ребенка сохраняются в `QSettings`

## Требования

- Python 3.8+
- Windows (используется ctypes + PowerShell для фаервола)
- PyQt6

## Установка

```bash
pip install -r requirements.txt
```

## Запуск

```bash
python main.py
# или
python -m parent_control
```

## Сборка

```bash
pyinstaller ParentControl.spec
```

> Для блокировки сайтов требуются права администратора.
