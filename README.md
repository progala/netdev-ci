# NetDev CI

## General notes

Example of a simple NetDev CI pipeline with Gitlab.

- Gitlab pipeline uses local runner and virtual Python environment.

- Pipeline scripts rely on Python Invoke tasks in `tasks.py`

- Pre-checks run with Python pre-commit.

## Pipeline overview

- Prepare environment (Python venv and dependencies)
- Static checks (black and ansible-lint)
- Deploy lab using Ansible, Docker and vrnetlab
- Configure connections (Docker + vrnetlab) and apply config with Ansible + Napalm
- Validate deployment using Ansible and Napalm validate
- Tear down the lab