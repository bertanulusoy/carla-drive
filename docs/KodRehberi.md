# KOD REHBERİ

## Komut Gönderme kodu
git add dosyanızın adı
git status
git commit -m "mesaj"
git push


## Kod Kaydetme Kodu

git add .
git commit -m "Save changes"

## Kod çalıştırma 

poetry install
poetry run python -m carla_drive
poetry run pytest   


## kodları doğru yazıp yazmadığını kontrol eder
poetry run ruff check . --fix
poetry run ruff format .
poetry run ruff check .
poetry run ruff format --check .
pre-commit run --all-files
poetry run pytest

