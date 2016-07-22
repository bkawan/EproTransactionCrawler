# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import csv
csv_path = "data/csv/"
import sys
# from sheets import Sheets
from epro.sheets import Sheets
from epro.items import EproItem


class EproPipeline(object):
    def process_item(self, item, spider):
        return item

class EproCsvPipeline(object):

    def __init__(self):
        sys.setdefaultencoding('utf8')
        self.sheet = Sheets('1mKAsY92nA3I6PhTkNd9aLIY8_SZMXERr2wg5WTYMk34', 'client_secret.json',
                       'FinancialData')

    def close_spider(self, spider):
        self.sheet.sort_sheet()


    def process_item(self, item, spider):

        self.sheet.append_row([item['DepositID'],
                               item['CheckDate'],
                               item['BankCode'],
                               item['BankName'],
                               item['AccountNumber'],
                               item['BankCurrency'],
                               item['SenderName'],
                               item['SenderNameAlphabet'],
                               item['Currency'],
                               item['DepositAmount'],
                               item['RemittingBank'],
                               item['RemittingBankBranchName'],
                               item['LIFT_CHG_CUR1'],
                               item['LIFT_CHG_1'],
                               item['LIFT_CHG_CUR2'],
                               item['LIFT_CHG_2'],
                               item['REMIT_CHG_CUR'],
                               item['REMIT_CHG'],
                               item['Status'],
                               item['StatusChangeDate'],
                               item['API'],
                               item['APIDateAndTime'],
                               item['TransferStatus'],
                               item['TransferDate'],
                               item['RefundDate'],
                               item['TimeStamp']
                               ])

        return item


