pipeline {
    agent any

    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['all', 'api', 'ui', 'demo'],
            description: 'Какой набор тестов запускать'
        )
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'stage', 'prod'],
            description: 'Окружение для запуска тестов'
        )
    }

    triggers {
        cron('H 2 * * *')
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 1, unit: 'HOURS')
        timestamps()
    }

    environment {
        PYTHONIOENCODING = 'UTF-8'
    }

    stages {
        stage('Setup') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat
                    flake8 . --output-file=flake8.log --exit-zero --exclude=venv
                '''
            }
        }

        stage('Test') {
            steps {
                script {
                    def cmd = 'pytest tests/ -v -m "api or ui"'
                    if (params.TEST_SUITE == 'api') {
                        cmd = 'pytest tests/ -v -m api'
                    } else if (params.TEST_SUITE == 'ui') {
                        cmd = 'pytest tests/ -v -m ui'
                    } else if (params.TEST_SUITE == 'demo') {
                        cmd = 'pytest tests/ -v -m demo'
                    }
                    bat """
                        call venv\\Scripts\\activate.bat
                        ${cmd} --junitxml=results.xml --alluredir=allure-results
                    """
                }
            }
        }

        stage('Deploy') {
            when {
                allOf {
                    branch 'main'
                    expression { params.ENVIRONMENT == 'prod' }
                }
            }
            steps {
                input message: 'Задеплоить в prod?', ok: 'Deploy'
                echo 'Деплой выполнен'
            }
        }
    }

    post {
        always {
            junit testResults: 'results.xml', allowEmptyResults: true
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            archiveArtifacts artifacts: 'flake8.log, results.xml, allure-results/**', allowEmptyArchive: true
        }
    }
}