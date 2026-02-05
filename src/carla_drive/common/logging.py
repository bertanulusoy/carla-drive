get_logger(name: str)

from __future__ import annotations

"""
🎯 Bu dosyanın görevi:
- Projedeki herkes aynı şekilde "log" yazabilsin.
- Log = programın "ben şu anda şunu yapıyorum" diye not alması.
- Biz logları seviyelere ayıracağız:
DEBUG : Çok detay (genelde geliştirici için)
INFO : Normal bilgi
WARNING: Dikkat edilmesi gereken durum
ERROR : Hata oldu

✅ Kullanım (bu dosyada değil, başka dosyalarda):
from carla_drive.common.logging import get_logger
log = get_logger(__name__)
log.info("program_basladi", mode="dev")
"""

import logging
import os
from typing import Optional

import structlog

# Bu bayrak şunu anlatır:
# "Ayarları bir kere yaptıysak, tekrar tekrar yapmayalım."
_CONFIGURED = False


def _normalize_level(level: Optional[str]) -> int:
"""
🎯 Amaç:
LOG_LEVEL diye bir ayar olacak (mesela "debug" veya "INFO").
Ama insanlar farklı şekillerde yazabilir:
"debug", "DEBUG", " Debug " gibi...
Biz bunu temizleyip "standart" hale getireceğiz.

✅ Senin yapacağın:
1) level boşsa "INFO" kabul et.
2) strip() ile boşlukları sil, upper() ile büyük harf yap.
3) Bir sözlük (mapping) kur:
"DEBUG" -> logging.DEBUG
"INFO" -> logging.INFO
"WARNING" veya "WARN" -> logging.WARNING
"ERROR" -> logging.ERROR
"CRITICAL" veya "FATAL" -> logging.CRITICAL
4) Eğer tanımadığın bir kelime gelirse INFO'ya düş.

🧩 Fill in the blanks: Aşağıdaki ___ yerleri doldur lütfen.
"""
# 1) Default seç
raw = (level or ___).strip().upper()

# 2) Mapping tablosu
mapping = {
___: logging.DEBUG,
___: logging.INFO,
"WARNING": logging.WARNING,
"WARN": logging.WARNING,
___: logging.ERROR,
"CRITICAL": logging.CRITICAL,
"FATAL": logging.CRITICAL,
}

# 3) Bulamazsan INFO
return mapping.get(raw, ___)


def _configure_logging(level: Optional[str] = None) -> None:
"""
🎯 Amaç:
Log sistemini kurmak. Ama sadece 1 kere kuracağız.

✅ Neden 1 kere?
Çünkü aynı ayarları 10 kere yaparsan loglar karışabilir.

✅ Senin yapacağın (basit algoritma):
1) Eğer _CONFIGURED True ise return et.
2) LOG_LEVEL seç:
- level parametresi geldiyse onu kullan
- gelmediyse os.getenv("LOG_LEVEL", "INFO") kullan
3) _normalize_level ile sayıya çevir (logging level integer)
4) logging.basicConfig(...) ile stdlib logging'i kur:
- level = numeric_level
- format = "%(message)s"
5) structlog.configure(...) ile structlog'u kur:
- loglara zaman ve seviye ekle
- en sonda JSON gibi yazdır
6) _CONFIGURED = True yap

🧩 Fill in the blanks: Aşağıdaki ___ yerleri doldur lütfen.
"""
global _CONFIGURED

# 1) Daha önce kurulduysa tekrar kurma
if _CONFIGURED:
return

# 2) Level seçimi (parametre varsa onu kullan)
env_level = os.getenv(___, ___)
chosen_level = level if level is not None else env_level

# 3) Normalize et (string -> sayı)
numeric_level = _normalize_level(___)

# 4) Stdlib logging'i kur
logging.basicConfig(
level=___,
format=___,
)

# 5) structlog ayarı
structlog.configure(
wrapper_class=structlog.make_filtering_bound_logger(___),
cache_logger_on_first_use=True,
processors=[
# Zaman damgası (logun üstüne saat ekler)
structlog.processors.TimeStamper(fmt=___, utc=___),
# Seviye bilgisi (debug/info/warning gibi)
structlog.processors.add_log_level,
# Eğer hata (exception) olursa bunu loga ekler
structlog.processors.format_exc_info,
# En sonunda JSON olarak yazdır (makineler için okunabilir)
structlog.processors.JSONRenderer(),
],
)

# 6) Kurulum tamam
_CONFIGURED = True


def get_logger(name: str) -> structlog.BoundLogger:
"""
🎯 Amaç:
Bu fonksiyon çağrılınca, hazır bir logger döndürmek.

✅ Senin yapacağın:
1) _configure_logging() çağır (kurulu değilse kursun).
2) structlog.get_logger(name) ile logger al.
3) log.bind(app="carla-drive") ekle:
Böylece her logda "app" alanı gözüksün.

🧩 Fill in the blanks: Aşağıdaki ___ yerleri doldur lütfen.
"""
_configure_logging()

log = structlog.get_logger(___)
return log.bind(app=___)