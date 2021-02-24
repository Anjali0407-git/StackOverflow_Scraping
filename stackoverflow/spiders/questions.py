import scrapy


class Questions(scrapy.Spider):
    name = "questions"

    start_urls = [
        'https://stackoverflow.com/questions/218123/what-was-the-strangest-coding-standard-rule-that-you-were-forced-to-follow'
    ]
    i = 1

    def parse(self, response):
        j = '1'

        for data in response.xpath('//*[@id="answers"]//*[@class="answer"]'):
            if self.i <= 50:
                yield{
                    'ID': self.i,
                    'ANSWERS': data.xpath('//div[@class="answer" or @class="answer accepted-answer"]['+j+']/div[@class="post-layout"]/div[2]/div[1]/p/text()').extract(),
                    'COMMENTS': data.xpath('//div[@class="answer" or @class="answer accepted-answer"]['+j+']/div[@class="post-layout"]/div[3]/div[1]/ul/li/div[2]/div/span/text()').extract(),
                    'VOTES': data.xpath('//div[@class="answer" or @class="answer accepted-answer"]['+j+']/div[@class="post-layout"]/div[1]/div/div[1]/div[1]/text()').get(),
                }
                j = int(j)+1
                j = str(j)
            self.i += 1

        next_page = response.xpath(
            '//*[@id="answers"]/div[2]/a[4]/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page)
