# note-management-system-223175-223175-223266

Backend: Django REST Framework Notes API

## Quick start
- Install deps (already pinned in requirements.txt)
- Apply migrations and seed data:
  - python notes_app_backend/manage.py migrate
  - python notes_app_backend/manage.py loaddata  # optional if fixtures exist
  - python notes_app_backend/manage.py seed_notes
- Run server:
  - python notes_app_backend/manage.py runserver 0.0.0.0:3001

## API Endpoints
Base path: /api/

- Health: GET /api/health/
- Notes:
  - GET /api/notes/?q=<substr>&archived=true|false&tag=<tag>&page=1&page_size=10
  - POST /api/notes/
  - GET /api/notes/:id/
  - PUT /api/notes/:id/
  - PATCH /api/notes/:id/
  - DELETE /api/notes/:id/

## OpenAPI/Docs
- Schema JSON: /api/schema/
- Swagger UI: /api/docs/

## CORS
CORS is enabled for localhost/127.0.0.1 ports commonly used by frontends.

## Curl examples
Create:
curl -sS -X POST http://localhost:3001/api/notes/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Sample","content":"Body","tags":["cli","demo"],"archived":false}'

List:
curl -sS "http://localhost:3001/api/notes/?page=1&page_size=10"

Filter:
curl -sS "http://localhost:3001/api/notes/?q=sample&archived=false&tag=cli"

Retrieve:
curl -sS "http://localhost:3001/api/notes/1/"

Update (PATCH):
curl -sS -X PATCH http://localhost:3001/api/notes/1/ \
  -H "Content-Type: application/json" \
  -d '{"archived": true}'

Delete:
curl -sS -X DELETE "http://localhost:3001/api/notes/1/"