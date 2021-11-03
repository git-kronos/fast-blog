run:
	uvicorn app.main:app --reload

requirements:
	pip install "fastapi[all]"
	pip install SQLAlchemy
	pip install "passlib[bcrypt]"
	pip freeze > requirements.txt
