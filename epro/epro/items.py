# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EproItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()







    DepositID = scrapy.Field()
    CheckDate = scrapy.Field()
    BankCode = scrapy.Field()
    BankName = scrapy.Field()
    AccountNumber = scrapy.Field()
    BankCurrency = scrapy.Field()
    SenderName = scrapy.Field()
    SenderNameAlphabet = scrapy.Field()
    Currency = scrapy.Field()
    DepositAmount = scrapy.Field()
    RemittingBank = scrapy.Field()
    RemittingBankBranchName = scrapy.Field()
    LIFT_CHG_CUR1 = scrapy.Field()
    LIFT_CHG_1 = scrapy.Field()
    LIFT_CHG_CUR2 = scrapy.Field()
    LIFT_CHG_2 = scrapy.Field()
    REMIT_CHG_CUR = scrapy.Field()
    REMIT_CHG = scrapy.Field()
    Status = scrapy.Field()
    StatusChangeDate = scrapy.Field()
    API = scrapy.Field()
    APIDateAndTime = scrapy.Field()
    TransferStatus = scrapy.Field()
    TransferDate = scrapy.Field()
    RefundDate = scrapy.Field()
    TimeStamp = scrapy.Field()




