# Практическое занятие 53: Конвейеры CI/CD

## Непрерывная интеграция, непрерывная доставка, непрерывное развёртывание, автоматизация

### Цель занятия:
Изучить принципы CI/CD, научиться создавать конвейеры непрерывной интеграции и развёртывания, освоить инструменты автоматизации.

### Задачи:
1. Понять принципы CI/CD
2. Освоить основные инструменты CI/CD
3. Научиться создавать конвейеры
4. Настроить автоматическое развёртывание

### План работы:
1. Введение в CI/CD
2. Основные понятия
3. GitHub Actions
4. GitLab CI
5. Jenkins
6. Практические задания

---

## 1. Введение в CI/CD

CI/CD - это набор практик, направленных на автоматизацию процессов разработки, тестирования и развёртывания программного обеспечения.

### Этапы CI/CD:

```
Разработка → Коммит → CI → CD → Деплой → Мониторинг
                    ↓
              Тестирование
                    ↓
              Сборка
                    ↓
              Артефакты
```

### Типы CI/CD:

1. **CI (Continuous Integration)** - непрерывная интеграция
   - Автоматическая сборка при каждом коммите
   - Автоматическое тестирование
   - Проверка качества кода

2. **CD (Continuous Delivery)** - непрерывная доставка
   - Автоматическое развёртывание в тестовой среде
   - Готовность к развёртыванию в production
   - Ручной деплой в production

3. **CD (Continuous Deployment)** - непрерывное развёртывание
   - Полностью автоматическое развёртывание
   - Автоматический деплой после успешных тестов

---

## 2. Основные инструменты CI/CD

| Инструмент | Особенности |
|------------|-------------|
| GitHub Actions | Интегрирован в GitHub, бесплатен для открытых проектов |
| GitLab CI | Встроен в GitLab, мощный и гибкий |
| Jenkins | Открытый код, огромное количество плагинов |
| CircleCI | Облачный сервис, быстрая настройка |
| Travis CI | Простота настройки, бесплатен для открытых проектов |
| Azure DevOps | Интеграция с Azure, корпоративные функции |

---

## 3. GitHub Actions

### Пример 1: Базовый workflow

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run linter
        run: |
          pip install flake8
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
      
      - name: Run tests
        run: |
          pytest --cov=. --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

### Пример 2: Workflow с несколькими этапами

```yaml
# .github/workflows/full-ci-cd.yml
name: Full CI/CD Pipeline

on:
  push:
    branches: [ main ]
  release:
    types: [ published ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install flake8 black isort
      
      - name: Check formatting
        run: |
          black --check .
          isort --check .
      
      - name: Run linter
        run: flake8 . --count --show-source --statistics

  test:
    needs: lint
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run tests
        run: pytest --cov=. --cov-report=xml --junitxml=test-results.xml
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results-${{ matrix.python-version }}
          path: test-results.xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=sha,prefix=
            type=raw,value=latest,enable={{is_default_branch}}
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
          cache-to: type=inline

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name == 'release'
    
    steps:
      - name: Deploy to production
        run: |
          echo "Deploying image ${{ needs.build.outputs.image-tag }}"
          # Здесь команды деплоя
```

### Пример 3: Workflow для pull requests

```yaml
# .github/workflows/pr.yml
name: Pull Request Pipeline

on:
  pull_request:
    types: [ opened, synchronize, reopened ]

jobs:
  pr-checks:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
      
      - name: Run type checker
        run: mypy .
      
      - name: Run security audit
        run: pip-audit || true
      
      - name: Comment PR with test results
        uses: actions/github-script@v6
        with:
          script: |
            const { data: comments } = await github.rest.issues.listComments({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number
            });
            
            const botComment = comments.find(c => c.user.type === 'Bot');
            
            const body = `✅ PR checks passed`;
            
            if (botComment) {
              await github.rest.issues.updateComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                comment_id: botComment.id,
                body
              });
            } else {
              await github.rest.issues.createComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: context.issue.number,
                body
              });
            }
```

---

## 4. GitLab CI

### Пример 4: .gitlab-ci.yml

```yaml
stages:
  - lint
  - test
  - build
  - deploy

variables:
  DOCKER_IMAGE: registry.gitlab.com/$CI_PROJECT_PATH
  DOCKER_DRIVER: overlay2

default:
  image: python:3.11-slim
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - .cache/pip

lint:
  stage: lint
  script:
    - pip install flake8 black isort
    - black --check .
    - isort --check .
    - flake8 . --count --show-source --statistics
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH

test:unit:
  stage: test
  script:
    - pip install -r requirements.txt
    - pip install -r requirements-dev.txt
    - pytest --junitxml=report.xml --cov=. --cov-report=xml
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    when: always
    reports:
      junit: report.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH

test:integration:
  stage: test
  services:
    - postgres:15
    - redis:7
  variables:
    POSTGRES_DB: test
    POSTGRES_USER: test
    POSTGRES_PASSWORD: test
    DATABASE_URL: postgresql://test:test@postgres:15/test
    REDIS_URL: redis://redis:6379
  script:
    - pip install -r requirements.txt
    - pip install -r requirements-dev.txt
    - pytest tests/integration -v
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

build:docker:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $DOCKER_IMAGE:$CI_COMMIT_SHA .
    - docker push $DOCKER_IMAGE:$CI_COMMIT_SHA
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
    - if: $CI_COMMIT_TAG

deploy:staging:
  stage: deploy
  image: alpine:latest
  script:
    - apk add --no-cache curl
    - curl -X POST $STAGING_WEBHOOK_URL
  environment:
    name: staging
    url: https://staging.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"

deploy:production:
  stage: deploy
  image: alpine:latest
  script:
    - apk add --no-cache curl
    - curl -X POST $PRODUCTION_WEBHOOK_URL
  environment:
    name: production
    url: https://example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  when: manual
```

---

## 5. Jenkins

### Пример 5: Jenkinsfile

```groovy
// Jenkinsfile
pipeline {
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
                docker {
                    image 'python:3.11-slim'
                    reuseNode true
                }
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
                        docker {
                            image 'python:3.11-slim'
                            reuseNode true
                        }
                    }
                    steps {
                        sh '''
                            pip install -r requirements.txt
                            pip install -r requirements-dev.txt
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
                
                stage('Integration Tests') {
                    agent {
                        docker {
                            image 'python:3.11-slim'
                            reuseNode true
                        }
                    }
                    environment {
                        DATABASE_URL = credentials('database-url')
                    }
                    steps {
                        sh '''
                            pip install -r requirements.txt
                            pip install -r requirements-dev.txt
                            pytest tests/integration -v
                        '''
                    }
                }
            }
        }
        
        stage('Build Docker') {
            steps {
                script {
                    def imageTag = "${env.BUILD_NUMBER}-${env.GIT_COMMIT.take(7)}"
                    env.IMAGE_TAG = imageTag
                    
                    docker.build("${DOCKER_IMAGE}:${imageTag}")
                }
            }
        }
        
        stage('Push to Registry') {
            steps {
                script {
                    docker.withRegistry('https://docker.io', 'docker-hub-credentials') {
                        docker.image("${DOCKER_IMAGE}:${env.IMAGE_TAG}").push()
                        docker.image("${DOCKER_IMAGE}:latest").push()
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                sh '''
                    kubectl set image deployment/myapp myapp=${DOCKER_IMAGE}:${IMAGE_TAG} -n staging
                '''
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to production?', ok: 'Deploy'
                sh '''
                    kubectl set image deployment/myapp myapp=${DOCKER_IMAGE}:${IMAGE_TAG} -n production
                '''
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            slackSend(color: 'good', message: "Build ${env.JOB_NAME} #${env.BUILD_NUMBER} succeeded")
        }
        failure {
            slackSend(color: 'danger', message: "Build ${env.JOB_NAME} #${env.BUILD_NUMBER} failed")
        }
    }
}
```

---

## 6. Практические задания

### Задание 1: Настройка GitHub Actions

Создайте GitHub Actions workflow для Python проекта:
- Линтинг кода (flake8, black)
- Юнит-тесты с pytest
- Сборка Docker образа
- Публикация в GitHub Container Registry

### Задание 2: CI/CD Pipeline

Настройте полный CI/CD pipeline:
- Автоматический запуск при push в ветку develop
- Статический анализ кода
- Запуск тестов
- Деплой в staging среду
- Деплой в production только после релиза

### Задание 3: Тестирование в CI

Добавьте различные типы тестов в pipeline:
- Unit тесты
- Интеграционные тесты
- E2E тесты
- Нагрузочное тестирование

### Задание 4: Безопасность в CI

Интегрируйте инструменты безопасности:
- Сканирование уязвимостей зависимостей (pip-audit)
- Проверка секретов в коде (git-secrets)
- Сканирование Docker образов (Trivy)

### Задание 5: GitOps

Настройте GitOps подход:
- Хранение конфигурации в Git
- Автоматический деплой при изменениях
- Синхронизация состояния

---

## Контрольные вопросы:

1. В чём разница между Continuous Integration, Continuous Delivery и Continuous Deployment?
2. Какие инструменты CI/CD вы знаете?
3. Зачем нужны stages в pipeline?
4. Как настроить автоматический деплой при push в определённую ветку?
5. Какие практики безопасности следует применять в CI/CD?

---

## Дополнительные материалы:

- GitHub Actions Documentation: https://docs.github.com/en/actions
- GitLab CI/CD Documentation: https://docs.gitlab.com/ee/ci/
- Jenkins Documentation: https://www.jenkins.io/doc/
