make-env:
	python -m venv .venv
	.venv\Scripts\activate
	pip install -r requirements.txt

start-env:
	.venv\Scripts\activate

run:
	uvicorn main:app --reload --port 8080

init-db:
	python  -m app.db.init_db