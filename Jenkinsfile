pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh './hydra-report.py  accounting/201805??'
      }
    }
    stage('Tests') {
      steps {
        echo 'Faire les tests'
      }
    }
    stage('Deploy') {
      steps {
        sh '''cp /report/201805/ /report-test/201805/
cp /report/201805.html /report-test/201805'''
      }
    }
  }
}