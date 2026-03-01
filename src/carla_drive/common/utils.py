from __future__ import annotations

import os
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Union

import numpy as np

try:
    import torch
except Exception:
    torch = None  # type: ignore[assignment]


PathLike = Union[str, os.PathLike, Path]


def ensure_dir(path: PathLike) -> Path:
    """
    Verilen klasör yoksa oluturur, varsa dokunmaz.
    ML projelerinde data/runs/models gibi klasörleri garantiye almak için kullanılır.
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def now_ts(fmt: str = "%Y-%m-%dT%H-%M-%SZ", use_utc: bool = True) -> str:
    """
    Dosya/klasör ismi üretmek için 'güvenli' timestamp string döndürür.
    Varsalın formatta ':' yerine '-' var (Windows için sorun çıkartmasın diye).
    """
    dt = datetime.now(timezone.utc) if use_utc else datetime.now()
    return dt.strftime(fmt)


def set_seed(seed: int, deterministic_torch: bool = True) -> None:
    """
    Tekrar üretebilirlik içn seed ayarları:
    - Python random
    - NumPy
    - Torch
    """
    if not isinstance(seed, int):
        raise TypeError(f"Seed must be an integer, got {type(seed)}")

    os.environ["PYTHONHASHSEED"] = str(seed)

    random.seed(seed)
    np.random.seed(seed)

    if torch is not None:
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)

        if deterministic_torch:
            # determinism için "iyi pratik" ayarlar
            try:
                torch.backends.cudnn.deterministic = True  # type: ignore[attr-defined]
                torch.backends.cudnn.benchmark = False  # type: ignore[attr-defined]
            except Exception:
                pass
    return None
