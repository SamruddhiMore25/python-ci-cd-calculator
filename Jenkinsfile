pipeline {

    agent {  label 'Jenkins-Agent'  }

    environment {
        // Use Python 3.12.3 for the build
        PYTHON_VERSION = '3.12.3'
    }
//--------CI Stages-----------

    stages {

        stage('CI - Checkout from SCM') {
            steps {
                cleanWs()
                // Checkout the latest code from the GitHub repository
                git branch: 'main', credentialsId: 'github', url: 'https://github.com/SamruddhiMore25/python-ci-cd-calculator'
            }
        }
        stage ('CI - Build and Test Python code'){
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    # run tests (we will adjust this to use unittest instead)
                    pytest || python -m pytest
                '''
            }
        }
      }
}
