scrape-healthcare.gov
===

Python script that pulls down details of all plans on HealthCare.gov 

This only works with zipcodes in [states without their own health insurance exchange](http://en.wikipedia.org/wiki/Health_insurance_marketplace).

1. Edit `script.py` to set zipcode, income, and family members.
1. Run `python script.py > plans.tsv` to generate a TSV file containing all plan details.
