# -*- coding: utf-8 -*-
"""Translation content for all china-flag.cn language pages.

Edit the per-language files (lang_<code>.py), then run
`python scripts/build.py` to regenerate the /xx/index.html pages,
/assets/<lang>/*.svg copies, sitemap.xml and the root redirect page.
The build validates that every language defines exactly the same
keys as English and aborts otherwise.
"""

# The 30 most spoken languages of the world (web-practical written
# standards; unwritten Chinese varieties are covered by zh, colloquial
# Arabic varieties by ar). sv/nl were on the site before the top-30
# expansion and are kept. Order = rough order by total speakers.
LANGS = [
    "en", "zh", "hi", "es", "fr", "ar", "bn", "pt", "ru", "ur",
    "id", "de", "ja", "mr", "te", "tr", "ta", "vi", "ko", "fa",
    "it", "th", "tl", "pa", "sw", "ha", "gu", "sv", "nl", "pl",
]

# gfont: Google-Fonts family for the language's script (None = Inter
# covers it). Loaded per page by build.font_head().
LANG_META = {
    "en": {"native": "English", "html_lang": "en", "dir": "ltr", "og_locale": "en_US", "gfont": None},
    "zh": {"native": "中文", "html_lang": "zh-Hans", "dir": "ltr", "og_locale": "zh_CN", "gfont": "Noto Sans SC"},
    "hi": {"native": "हिन्दी", "html_lang": "hi", "dir": "ltr", "og_locale": "hi_IN", "gfont": "Noto Sans Devanagari"},
    "es": {"native": "Español", "html_lang": "es", "dir": "ltr", "og_locale": "es_ES", "gfont": None},
    "fr": {"native": "Français", "html_lang": "fr", "dir": "ltr", "og_locale": "fr_FR", "gfont": None},
    "ar": {"native": "العربية", "html_lang": "ar", "dir": "rtl", "og_locale": "ar_AR", "gfont": "Noto Sans Arabic"},
    "bn": {"native": "বাংলা", "html_lang": "bn", "dir": "ltr", "og_locale": "bn_BD", "gfont": "Noto Sans Bengali"},
    "pt": {"native": "Português", "html_lang": "pt", "dir": "ltr", "og_locale": "pt_PT", "gfont": None},
    "ru": {"native": "Русский", "html_lang": "ru", "dir": "ltr", "og_locale": "ru_RU", "gfont": None},
    "ur": {"native": "اردو", "html_lang": "ur", "dir": "rtl", "og_locale": "ur_PK", "gfont": "Noto Nastaliq Urdu"},
    "id": {"native": "Bahasa Indonesia", "html_lang": "id", "dir": "ltr", "og_locale": "id_ID", "gfont": None},
    "de": {"native": "Deutsch", "html_lang": "de", "dir": "ltr", "og_locale": "de_DE", "gfont": None},
    "ja": {"native": "日本語", "html_lang": "ja", "dir": "ltr", "og_locale": "ja_JP", "gfont": "Noto Sans JP"},
    "mr": {"native": "मराठी", "html_lang": "mr", "dir": "ltr", "og_locale": "mr_IN", "gfont": "Noto Sans Devanagari"},
    "te": {"native": "తెలుగు", "html_lang": "te", "dir": "ltr", "og_locale": "te_IN", "gfont": "Noto Sans Telugu"},
    "tr": {"native": "Türkçe", "html_lang": "tr", "dir": "ltr", "og_locale": "tr_TR", "gfont": None},
    "ta": {"native": "தமிழ்", "html_lang": "ta", "dir": "ltr", "og_locale": "ta_IN", "gfont": "Noto Sans Tamil"},
    "vi": {"native": "Tiếng Việt", "html_lang": "vi", "dir": "ltr", "og_locale": "vi_VN", "gfont": None},
    "ko": {"native": "한국어", "html_lang": "ko", "dir": "ltr", "og_locale": "ko_KR", "gfont": "Noto Sans KR"},
    "fa": {"native": "فارسی", "html_lang": "fa", "dir": "rtl", "og_locale": "fa_IR", "gfont": "Noto Sans Arabic"},
    "it": {"native": "Italiano", "html_lang": "it", "dir": "ltr", "og_locale": "it_IT", "gfont": None},
    "th": {"native": "ไทย", "html_lang": "th", "dir": "ltr", "og_locale": "th_TH", "gfont": "Noto Sans Thai"},
    "tl": {"native": "Filipino", "html_lang": "fil", "dir": "ltr", "og_locale": "fil_PH", "gfont": None},
    "pa": {"native": "ਪੰਜਾਬੀ", "html_lang": "pa", "dir": "ltr", "og_locale": "pa_IN", "gfont": "Noto Sans Gurmukhi"},
    "sw": {"native": "Kiswahili", "html_lang": "sw", "dir": "ltr", "og_locale": "sw_KE", "gfont": None},
    "ha": {"native": "Hausa", "html_lang": "ha", "dir": "ltr", "og_locale": "ha_NG", "gfont": None},
    "gu": {"native": "ગુજરાતી", "html_lang": "gu", "dir": "ltr", "og_locale": "gu_IN", "gfont": "Noto Sans Gujarati"},
    "sv": {"native": "Svenska", "html_lang": "sv", "dir": "ltr", "og_locale": "sv_SE", "gfont": None},
    "nl": {"native": "Nederlands", "html_lang": "nl", "dir": "ltr", "og_locale": "nl_NL", "gfont": None},
    "pl": {"native": "Polski", "html_lang": "pl", "dir": "ltr", "og_locale": "pl_PL", "gfont": None},
}

GALLERY_GROUPS = [
    ("objects", None),
    ("animals", None),
    ("landmarks", None),
]

GALLERY_ITEMS = {
    "box": {"base_file": "chinese-flag-shaped-shipping-box.svg", "group": "objects"},
    "car": {"base_file": "chinese-flag-shaped-car.svg", "group": "objects"},
    "phone": {"base_file": "chinese-flag-shaped-smartphone.svg", "group": "objects"},
    "chest": {"base_file": "chinese-flag-shaped-treasure-chest.svg", "group": "objects"},
    "teapot": {"base_file": "chinese-flag-shaped-teapot.svg", "group": "objects"},
    "teacup": {"base_file": "chinese-flag-shaped-tea-cup.svg", "group": "objects"},
    "umbrella": {"base_file": "chinese-flag-shaped-umbrella.svg", "group": "objects"},
    "fan": {"base_file": "chinese-flag-shaped-folding-fan.svg", "group": "objects"},
    "lantern": {"base_file": "chinese-flag-shaped-red-lantern.svg", "group": "objects"},
    "bicycle": {"base_file": "chinese-flag-shaped-bicycle.svg", "group": "objects"},
    "backpack": {"base_file": "chinese-flag-shaped-backpack.svg", "group": "objects"},
    "sneaker": {"base_file": "chinese-flag-shaped-sneaker.svg", "group": "objects"},

    "bird": {"base_file": "chinese-flag-shaped-bird.svg", "group": "animals"},
    "dragon": {"base_file": "chinese-flag-shaped-dragon.svg", "group": "animals"},
    "dog": {"base_file": "chinese-flag-shaped-dog.svg", "group": "animals"},
    "snake": {"base_file": "chinese-flag-shaped-snake.svg", "group": "animals"},
    "panda": {"base_file": "chinese-flag-shaped-panda.svg", "group": "animals"},
    "tiger": {"base_file": "chinese-flag-shaped-tiger.svg", "group": "animals"},
    "rabbit": {"base_file": "chinese-flag-shaped-rabbit.svg", "group": "animals"},
    "ox": {"base_file": "chinese-flag-shaped-ox.svg", "group": "animals"},
    "horse": {"base_file": "chinese-flag-shaped-horse.svg", "group": "animals"},
    "monkey": {"base_file": "chinese-flag-shaped-monkey.svg", "group": "animals"},
    "rooster": {"base_file": "chinese-flag-shaped-rooster.svg", "group": "animals"},
    "koi": {"base_file": "chinese-flag-shaped-koi-fish.svg", "group": "animals"},

    "map": {"base_file": "chinese-flag-shaped-china-map.svg", "group": "landmarks"},
    "greatwall": {"base_file": "chinese-flag-shaped-great-wall.svg", "group": "landmarks"},
    "forbiddencity": {"base_file": "chinese-flag-shaped-forbidden-city.svg", "group": "landmarks"},
    "templeofheaven": {"base_file": "chinese-flag-shaped-temple-of-heaven.svg", "group": "landmarks"},
    "terracotta": {"base_file": "chinese-flag-shaped-terracotta-warrior.svg", "group": "landmarks"},
    "pearltower": {"base_file": "chinese-flag-shaped-oriental-pearl-tower.svg", "group": "landmarks"},
    "potala": {"base_file": "chinese-flag-shaped-potala-palace.svg", "group": "landmarks"},
    "guilin": {"base_file": "chinese-flag-shaped-guilin-mountains.svg", "group": "landmarks"},
    "pagoda": {"base_file": "chinese-flag-shaped-big-wild-goose-pagoda.svg", "group": "landmarks"},
}

# Historical flags of China (own stylized illustrations).
HISTORICAL_ITEMS = {
    "qing": {"base_file": "historical-qing-dragon-flag.svg"},
    "fivecolor": {"base_file": "historical-five-colored-flag.svg"},
    "bluesky": {"base_file": "historical-blue-sky-white-sun-flag.svg"},
}

# Printable coloring page (outline of the flag).
COLORING_BASE_FILE = "chinese-flag-coloring-page.svg"

from lang_en import DATA as _en
from lang_zh import DATA as _zh
from lang_hi import DATA as _hi
from lang_es import DATA as _es
from lang_fr import DATA as _fr
from lang_ar import DATA as _ar
from lang_bn import DATA as _bn
from lang_pt import DATA as _pt
from lang_ru import DATA as _ru
from lang_ur import DATA as _ur
from lang_id import DATA as _id
from lang_de import DATA as _de
from lang_ja import DATA as _ja
from lang_mr import DATA as _mr
from lang_te import DATA as _te
from lang_tr import DATA as _tr
from lang_ta import DATA as _ta
from lang_vi import DATA as _vi
from lang_ko import DATA as _ko
from lang_fa import DATA as _fa
from lang_it import DATA as _it
from lang_th import DATA as _th
from lang_tl import DATA as _tl
from lang_pa import DATA as _pa
from lang_sw import DATA as _sw
from lang_ha import DATA as _ha
from lang_gu import DATA as _gu
from lang_sv import DATA as _sv
from lang_nl import DATA as _nl
from lang_pl import DATA as _pl

CONTENT = {
    "en": _en, "zh": _zh, "hi": _hi, "es": _es, "fr": _fr, "ar": _ar,
    "bn": _bn, "pt": _pt, "ru": _ru, "ur": _ur, "id": _id, "de": _de,
    "ja": _ja, "mr": _mr, "te": _te, "tr": _tr, "ta": _ta, "vi": _vi,
    "ko": _ko, "fa": _fa, "it": _it, "th": _th, "tl": _tl, "pa": _pa,
    "sw": _sw, "ha": _ha, "gu": _gu, "sv": _sv, "nl": _nl, "pl": _pl,
}
