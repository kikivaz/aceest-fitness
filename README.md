# ACEest Fitness & Gym

A small Flask service for gym management (members + BMI calculator), with a full
DevOps pipeline: Git/GitHub, Pytest, Docker, Jenkins and GitHub Actions.

## API

| Method | Endpoint          | Description                                   |
|--------|-------------------|-----------------------------------------------|
| GET    | `/`               | Welcome message                               |
| GET    | `/health`         | Health check                                  |
| GET    | `/members`        | List members                                  |
| POST   | `/members`        | Add member `{"name": "...", "plan": "basic\|premium\|elite"}` |
| GET    | `/members/<id>`   | Get a member                                  |
| DELETE | `/members/<id>`   | Delete a member                               |
| GET    | `/bmi?weight=70&height=1.75` | BMI (kg, metres)                   |

## Local setup & execution

```bash
git clone https://github.com/kikivaz/aceest-fitness.git
cd aceest-fitness

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt

python app.py                     # runs on http://localhost:5000
```

Try it:

```bash
curl http://localhost:5000/health
curl -X POST http://localhost:5000/members -H "Content-Type: application/json" \
     -d '{"name": "Arun", "plan": "premium"}'
curl "http://localhost:5000/bmi?weight=70&height=1.75"
```

## Running tests manually

Locally:

```bash
pytest -v
flake8 .
```

Inside Docker (same as CI):

```bash
docker build --target test -t aceest-fitness:test .
docker run --rm aceest-fitness:test
```

## Docker

```bash
docker build -t aceest-fitness .
docker run -d -p 5000:5000 --name aceest aceest-fitness
curl http://localhost:5000/health
docker stop aceest && docker rm aceest
```

The image uses `python:3.12-slim`, a multi-stage build (dev tools stay out of the
final image), a non-root user, and gunicorn as the server.

## CI/CD overview

### GitHub Actions (`.github/workflows/main.yml`)
Triggered on every `push` and `pull_request`:
1. **Build & Lint** - installs dependencies, syntax-checks with `py_compile`, lints with `flake8`.
2. **Docker Image Assembly** - builds the production image.
3. **Automated Testing** - builds the `test` stage and runs Pytest inside the container.

Each job depends on the previous one, so a failure stops the pipeline early.

### Jenkins (`Jenkinsfile`)
Jenkins acts as a secondary build/validation layer:
1. Pulls the latest code from GitHub.
2. Performs a clean build (`docker build --no-cache`).
3. Runs the Pytest suite in the test container.

Setup summary:
1. Run Jenkins with Docker access:
   ```bash
   docker run -d --name jenkins -p 8080:8080 -p 50000:50000 \
     -v jenkins_home:/var/jenkins_home \
     -v /var/run/docker.sock:/var/run/docker.sock \
     jenkins/jenkins:lts
   ```
2. Install the Docker CLI inside the container (or use a custom image that includes it).
3. Create a **Pipeline** job -> *Pipeline script from SCM* -> Git -> your repo URL -> script path `Jenkinsfile`.
4. Click **Build Now** and confirm the build is green.

## Git workflow

- `main`: stable branch
- `feature/*`, `fix/*`, `ci/*`: short-lived branches merged through pull requests
- Commit style: `feat: ...`, `fix: ...`, `test: ...`, `ci: ...`, `docs: ...`
