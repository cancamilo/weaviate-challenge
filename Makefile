help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: extract-data
extract-data:
	@poetry run python backfill

.PHONY: load-data
load-data:
	@poetry run python load_weaviate.py

.PHONY: test-endpoint
test-endpoint: 
	@curl -X POST "http://localhost:8000/search" -H "accept: application/json" -H "Content-Type: application/json" \
	-d "{\"query\":\"bitcoin news\"}"

.PHONY: run-frontend
run-frontend:
	@cd frontend && npm run dev

.PHONY: run-backend
run-backend:
	@poetry run uvicorn main:app --reload