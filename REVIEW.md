# Code Review Feedback


---

### 1. Terraform Syntax and Path Issues
* **Problem:** `terraform/main.tf` had invalid HCL syntax (an empty `value =` and unquoted `prod`), and the path to the Helm chart pointed to `../helm/homework` instead of `../helm`.
* **Fix:** Corrected the paths, quoted string variables, and wired `var.namespace`, `var.image_tag`, and `var.environment` cleanly.

---

### 2. Kubernetes Selector and Port Mismatches
* **Problem:** 
  - `helm/templates/service.yaml` had a selector typo (`app: myapps` instead of `myapp`).
  - `helm/templates/ingress.yaml` pointed to a non-existent service name (`homeworks`).
  - `deployment.yaml` listened on port `5000`, while the application ran on `8080`.
* **Fix:** Standardized all selectors, service names, and container ports to `myapp` on port `8080`.

---

### 3. Missing Kubernetes Health Probes & Resource Limits
* **Problem:** `deployment.yaml` didn't specify `livenessProbe` or `readinessProbe`, and lacked CPU/memory resource requests and limits. Without these, Kubernetes can't monitor pod health or schedule cluster resources safely.
* **Fix:** Added liveness/readiness checks pointing to `/health` and added standard resource requests and limits.

---

### 4. Container Security (Running as Root)
* **Problem:** The app was running as `root` inside the container, which is a security risk in shared Kubernetes environments.
* **Fix:** Added a dedicated non-root user (`appuser` with UID `10001`) in the `Dockerfile`.

---

### 5. Incomplete CI/CD Pipeline
* **Problem:** `.gitlab-ci.yml` only ran `echo` statements and didn't actually build, test, or deploy the code.
* **Fix:** Restructured the pipeline into 4 clear stages (`lint`, `build`, `test`, `deploy`) so every commit builds the container, runs a quick health test, and applies the changes via Terraform on `main`.
