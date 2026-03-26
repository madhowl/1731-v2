#!/usr/bin/env python3
"""
Практическое занятие 53: Конвейеры CI/CD
Решение упражнений
"""

import os
import yaml
import json
from typing import Dict, List, Any


# ==============================================================================
# УПРАЖНЕНИЕ 1: GitHub Actions Workflow
# ==============================================================================

print("=" * 60)
print("Упражнение 1: GitHub Actions Workflow")
print("=" * 60)


def create_github_actions_workflow() -> str:
    """Создание GitHub Actions workflow"""
    
    workflow = {
        'name': 'CI Pipeline',
        'on': {
            'push': {'branches': ['main', 'develop']},
            'pull_request': {'branches': ['main']}
        },
        'jobs': {
            'test': {
                'runs-on': 'ubuntu-latest',
                'steps': [
                    {
                        'name': 'Checkout code',
                        'uses': 'actions/checkout@v4'
                    },
                    {
                        'name': 'Set up Python',
                        'uses': 'actions/setup-python@v4',
                        'with': {'python-version': '3.11'}
                    },
                    {
                        'name': 'Cache dependencies',
                        'uses': 'actions/cache@v3',
                        'with': {
                            'path': '~/.cache/pip',
                            'key': "${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}"
                        }
                    },
                    {
                        'name': 'Install dependencies',
                        'run': 'pip install -r requirements.txt'
                    },
                    {
                        'name': 'Run linter',
                        'run': 'pip install flake8 && flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics'
                    },
                    {
                        'name': 'Run tests',
                        'run': 'pytest --cov=. --cov-report=xml'
                    },
                    {
                        'name': 'Upload coverage',
                        'uses': 'codecov/codecov-action@v3',
                        'with': {'file': './coverage.xml'}
                    }
                ]
            }
        }
    }
    
    return yaml.dump(workflow, default_flow_style=False, sort_keys=False)


print("GitHub Actions Workflow (.github/workflows/ci.yml):")
print(create_github_actions_workflow())


# ==============================================================================
# УПРАЖНЕНИЕ 2: GitLab CI
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 2: GitLab CI")
print("=" * 60)


def create_gitlab_ci() -> str:
    """Создание .gitlab-ci.yml"""
    
    ci_config = {
        'stages': ['lint', 'test', 'build', 'deploy'],
        'variables': {
            'DOCKER_IMAGE': 'registry.gitlab.com/$CI_PROJECT_PATH'
        },
        'lint': {
            'stage': 'lint',
            'image': 'python:3.11-slim',
            'script': [
                'pip install flake8 black isort',
                'black --check .',
                'isort --check .',
                'flake8 . --count --show-source --statistics'
            ]
        },
        'test:unit': {
            'stage': 'test',
            'image': 'python:3.11-slim',
            'script': [
                'pip install -r requirements.txt',
                'pytest --junitxml=report.xml --cov=. --cov-report=xml'
            ],
            'artifacts': {
                'when': 'always',
                'reports': {
                    'junit': 'report.xml',
                    'coverage_report': {
                        'coverage_format': 'cobertura',
                        'path': 'coverage.xml'
                    }
                }
            }
        },
        'test:integration': {
            'stage': 'test',
            'image': 'python:3.11-slim',
            'services': ['postgres:15', 'redis:7'],
            'variables': {
                'POSTGRES_DB': 'test',
                'POSTGRES_USER': 'test',
                'POSTGRES_PASSWORD': 'test',
                'DATABASE_URL': 'postgresql://test:test@postgres:15/test'
            },
            'script': [
                'pip install -r requirements.txt',
                'pytest tests/integration -v'
            ]
        },
        'build:docker': {
            'stage': 'build',
            'image': 'docker:24',
            'services': ['docker:24-dind'],
            'script': [
                'docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY',
                'docker build -t $DOCKER_IMAGE:$CI_COMMIT_SHA .',
                'docker push $DOCKER_IMAGE:$CI_COMMIT_SHA'
            ],
            'rules': [
                {'if': '$CI_COMMIT_BRANCH == "main"'},
                {'if': '$CI_COMMIT_TAG'}
            ]
        },
        'deploy:staging': {
            'stage': 'deploy',
            'image': 'alpine:latest',
            'script': ['apk add --no-cache curl', 'curl -X POST $STAGING_WEBHOOK_URL'],
            'environment': {
                'name': 'staging',
                'url': 'https://staging.example.com'
            },
            'rules': [{'if': '$CI_COMMIT_BRANCH == "develop"'}]
        },
        'deploy:production': {
            'stage': 'deploy',
            'image': 'alpine:latest',
            'script': ['apk add --no-cache curl', 'curl -X POST $PRODUCTION_WEBHOOK_URL'],
            'environment': {
                'name': 'production',
                'url': 'https://example.com'
            },
            'rules': [{'if': '$CI_COMMIT_BRANCH == "main"'}],
            'when': 'manual'
        }
    }
    
    return yaml.dump(ci_config, default_flow_style=False, sort_keys=False)


print("GitLab CI (.gitlab-ci.yml):")
print(create_gitlab_ci())


# ==============================================================================
# УПРАЖНЕНИЕ 3: Jenkins Pipeline
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 3: Jenkins Pipeline")
print("=" * 60)


def create_jenkinsfile() -> str:
    """Создание Jenkinsfile"""
    
    jenkinsfile = '''pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'myapp'
        REGISTRY = 'docker.io'
    }
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Lint') {
            agent {
                docker { image 'python:3.11-slim' }
            }
            steps {
                sh '''
                    pip install flake8 black isort
                    black --check .
                    isort --check .
                    flake8 . --count --show-source --statistics
                '''
            }
        }
        
        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    agent {
                        docker { image 'python:3.11-slim' }
                    }
                    steps {
                        sh '''
                            pip install -r requirements.txt
                            pytest --cov=. --cov-report=xml --junitxml=unit-results.xml
                        '''
                    }
                    post {
                        always {
                            junit 'unit-results.xml'
                            publishHTML(target: [
                                reportDir: 'htmlcov',
                                reportFiles: 'index.html',
                                reportName: 'Coverage Report'
                            ])
                        }
                    }
                }
            }
        }
        
        stage('Build') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:$BUILD_NUMBER .'
            }
        }
        
        stage('Deploy to Staging') {
            when { branch 'develop' }
            steps {
                sh 'docker-compose up -d'
            }
        }
        
        stage('Deploy to Production') {
            when { branch 'main' }
            input {
                message "Deploy to production?"
                ok "Deploy"
            }
            steps {
                sh 'docker-compose -f docker-compose.prod.yml up -d'
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
'''
    return jenkinsfile


print("Jenkins Pipeline (Jenkinsfile):")
print(create_jenkinsfile())


# ==============================================================================
# УПРАЖНЕНИЕ 4: CI/CD Best Practices
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 4: CI/CD Best Practices")
print("=" * 60)


class CICDPipelineBuilder:
    """Построитель CI/CD пайплайнов"""
    
    @staticmethod
    def get_best_practices() -> List[str]:
        return [
            "Коммиты должны быть маленькими и частыми",
            "Каждый коммит должен проходить тесты",
            "Используйте feature branches для разработки",
            "Настройте автоматическое форматирование кода",
            "Включите линтинг в pipeline",
            "Покрытие кода должно быть не менее 80%",
            "Используйте матрицу для тестирования на разных версиях",
            "Кэшируйте зависимости для ускорения сборки",
            "Используйте container registry для хранения образов",
            "Настройте автоматическое развёртывание при merge",
            "Используйте environments (staging, production)",
            "Настройте уведомления о результатах сборки",
            "Включите security scanning в pipeline",
            "Используйте semantic versioning для релизов",
            "Документируйте ваш pipeline"
        ]
    
    @staticmethod
    def get_security_checks() -> List[str]:
        return [
            "Запуск SAST инструментов (Bandit, SonarQube)",
            "Проверка зависимостей на уязвимости (pip-audit, npm audit)",
            "Сканирование контейнеров (Trivy, Clair)",
            "Проверка секретов в коде (GitLeaks)",
            "Валидация Dockerfiles",
            "Проверка политик безопасности"
        ]


practices = CICDPipelineBuilder.get_best_practices()
print("Лучшие практики CI/CD:")
for i, practice in enumerate(practices, 1):
    print(f"  {i}. {practice}")

security_checks = CICDPipelineBuilder.get_security_checks()
print("\nПроверки безопасности в CI/CD:")
for i, check in enumerate(security_checks, 1):
    print(f"  {i}. {check}")


# ==============================================================================
# УПРАЖНЕНИЕ 5: Pipeline Configuration Examples
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 5: Примеры конфигурации")
print("=" * 60)


def create_advanced_workflow() -> Dict[str, Any]:
    """Расширенный workflow с несколькими этапами"""
    
    return {
        'name': 'Full CI/CD Pipeline',
        'on': {
            'push': {'branches': ['main']},
            'release': {'types': ['published']}
        },
        'env': {
            'REGISTRY': 'ghcr.io',
            'IMAGE_NAME': '${{ github.repository }}'
        },
        'jobs': {
            'lint': {
                'runs-on': 'ubuntu-latest',
                'steps': [
                    {'uses': 'actions/checkout@v4'},
                    {'uses': 'actions/setup-python@v4', 'with': {'python-version': '3.11'}},
                    {'run': 'pip install flake8 black isort && black --check . && isort --check . && flake8 .'}
                ]
            },
            'test': {
                'needs': 'lint',
                'runs-on': 'ubuntu-latest',
                'strategy': {
                    'matrix': {'python-version': ['3.9', '3.10', '3.11']}
                },
                'steps': [
                    {'uses': 'actions/checkout@v4'},
                    {'uses': 'actions/setup-python@v4', 'with': {'python-version': '${{ matrix.python-version }}'}},
                    {'run': 'pip install -r requirements.txt && pytest'}
                ]
            },
            'build': {
                'needs': 'test',
                'runs-on': 'ubuntu-latest',
                'outputs': {'image-tag': '${{ steps.meta.outputs.tags }}'},
                'steps': [
                    {'uses': 'actions/checkout@v4'},
                    {'uses': 'docker/setup-buildx-action@v3'},
                    {'uses': 'docker/login-action@v3', 'with': {
                        'registry': '${{ env.REGISTRY }}',
                        'username': '${{ github.actor }}',
                        'password': '${{ secrets.GITHUB_TOKEN }}'
                    }},
                    {'id': 'meta', 'uses': 'docker/metadata-action@v5', 'with': {
                        'images': '${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}',
                        'tags': 'type=ref,event=branch|type=sha|type=raw,value=latest,enable={{is_default_branch}}'
                    }},
                    {'uses': 'docker/build-push-action@v5', 'with': {
                        'context': '.',
                        'push': 'true',
                        'tags': '${{ steps.meta.outputs.tags }}',
                        'cache-from': f'type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest',
                        'cache-to': 'type=inline'
                    }}
                ]
            },
            'deploy': {
                'needs': 'build',
                'runs-on': 'ubuntu-latest',
                'if': 'github.event_name == "release"',
                'steps': [
                    {'run': 'echo "Deploying image ${{ needs.build.outputs.image-tag }}"'}
                ]
            }
        }
    }


print("Расширенный workflow:")
print(yaml.dump(create_advanced_workflow(), default_flow_style=False, sort_keys=False)[:500])


print("\n" + "=" * 60)
print("Все упражнения выполнены!")
print("=" * 60)
