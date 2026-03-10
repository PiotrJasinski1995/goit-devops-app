# GoIT DevOps Application Repository

This repository contains the **Django application used in the CI/CD pipeline project**.

The application is automatically built and deployed using:

- Jenkins
- Docker
- Amazon ECR
- Helm
- Argo CD
- Kubernetes (EKS)

---

# Related repositories

Infrastructure repository  
https://github.com/PiotrJasinski1995/goit-devops-infra

Helm charts repository  
https://github.com/PiotrJasinski1995/goit-devops-charts

---

# Repository purpose

This repository contains:

- Django application source code
- Dockerfile used to build the container image
- Jenkins pipeline configuration

The Jenkins pipeline automatically builds and publishes the Docker image and updates the Helm chart repository.

---

# Repository structure

```
.
├── app/
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
└── docker-compose.yaml
```

---

# Docker image build

The application image is built using the Dockerfile in this repository.

Example build command:

```
docker build -t django-app .
```

In the CI/CD pipeline the image is built automatically by **Jenkins** and pushed to **Amazon ECR**.

---

# Jenkins pipeline

The CI/CD pipeline is defined in the `Jenkinsfile`.

Pipeline workflow:

1. Jenkins checks out this repository
2. Builds a Docker image from the Dockerfile
3. Pushes the image to Amazon ECR
4. Updates the image tag in the Helm chart repository
5. Pushes the updated `values.yaml` file to Git

After the chart is updated, **Argo CD automatically synchronizes the Kubernetes cluster**.

---

# Deployment workflow

The full CI/CD pipeline works as follows:

1. Code changes are pushed to this repository
2. Jenkins builds a new Docker image
3. Jenkins pushes the image to Amazon ECR
4. Jenkins updates the Helm chart repository
5. Argo CD detects the change
6. Kubernetes cluster deploys the new application version automatically

---

# Application deployment

The application is deployed using Helm from the repository:

https://github.com/PiotrJasinski1995/goit-devops-charts

The deployment configuration is located in:

```
charts/django-app/values.yaml
```

The image tag is automatically updated by Jenkins during the pipeline execution.
