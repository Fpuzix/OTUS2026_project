pipeline {
    agent any

    parameters {
        choice(
            name: 'TEST_SCOPE',
            choices: ['all', 'api', 'ui'],
            description: 'Which tests to run'
        )
        booleanParam(
            name: 'HEADLESS',
            defaultValue: true,
            description: 'Run UI tests in headless mode'
        )
        string(
            name: 'BASE_UI_URL',
            defaultValue: 'https://www.saucedemo.com/',
            description: 'Base URL for UI tests'
        )
        string(
            name: 'BASE_API_URL',
            defaultValue: 'https://httpbin.org',
            description: 'Base URL for API tests'
        )
    }

    environment {
        VENV_DIR = '.venv'
        ALLURE_DIR = 'allure-results'
        JUNIT_API_FILE = 'junit-api.xml'
        JUNIT_UI_FILE = 'junit-ui.xml'
    }

    stages {
        stage('Setup') {
            steps {
                sh '''
                    rm -rf "${VENV_DIR}" "${ALLURE_DIR}" "${JUNIT_API_FILE}" "${JUNIT_UI_FILE}"

                    python3 -m venv "${VENV_DIR}"
                    . "${VENV_DIR}/bin/activate"

                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run API tests') {
            when {
                anyOf {
                    expression { params.TEST_SCOPE == 'all' }
                    expression { params.TEST_SCOPE == 'api' }
                }
            }
            steps {
                sh """
                    . "${VENV_DIR}/bin/activate"
                    pytest tests/api -v \
                      --base-api-url="${params.BASE_API_URL}" \
                      --junitxml="${JUNIT_API_FILE}" \
                      --alluredir="${ALLURE_DIR}"
                """
            }
        }

        stage('Run UI tests') {
            when {
                anyOf {
                    expression { params.TEST_SCOPE == 'all' }
                    expression { params.TEST_SCOPE == 'ui' }
                }
            }
            steps {
                script {
                    if (params.HEADLESS) {
                        sh """
                            . "${VENV_DIR}/bin/activate"
                            pytest tests/ui -v \
                              --headless \
                              --base-ui-url="${params.BASE_UI_URL}" \
                              --junitxml="${JUNIT_UI_FILE}" \
                              --alluredir="${ALLURE_DIR}"
                        """
                    } else {
                        sh """
                            . "${VENV_DIR}/bin/activate"
                            pytest tests/ui -v \
                              --base-ui-url="${params.BASE_UI_URL}" \
                              --junitxml="${JUNIT_UI_FILE}" \
                              --alluredir="${ALLURE_DIR}"
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'junit-*.xml'
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
            allure([
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']],
                commandline: 'allure'
            ])
        }
        success {
            echo 'Сборка успешна!'
        }
        failure {
            echo '!!!!!! Сборка провалена !!!!!!'
        }
    }
}