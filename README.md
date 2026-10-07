# DevOps Engineer Homework Solution

## Summary of Changes

### 1. Application (`app/main.py`)
- Implemented a Python Flask app delivering all specified REST endpoints: `/health`, `/version`, `/env`, and `/config` (POST, GET, DELETE).
- Utilized an in-memory dictionary for `/config` key-value storage.

### 2. Containerization (`Dockerfile`)
- Used `python:3.11-slim` as a minimal base image.
- Configured non-root execution (`appuser`, UID 10001) for security.
- Standardized exposed port to `8080`.

### 3. Helm Chart (`helm/`)
- Fixed Service label selector (`app: myapp`).
- Corrected Ingress backend service reference (`myapp`).
- Aligned container and service target ports to `8080`.
- Added liveness and readiness probes pointing to `/health`.
- Configured baseline CPU/memory requests and limits.

### 4. Terraform (`terraform/`)
- Fixed HCL syntax errors and missing quotes in `main.tf`.
- Corrected Helm chart path to `../helm`.
- Linked `namespace`, `image_tag`, and `environment` dynamically to Terraform variables.
- Defined explicit provider version constraints and outputs.

### 5. CI/CD Pipeline (`.gitlab-ci.yml`)
- Structured pipeline into 4 distinct stages: `lint`, `build`, `test`, and `deploy`.
- Added automated container health tests against `/health` and `/version` endpoints prior to deployment.

---

## Assumptions

- **In-Memory State:** Since no database was required by the specification, state for `/config` resides in process memory and resets on pod restart.
- **Environment Overrides:** `helm/values.yaml` provides `dev` fallback defaults for local development, while Terraform sets `prod` when provisioning infrastructure.
- **Cluster Target:** Targeted for local Kubernetes environments using `~/.kube/config`.

---

## Known Limitations

- **Volatile Storage:** `/config` entries do not persist across container restarts.
- **Horizontal Scaling:** Scaling `replicaCount > 1` will lead to inconsistent key lookups across pods due to isolated in-memory stores.
- **Ingress TLS:** Ingress manifest does not configure HTTPS/TLS termination certificates.

---

## Production Improvements

1. **Persistent Backing Store:** Migrate `/config` key-value handling to Redis or PostgreSQL.
2. **Remote Terraform State:** Use S3/GCS backends with distributed state locking (DynamoDB / GCP Cloud Storage).
3. **Secret Management:** Manage sensitive parameters using HashiCorp Vault or Kubernetes External Secrets Operator.
4. **GitOps Pipeline:** Shift from a direct `terraform apply` step in CI to a GitOps operator like ArgoCD or FluxCD.
5. **TLS Integration:** Implement `cert-manager` for automatic Let's Encrypt TLS provisioning.

---

## Local Verification Guide

### Run Container Locally
```bash
podman build -t myapp:1.0.0 .
podman run -d -p 8080:8080 -e ENVIRONMENT=dev --name myapp myapp:1.0.0
curl [http://127.0.0.1:8080/health](http://127.0.0.1:8080/health)
podman stop myapp && podman rm myapp
