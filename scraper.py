import re
import requests
import urllib
import urlparse

from bs4 import BeautifulSoup
from collections import OrderedDict



class PlanScraper(object):
    def get_plans(self, zipcode, income, people):
        plan_urls = self.get_plan_urls(zipcode, income, people)
        return [self.get_plan(plan_url) for plan_url in plan_urls]



    def get_plan(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content)

        plan_name = soup.find_all('h2', class_='plan-name')[0].text
        company, name = [s.strip() for s in plan_name.split(u'\xb7')]

        plan_files = soup.find_all('ul', class_='plan-files')[0]
        plan_link = plan_files.findAll('a')[0]['href']

        plan = [
            ('url', url),
            ('company', company),
            ('name', name),
            ('link', plan_link),
        ]

        details = soup.find_all('ol', class_='results')[0]
        rows = details.find_all('div', class_='row')

        plan.extend(self.parse_overview(rows[1]))
        plan.extend(self.parse_premiums(rows[3]))
        plan.extend(self.parse_details(rows[4]))

        return OrderedDict(plan)


    def parse_overview(self, row):
        bs = row.find_all('b')
        metal = bs[0].text.split(' ')[0]
        plan_type = bs[1].text

        lis = row.find_all('li')
        network = lis[1].text if 3 == len(lis) else None
        plan_id = lis[-1].text.split(':')[-1].strip()

        return [
            ('metal', metal),
            ('plan_type', plan_type),
            ('network', network),
            ('plan_id', plan_id),
        ]


    def parse_premiums(self, row):
        ps = row.find_all('p')

        premium = int(ps[0].text.strip('$'))
        deductible = int(re.split(' |\n', ps[1].text)[1].strip('$')) 
        oop_max = int(re.split(' |\n', ps[2].text)[1].strip('$')) 

        return [
            ('premium', premium),
            ('deductible', deductible),
            ('oop_max', oop_max),
        ]


    def parse_details(self, row):
        details = []

        for dd in row.find_all('dd'):
            dd_text = dd.text.strip(' \n\t')
            value = dd.find_all('span')[-1].text.strip(' \n\t')
            key = dd_text[:-len(value)]

            details.append((
                key.strip(' \n\t'),
                value
            ))
            #print '**{}**'.format(span.text)
            #print '**{}**'.format(span.parent.text)
            #costs.append((
            #    span.parent.text[:-len(span.text)].strip(' \n\t'),
            #    span.text.strip(' \n\t')
            #))

        return details


    def get_plan_urls(self, zipcode, income, people):
        plan_urls = []

        while True:
            url = self.url(zipcode, income, people, start=len(plan_urls))
            page_urls = list(self.get_page_urls(url))

            if not len(page_urls):
                break

            plan_urls.extend(page_urls)

            if len(page_urls) < 10:
                break

        return plan_urls


    def get_page_urls(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content)
        results = soup.findAll('ol', {'class': 'results'})[0]

        for result in results.findAll('li'):
            for a in result.findAll('a'):
                if a.parent.name == 'h2':
                    yield urlparse.urljoin(url, a['href'])


    def url(self, zipcode, income, people, start=0):
        qs = [
            ('zip', zipcode),
            ('income', income),
        ]

        for person in people:
            qs.extend(self.person_qs(person).items())

        if start:
            qs.append(('start', start))

        return 'https://www.healthcare.gov/see-plans/{}/results/?{}'.format(
            zipcode,
            urllib.urlencode(qs)
        )


    def person_qs(self, person):
        return {
            'age': person.age,
            'mec': 1 if person.covered else '',
            'parent': 1 if person.parent else '',
            'smoker': 1 if person.smoker else '',
            'pregnant': 1 if person.pregnant else '',
        }
