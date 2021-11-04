run:
	uvicorn app.main:app --reload

requirements:
	pip install "fastapi[all]"
	pip install SQLAlchemy
	pip install "passlib[bcrypt]"
	pip install "python-jose[cryptography]"
	pip install alembic
	pip freeze > requirements.txt


alembic:
	alembic init alembic
	alembic revision -m "message"
	alembic revision --autogenerate -m "message"

	alembic upgrade revision_id
	alembic upgrade head
	alembic upgrade +1
	alembic downgrade down_revision_id
	alembic history
	alembic current

migrate:
	alembic upgrade head
