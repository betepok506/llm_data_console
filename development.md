# Установка

## Виртуальное окружение

Для создания виртуального окружения воспользуйтесь командой:
```
python -m venv venv
```

Далее активируйте его:
```
# Linux
source venv/Scripts/activate

venv/Scripts/activate
```

## Разработка с помощью .devcontainer

Нажмите `Ctrl + Shift + P`
И выберите `Dev containers: Rebuild and Reopen in Container`
После чего соберется Devcontainer

# Зависимости


# Линтер

Для линковки кода выполните команду `make lint`
Для этого используются `black`, `flake8`, `ruff`

# Форматирование кода

Для форматирования кода выполните команду `make fmt`

# Документирование