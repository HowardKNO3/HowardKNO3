from time import sleep
from datetime import datetime
import requests
from lxml import etree
class Crawler(object):
    def __init__(self,
                base_url='https://www.csie.ntu.edu.tw/news/',
                rel_url='news.php?class=101'):
        self.base_url = base_url
        self.rel_url = rel_url

    def crawl(self, start_date, end_date,
            date_thres=datetime(2012, 1, 1)):
        """Main crawl API

        1. Note that you need to sleep 0.1 seconds for any request.
        2. It is welcome to modify TA's template.
        """
        if end_date < date_thres:
            end_date = date_thres
        contents = list()
        page_num = 0
        while True:
            rets, last_date = self.crawl_page(
                start_date, end_date, page=f'&no={page_num}')
            page_num += 10
            
            if rets:
                contents += rets
            if last_date < start_date:
                break
            
        return contents

    def crawl_page(self, start_date, end_date, page=''):
        """Parse ten rows of the given page

        Parameters:
            start_date (datetime): the start date (included)
            end_date (datetime): the end date (included)
            page (str): the relative url specified page num

        Returns:
            content (list): a list of date, title, and content
            last_date (datetime): the smallest date in the page
        """
        
        res = requests.get(
            self.base_url + self.rel_url + page,
            headers={'Accept-Language':
                    'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6'}
        ).content.decode()
        sleep(0.1)
        root = etree.HTML(res)
        # TODO: parse the response and get dates, titles and relative url with etree
        
        dates = root.xpath("//html/body/div[1]/div/div[2]/div/div/div/div/table/tbody/tr/td[1]/text()")
        titles = root.xpath("//html/body/div[1]/div/div[2]/div/div/div/div/table/tbody/tr/td[2]/a/text()")
        rel_urls = root.xpath("//html/body/div[1]/div/div[2]/div/div/div/div/table/tbody/tr/td[2]//a/@href")
        contents = list()
        last_date = datetime(2050, 1, 1)
        #print(rel_urls)
        for i in range(0, 10):
            last_date = min(last_date, datetime.strptime(dates[i], "%Y-%m-%d"))
            if ((datetime.strptime(dates[i], "%Y-%m-%d") > start_date) & (datetime.strptime(dates[i], "%Y-%m-%d") < end_date)):
                # TODO: 1. concatenate relative url to full url
                #       2. for each url call self.crawl_content
                #          to crawl the content
                #       3. append the date, title and content to
                #          contents
                #print(datetime.strptime(dates[i], "%Y-%m-%d"), start_date, end_date)
                
                this_site = list()
                this_site.append(dates[i])
                this_site.append(titles[i])
                new_url = self.base_url + rel_urls[i]
                this_site.append(self.crawl_content(new_url))
                contents.append(this_site)
                #print(this_site)
        return contents, last_date
        

    def crawl_content(self, url):
        """Crawl the content of given url

        For example, if the url is
        https://www.csie.ntu.edu.tw/news/news.php?Sn=15216
        then you are to crawl contents of
        ``Title : 我與DeepMind的A.I.研究之路, My A.I. Journey with DeepMind Date : 2019-12-27 2:20pm-3:30pm Location : R103, CSIE Speaker : 黃士傑博士, DeepMind Hosted by : Prof. Shou-De Lin Abstract: 我將與同學們分享，我博士班研究到加入DeepMind所參與的projects (AlphaGo, AlphaStar與AlphaZero)，以及從我個人與DeepMind的視角對未來AI發展的展望。 Biography: 黃士傑, Aja Huang 台灣人，國立臺灣師範大學資訊工程研究所博士，現為DeepMind Staff Research Scientist。``
        """
        response = requests.get(
            url,
            headers={'Accept-Language':
                    'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6'}
        ).content.decode()

        root = etree.HTML(response)
        content = root.xpath("/html/body/div/div/div[2]/div/div/div[2]/div/div[@class = \"editor content\"]")
        ret_content = str()
        for element in content:
            sub_content = element.xpath("string(.)")
            sub_content = sub_content.replace('\"', '\"\"')
            ret_content += sub_content
            
        
        return ret_content
        raise NotImplementedError
