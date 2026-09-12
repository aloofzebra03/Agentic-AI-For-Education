# Building the Image

```powershell
docker build `
  --build-context whiteboard_poc=../Whiteboard_Tutor_Education_POC `
  -t aloofzebra03/educational-api:latest .
```

The sibling POC checkout is required because it is the single source for the
`whiteboard_tutor` package. See `WHITEBOARD_TUTOR_DOCKER_INTEGRATION.md` for API
examples.

# Running the Container

```powershell
docker run -it -p 8000:8000 --name educational-api-test --env-file .env aloofzebra03/educational-api:latest
```

# Giving the latest Tags

> ```powershell
> docker tag aloofzebra03/educational-api:latest aloofzebra03/educational-api:v1.0.0 aloofzebra03/educational-api:2026-01-29
> ```

# Push all tags at once

```powershell
docker login
docker push --all-tags aloofzebra03/educational-api
```
