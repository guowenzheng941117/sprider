# import scrapy


# class generalSpider(scrapy.Spider):

#     urls = []
#     link_header = ""
#     rows = ""
#     a = ""
#     title = ""
#     detail = ""

#     def start_requests(self):
#         for url in self.urls:
#             # 根据实际链接继续爬
#             yield scrapy.Request(url=url, callback=self.parse)

#     def parse(self, response):
#         url_detail = response.xpath(self.rows)
#         for h in url_detail:
#             print("link: " + self.link_header + h.xpath(self.a).get() +
#                   " title " + h.xpath(self.title).get())
#             yield scrapy.Request(url=self.link_header + h.xpath(self.a).get(),
#                                  callback=self.parse_detail)
#         self.page()

#     def parse_detail(self, response):
#         print(response.xpath(self.detail).get())

#     def page(self):
#         # 默认翻页 子类可重构覆盖
#         print("father")
