# Loans module for mp2.
# Author: Andrew VanDerKolk, 6.24.24

#imports
import json
import zipfile
import csv
from io import TextIOWrapper

race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander",
    "5": "White",
}


class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()
        for r in race:
            try:
                self.race.add(race_lookup[r])
            except KeyError:
                if r == "6":
                    self.race.add("-1")
                else:
                    continue
    
    def __repr__(self):
        self.race = sorted(list(self.race))
        return f"Applicant('{self.age}', {self.race})"
    
    def __lt__(self, other):
        return self.lower_age() < other.lower_age()
    
    def lower_age(self):
        # capture < or > cases.
        _ = self.age.replace("<", "-").replace(">", "-").split("-")
        return int(next(x for x in _ if x))
    
class Loan:
    def __init__(self, values):
        # set loan amount, property value, and interest rate
        self.loan_amount = float(values['loan_amount']) if values['loan_amount'] not in ['NA', 'Exempt'] else -1
        self.property_value = float(values['property_value']) if values['property_value'] not in ['NA', 'Exempt'] else -1
        self.interest_rate = float(values['interest_rate']) if values['interest_rate'] not in ['NA', 'Exempt'] else -1
        self.applicants = []
        
        # applicant Applicant object
        app_races = []
        for i in range(1,6):
            app_race = values[f'applicant_race-{i}']
            if app_race:
                app_races.append(app_race)
            else:
                break
        self.applicants.append(Applicant(values['applicant_age'], app_races)) # append Applicant object
        
        # co-applicant Applicant object
        if values['co-applicant_age'] != "9999" and values['co-applicant_race-1']:
            co_app_races = list()
            for i in range(1,6):
                co_app_race = values[f'co-applicant_race-{i}']
                if co_app_race != '':
                    co_app_races.append(co_app_race)
                else:
                    break
            self.applicants.append(Applicant(values['co-applicant_age'], co_app_races)) # append if applicable
    
    def __repr__(self):
        return f"<Loan: {self.interest_rate}% on ${self.loan_amount} with {len(self.applicants)} applicant(s)>"
        
    def __str__(self):
        return f"<Loan: {self.interest_rate}% on ${self.loan_amount} with {len(self.applicants)} applicant(s)>"
    
    def yearly_amounts(self, yearly_payment):
        assert self.interest_rate > 0 and self.loan_amount > 0
        amt = self.loan_amount
        
        while amt > 0:
            yield amt
            # add interest rate multiplied by amt to amt
            amt *= (self.interest_rate / 100) + 1
            # subtract yearly payment from amt
            amt -= yearly_payment


# banks dictionary from banks.json
with open('banks.json') as f:
    bank_list_simple = json.load(f)
#bank_list_simple # len 919 - len(bank_list_simple)
banks_dict = {}
for bank in bank_list_simple:
    name = bank['name']
    if name in banks_dict:
        banks_dict[name].append(bank)
    else:
        banks_dict[name] = list()
        banks_dict[name].append(bank)
            
class Bank:
    def __init__(self, name):
        # set self.name to given name
        self.name = name
        
        # set self.lei to found lei, -1 for invalid bank name
        if self.name in banks_dict:
            self.lei = banks_dict[self.name][0]['lei']
        else:
            self.lei = -1
        
        # const filename
        filename = 'wi'
        # use wi.zip-wi.csv to build loan_list with lei as key
        self.loan_list = []
        zf = zipfile.ZipFile(filename + '.zip') # open and read zipfile
        f = zf.open(filename + '.csv')
        reader = csv.DictReader(TextIOWrapper(f)) # create reader
        for row in reader: # iterate over loan data. skip row if lei doesn't match, or create a Loan object.
            if row['lei'] == self.lei:
                self.loan_list.append(Loan(row))
            else:
                continue
            
    def __repr__(self): # 'programmer' str representation
        return f"Bank({self.name}, {self.lei})"
    
    def __str__(self): # 'non-programmer' str representation
        return f"Bank name: {self.name}, LEI: {self.lei}, Num Loans: {len(self.loan_list)}."
    
    def __getitem__(self, lookup): # allows indexing(?) directly on bank objects
        #lookup = int(lookup) # what about slicing?
        return self.loan_list[lookup]
    
    def __len__(self): # can use len directly on Bank objects
        return len(self.loan_list)