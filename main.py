from crawler import Crawler
from args import get_args
import csv

if __name__ == '__main__':
    args = get_args()
    crawler = Crawler()
    content = crawler.crawl(args.start_date, args.end_date)
    #print(content)
    # TODO: write content to file according to spec
    with open(args.output + '\content.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(content)
