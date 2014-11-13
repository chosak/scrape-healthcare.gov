import itertools
from scraper import PlanScraper


class Person(object):
    def __init__(self, age, parent=False, smoker=False, pregnant=False,
                 covered=False):
        self.age = age
        self.parent = parent
        self.smoker = smoker
        self.pregnant = pregnant
        self.covered = covered


def unique(sequence):
    seen = {}
    result = []

    for x in sequence:
        if x in seen:
            continue

        seen[x] = 1
        result.append(x)

    return result


def run():
    zipcode = 19101
    income = 50000
    people = [
        Person(40, parent=True, covered=True),
        Person(38, parent=True, pregnant=True),
        Person(2),
    ]

    plans = PlanScraper().get_plans(zipcode, income, people)

    keys = unique(itertools.chain(*[p.keys() for p in plans]))
    print '\t'.join(keys)

    for plan in plans:
        print '\t'.join([
            unicode(plan.get(k, '')).encode('utf-8') for k in keys
        ])


if __name__ == '__main__':
    run()
