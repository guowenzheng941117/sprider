import scrapy
import json
from Bs.items import BsItem


class BsSpider(scrapy.Spider):
    name = "bs"

    def start_requests(self):
        yield scrapy.http.FormRequest(
            url='http://www.ccgp-hunan.gov.cn/mvc/getNoticeList4Web.do',
            formdata={
                'pType': '',
                'prcmPrjName': '',
                'prcmItemCode': '',
                'prcmOrgName': '',
                'startDate': '2019-05-24',
                'endDate': '2019-05-24',
                'prcmPlanNo': '',
                'page': "1",
                'pageSize': '1'
            },
            callback=self.parselist,
            dont_filter=True)

    def parselist(self, response):
        main_data = json.loads(response.body.decode('utf-8'))['rows']
        # 处理数据
        for i_item in range(len(main_data)):
            # 初始化item对象
            bs_item = BsItem()
            # 标题
            bs_item['title'] = main_data[i_item]['NOTICE_TITLE']
            # 时间
            bs_item['issueTime'] = main_data[i_item]['NEWWORK_DATE_ALL'][
                'time']
            # 实际链接
            bs_item[
                'link'] = 'http://www.ccgp-hunan.gov.cn/page/notice/notice.jsp?noticeId=' + str(
                    main_data[i_item]['NOTICE_ID'])
            # 根据实际链接继续爬
            yield scrapy.Request(bs_item['link'],
                                 callback=self.parseDetail,
                                 meta={'bs_item': bs_item})
        # 如果有数据就继续请求下一页
        # if main_data:
        #     self.page += 1
        #     page = self.page
        #     yield scrapy.http.FormRequest(
        #         url='http://www.ccgp-hunan.gov.cn/mvc/getNoticeList4Web.do',
        #         formdata={
        #             'pType': '',
        #             'prcmPrjName': '',
        #             'prcmItemCode': '',
        #             'prcmOrgName': '',
        #             'startDate': '2019-05-16',
        #             'endDate': '2019-05-16',
        #             'prcmPlanNo': '',
        #             'page': str(page),
        #             'pageSize': '10'
        #         },
        #         callback=self.parselist,
        #         dont_filter=True)

    def parseDetail(self, response):
        bs_item = response.meta['bs_item']
        frameLink = "http://www.ccgp-hunan.gov.cn" + response.xpath(
            "//iframe/@src").get()
        # 根据实际链接继续爬
        yield scrapy.Request(frameLink,
                             callback=self.parseFrame,
                             meta={'bs_item': bs_item})

    def parseFrame(self, response):
        bs_item = response.meta['bs_item']
        bs_item['detail'] = response.text
        yield bs_item
