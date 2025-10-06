make-env:
	python -m venv .venv
	.venv\Scripts\activate
	pip install -r requirements.txt

start-env:
	.venv\Scripts\activate

run:
	uvicorn main:app --reload --port 1234

init-db:
	python  -m app.db.init_db