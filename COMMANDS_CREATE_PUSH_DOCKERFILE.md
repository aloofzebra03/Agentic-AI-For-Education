# Building the Image

```python
docker build -t aloofzebra03/educational-api:latest .                                             
```

# Running the Container

```python
docker run -it -p 8000:8000 --name educational-api-test --env-file .env aloofzebra03/educational-api:latest
```

# Giving the latest Tags

> ```python
> docker tag aloofzebra03/educational-api:latest aloofzebra03/educational-api:v1.0.0 aloofzebra03/educational-api:2026-01-29
> ```

# Push all tags at once

```python
docker login
docker push --all-tags aloofzebra03/educational-api
```
