# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import csv
csv_path = "data/csv/"
import sys


class EproPipeline(object):
    def process_item(self, item, spider):
        return item

class EproCsvPipeline(object):

    def __init__(self):
        reload(sys)
        # sys.setdefaultencoding('utf8')
        self.csvwriter = csv.writer(codecs.open('{}alltransaction8.csv'.format(csv_path),'wb'))
        self.csvwriter.writerow([
            'Deposit ID',
             'Check Date',
             'Bank Code',
             'Bank Name',
             'Account Number',
             'Bank Currency',
            "Sender's Name",
             "Sender's Name(Alphabet)",
             'Currency',
             'Deposit Amount',
             'Remitting Bank',
             'Remitting Bank Branch Name',
             'LIFT.CHG.CUR1',
             'LIFT.CHG.1',
             'LIFT.CHG.CUR2',
             'LIFT.CHG.2',
             'REMIT.CHG.CUR',
             'REMIT.CHG',
             'Status',
             'StatusChange Date',
             'API',
             'API Date and Time',
             'Transfer Status',
             'Transfer Date',
             'Refund Date'
             'TimeStamp'


        ])

    def process_item(self, item, spider):
        self.csvwriter.writerow([

        item['DepositID'],
        item['CheckDate'] ,
        item['BankCode'] ,
        item['BankName'] ,
        item['AccountNumber'] ,
        item['BankCurrency'] ,
        item['SenderName'] ,
        item['SenderNameAlphabet'],
        item['Currency'] ,
        item['DepositAmount'] ,
        item['RemittingBank'],
        item['RemittingBankBranchName'],
        item['LIFT_CHG_CUR1'] ,
        item['LIFT_CHG_1'] ,
        item['LIFT_CHG_CUR2'] ,
        item['LIFT_CHG_2'] ,
        item['REMIT_CHG_CUR'] ,
        item['REMIT_CHG'] ,
        item['Status'] ,
        item['StatusChangeDate'] ,
        item['API'] ,
        item['APIDateAndTime'] ,
        item['TransferStatus'] ,
        item['TransferDate'] ,
        item['RefundDate'] ,
        item['TimeStamp']
        ])

        return item