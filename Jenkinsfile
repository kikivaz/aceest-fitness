pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Clean Build') {
            steps {
                sh 'docker build --no-cache -t aceest-fitness:jenkins .'
            }
        }
        stage('Test') {
            steps {
                sh 'docker build --target test -t aceest-fitness:jenkins-test .'
                sh 'docker run --rm aceest-fitness:jenkins-test'
            }
        }
    }

    post {
        always {
            sh 'docker image prune -f || true'
        }
    }
}
