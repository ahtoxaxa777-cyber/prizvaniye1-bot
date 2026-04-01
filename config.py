"""
Конфигурация бота
ВАЖНО: Здесь хранятся все ключи и настройки
"""

import os

# ========== ТОКЕНЫ ==========
BOT_TOKEN = os.environ.get("BOT_TOKEN") or os.environ["API_TOKEN"]
YOKASSA_TOKEN = os.environ["YOKASSA_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])

# ========== ЦЕНА КУРСА (МОЖНО МЕНЯТЬ) ==========
COURSE_PRICE = 9900      # в рублях
DIAGNOSTIC_PRICE = 1490  # в рублях

# ========== ССЫЛКИ (МЕНЯЙ ЗДЕСЬ) ==========

# МОДУЛЬ 0 (лид-магнит, бесплатный)
NOTION_MODULE0 = "https://tame-headstand-52f.notion.site/0-30681644b85b809b8c5ce09eace5f114"

# МОДУЛИ 1-10 (платные)
NOTION_MODULE1 = "https://tame-headstand-52f.notion.site/1-32281644b85b802d9c1df872182ffd79?source=copy_link" # финальная
NOTION_MODULE2 = "https://tame-headstand-52f.notion.site/2-30981644b85b8041a494da6721a523f6?source=copy_link" # финальная
NOTION_MODULE3 = "https://tame-headstand-52f.notion.site/3-30981644b85b80ccb7afe698c6881e4e?source=copy_link" # финальная
NOTION_MODULE4 = "https://tame-headstand-52f.notion.site/4-32281644b85b80bc8401d7fb6e5090c6?source=copy_link" # финальная
NOTION_MODULE5 = "https://tame-headstand-52f.notion.site/5-32281644b85b80eda382debcd1619389?source=copy_link" # финальная
NOTION_MODULE6 = "https://tame-headstand-52f.notion.site/6-32281644b85b80658c87d4e79d37e155?source=copy_link" # финальная
NOTION_MODULE7 = "https://tame-headstand-52f.notion.site/7-MVP-32281644b85b80cfa17ce9dc65014ec3?source=copy_link" # финальная
NOTION_MODULE8 = "https://tame-headstand-52f.notion.site/8-32281644b85b80ad9d37d3d73c993cf9?source=copy_link" # финальная
NOTION_MODULE9 = "https://tame-headstand-52f.notion.site/9-32281644b85b806fbbd8cd8b9d9c5630?source=copy_link" # финальная
NOTION_MODULE10 = "https://tame-headstand-52f.notion.site/10-32281644b85b804e92c4d57b32ca4a95?source=copy_link" # финальная

# Комьюнити и поддержка
COMMUNITY_LINK = "https://t.me/+MNSHhaRMFk9iMjJi"  # Закрытая группа
SUPPORT_USERNAME = "@твой_ник"  # ВСТАВЬ свой username для поддержки

# ========== ТАЙМЕРЫ ТРИГГЕРОВ ==========
# Время в секундах (можно менять)

# ДЛЯ ПРОДАКШЕНА (реальные интервалы):
TRIGGER_1_DELAY = 3600      # 1 час = 3600 секунд
TRIGGER_2_DELAY = 18000     # 5 часов = 18000 секунд
TRIGGER_3_DELAY = 86400     # 24 часа = 86400 секунд
TRIGGER_4_DELAY = 259200    # 3 дня = 259200 секунд
TRIGGER_5_DELAY = 604800    # 7 дней = 604800 секунд

# Для тестирования раскомментируй (убери #):
# TRIGGER_1_DELAY = 60      # 1 минута
# TRIGGER_2_DELAY = 120     # 2 минуты
# TRIGGER_3_DELAY = 180     # 3 минуты
# TRIGGER_4_DELAY = 240     # 4 минуты
# TRIGGER_5_DELAY = 300     # 5 минут
