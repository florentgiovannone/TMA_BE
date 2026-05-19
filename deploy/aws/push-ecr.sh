#!/usr/bin/env bash
# Build the API image and push to Amazon ECR.
# Prereqs: AWS CLI v2, Docker, credentials (aws configure / SSO).
set -euo pipefail

AWS_REGION="${AWS_REGION:-eu-west-1}"
AWS_ACCOUNT_ID="${AWS_ACCOUNT_ID:-$(aws sts get-caller-identity --query Account --output text)}"
ECR_REPO="${ECR_REPO:-tma-be-api}"
IMAGE_TAG="${IMAGE_TAG:-latest}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"

echo "Region:  ${AWS_REGION}"
echo "Account: ${AWS_ACCOUNT_ID}"
echo "Repo:    ${ECR_REPO}"
echo "Image:   ${ECR_URI}:${IMAGE_TAG}"

aws ecr describe-repositories --repository-names "${ECR_REPO}" --region "${AWS_REGION}" >/dev/null 2>&1 \
  || aws ecr create-repository --repository-name "${ECR_REPO}" --region "${AWS_REGION}"

aws ecr get-login-password --region "${AWS_REGION}" \
  | docker login --username AWS --password-stdin "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

docker build -t "${ECR_REPO}:${IMAGE_TAG}" "${ROOT}"
docker tag "${ECR_REPO}:${IMAGE_TAG}" "${ECR_URI}:${IMAGE_TAG}"
docker push "${ECR_URI}:${IMAGE_TAG}"

echo ""
echo "Pushed: ${ECR_URI}:${IMAGE_TAG}"
echo "Use this image URI when creating an App Runner service or ECS task."
