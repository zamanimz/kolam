# Running Backend and Frontend

This repo includes a small helper script `run.py` to start both the backend and frontend from the repository root.

Basic usage (PowerShell):

```powershell
# Run both backend and frontend
python run.py

# Run only the backend
python run.py --backend

# Run only the frontend and open browser
python run.py --frontend --open

# Change ports if needed
python run.py --backend-port 5001 --ui-port 5174
```

Notes:
- The backend is a Flask app located in `backend/app.py`. The script uses `python -m flask run` and sets `FLASK_APP=backend/app.py`.
- The frontend is a Svelte/Vite app in `frontend/pond-ui`. The script runs `npm run dev` in that directory.
- Ensure you have dependencies installed: Python packages (Flask, SQLAlchemy) and Node (`npm install`) in the `frontend/pond-ui` folder.

If you want, I can also:
- Add a `requirements.txt` or `pyproject.toml` for the backend.
- Add a small `start` npm script wrapper or `.env` handling for ports.
