pipeline {
  agent any

  triggers {
    // Run daily at 2:30am
    cron('30 2 * * *')
    // Trigger on GitHub push
    githubPush()
  }

  environment {
    DEPLOY_DIR = "/opt/simple-add-app"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python') {
      steps {
        sh '''
          python3 -V
          python3 -m venv .venv
          . .venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Test') {
      steps {
        sh '''
          . .venv/bin/activate
          export PYTHONPATH=$WORKSPACE
          pytest -q --junitxml=report.xml
        '''
      }
      post {
        always {
          junit 'report.xml'
        }
      }
    }

    stage('Package') {
      steps {
        sh '''
          rm -f build.zip
          zip -r build.zip app run.sh README.md requirements.txt || true
          ls -l build.zip
        '''
        archiveArtifacts artifacts: 'build.zip', fingerprint: true
      }
    }

    stage('Deploy') {
      steps {
        sh '''
          echo "Deploying to ${DEPLOY_DIR}"
          sudo mkdir -p ${DEPLOY_DIR}
          sudo chown -R $(whoami):$(whoami) ${DEPLOY_DIR}
          sudo rm -rf ${DEPLOY_DIR}/*
          sudo cp -r app run.sh requirements.txt ${DEPLOY_DIR}/ || true
          sudo chown -R simpleapp:simpleapp ${DEPLOY_DIR} || true
          sudo systemctl restart simple-add.service || true
        '''
      }
    }
  }

  post {
    always {
      cleanWs()
    }
    success {
      echo "Build and deploy succeeded"
    }
    failure {
      echo "Build failed"
    }
  }
}

