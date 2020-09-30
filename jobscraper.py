import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

TEST_URL = r'http://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=yes&rec_idx=38560946&recommend_ids=eJxtkEsSAjEIBU%2FjHh7%2FtQfJ%2FW9hxjFgWWbXAZqXSKYUgpeVPeIp6eVSuUL9B5e%2BL1LAPO3hylwb41RL%2FA%2BeaRjAbR8cexqvvfW2J7PG6OCU8TV9sO0CoeWEG9UU1VEHP%2B0BEO90zvdT0xU0dvIMadnOUGJ7%2BvzLPt4YZAbroJYSmKrHzlWNZkRsl%2FkFJSxUNw%3D%3D&view_type=apply_status&gz=1#seq=0'
D_REGEX = re.compile(r'D-(\d{1,})')
COMPANY_REGEX = re.compile(r'\[(.*)\]')
JU_REGEX = re.compile(r'\(주\)')
DESCRIPTION_REGEX = re.compile(r'.*\](.*)\(.*')


def findDesc(tag):
    attrs = tag.attrs
    if 'name' in attrs:
        if attrs['name'] == 'description':
            return attrs['content']


def getTimelessDate(dateObject):
    
    return datetime(dateObject.year, dateObject.month, dateObject.day)



class SaraminRole:
    # D_REGEX = re.compile(r'D-(\d\d)')
    # COMPANY_REGEX = re.compile(r'\[(.+)\(주\)?\]')

    def __init__(self, url):
        self.url = url
        self.title = self.getTitle(self.url)
        self.D = self.getDCountdown()
        self.company = self.getCompany()
        # self.submission_date = getTimelessDate(datetime.today())
        # self.__closing_date = None




    def getTitle(self, url):
        page = requests.get(self.url)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, features='lxml')
        page_title = soup.title.text
        
        return page_title

    def getDCountdown(self):
        
        return D_REGEX.search(self.title).group(1)

    def getCompany(self):
        company = COMPANY_REGEX.search(self.title).group(1)
        if JU_REGEX.search(company):
            company = JU_REGEX.sub('', company)

        return company

    def getTimeTilDue(self):
        today = getTimelessDate(datetime.today())
        return today + timedelta(days=int(self.D))

    @property
    def closing_date(self):
        date = self.getTimeTilDue()
        return date

    @property
    def submission_date(self):
        date = getTimelessDate(datetime.today())
        return date

    @property
    def description(self):
        desc = DESCRIPTION_REGEX.search(self.title).group(1).strip()
        return desc
# testRole = SaraminRole(TEST_URL)
# # print(testRole.title)
# # print(testRole.submission_date)
# # print(testRole.D)
# # print(testRole.company)
# print(testRole.description)