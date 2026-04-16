pipeline {
    agent any

    parameters {
        booleanParam(name: 'HEADLESS', defaultValue: true, description: 'Run UI tests in headless mode')
    }

    environment {
        VENV_DIR = 'venv'
        ALLURE_DIR = 'allure-results'
        JUNIT_FILE = 'junit.xml'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Клонирование репозитория...'
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                echo 'Установка зависимостей...'
                bat '''
                    if exist %VENV_DIR% rmdir /s /q %VENV_DIR%
                    if exist %ALLURE_DIR% rmdir /s /q %ALLURE_DIR%
                    if exist %JUNIT_FILE% del /f /q %JUNIT_FILE%

                    python -m venv %VENV_DIR%
                    call %VENV_DIR%\\Scripts\\activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run API tests') {
            steps {
                echo 'Запуск API тестов...'
                bat '''
                    call %VENV_DIR%\\Scripts\\activate
                    pytest tests\\api -v --junitxml=%JUNIT_FILE% --alluredir=%ALLURE_DIR%
                '''
            }
        }

        stage('Run UI tests') {
            steps {
                echo 'Запуск UI тестов...'
                script {
                    if (params.HEADLESS) {
                        bat '''
                            call %VENV_DIR%\\Scripts\\activate
                            pytest tests\\ui -v --headless --alluredir=%ALLURE_DIR%
                        '''
                    } else {
                        bat '''
                            call %VENV_DIR%\\Scripts\\activate
                            pytest tests\\ui -v --alluredir=%ALLURE_DIR%
                        '''
                    }
                }
            }
        }

        stage('Lint') {
            steps {
                echo 'Проверка качества кода...'
                bat '''
                    call %VENV_DIR%\\Scripts\\activate
                    ruff check . || exit /b 0
                '''
            }
        }
    }

    post {
        always {
            echo 'Публикация отчетов...'
            junit allowEmptyResults: true, testResults: 'junit.xml'
            allure includeProperties: false,
                   jdk: '',
                   results: [[path: 'allure-results']]
        }
        success {
            echo '!Сборка успешна!'
        }
        failure {
            echo '!!!!!! Сборка провалена !!!!!!'
        }
    }
}