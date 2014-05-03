from pivotal_stocks import database
import csv
import urllib2
import re

SECURITIES_LIST_URL = "http://www.afrsmartinvestor.com.au/rw/SMI/Web/Tables/Share_Tables_Monthly/2014-04-09/Securities_140409.csv"

INDUSTRY_GROUPS_URL = "http://www.asx.com.au/asx/research/ASXListedCompanies.csv"


def parse_remote_csv(url):
    """Return the parsed CSV reader from remote URL"""
    file = urllib2.urlopen(url)
    return csv.reader(file)

def seed_securities_list():
    db = database.get_db()
    db.execute("delete from stocks")
    csv = parse_remote_csv(SECURITIES_LIST_URL)
    for row in csv:
        prog = re.compile('[A-Z]+\/[A-Z]')
        if len(row) >= 24 and prog.match(row[8]):  # Match ASX codes like "ONT/S". Ignore derivatives and non-stock securities.
            db.execute("insert into stocks (ticker, company_name, market_cap, div_yield, pe_ratio, franking_percentage) values (?,?,?,?,?,?)", (row[8][:3], row[7], row[6], row[17], row[22], row[18]))
    db.commit()

def seed_industry_groups():
    db = database.get_db()
    csv = parse_remote_csv(INDUSTRY_GROUPS_URL)
    for row in csv:
        if len(row) >=3 and len(row[1]) == 3:  # Only take rows with valid ASX codes
            if row[2] != "GICS Sector Code Not Applicable":
                db.execute("update stocks set industry_group = ? where ticker = ?", (row[2], row[1]))
    db.commit()
