# Summary — Lab 3

## Baseline
- Checkov findings: (fill after running)  
- Semgrep findings: (fill after running)

## Changes applied (at least 3)
| File | Issue ID | Your change | Reference link | Status |
|------|----------|-------------|----------------|--------|
| terraform/main.tf | CKV_AWS_* | Enabled S3 Block Public Access and encryption | https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html | fixed |
| k8s/deployment.yaml | k8s-no-privileged | Set `privileged: false`, `runAsNonRoot: true` | https://kubernetes.io/docs/tasks/configure-pod-container/security-context/ | fixed |
| docker/Dockerfile | docker-avoid-latest | Pinned base image to a digest | https://semgrep.dev/p/dockerfile | fixed |

## After
- Checkov findings: (fill)  
- Semgrep findings: (fill)

## Reflection (≈200 words)
- Biggest risk patterns observed and how to prevent regressions (policy or CI gating idea).
