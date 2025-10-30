pipeline {
  agent any

  triggers {
    // Schedule: run daily at 2:30am (example). Change cron as needed.
    // Format: MIN HOUR DOM MON DOW
    cron('30 2 * * *')

    // GitHub webhook trigger (requires GitHub plugin & job set to "GitHub hook trigger for GITScm polling")
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
          pytest -q
        '''
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: '**/test-*.xml' // optional if generating junit xml
        }
      }
    }

    stage('Package') {
      steps {
        sh '''
          # create a zip package (artifact)
          rm -f build.zip
          zip -r build.zip app run.sh README.md requirements.txt
          ls -l build.zip
        '''
        archiveArtifacts artifacts: 'build.zip', fingerprint: true
      }
    }

    stage('Deploy') {
      steps {
        // requires jenkins user has sudo rights for the deploy commands or use ssh to remote host
        sh '''
          echo "Deploying to ${DEPLOY_DIR}"
          sudo mkdir -p ${DEPLOY_DIR}
          sudo chown -R $(whoami):$(whoami) ${DEPLOY_DIR}
          sudo rm -rf ${DEPLOY_DIR}/*
          sudo cp -r app run.sh requirements.txt ${DEPLOY_DIR}/
          sudo chown -R simpleapp:simpleapp ${DEPLOY_DIR} || true
        '''
        // restart systemd service (if applicable)
        sh 'sudo systemctl restart simple-add.service || true'
      }
    }
    stage('Test') {
	    steps {
		sh '''
		. .venv/bin/activate
		pytest -q --junitxml=report.xml
		'''
	    }
	    post {
		always {
		    junit 'report.xml'
		}
	    }
	}

  }

  post {
    always {
      // Clean workspace (needs Workspace Cleanup plugin)
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

