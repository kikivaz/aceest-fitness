pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo "📥 Checking out code from GitHub..."
                checkout([$class: 'GitSCM',
                          branches: [[name: '*/main']],
                          userRemoteConfigs: [[url: 'https://github.com/kikivaz/aceest-fitness.git']]
                ])
            }
        }

        stage('Clean Build') {
            steps {
                echo "🔨 Building Docker image (no cache)..."
                sh 'docker build --no-cache -t aceest-fitness:jenkins .'
            }
        }

        stage('Test') {
            steps {
                echo "🧪 Running tests inside Docker..."
                sh 'docker build --target test -t aceest-fitness:jenkins-test .'
                sh 'docker run --rm aceest-fitness:jenkins-test'
            }
        }
    }

    post {
        success {
            echo "✅ Build and tests completed successfully!"
        }
        failure {
            echo "❌ Build or tests failed. Check logs above."
        }
        always {
            echo "🧹 Cleaning up unused Docker images..."
            sh 'docker image prune -f || true'
        }
    }
}
