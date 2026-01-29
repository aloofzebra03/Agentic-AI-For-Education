# Building the Image

```
docker build -t aloofzebra03/educational-api:latest .                                               
```

# Running the Container

```
docker run -it -p 8000:8000 --name educational-api-test --env-file .env aloofzebra03/educational-api:latest
```

# Giving the latest Tags

> ```
> docker tag aloofzebra03/educational-api:latest aloofzebra03/educational-api:v1.0.0 aloofzebra03/educational-api:2026-01-29
> ```

# Push all tags at once

```
docker login
docker push --all-tags aloofzebra03/educational-api
```
