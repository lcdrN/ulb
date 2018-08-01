pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh './hydra-report.py  /home/noe/Desktop/script/sisc-scripts/accounting/201805??'
      }
    }
    stage('Tests') {
      steps {
        echo 'Faire les tests'
        sh '''ls
cd ../
ls
cd ../
ls'''
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