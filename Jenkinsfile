pipeline {
  agent {
    kubernetes {
      yaml """
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins
  volumes:
    - name: docker-config
      emptyDir: {}
  containers:
    - name: aws
      image: amazon/aws-cli:2.15.57
      command:
        - sh
        - -c
        - cat
      tty: true
      volumeMounts:
        - name: docker-config
          mountPath: /kaniko/.docker

    - name: kaniko
      image: gcr.io/kaniko-project/executor:v1.23.2-debug
      command:
        - /busybox/cat
      tty: true
      volumeMounts:
        - name: docker-config
          mountPath: /kaniko/.docker

    - name: git
      image: alpine/git:2.45.2
      command:
        - /bin/sh
        - -c
        - cat
      tty: true
"""
    }
  }

  environment {
    AWS_REGION   = "us-east-2"
    ECR_REGISTRY = "167357861486.dkr.ecr.us-east-2.amazonaws.com"
    IMAGE_NAME   = "django-app"
    IMAGE_TAG    = "${BUILD_NUMBER}"

    CHARTS_REPO  = "https://github.com/PiotrJasinski1995/goit-devops-charts.git"
    CHARTS_BRANCH = "final-project"
    CHARTS_FILE  = "charts/django-app/values.yaml"

    GIT_EMAIL    = "piotr.jasinski1995@gmail.com"
    GIT_NAME     = "Piotr Jasinski"
  }

  stages {
    stage('Checkout app repo') {
      steps {
        checkout scm
      }
    }

    stage('Prepare ECR auth') {
      steps {
        container('aws') {
          sh '''
            mkdir -p /kaniko/.docker
            TOKEN=$(aws ecr get-login-password --region ${AWS_REGION})
            cat > /kaniko/.docker/config.json <<EOF
{
  "auths": {
    "${ECR_REGISTRY}": {
      "username": "AWS",
      "password": "${TOKEN}"
    }
  }
}
EOF
          '''
        }
      }
    }

    stage('Build and push image to ECR') {
      steps {
        container('kaniko') {
          sh '''
            /kaniko/executor \
              --context "${WORKSPACE}" \
              --dockerfile "${WORKSPACE}/Dockerfile" \
              --destination "${ECR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}" \
              --cache=true
          '''
        }
      }
    }

    stage('Update charts repo') {
      steps {
        container('git') {
          withCredentials([usernamePassword(credentialsId: 'github-token', usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
            sh '''
              rm -rf charts-repo
              git clone https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/PiotrJasinski1995/goit-devops-charts.git charts-repo
              cd charts-repo
              git checkout ${CHARTS_BRANCH}

              sed -i "s|repository: .*|repository: ${ECR_REGISTRY}/${IMAGE_NAME}|g" ${CHARTS_FILE}
              sed -i "s|tag: .*|tag: ${IMAGE_TAG}|g" ${CHARTS_FILE}

              git config user.email "${GIT_EMAIL}"
              git config user.name "${GIT_NAME}"

              git add ${CHARTS_FILE}
              git commit -m "ci: update django-app image tag to ${IMAGE_TAG}" || echo "No changes to commit"
              git push origin ${CHARTS_BRANCH}
            '''
          }
        }
      }
    }
  }
}