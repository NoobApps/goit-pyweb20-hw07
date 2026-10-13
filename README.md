docker compose up -d


alembic revision --autogenerate -m 'Init'


alembic upgrade head


python seed.py
