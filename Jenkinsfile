pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'gestion-buget'
        DOCKER_REGISTRY = 'https://hub.docker.com/repository/docker/yaogameli/devops/general'
        DOCKER_CREDENTIALS_ID = 'docker'
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

        //stage('Push Docker Image') {
            //steps {
                //script {
                    //docker.withRegistry("${DOCKER_REGISTRY}", "${DOCKER_CREDENTIALS_ID}") {
                        //docker.image("${DOCKER_IMAGE}:${env.BUILD_ID}").push()
                    //}
                //}
            //}
        //}

        stage('Deploy') {
            steps {
                script {
                    // Déployez votre application Docker sur l'environnement souhaité
                    // Par exemple, en utilisant docker-compose ou des commandes Docker CLI
                    sh """
                    docker run -d --name gestion_budget -p 5000:5000 ${DOCKER_IMAGE}:${env.BUILD_ID}
                    """
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



