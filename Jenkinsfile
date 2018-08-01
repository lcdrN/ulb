pipeline {
  agent any
  stages {
    stage('Tests') {
      steps {
        sh './hydra-report.py  /home/noe/Desktop/script/sisc-scripts/accounting/$(date -d "1 month ago" "+%Y%m")??'
      }
    }
    stage('Build') {
      steps {
        echo 'Build 6 month'
        sh '''./hydra-report.py  /home/noe/Desktop/script/sisc-scripts/accounting/$(date -d "1 month ago" "+%Y%m")??
./hydra-report.py  /home/noe/Desktop/script/sisc-scripts/accounting/$(date -d "2 month ago" "+%Y%m")??
./hydra-report.py  /home/noe/Desktop/script/sisc-scripts/accounting/$(date -d "3 month ago" "+%Y%m")??
./hydra-report.py  /home/noe/Desktop/script/sisc-scripts/accounting/$(date -d "4 month ago" "+%Y%m")??
./hydra-report.py  /home/noe/Desktop/script/sisc-scripts/accounting/$(date -d "5 month ago" "+%Y%m")??
./hydra-report.py  /home/noe/Desktop/script/sisc-scripts/accounting/$(date -d "6 month ago" "+%Y%m")??'''
      }
    }
    stage('Deploy') {
      when {
        branch 'master'
      }
      steps {
        sh '''mkdir -p report-test
mkdir -p report-test/$(date -d "1 month ago" "+%Y%m")



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