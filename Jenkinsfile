pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/kikivaz/aceest-fitness.git'
        IMAGE_NAME = 'aceest-fitness:jenkins'
        TEST_IMAGE = 'aceest-fitness:jenkins-test'
        SAFE_DIR = '/var/jenkins_home/workspace/fitness_app'
    }

    stages {
        stage('Prepare Workspace') {
            steps {
                echo "🧩 Marking workspace as safe for Git..."
                sh "git config --global --add safe.directory '${SAFE_DIR}' || true"
            }
        }

        stage('Checkout') {
            steps {
                echo "📥 Checking out code from ${REPO_URL}..."
                checkout([$class: 'GitSCM',
                          branches: [[name: '*/main']],
                          userRemoteConfigs: [[url: "${REPO_URL}"]]
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🔨 Building Docker image..."
                sh "docker build --no-cache --progress=plain -t ${IMAGE_NAME} ."
            }
        }

        stage('Run Tests') {
            steps {
                echo "🧪 Running tests..."
                sh "docker build --target test --progress=plain -t ${TEST_IMAGE} ."
                sh "docker run --rm ${TEST_IMAGE}"
            }
        }
    }

    post {
        success {
            echo "✅ Build and tests passed successfully!"
        }
        failure {
            echo "❌ Build or tests failed."
        }
        always {
            echo "🧹 Cleaning up Docker images..."
            sh "docker image prune -f || true"
        }
    }
}
