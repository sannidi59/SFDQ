pipeline {
    agent any

    environment {
        // You can define environment variables here if needed.
        // E.g.: DATABASE_URL = 'your-test-database-url'
    }

    stages {
        stage('Checkout') {
            steps {
                // Pull the latest code from the repository
                checkout scm
            }
        }

        stage('Set up environment') {
            steps {
                // Set up a virtual environment and install dependencies
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest tests/ --junitxml=test-results.xml
                '''
            }
        }
    }

    post {
        always {
            // Publish test results to Jenkins dashboard
            junit '**/test-results.xml'
        }
        success {
            echo 'Tests completed successfully!'
        }
        failure {
            echo 'Tests failed!'
        }
    }
}
