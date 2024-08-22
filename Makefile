dev:
	cd kadastr/ && python3 -m uvicorn main:app --reload --port=8001
external_server:
	cd external/ && uvicorn main:app --reload
install:
	poetry install