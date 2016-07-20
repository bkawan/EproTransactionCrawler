# -*- coding: utf-8 -*-
import scrapy
import sys
import codecs
import locale
import re
from epro.items import EproItem


class EprosgSpider(scrapy.Spider):
    name = "epro"
    allowed_domains = ["epro.sg"]
    start_urls = [
        "https://admin.epro.sg/adms/titan/login/",


    ]
    def __init__(self):
        sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
        reload(sys)
        sys.setdefaultencoding('utf-8')

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata = {'userid': 'admin', 'userpass': '7n4TTE2N'},
            callback=self.after_login
        )

    def after_login(self,response):
        response = response.urljoin('request')
        return scrapy.Request(response,callback=self.parse_all_transaction)

    def parse_all_transaction(self,response):

        all_transaction_sel = response.xpath("//td[@rowspan='2']/a/@href").extract()
        for transaction in all_transaction_sel:
            info_regex = re.search(r'request/info/\d+', transaction)
            if info_regex:
                link = "https://admin.epro.sg/adms/titan/{}".format(info_regex.group())
                yield scrapy.Request(link,self.parse_each_transaction)

        all_a_tags_sel = response.xpath("//li/a")
        for sel in all_a_tags_sel:
            text = sel.xpath("text()").extract_first()
            if text == u'\uff1e':
                next = sel.xpath('@href').extract_first()
                next_pagi = "https://admin.epro.sg/adms/titan/{}".format(next)
                yield scrapy.Request(next_pagi,self.parse_all_transaction)


    def parse_each_transaction(self,response):

        # inspect_response(response, self)

        detailform_sel = response.xpath("//div[@class='detailform clear']")
        transaction_detail_sel = detailform_sel.xpath(".//td")

        transaction_detail = []
        for item in transaction_detail_sel:
            transaction_detail.append(item.xpath(".//text()").extract_first())

        item = EproItem()
        item['DepositID'] = transaction_detail[0]
        item['CheckDate'] = transaction_detail[1]
        item['BankCode'] = transaction_detail[2]
        item['BankName'] = transaction_detail[3]
        item['AccountNumber'] = transaction_detail[4]
        item['BankCurrency'] = transaction_detail[5]
        item['SenderName'] = transaction_detail[6]
        item['SenderNameAlphabet'] = transaction_detail[7]
        item['Currency'] = transaction_detail[8]
        item['DepositAmount'] = transaction_detail[9]
        item['RemittingBank'] = transaction_detail[10]
        item['RemittingBankBranchName'] = transaction_detail[11]
        item['LIFT_CHG_CUR1'] = transaction_detail[12]
        item['LIFT_CHG_1'] = transaction_detail[13]
        item['LIFT_CHG_CUR2'] = transaction_detail[14]
        item['LIFT_CHG_2'] = transaction_detail[15]
        item['REMIT_CHG_CUR'] = transaction_detail[16]
        item['REMIT_CHG'] = transaction_detail[17]
        item['Status'] = transaction_detail[18]
        item['StatusChangeDate'] = transaction_detail[19]
        item['API'] = transaction_detail[20]
        item['APIDateAndTime'] = transaction_detail[21]
        item['TransferStatus'] = transaction_detail[22]
        item['TransferDate'] = transaction_detail[23]
        item['RefundDate'] = transaction_detail[24]
        item['TimeStamp'] = transaction_detail[25]

        return  item
