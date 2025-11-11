pipeline {
    agent any

    environment {
        APP_NAME       = "fastapi-app"
        IMAGE_NAME     = "fastapi-todos:latest"
        GIT_REPO       = "https://github.com/Greenapple0101/FastApi_Todos.git"
        BRANCH         = "main"
        CONTAINER_PORT = "5001"
        HOST_PORT      = "5001"
    }

    stages {
        stage('Checkout Source') {
            steps {
                echo "📦 Pulling source code from ${GIT_REPO}"
                git branch: "${BRANCH}", url: "${GIT_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image ${IMAGE_NAME}"
                sh """
                    docker build -t ${IMAGE_NAME} .
                """
            }
        }

        stage('Stop Old Container') {
            steps {
                echo "🧹 Stopping old container if it exists"
                sh """
                    docker rm -f ${APP_NAME} || true
                """
            }
        }

        stage('Run New Container') {
            steps {
                echo "🚀 Running container ${APP_NAME}"
                sh """
                    docker run -d \
                        --name ${APP_NAME} \
                        -p ${HOST_PORT}:${CONTAINER_PORT} \
                        ${IMAGE_NAME}
                """
            }
        }
    }

    post {
        success {
            echo "✅ Deployment completed successfully!"
            echo "🌐 Application is available at http://localhost:${HOST_PORT}"
        }
        failure {
            echo "❌ Deployment failed. Check Jenkins console output."
        }
    }
}

