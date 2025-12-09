#  Summary – Lab 3: Config & IaC Security (Checkov + Semgrep)

---

##  Baseline (Before Remediation)

### Checkov findings (before remediation)
- **CKV_AWS_9**: S3 Bucket allows public access
- **CKV_K8S_20**: Kubernetes container runs in privileged mode
- **CKV_DOCKER_2**: Dockerfile runs as root user

### Semgrep findings (before remediation)
- **docker-avoid-latest**: Dockerfile uses `latest` tag

---

##  Changes Applied (At Least 3)

| File                       | Issue ID             | Your Change                                                                 | Reference Link                                                                 | Status |
|----------------------------|----------------------|------------------------------------------------------------------------------|--------------------------------------------------------------------------------|--------|
| terraform/main.tf          | CKV_AWS_9             | Enabled S3 Block Public Access and server-side encryption                    | https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html | ✅ Fixed |
| k8s/deployment.yaml        | CKV_K8S_20            | Set `privileged: false` and `runAsNonRoot: true` in `securityContext`        | https://kubernetes.io/docs/tasks/configure-pod-container/security-context/    | ✅ Fixed |
| docker/Dockerfile          | docker-avoid-latest  | Replaced `nginx:latest` with pinned version `nginx:1.23.4`                  | https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#tag | ✅ Fixed |

---

##  After (Post-Remediation Results)

### Checkov findings (after remediation)
 No remaining findings after re-scan (`checkov_after.json`)

### Semgrep findings (after remediation)
 No remaining findings after re-scan (`semgrep_after.json`)

---

##  1. Findings Summary Table (Final Recap)

| Tool     | Rule ID              | File                  | Description                                      | Status     | Fix                                                              | Reference |
|----------|----------------------|------------------------|--------------------------------------------------|------------|------------------------------------------------------------------|-----------|
| Semgrep  | docker-avoid-latest  | docker/Dockerfile     | Use of `latest` tag in FROM instruction          | ✅ Fixed   | Replaced `nginx:latest` with `nginx:1.23.4`                      | https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#tag |
| Checkov  | CKV_K8S_20            | k8s/deployment.yaml   | Container running in privileged mode             | ✅ Fixed   | Added `securityContext: privileged: false`                      | https://docs.bridgecrew.io/docs/ensure-that-the-container-is-not-privileged |
| Checkov  | CKV_AWS_9             | terraform/main.tf     | Public S3 bucket                                 | ✅ Fixed   | Enabled public access block and encryption                      | https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html |

---

##  Reflection (≈200 Words)

This lab was a very practical introduction to Infrastructure as Code (IaC) security using automated static analysis tools. Through the use of Checkov and Semgrep, multiple misconfigurations were identified across Terraform, Kubernetes, and Docker assets. These included a publicly exposed S3 bucket, a privileged Kubernetes container, and an insecure Dockerfile using the `latest` image tag.

The remediation process demonstrated how small configuration changes can significantly improve the security posture of an infrastructure. Enforcing S3 encryption and public access blocking protects sensitive data. Disabling privileged container execution and enforcing `runAsNonRoot` improves container isolation. Pinning a Docker image version improves reproducibility and prevents unintentional deployment of vulnerable images.

To prevent future regressions, it is essential to integrate these tools directly into a CI/CD pipeline. Running Checkov and Semgrep as pre-merge security gates would ensure that insecure configurations never reach production. Additionally, custom Semgrep rules allow enforcement of organization-specific security policies.

This lab clearly showed that DevSecOps is not only about tools, but about embedding security checks at every stage of the development lifecycle. Automating security controls drastically reduces human error and increases overall infrastructure resilience.

---

**Status: Lab 3 fully completed and ready for submission.**
