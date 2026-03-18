from __future__ import annotations
# Bu satır, Python'da type hint'leri (tip ipuçlarını) daha rahat kullanmamıza yardım eder.
# (Örn: list[Path] gibi yazabilmek için.)

# Dosya yollarını OS bağımsız (Windows/Mac) yönetmek için.
from pathlib import Path


# Callable: transform gibi "fonksiyon parametresi" için
# Optional: opsiyonel değerler için (None olabilir)
# Tuple: (image_tensor, action_tensor) gibi ikili dönüşler için.
from typing import Callable, Optional, Tuple

# .np dosyalarını okumak ve numpy ile işlem yapmak için.
import numpy as np

# Tensor üretmek için.
import torch

# PyTorch Dataset sınıfı: DataLoader bu sınıfla çalışır.
from torch.utils.data import Dataset

# PNG dosyasını okumak için (Pillow).
# Image.open(...) ile .png açarız.
from PIL import Image

"""
Bu dosya ne yapar?
- Behavior Cloning (BC) için katdedilmiş veriyi PyTorch Dataset olarak okur.

BC (Behavior Cloning) = "Usta sürücüyü taklit etme"
- CARLA autopilot sürer (usta sürücü gibi düşünüyoruz).
- Biz her an şunu kaydederiz:
  1) Görüntü (kamera) -> araba ne görüyor?
  2) Aksiyon (kontrol) -> usta ne yaptı? (direksiyon, gaz, fren)

Sonra model şunu öğrenir:
- "Bu görüntüyü görünce şu kontrolü yap."

Dataset ne döndürür?
Dataset, her örnek için 2 şey döndürür:
  1) image -> torch.float32 tensor
    - shape: (C, H, W)
    - değer aralığı: [0, 1]
  2) action -> torch.float32 tensor
    - shape: (3,)
    - anlamı: [steer, throttle, brake]

Dosya formatı (Sprint-1 varsayımı):
  - 0001.png -> görüntü
  - 0001.npy -> action (3 eleman: steer, throttle, brake)

-----------------------------------------------------------------

H, W, C nedir?
  - H = Height (yükseklik): resmin kaç satır pikselden oluştuğu
  - W = Width (genişlik): resmin kaç sütun pikselden oluştuğu
  - C = Channels (kanal sayısı): her pikselde kaç renk bilgisi olduğu
     - RGB resim -> 3 kanal (R, G, B)

Örnek:
  - 10x20 boyut RGB resim:
    - H = 10
    - W = 20
    - C = 3

-----------------------------------------------------------------

HWC ve CHW farkı nedir?

Resim dosyaları genelde HWC ile gelir:
  - HWC = (H, W, C)
  - Örn: (10, 20, 3)

PyTorch CNN modelleri genelde CHW ister:
  - CHW = (C, H, W)
  - Örn: (3, 10, 20)

Bu yüzden dataset içinde HWC -> CHW dönüşümünü yapıyoruz.

-----------------------------------------------------------------

Normalize neden var?

Resimler çoğunlukla 0..255 arası tam sayı (uint8) gelir.
Modelin öğrenmesi için genelde 0..1 arası float daha iyi.

Bu yüzden:
  - 0..255 değerleri 255'e bölerek 0..1 aralığına alıyoruz.
    image = image / 255.0
"""

# Dataset bir örnek için (image_tensor, action_tensor) döndürür.
# image_tensor: torch.Tensor
# action_tensor: torch.Tensor
TensorPair = Tuple[torch.Tensor, torch.Tensor]


class BCDataset(Dataset[TensorPair]):
    """
    BCDataset: PyTorch Dataset sınıfı

    Dataset'in mantığı:
    - Klasördeki tüm .png dosyalarını bulur (Örn 0001.png)
    - Her resim için aynı isimli .nyp dosyasını arar (Örn 0001.nyp)
    - __getitem__ ile:
        image -> (C,H,W) float32 [0,1]
        action -> (3,) float32
        döndürür.

    Dataset + DataLoader ilişkisi:
    - Dataset tek örnek verir: image, action
    - DataLoader bu örnekleri "batch" halinde toplar:
      - image batch shape: (B, C, H, W)
      - action batch shape: (B, 3)
      Buarada B = batch_size (batch büyüklüğü)
    """

    def __init__(
        self,
        data_dir: str | Path,
        transform: Optional[Callable[[torch.Tensor], torch.Tensor]] = None,
        strict: bool = True,
    ) -> None:
        """
        data_dir:
          - Resimler (.png) ve aksiyonlar (.nyp) burada olacak

        transform:
          - İstersen image üzerinde ekstra işlem uygularsın.
          Örn:
            - resize (boyut değiştirme)
            - normalize (farklı bir normalize)
            - augmentation (çevirme, kırpma vb.)
        strict:
          - True ise: Bir resmin action dosyası yoksa hata verir.
            (Öğrenme ve hata yakalama için iyi)
          - False ise: Eksik çiftleri atlar.
            (İleri seviye senaryolarda işe yarar)
        """
        # Gelen data_dir string bile olsa Path'e çeviriyoruz.
        # Path kullanmak daha güvenli ve okunaklı
        self.data_dir = Path(data_dir)

        # transform fonksiyonunu saklıyoruz (opsiyonel).
        self.transform = transform

        # strict mode ayarı
        self.strict = strict

        # Klasör yoksa erken ve anlaşılır hata ver.
        if not self.data_dir.exists():
            raise FileNotFoundError(f"data_dir bulunamadı: {self.data_dir}")

        # pairs: (image_path, action_path) şeklinde eşleştirilmiş dosya listesi.
        # Örn: (0001.png, 000.nyp)
        self.pairs: list[tuple[Path, Path]] = self._index_pairs()

        # srict modda hiç veri yoksa bunu da erken söylemek gerekiyor.
        if self.strict and len(self.pairs) == 0:
            raise ValueError(f"Hiç dataset çifti bulunamadı: {self.data_dir}")

    def _index_pairs(self) -> list[tuple[Path, Path]]:
        """
        Klasördeki dosyaları tarar ve (image, action) eşlemelerini çıkarır.

        Beklenen eşleme:
          0001.png + 0001.npy

        Nasıl eşleştiriyoruz?
          - Klasördeki bütün .png'leri buluyoruz.
          - Her png için aynı isimli .npy var mı diye bakıyoruz.

        strict=Teue is:
        - png var ama npy yoksa hata ver.
        strict False ise:
        - o örneği atla (pairs listesine ekleme.)
        """
        pairs: list[tuple[Path, Path]] = []

        # Klasördeki tüm .png dosyalarını buluruz.
        # sorted(...) -> her çalıştırmada aynı sırada olsun (deterministik).
        image_files = sorted(self.data_dir.glob(".png"))

        for img_path in image_files:
            # Aynı isimli action dosyası bekliyoruz
            # 0001.png -> 0001.npy
            act_path = img_path.with_suffix(".npy")

            if act_path.exists():
                # Hem png hem npy varsa eşlemeyi ekle.
                pairs.append((img_path, act_path))
            else:
                # strict ise hata ver, değşilse bu örneği atla.
                if self.strict:  # Eğer strict=True ise
                    raise FileNotFoundError(
                        f"Action dosyası eksik: {img_path.name} için {act_path.name} bulunamadı."
                    )

        return pairs

    def __len__(self) -> int:
        """
        Dataset kaç örnek içeriyor?

        pairs listesi ne kadar uzunsa, dataset o kadar örnek içerir.
        """
        return len(self.pairs)

    def __getitem__(self, idx: int) -> TensorPair:
        """
        PyTorch DataLoader bu fonksiyonu çağırır.

        idx: kaçıncı örnek isteniyor?
        - idx=0 -> ilk örnek
        - idx=1 -> ikinci örnek
        vb.

        Dönen:
        - image_tensor: (C,H,W) float32 [0,1]
        - action_tensor: (3,) float32
        """
        # pairs[idx] bize şu ikiliyi verir:
        # (image_patch, action_path)
        img_path, act_path = self.pairs[idx]  # => idx=1 => (image_patch1, action_path1)

        # -----------------------------------------------------
        # 1) IMAGE (GÖRÜNTÜ) YÜKLE
        # -----------------------------------------------------
        # Image.open(img_path):
        # - png dosyasını açar.
        #
        # .convert("RGB"):
        # - resmi RGB formatına çevirir.
        # - Böylece her zaman 3 kanal (C=3) elde ederiz.
        pil_img = Image.open(img_path).convert("RGB")

        # PIL -> numpy array
        # Bu array genelde HWC gelir: (H, W, C)
        # Örn: (10, 20, 3)
        img_np = np.asarray(pil_img, dtype=np.uint8)

        # HWC -> CHW dönüşümü:
        # - HWC: (H, W, C)
        # - CHW: (C, H, W)
        #
        # np.transpose(image_np, (2, 0, 1)) şu anlama gelir:
        # - 2. ekseni (C) en başa al
        # - 0. ekseni (H) ikinci yap
        # 1. ekseni (W) üçüncü yap
        #
        # Sonuç: (C, H, W)
        imag_chw = np.transpose(img_np, (2, 0, 1))

        # numpy -> torch tensor
        # dtype=torch.float32:
        # - model eğitimi için float kullanmak daha uygundur
        img_t = torch.tensor(imag_chw, dtype=torch.float32)

        # Normalize:
        # img_t değerleri şu an 0..255 olabilir
        # /255.0 yaparak 0..1 aralığına çeviriyoruz.
        img_t = img_t / 255.0

        # Opsiyonel transform:
        # Eğer transform verildiyse image tensor üzerinde ekstra işlem yap.
        # Örn: resize/augmentation vb.
        if self.transform is not None:
            img_t = self.transform(img_t)

        # ----------------------------------------------------------
        # 2) ACTION (AKSİYON) YÜKLE
        # ----------------------------------------------------------
        # Action dosyası numpy formatında bekleniyor:
        # - 0001.npy
        # - shape: (3,)
        # - anlamı: [steer, throttle, brake]
        action_np = np.load(act_path)

        # numpy -> torch tensor
        action_t = torch.tensor(action_np, dtype=torch.float32)

        # Güvenlik kontrolü: action kesin (3,) olmalı
        # action_t.ndim: (number of dimension - kaç eksenli)
        # - 1 ise tek boyutlu dizi demektir (örn: [a, b, c])
        #
        # action_t.shape[0] == 3:
        # - 3 tane sayı olmalı: steer(yönlendirme), throttle(gaz), brake(fren)
        if action_t.ndim != 1 or action_t.shape[0] != 3:
            raise ValueError(
                "Action shape yanlış! "
                f"Beklenen (3,), gelen: {tuple(action_t.shape)}"
                f"Dosya: {act_path.name}"
            )

        # -------------------------------------------------------
        # 3) DÖNÜŞ
        # -------------------------------------------------------
        # image: (C,H,W) örn (3, 10, 20)
        # action: (3,) örn [0.1, 0.6, 0.0]
        return img_t, action_t
