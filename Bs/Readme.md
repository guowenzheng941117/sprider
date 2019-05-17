安装python(科学环境https://www.anaconda.com/distribution/) 

conda install -c conda-forge scrapy  安装爬虫的库  anaconda会自动安装其所依赖的库

conda install psycopg2  安装pgsql的库

如何同时运行多个爬虫(添加一条新的命令)
1. 在spiders目录的同级目录下创建一个commands目录，并在该目录中创建一个crawlall.py，将scrapy源代码里的commands文件夹里的crawl.py源码复制过来，只修改run()方法即可！
2. 在里面加个_init_.py文件
3. settings.py配置文件还需要加一条.
　　 COMMANDS_MODULE = '项目名称.目录名称'    # COMMANDS_MODULE = 'Bs.commands'
4. 使用命令scrapy crawlall