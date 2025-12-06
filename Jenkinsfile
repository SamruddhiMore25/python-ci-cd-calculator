pipeline {

    agent { label 'Jenkins-Agent' }

    environment {
        PYTHON_VERSION = '3.12.3'
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

    } // end stages

} // end pipeline
