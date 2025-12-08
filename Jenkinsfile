pipeline {

    agent { label 'Jenkins-Agent' }

    environment {
        PYTHON_VERSION = '3.12.3'
        APP_NAME = "python-ci-cd-calculator"
        RELEASE = "1.0.0"
        DOCKER_USER = 'samdocksimages'
        DOCKER_PASS = 'dockerhub-token'
        IMAGE_NAME = "${DOCKER_USER}/${APP_NAME}"
        IMAGE_TAG = "${RELEASE}-${BUILD_NUMBER}"
    }

    stages {

        stage('CI - Checkout from SCM') {
            steps {
                cleanWs()
                git branch: 'main',
                    credentialsId: 'github',
                    url: 'https://github.com/SamruddhiMore25/python-ci-cd-calculator'
            }
        }

        stage('CI - Build and Test Python code') {
            steps {
                sh '''
                    export TESTING=1
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pytest || python -m pytest
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube-server') {
                    script {
                        def scannerHome = tool 'sonarqube-scanner'
                        withCredentials([string(credentialsId: 'jenkins-sonarqube-token',
                                                variable: 'SONAR_TOKEN')]) {
                            sh'''
                            echo "Using Node:" 
                            /usr/bin/node -v
                            '''
                            sh """
                                ${scannerHome}/bin/sonar-scanner \
                                    -Dsonar.projectKey=python-calculator \
                                    -Dsonar.sources=. \
                                    -Dsonar.host.url=http://172.31.20.87:9000 \
                                    -Dsonar.login=$SONAR_TOKEN \
                                    -Dsonar.nodejs.executable=/usr/bin/node
                            """
                        } // end withCredentials
                    } // end script
                } // end withSonarQubeEnv
            }
        }
        stage('Quality Gate') {
            steps {
                script {
                    waitForQualityGate abortPipeline: false
                }
            }
        }
        stage('Build & Push Docker Image') {
            steps {
                script {

                    // Read credentials from Jenkins Credentials Store
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-token', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {

                        // Name/tag for the image
                        def appImage = docker.build("${IMAGE_NAME}:${IMAGE_TAG}")

                        // Login
                        sh """
                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        """

                        // Push tagged image
                        sh """
                            docker build -t $DOCKER_USER/python-calculator:$IMAGE_TAG .
                            docker push $DOCKER_USER/python-calculator:$IMAGE_TAG
                            docker tag $DOCKER_USER/python-calculator:$IMAGE_TAG $DOCKER_USER/python-calculator:latest
                            docker push $DOCKER_USER/python-calculator:latest
                        """

                        // Logout
                        sh "docker logout"
                    }
                }
            }
        }

    } // end stages

} // end pipeline
