#!/usr/bin/env bash
# Build on EC2 from GitHub and restart the API container.
# Use when Docker Hub push or SSM is unavailable (EC2 Instance Connect):
#   curl -sL https://raw.githubusercontent.com/aloofzebra03/Agentic-AI-For-Education/main/deployment/redeploy-from-git.sh | bash
set -euo pipefail

REPO_DIR="${REPO_DIR:-/home/ubuntu/EduAgent}"
REPO_URL="${REPO_URL:-https://github.com/aloofzebra03/Agentic-AI-For-Education.git}"
BRANCH="${GIT_BRANCH:-main}"
IMAGE="${DOCKER_IMAGE:-aloofzebra03/educational-api:latest}"
CONTAINER="${CONTAINER_NAME:-fastapi}"
ENV_FILE="${ENV_FILE_ON_EC2:-/etc/fastapi/.env}"
PORT="${HOST_PORT:-8000}"

echo "==> Repo: ${REPO_URL} (${BRANCH})"
if [ ! -d "${REPO_DIR}/.git" ]; then
  git clone --branch "${BRANCH}" "${REPO_URL}" "${REPO_DIR}"
fi

cd "${REPO_DIR}"
git fetch origin "${BRANCH}"
git checkout "${BRANCH}"
git pull origin "${BRANCH}"

echo "==> Building ${IMAGE}"
docker build -t "${IMAGE}" .

echo "==> Restarting ${CONTAINER}"
docker stop "${CONTAINER}" 2>/dev/null || true
docker rm "${CONTAINER}" 2>/dev/null || true

docker run -d \
  --name "${CONTAINER}" \
  --restart unless-stopped \
  --env-file "${ENV_FILE}" \
  -p "${PORT}:8000" \
  "${IMAGE}"

echo "==> Waiting for health"
for i in $(seq 1 30); do
  if curl -sf "http://localhost:${PORT}/health" >/dev/null; then
    echo "==> Healthy"
    curl -s "http://localhost:${PORT}/health"
    exit 0
  fi
  sleep 2
done

echo "==> Health check failed"
docker logs "${CONTAINER}" --tail 80
exit 1
