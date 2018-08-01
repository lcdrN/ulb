pipeline {
  agent any
  stages {
    stage('Tests') {
      steps {
        sh './hydra-report.py  /home/hydra/torque/accounting/$(date -d "2 month ago" "+%Y%m")??'
      }
    }
    stage('Build') {
      when {
        branch 'master'
      }
      steps {
        echo 'Build 6 month'
        sh '''./hydra-report.py  /home/hydra/torque/accounting/$(date -d "1 month ago" "+%Y%m")??
./hydra-report.py  /home/hydra/torque/accounting/$(date -d "2 month ago" "+%Y%m")??
./hydra-report.py  /home/hydra/torque/accounting/$(date -d "3 month ago" "+%Y%m")??
./hydra-report.py  /home/hydra/torque/accounting/$(date -d "4 month ago" "+%Y%m")??
./hydra-report.py  /home/hydra/torque/accounting/$(date -d "5 month ago" "+%Y%m")??
./hydra-report.py  /home/hydra/torque/accounting/$(date -d "6 month ago" "+%Y%m")??'''
      }
    }
    stage('Deploy') {
      when {
        branch 'master'
      }
      steps {
        sh '''mkdir -p report-test/

cp -r report/$(date -d "1 month ago" "+%Y%m")/ report-test/$(date -d "1 month ago" "+%Y%m")/
cp report/$(date -d "1 month ago" "+%Y%m").html report-test/$(date -d "1 month ago" "+%Y%m")


cp -r report/$(date -d "2 month ago" "+%Y%m")/ report-test/$(date -d "2 month ago" "+%Y%m")/
cp report/$(date -d "2 month ago" "+%Y%m").html report-test/$(date -d "2 month ago" "+%Y%m")


cp -r report/$(date -d "3 month ago" "+%Y%m")/ report-test/$(date -d "3 month ago" "+%Y%m")/
cp report/$(date -d "3 month ago" "+%Y%m").html report-test/$(date -d "3 month ago" "+%Y%m")


cp -r report/$(date -d "4 month ago" "+%Y%m")/ report-test/$(date -d "4 month ago" "+%Y%m")/
cp report/$(date -d "4 month ago" "+%Y%m").html report-test/$(date -d "4 month ago" "+%Y%m")


cp -r report/$(date -d "5 month ago" "+%Y%m")/ report-test/$(date -d "5 month ago" "+%Y%m")/
cp report/$(date -d "5 month ago" "+%Y%m").html report-test/$(date -d "5 month ago" "+%Y%m")


cp -r report/$(date -d "6 month ago" "+%Y%m")/ report-test/$(date -d "6 month ago" "+%Y%m")/
cp report/$(date -d "6 month ago" "+%Y%m").html report-test/$(date -d "6 month ago" "+%Y%m")'''
      }
    }
  }
}