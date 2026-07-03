# -*- coding: utf-8 -*-
"""Translation content for all china-flag.cn language pages.

Edit this file, then run `python scripts/build.py` to regenerate the
/xx/index.html pages, /assets/<lang>/*.svg copies, sitemap.xml and the
root redirect page.
"""

LANGS = ["en", "zh", "de", "fr", "es", "it", "hi", "ar", "pt", "ja", "sv", "nl", "pl"]

LANG_META = {
    "en": {"native": "English", "html_lang": "en", "dir": "ltr", "og_locale": "en_US"},
    "zh": {"native": "中文", "html_lang": "zh-Hans", "dir": "ltr", "og_locale": "zh_CN"},
    "de": {"native": "Deutsch", "html_lang": "de", "dir": "ltr", "og_locale": "de_DE"},
    "fr": {"native": "Français", "html_lang": "fr", "dir": "ltr", "og_locale": "fr_FR"},
    "es": {"native": "Español", "html_lang": "es", "dir": "ltr", "og_locale": "es_ES"},
    "it": {"native": "Italiano", "html_lang": "it", "dir": "ltr", "og_locale": "it_IT"},
    "hi": {"native": "हिन्दी", "html_lang": "hi", "dir": "ltr", "og_locale": "hi_IN"},
    "ar": {"native": "العربية", "html_lang": "ar", "dir": "rtl", "og_locale": "ar_AR"},
    "pt": {"native": "Português", "html_lang": "pt", "dir": "ltr", "og_locale": "pt_PT"},
    "ja": {"native": "日本語", "html_lang": "ja", "dir": "ltr", "og_locale": "ja_JP"},
    "sv": {"native": "Svenska", "html_lang": "sv", "dir": "ltr", "og_locale": "sv_SE"},
    "nl": {"native": "Nederlands", "html_lang": "nl", "dir": "ltr", "og_locale": "nl_NL"},
    "pl": {"native": "Polski", "html_lang": "pl", "dir": "ltr", "og_locale": "pl_PL"},
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

from lang_en import DATA as _en
from lang_zh import DATA as _zh
from lang_de import DATA as _de
from lang_fr import DATA as _fr
from lang_es import DATA as _es
from lang_it import DATA as _it
from lang_hi import DATA as _hi
from lang_ar import DATA as _ar
from lang_pt import DATA as _pt
from lang_ja import DATA as _ja
from lang_sv import DATA as _sv
from lang_nl import DATA as _nl
from lang_pl import DATA as _pl

CONTENT = {
    "en": _en, "zh": _zh, "de": _de, "fr": _fr, "es": _es, "it": _it,
    "hi": _hi, "ar": _ar, "pt": _pt, "ja": _ja, "sv": _sv, "nl": _nl, "pl": _pl,
}
