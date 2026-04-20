"""
Bu dosya, projenin en temel smoke import testlerini içerir.

Amaç:
- paket import edilebiliyor mu?
- common modüller erişilebilir mi?
- feature modülleri erişilebilir mi?

Bu testler smoke testleri olduğu için ağır doğrulama testleri değildir.
Dış servis, CARLA server veya gerçek veri gerektirmez.
"""


def test_import_carla_drive_package() -> None:
    import carla_drive  # noqa: F401

    assert carla_drive is not None


def test_now_ts_returns_non_empty_string() -> None:
    from carla_drive.common.utils import now_ts

    result = now_ts()
    assert isinstance(result, str)
    assert len(result) > 0


def test_import_feature_dataset_bc_class() -> None:
    from carla_drive.feature.dataset_bc import BCDataset

    assert BCDataset.__name__ == "BCDataset"
