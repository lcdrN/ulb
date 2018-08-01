pipeline {
  agent any
  stages {
    stage('Tests') {
      steps {
        sh './hydra-report.py  /home/noe/Desktop/script/sisc-scripts/accounting/$(date -d "12 month ago" "+%Y%m")??'
      }
    }
    stage('Build') {
      when {
        branch 'master'
      }
      steps {
        echo 'Build 6 month'
        sh '''./hydra-report.py  /home/noe/Desktop/script/sisc-scripts/accounting/$(date -d "11 month ago" "+%Y%m")??
./hydra-report.py  /home/noe/Desktop/script/sisc-scripts/accounting/$(date -d "12 month ago" "+%Y%m")??
./hydra-report.py  /home/noe/Desktop/script/sisc-scripts/accounting/$(date -d "13 month ago" "+%Y%m")??
./hydra-report.py  /home/noe/Desktop/script/sisc-scripts/accounting/$(date -d "14 month ago" "+%Y%m")??
./hydra-report.py  /home/noe/Desktop/script/sisc-scripts/accounting/$(date -d "15 month ago" "+%Y%m")??
./hydra-report.py  /home/noe/Desktop/script/sisc-scripts/accounting/$(date -d "16 month ago" "+%Y%m")??'''
      }
    }
    stage('Deploy') {
      when {
        branch 'master'
      }
      steps {
        sh '''mkdir -p report-test/

cp -r report/$(date -d "11 month ago" "+%Y%m")/ report-test/$(date -d "11 month ago" "+%Y%m")/
cp report/$(date -d "11 month ago" "+%Y%m").html report-test/$(date -d "11 month ago" "+%Y%m")


cp -r report/$(date -d "12 month ago" "+%Y%m")/ report-test/$(date -d "12 month ago" "+%Y%m")/
cp report/$(date -d "12 month ago" "+%Y%m").html report-test/$(date -d "12 month ago" "+%Y%m")


cp -r report/$(date -d "13 month ago" "+%Y%m")/ report-test/$(date -d "13 month ago" "+%Y%m")/
cp report/$(date -d "13 month ago" "+%Y%m").html report-test/$(date -d "13 month ago" "+%Y%m")


cp -r report/$(date -d "14 month ago" "+%Y%m")/ report-test/$(date -d "14 month ago" "+%Y%m")/
cp report/$(date -d "14 month ago" "+%Y%m").html report-test/$(date -d "14 month ago" "+%Y%m")


cp -r report/$(date -d "15 month ago" "+%Y%m")/ report-test/$(date -d "15 month ago" "+%Y%m")/
cp report/$(date -d "15 month ago" "+%Y%m").html report-test/$(date -d "15 month ago" "+%Y%m")


cp -r report/$(date -d "16 month ago" "+%Y%m")/ report-test/$(date -d "16 month ago" "+%Y%m")/
cp report/$(date -d "16 month ago" "+%Y%m").html report-test/$(date -d "16 month ago" "+%Y%m")'''
      }
    }
  }
}