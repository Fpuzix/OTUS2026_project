pipeline {
    agent any

    parameters {
        booleanParam(
            name: 'HEADLESS',
            defaultValue: true,
            description: 'Run UI tests in headless mode'
        )
    }

    environment {
        VENV_DIR = '.venv'
        ALLURE_DIR = 'allure-results'
        JUNIT_FILE = 'junit.xml'
    }

    stages {
        stage('Setup') {
            steps {
                sh '''
                    rm -rf "${VENV_DIR}" "${ALLURE_DIR}" "${JUNIT_FILE}"

                    python3 -m venv "${VENV_DIR}"
                    . "${VENV_DIR}/bin/activate"

                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run API tests') {
            steps {
                sh '''
                    . "${VENV_DIR}/bin/activate"
                    pytest tests/api -v --junitxml="${JUNIT_FILE}" --alluredir="${ALLURE_DIR}"
                '''
            }
        }

        stage('Run UI tests') {
            steps {
                script {
                    if (params.HEADLESS) {
                        sh '''
                            . "${VENV_DIR}/bin/activate"
                            pytest tests/ui -v --headless --alluredir="${ALLURE_DIR}"
                        '''
                    } else {
                        sh '''
                            . "${VENV_DIR}/bin/activate"
                            pytest tests/ui -v --alluredir="${ALLURE_DIR}"
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'junit.xml'
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
            allure([
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']],
                commandline: 'allure'
            ])
        }
    }
}