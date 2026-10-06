# Course Notes

A simple course notes demo application for django. Link to production: https://coursenotes.carleton.university

## Run it on your own computer

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Then open http://localhost:8000. The `migrate` command creates the database and loads two sample notebooks.

Run the tests with `python manage.py test`.

## Uploaded files

A note can have one attached file, up to 10 MB. Images are shown on the note's page; other files are shown as a link.

Uploaded files are stored in the folder named by `MEDIA_ROOT`: `media/` on your own computer and `/var/lib/project_1/media` on the production server.

## Deployment

Every change on `main` is deployed to the production server by the GitHub Action in `.github/workflows/deploy.yml`. The settings of the production server are in `deploy/project_1.service`.
