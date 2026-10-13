docker compose up -d\n
alembic revision --autogenerate -m 'Init'\n
alembic upgrade head\n
python seed.py
