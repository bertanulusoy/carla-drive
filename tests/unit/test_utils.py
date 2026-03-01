from __future__ import annotations

from pathlib import Path

import numpy as np

from carla_drive.common.utils import ensure_dir, now_ts, set_seed


def test_ensure_dir_creates_directory(tmp_path: Path) -> None:
    target = tmp_path / "a" / "b" / "c"
    assert not target.exists()

    out = ensure_dir(target)

    assert out.exists()
    assert out.is_dir()
    assert out == target


def test_now_ts_returns_string() -> None:
    ts = now_ts()
    assert isinstance(ts, str)
    assert len(ts) > 5


def test_set_seed_makes_numpy_deterministic() -> None:
    set_seed(123)
    a1 = np.random.rand(5)

    set_seed(123)
    a2 = np.random.rand(5)

    assert np.allclose(a1, a2)


def test_set_seed_invalid_type() -> None:
    try:
        set_seed("123")  # type: ignore[arg-type]
        assert False, "Expected TypeError"
    except TypeError:
        assert True
