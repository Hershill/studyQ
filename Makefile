env:
	test -d env || python3 -m venv env

install:
	pip install -r requirements.txt

run:
	python -m flask run

# Don't use
deploy-prod:
	gcloud config set project home-prod
	gcloud app deploy app-prod.yaml

browser:
	gcloud app browse -s romdash-backend

logs:
	gcloud app logs tail -s romdash-backend