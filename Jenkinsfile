pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-credentials'   // Jenkins Credential에 등록된 Docker Hub 계정
        IMAGE_NAME = 'yorange50/fastapi-app'         // ← 본인 Docker Hub repo
        REMOTE_USER = 'ubuntu'
        REMOTE_HOST = '3.34.155.126'                      // ← 배포 서버
        REMOTE_PATH = '/home/ubuntu'
        CONTAINER_NAME = 'fastapi-app'
        EXTERNAL_PORT = '5001'
        INTERNAL_PORT = '5001'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Greenapple0101/FastApi_Todos.git', branch: 'main'
            }
        }

        stage('Build') {
            steps {
                script {
                    // repo root에서 Dockerfile을 바로 빌드 (Dockerfile이 최상위에 있으니 OK)
                    docker.build("${IMAGE_NAME}:latest")
                }
            }
        }

        stage('Push') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        docker.image("${IMAGE_NAME}:latest").push()
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sshagent(credentials: ['ubuntu']) {
                        sh """
                        ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} << 'EOF'
                        
                        # 기존 컨테이너 삭제 (있으면)
                        docker rm -f ${CONTAINER_NAME} || true
                        # 최신 이미지 pull
                        docker pull ${IMAGE_NAME}:latest
                        # 새 컨테이너 실행
                        docker run -d --name ${CONTAINER_NAME} -p ${EXTERNAL_PORT}:${INTERNAL_PORT} ${IMAGE_NAME}:latest
                        exit
                        EOF
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo "✅ 배포 완료!"
            echo "🌐 접속: http://${REMOTE_HOST}:${EXTERNAL_PORT}"
        }
        failure {
            echo "❌ 배포 실패. Jenkins Console Output 확인 바랍니다."
        }
    }
}
