from __future__ import annotations

import logging
import os
from typing import Optional

import structlog

"""
🎯 Bu dosyanın görevi:
- Projedeki herkes aynı şekilde "log" yazabilsin.
- Log = programın "ben şu anda şunu yapıyorum" diye not alması.
- structlog ile okunabilir / düzenli log üretmek

Logları seviyeleri:
- DEBUG : Çok detaylı geliştirici için
- INFO : Normal bilgi mesajları
- WARNING: Dikkat edilmesi gereken durumlar
- ERROR : Hata durumları
- CRITICAL: Çok ciddi hata durumları
"""


# Bu bayrak şunu anlatır:
# "Ayarları bir kere yaptıysak, tekrar tekrar yapmayalım."
_CONFIGURED = False


def _normalize_level(level: Optional[str]) -> int:
    """
    🎯 Amaç:
    LOG_LEVEL gibi bir ayar geldiğinde bunu standart logging seviyesine çevirmek.

    Örnek:
    - "debug" -> logging.DEBUG
    - "INFO" -> logging.INFO
    - " warn " -> logging.WARNING

    Eğer bilinmeyen bir değer gelirse güvenli varsayılan olarak INFO kullanılır.
    """
    # None geldiyse INFO olarak kabul ediyoruz.
    raw = (level or "INFO").strip().upper()  # dEbUg => "DEBUG"

    # Mapping tablosu (Key-Value Pairs)
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
    return mapping.get(raw, logging.INFO)


def _configure_logging(level: Optional[str] = None) -> None:
    """
    🎯 Amaç:
    Logging sistemini sadece 1 kere kuracağız.

    Akış:
    1) Daha önce kurulduysa çık
    2) Seviye bilgisini parametreden veya env'den al
    3) Seviyeyi normalize et
    4) Python stdlib logging'i kur
    5) structlog yapılandırmasını kur
    6) Kuruldu işaretini ver
    """
    global _CONFIGURED

    # Daha önce kurulduysa tekrar kurma
    if _CONFIGURED:
        return

    # Öncelik:
    # 1) Fonksiyona verilen level
    # 2) Ortam değişkeni LOG_LEVEL
    # 3) Varsayılan INFO

    # Level seçimi (parametre varsa onu kullan)
    env_level = os.getenv("LOG_LEVEL", "INFO")
    chosen_level = level if level is not None else env_level

    # Normalize et (string seviye -> sayısal logging seviyesi)
    numeric_level = _normalize_level(chosen_level)

    # Python'un standart logging sistemi
    # structlog son çıktıyı üreteceği için burada sade format yeterli.
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
    )

    # structlog ayarı
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

    # Artık logging kuruldu
    _CONFIGURED = True


def get_logger(name: str) -> structlog.BoundLogger:
    """
    🎯 Amaç:
    Hazir bir logger döndürmek.

    Kullanım örneği:
        from carla_drive.common.logging import get_logger

        log = get_logger(__name__)
        log.info("app_started", mode="dev")

    Neden __name__ alıyoruz?
    - Log'un hangi modülden geldiğini anlayabilmek için.
    - Genelde __name__ verilir.
    """
    _configure_logging()

    log = structlog.get_logger(name)

    # app alanını sabit bağlayarak tüm loglarda proje adını taşırız.
    return log.bind(app="carla-drive")
