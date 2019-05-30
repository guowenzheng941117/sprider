from Bs.spiders.generalSpider import generalSpider


class BsSpider(generalSpider):
    name = "bs"
    # 湖南商学院
    generalSpider.urls = ["http://www.hnuc.edu.cn/column/zbxx/index.shtml"]
    # 拼接路径的头
    generalSpider.link_header = "http://www.hnuc.edu.cn"
    # 信息列表规则
    generalSpider.rows = "//div[@class='ejlist']//ul//li//a"
    # 获取详情链接的规则
    generalSpider.a = "./@href"
    # 获取标题的规则
    generalSpider.title = "./text()"
    # 获取详情链接内容的规则
    generalSpider.detail = "//div[@class='detit']//h2"

    def page(self):
        print("son")
