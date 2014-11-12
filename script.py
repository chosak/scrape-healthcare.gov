from scraper import PlanScraper


class Person(object):
    def __init__(self, age, parent=False, smoker=False, pregnant=False,
                 covered=False):
        self.age = age
        self.parent = parent
        self.smoker = smoker
        self.pregnant = pregnant
        self.covered = covered


def run():
    zipcode = 19101
    income = 50000
    people = [
        Person(40, parent=True, covered=True),
        Person(38, parent=True, pregnant=True),
        Person(2),
    ]

    plans = PlanScraper().get_plans(zipcode, income, people)

    keys = sorted(plans[0].keys())
    print '\t'.join(keys)

    for plan in plans:
        print '\t'.join([unicode(plan[k]).encode('utf-8') for k in keys])


if __name__ == '__main__':
    run()
