pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh '''$date= expr ${BUILD_TIMESTAMP} - 1
./hydra-report.py  /home/noe/Desktop/script/sisc-scripts/accounting/$date??'''
      }
    }
    stage('Tests') {
      steps {
        echo 'Faire les tests'
        sh '''ls
ls report/
cd ../
ls
cd ../
ls'''
      }
    }
    stage('Deploy') {
      when {
        branch 'master'
      }
      steps {
        sh '''mkdir report-test
mkdir report-test/${BUILD_TIMESTAMP}
cp -r report/${BUILD_TIMESTAMP}/ report-test/${BUILD_TIMESTAMP}/
cp report/${BUILD_TIMESTAMP}.html report-test/${BUILD_TIMESTAMP}'''
      }
    }
  }
}