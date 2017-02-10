import os
print os.popen("pip install -r requirements.txt").read()
print os.popen("scrapy crawl facebookspider -o data12.csv -t csv").read()
