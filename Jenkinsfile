pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'gestion-budget'
        DOCKER_REGISTRY = 'https://index.docker.io/v1/'
        DOCKER_CREDENTIALS_ID = 'docker'
        COMMITHASH = env.GIT_COMMIT.take(7) 
        CONTAINER_NAME = 'my-flask-app'
        CONTAINER_PORT = '5010'
    }

    stages {
        //stage('Clone Repository') {
            //steps {
                //git branch: 'main', url: 'https://github.com/your-username/your-flask-repo.git'
            //}
        //}

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${env.BUILD_ID}")
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    sh 'echo test'
                    //docker.image("${DOCKER_IMAGE}:${env.BUILD_ID}").inside {
                        //sh 'python -m unittest discover'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Démarrage du conteneur dans l'environnement de test
                    sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker run -d --name ${CONTAINER_NAME} -p ${CONTAINER_PORT}:${CONTAINER_PORT} ${DOCKER_IMAGE}:${env.BUILD_ID}
                    """
                }
            }
        }
    

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry("${DOCKER_REGISTRY}", "${DOCKER_CREDENTIALS_ID}") {
                        def dockerImage = docker.build("yaogameli/${DOCKER_IMAGE}:${COMMITHASH}", "./")
                        dockerImage.push()
                        dockerImage.push("latest")
                    }
                }
            }
        }

    }

    post {
        always {
            cleanWs()
        }
    }
}




