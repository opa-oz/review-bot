

update_deps:
	pip-compile --output-file=requirements.txt pyproject.toml
	pip install -r requirements.txt

run:
	uvicorn main:app --reload

expose:
	ngrok http 8000