pipeline {
    agent any
    options {
        ansiColor('xterm')   // enables colored logs
    }

    stages {
        stage('Checkout') {
            steps {
                echo "📥 Checking out code..."
                checkout([$class: 'GitSCM',
                          branches: [[name: '*/main']],
                          userRemoteConfigs: [[url: 'https://github.com/kikivaz/aceest-fitness.git']]
                ])
            }
        }

        stage('Clean Build') {
            steps {
                echo "🔨 Building Docker image..."
                sh 'docker build --no-cache --progress=plain -t aceest-fitness:jenkins .'
            }
        }

        stage('Test') {
            steps {
                echo "🧪 Running tests..."
                sh 'docker build --target test --progress=plain -t aceest-fitness:jenkins-test .'
                sh 'docker run --rm aceest-fitness:jenkins-test'
            }
        }
    }

    post {
        success {
            echo "✅ Build and tests passed!"
        }
        failure {
            echo "❌ Build or tests failed."
        }
        always {
            echo "🧹 Cleaning up Docker images..."
            sh 'docker image prune -f || true'
        }
    }
}
