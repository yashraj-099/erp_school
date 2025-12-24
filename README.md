# School ERP (Demo)

This is a demo scaffold of the School ERP system you requested.

## Quick start (Docker)

```bash
docker compose up --build
```

This will run migrations and attempt to load demo data included in `demo_data.json`.

Access the app at `http://localhost:8000/` and Django admin at `http://localhost:8000/admin/`.

Demo admin user: `admin` / `admin123` (you may need to create superuser manually if fixture doesn't set usable password).

## Notes
- This scaffold aims to provide a working starting point with templates, API endpoints, and Docker support.
- For production, replace the demo SECRET_KEY and configure an appropriate database.
