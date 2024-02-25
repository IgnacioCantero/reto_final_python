pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS_ID = '1234567890'
        IMAGE_NAME = 'ignaciocantero/reto_final_python'
    }
    stages {
        stage('Clonar Repositorio') {
            steps {
                checkout scm
            }
        }
        stage('Ejecutar Tests') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                pytest
                '''
            }
        }
        stage('Linting') {
            steps {
                sh '''
                . venv/bin/activate
                pip install flake8
                flake8 . --exclude=venv,app/__pycache__,tests/__pycache__,.coverage
                '''
            }
        }
        stage('Construir Imagen Docker') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}:0.0.${env.BUILD_NUMBER}")
                }
            }
        }
        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: DOCKERHUB_CREDENTIALS_ID, passwordVariable: 'DOCKERHUB_PASSWORD', usernameVariable: 'DOCKERHUB_USER')]) {
                    sh "echo $DOCKERHUB_PASSWORD | docker login --username $DOCKERHUB_USER --password-stdin"
                }
            }
        }
        stage('Subir Imagen Docker') {
            steps {
                script {
                    // Obtengo el nombre de la rama desde GIT_BRANCH y limpio el prefijo 'origin/' incluído:
                    def branchName = env.GIT_BRANCH?.replaceAll('origin/', '').trim()
                    echo "La rama actual es: ${branchName}"

                    if (branchName == 'main') {
                        echo "Estamos en la rama main, procediendo a subir la imagen Docker..."
                        docker.image("${IMAGE_NAME}:0.0.${env.BUILD_NUMBER}").push()
                    } else {
                        echo "Esta etapa solo se ejecuta en la rama main."
                    }
                }
            }
        }
    }
}
