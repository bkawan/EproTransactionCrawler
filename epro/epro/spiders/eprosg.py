# -*- coding: utf-8 -*-
import scrapy
import sys
import codecs
import locale
import re
from epro.items import EproItem


from scrapy.shell import inspect_response





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
        try:
            login_file = open('login_details.txt')

            username = None
            password = None
            for detail in login_file:
                if detail.lower().startswith('username'):
                    username = detail.split(":")[1].strip()
                if detail.lower().startswith('password'):
                    password = detail.split(":")[1].strip()

            print("*****************")
            print ("Username: {}; Password: {}".format(username,password))
            print("*****************")

            return scrapy.FormRequest.from_response(
                response,
                formdata = {'userid': username, 'userpass': password},
                callback=self.after_login,
            )
        except (OSError, IOError) as e:
            print("*********************************")
            print(e)
            self.logger.error("File Not Found")
            print("********************************")


    def after_login(self,response):

        if "Login Failed" in response.body:
            print("********************************************************************************************************")
            self.logger.error("Login failed!! Please check user name and password in login_details.txt file")
            print("*******************************************************************************************************")
            return
        else:
            response = response.urljoin('request')
            return scrapy.Request(response,callback=self.parse_all_transaction)

    def parse_all_transaction(self,response):
        # inspect_response(response, self)

        all_tr_row = response.xpath("//tbody/tr")
        for tr in all_tr_row:
            id = tr.xpath("td/text()").extract_first()
            try:
                deposit_id = int(id)
                if deposit_id > 1750:
                    all_transaction_sel = response.xpath("//td[@rowspan='2']/a/@href").extract()
                    for transaction in all_transaction_sel:
                        info_regex = re.search(r'request/info/\d+', transaction)
                        if info_regex:
                            link = "https://admin.epro.sg/adms/titan/{}".format(info_regex.group())
                            yield scrapy.Request(link, self.parse_each_transaction)

            except ValueError:
                print ("********")
                print("deposit Id less than or equal to 1750")
                print("*************")



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
        item['DepositID'] = self.get_index(transaction_detail,0)
        item['CheckDate'] = self.get_index(transaction_detail,1)
        item['BankCode'] = self.get_index(transaction_detail,2)
        item['BankName'] = self.get_index(transaction_detail,3)
        item['AccountNumber'] = self.get_index(transaction_detail,4)
        item['BankCurrency'] = self.get_index(transaction_detail,5)
        item['SenderName'] = self.get_index(transaction_detail,6)
        item['SenderNameAlphabet'] = self.get_index(transaction_detail,7)
        item['Currency'] = self.get_index(transaction_detail,8)
        item['DepositAmount'] = self.get_index(transaction_detail,9)
        item['RemittingBank'] = self.get_index(transaction_detail,10)
        item['RemittingBankBranchName'] = self.get_index(transaction_detail,11)
        item['LIFT_CHG_CUR1'] = self.get_index(transaction_detail,12)
        item['LIFT_CHG_1'] = self.get_index(transaction_detail,13)
        item['LIFT_CHG_CUR2'] = self.get_index(transaction_detail,14)
        item['LIFT_CHG_2'] = self.get_index(transaction_detail,15)
        item['REMIT_CHG_CUR'] = self.get_index(transaction_detail,16)
        item['REMIT_CHG'] = self.get_index(transaction_detail,17)
        item['Status'] = self.get_index(transaction_detail,18)
        item['StatusChangeDate'] = self.get_index(transaction_detail,19)
        item['API'] = self.get_index(transaction_detail,20)
        item['APIDateAndTime'] = self.get_index(transaction_detail,21)
        item['TransferStatus'] = self.get_index(transaction_detail,22)
        item['TransferDate'] = self.get_index(transaction_detail,23)
        item['RefundDate'] = self.get_index(transaction_detail,24)
        item['TimeStamp'] = self.get_index(transaction_detail,25)

        return item

    def get_index(self, item_list, index):
        try:
            value = item_list[index]
            try:
                value = value.strip()
            except:
                value = value
        except:
            value = ""
        return value