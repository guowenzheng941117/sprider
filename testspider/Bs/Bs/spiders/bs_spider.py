import scrapy
import json


class BsSpider(scrapy.Spider):
    name = "bs"
    start_urls = [
        "http://exercise.kingname.info/exercise_middleware_ua",
        "http://exercise.kingname.info/exercise_middleware_ua",
        "http://exercise.kingname.info/exercise_middleware_ua"
    ]

    # 如果有区别就不共用一个pipeitem 不同的item要在pipeitem进行判断
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'Bs.pipelines.TsPipeline': 301,
    #     }
    # }

    def parse(self, response):
        json.loads(response.body.decode())
