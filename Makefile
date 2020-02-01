env:
	test -d env || python3 -m venv env

install:
	pip install -r requirements.txt

run:
	python -m flask run

deploy-prod:
	gcloud builds submit --tag gcr.io/studyq-266906/studyq-backend
	gcloud run deploy --image gcr.io/studyq-266906/studyq-backend --platform managed

# Don't use
browser:
	gcloud app browse -s romdash-backend

logs:
	gcloud app logs tail -s romdash-backend
