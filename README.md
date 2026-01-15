# carla-drive

FTI (Feature → Training → Inference) yaklaşımıyla **PyTorch + CARLA** üzerinde:
- Behavior Cloning (BC) (autopilot → supervised)
- RL baselines (DQN / PPO vb.)
- Güvenli inference (safety wrappers, evaluation scripts)

hedefleyen bir deney/araştırma repo’su.

> Repo adı: **carla-drive**
> Python package: **carla_drive** (src layout)

---

## Hızlı Başlangıç (Mac / Linux)

### Gereksinimler
- Python **3.12**
- Poetry **2.x**
- (Opsiyonel) GitHub CLI (`gh`)

### Kurulum
```bash
poetry install --extras dev
poetry run pytest

işte böyle yapılıyor
