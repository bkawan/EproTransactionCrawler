# EproTransactionCrawler

follow Steps 1 https://developers.google.com/sheets/quickstart/python#troubleshooting to generate client_secret.json

$ git clone https://github.com/bkawan/EproTransactionCrawler.git

- replace client_secret.json located at EproTransactionCrawler/epro/epro with newly generated

- open **login_details.txt** and make changes to following and save the file

  - Username: yourloginusername
  - Password: yourloginpassword

$ cd epro


$ scrapy crawl epro

Extracted data will be sinked with google sheets ( need permission for google sheets)

** Dependencies **

$pip install httplib2

$pip install oauth2client

$pip install google-api-python-client
