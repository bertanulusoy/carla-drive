from carla_drive.common.utils import now_ts
from carla_drive.feature.dataset_bc import BCDataset


def test_import_package() -> None:
    import carla_drive  # noqa: F401


def test_now_ts_returns_string() -> None:
    result = now_ts()
    assert isinstance(result, str)
    assert len(result) > 0


def test_import_bc_dataset_class() -> None:
    assert BCDataset is not None
    assert BCDataset.__name__ == "BCDataset"