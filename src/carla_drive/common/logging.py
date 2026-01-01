from __future__ import annotations

# Not: structlog built-in değildir; 3rd-party bir kütüphanedir.
# v0'da "nasıl entegre edilir" yönlendirmesi yapıyoruz.
import structlog

from typing import Optional

"""
Bu modülün amacı:
- Proje genelinde tek tip logging standardı oluşturmak
- Uygulama kodu (feature/training/inference) log almak istediğinde:
    from carla_drive.common.logging import get_logger
    log = get_logger(__name__)
    log.info("app_started", mode="dev")

Önemli kural:
- Bu dosya "kütüphane" gibi kalmalı.
- İçinde örnek kullanım veya çalıştırılabilir kod OLMAMALI.
- Sadece logger üretme (factory) + (gerekiyorsa) konfigürasyon olmalı.
"""


# Bu bayrak, konfigürasyonun bir kere yapılmasını sağlayacak.
_CONFIGURED = False


def _normalize_level(level: Optional[str]) -> int:
    """
    Amaç:
    - Log'ların seviyesi olacak.
    - Kullanıcıdan gelen seviye bilgisini normalize edeceğiz.
    - "debug", "DEBUG", "Warn", "warning" gibi varyasyonları tek standarda indirgemek.
    - Stdlib logging seviyesine (int) çevirmek.

    Algoritma (öneri):
    1) level None ise default "INFO" kullan.
    2) string'i strip + upper yap.
    3) Bir mapping oluştur:
       DEBUG -> logging.DEBUG
       INFO -> logging.INFO
       WARNING/WARN -> logging.WARNING
       ERROR -> logging.ERROR
       CRITICAL/FATAL -> logging.CRITICAL
    4) mapping'te yoksa INFO'ya düş.
    """
    # TODO: implementasyona buradan devam edebilrsin :)
    raise NotImplementedError


def _configure_logging(level: Optional[str] = None) -> None:
    """
    Amaç:
    - Logging altyapısını (stdlib logging + structlog) tek seferlik kurmak.
    - get_logger() çağrıldığında hazır bir logger dönebilmek.

    Neden tek sefer?
    - Aynı proses içinde configure işlemi tekrar tekrar yapılırsa loglar bozulabilir,
      handler'lar çoğalabilir, formatlar karışabilir.

    Algoritma (öneri):
    1) global _CONFIGURED True ise direkt return et.
    2) level parametresi yoksa env'den oku: LOG_LEVEL (default INFO).
    3) _normalize_level ile sayısal seviyeye çevir.
    4) logging.basicConfig(...) ile stdlib logging'i kur:
       - level: normalize edilmiş seviye
       - format: şimdilik basit (örn. "%(message)s")
    5) structlog.configure(...) yap:
       - timestamp + level + json renderer gibi processor'lar ekle
       - v0'da minimal bir pipeline yeter (çok advanced olmayacak)
    6) _CONFIGURED = True yap.
    """
    # TODO: burayı da implement edebilirsin :)
    raise NotImplementedError


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Amaç:
    - Uygulama tarafına "hazır logger" vermek.

    Beklenen kullanım:
    - name genelde __name__ olur. (__name__ bir string'dir)
      Örn: "carla_drive.training.bc_train"
    - Böylece logların kaynağı okunur. Hangi modülden geldiği anlaşılır.

    Algoritma (öneri):
    1) _configure_logging() çağır (gerekirse kurulum yapsın).
    2) structlog.get_logger(name) döndür.
    """
    # TODO: burayı da implement edebilirsin :)
    raise NotImplementedError
