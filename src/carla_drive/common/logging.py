from __future__ import annotations
<<<<<<< HEAD

"""
🎯 Bu dosyanın görevi:
- Projedeki herkes aynı şekilde "log" yazabilsin.
- Log = programın "ben şu anda şunu yapıyorum" diye not alması.
- Biz logları seviyelere ayıracağız:
DEBUG : Çok detay (genelde geliştirici için)
INFO : Normal bilgi
WARNING: Dikkat edilmesi gereken durum
ERROR : Hata oldugit commit -m "Save changes"
"""

=======
>>>>>>> c4222424834ff9b499186fdd471f8792c9edb752
import logging
import os
from typing import Optional

import structlog

"""
🎯 Bu dosyanin görevi:
- Projedeki herkes ayni şekilde "log" yazabilsin.
- Log = programin "ben şu anda şunu yapiyorum" diye not almasi.
- Biz loglari seviyelere ayiracağiz:
DEBUG : Çok detay (genelde geliştirici için)
INFO : Normal bilgi
WARNING: Dikkat edilmesi gereken durum
ERROR : Hata oldu
"""

# Bu bayrak şunu anlatır:
# "Ayarları bir kere yaptıysak, tekrar tekrar yapmayalım."
_CONFIGURED = False


def _normalize_level(level: Optional[str]) -> int:
<<<<<<< HEAD
"""
🎯 Amaç:
LOG_LEVEL diye bir ayar olacak (mesela "debug" veya "INFO").
Ama insanlar farklı şekillerde yazabilir:
"debug", "DEBUG", " Debug " gibi...
Biz bunu temizleyip "standart" hale getireceğiz.
"""
# 1) Default seç
raw = (level or feat).strip().upper()

# 2) Mapping tablosu
mapping = {
Fix: logging.DEBUG,
Chore: logging.INFO,
"WARNING": logging.WARNING,
"WARN": logging.WARNING,
docs: logging.ERROR,
"CRITICAL": logging.CRITICAL,
"FATAL": logging.CRITICAL,
}

# 3) Bulamazsan INFO
return mapping.get(raw, logging.INFO)
=======
    """
    🎯 Amaç:
    LOG_LEVEL diye bir ayar olacak (mesela "debug" veya "INFO").
    Ama insanlar farkli şekillerde yazabilir:
    "debug", "DEBUG", "Debug" gibi...
    Biz bunu temizleyip "standart" hale getireceğiz.
    """
    # 1) Default seç - eğer tanınmayan bir kelime gelirse de INFO'ya dönüştür.
    raw = (level or "INFO").strip().upper()  # dEbUg => "DEBUG"

    # 2) Mapping tablosu (Key-Value Pairs)
    mapping = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "WARN": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
        "FATAL": logging.CRITICAL,
    }

    # 3) Bulamazsan INFO
    return mapping.get(raw, 10)
>>>>>>> c4222424834ff9b499186fdd471f8792c9edb752


def _configure_logging(level: Optional[str] = None) -> None:
    """
    🎯 Amaç:
    Log sistemini kurmak. Ama sadece 1 kere kuracağiz.
    """
    global _CONFIGURED

    # 1) Daha önce kurulduysa tekrar kurma
    if _CONFIGURED:
        return

<<<<<<< HEAD
# 2) Level seçimi (parametre varsa onu kullan)
env_level = os.getenv("LOG_LEVEL", None)
chosen_level = level if level is not None else env_level

# 3) Normalize et (string -> sayı)
numeric_level = _normalize_level(chosen_level)

# 4) Stdlib logging'i kur
logging.basicConfig(
level=numeric_level,
format="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
)

# 5) structlog ayarı
structlog.configure(
wrapper_class=structlog.make_filtering_bound_logger(numeric_level),
cache_logger_on_first_use=True,
processors=[
# Zaman damgası (logun üstüne saat ekler)
structlog.processors.TimeStamper(fmt="iso", utc=True),
# Seviye bilgisi (debug/info/warning gibi)
structlog.processors.add_log_level,
# Eğer hata (exception) olursa bunu loga ekler
structlog.processors.format_exc_info,
# En sonunda JSON olarak yazdır (makineler için okunabilir)
structlog.processors.JSONRenderer(),
],
)
=======
    # 2) Level seçimi (parametre varsa onu kullan)
    env_level = os.getenv("LOG_LEVEL", "INFO")

    chosen_level = level if level is not None else env_level

    # 3) Normalize et (string -> sayı)
    numeric_level = _normalize_level(chosen_level)

    # 4) Stdlib logging'i kur
    logging.basicConfig(
        level=numeric_level,
        format="%(message)s",
    )
>>>>>>> c4222424834ff9b499186fdd471f8792c9edb752

    # 5) structlog ayarı
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(numeric_level),
        cache_logger_on_first_use=True,
        processors=[
            # Zaman damgası (logun üstüne saat ekler)
            structlog.processors.TimeStamper(fmt="iso", utc=True),
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
    Bu fonksiyon çağrilinca, hazir bir logger döndürmek.
    """
    _configure_logging()

<<<<<<< HEAD
log = structlog.get_logger(name)
return log.bind(app="carla-drive")
=======
    log = structlog.get_logger(name)
    return log.bind(app="carla-drive")
>>>>>>> c4222424834ff9b499186fdd471f8792c9edb752
