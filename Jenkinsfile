pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'gestion-budget'
        DOCKER_REGISTRY = 'https://index.docker.io/v1/'
        DOCKER_CREDENTIALS_ID = 'docker'
        DOCKER_USERNAME = 'yaogameli'
        COMMITHASH = "${env.GIT_COMMIT?.take(7) ?: 'unknown'}"
        CONTAINER_NAME = 'my-flask-app'
        CONTAINER_PORT = '5010'

        // Paramètres de déploiement
        SSH_CREDENTIALS_ID = 'jenkins-ssh-key'
        PRODUCTION_SERVER = 'yao@192.168.1.46'

        // Paramètre de l'application
        APP_NAME = 'Suivi_des_depenses'

        // gestion des ressources
        CONTAINER_CPU = '512'
        CONTAINER_MEMORY = '512M'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${env.BUILD_ID}")
                }
            }
        }

        stage('Test') {
            when {
                branch 'dev'
            }
            steps {
                script {
                    sh 'echo "Running tests"'
                    // docker.image("${DOCKER_IMAGE}:${env.BUILD_ID}").inside {
                    //     sh 'python -m unittest discover'
                    // }
                }
            }
        }

        stage('Deploy in Test Environment') {
            when {
                branch 'dev'
            }
            steps {
                script {
                    sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker run -d --name ${CONTAINER_NAME} -p ${CONTAINER_PORT}:${CONTAINER_PORT} ${DOCKER_IMAGE}:${env.BUILD_ID}
                    """
                }
            }
        }

        stage('Push Docker Image to Dev') {
            when {
                branch 'dev'
            }
            steps {
                script {
                    docker.withRegistry("${DOCKER_REGISTRY}", "${DOCKER_CREDENTIALS_ID}") {
                        def dockerImage = docker.build("${DOCKER_USERNAME}/${DOCKER_IMAGE}:${COMMITHASH}", "./")
                        dockerImage.push()
                        dockerImage.push("dev")
                    }
                }
            }
        }

        stage('Build and Push Docker Image to Main') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry("${DOCKER_REGISTRY}", "${DOCKER_CREDENTIALS_ID}") {
                        def dockerImage = docker.build("${DOCKER_USERNAME}/${DOCKER_IMAGE}:${COMMITHASH}", "--no-cache .")
                        dockerImage.push()
                        dockerImage.push("latest")
                    }
                }
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                sshagent([SSH_CREDENTIALS_ID]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ${PRODUCTION_SERVER} '
                        docker pull ${DOCKER_USERNAME}/${DOCKER_IMAGE}:${COMMITHASH}
                        docker stop ${APP_NAME} || true
                        docker rm ${APP_NAME} || true
                        docker run -d --name ${APP_NAME} \\
                            -p ${CONTAINER_PORT}:${CONTAINER_PORT} \\
                            --restart unless-stopped \\
                            --cpu-shares=${CONTAINER_CPU} \\
                            --memory=${CONTAINER_MEMORY} \\
                            -e APP_PORT=${CONTAINER_PORT} \\
                            -v gestion-budget-db-data:/app/instance \\
                            ${DOCKER_USERNAME}/${DOCKER_IMAGE}:${COMMITHASH}
                    '
                    """
                }
            }
        }

        stage('Verify Deployment') {
            when {
                branch 'main'
            }
            steps {
                sshagent([SSH_CREDENTIALS_ID]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ${PRODUCTION_SERVER} << EOF
                        if docker ps | grep -q ${APP_NAME}; then
                            echo "Déploiement réussi: ${APP_NAME} est en cours d'exécution"
                        else
                            echo "Échec du déploiement: ${APP_NAME} n'est pas en cours d'exécution"
                            exit 1
                        fi
EOF
                    """
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline exécuté avec succès!'
        }
        failure {
            echo "Échec durant l'exécution du pipeline. Vérifiez les logs SVP."
        }
    }
}
