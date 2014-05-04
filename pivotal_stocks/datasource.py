from pivotal_stocks import database
import csv
import urllib2
import re

SECURITIES_LIST_URL = "http://www.afrsmartinvestor.com.au/rw/SMI/Web/Tables/Share_Tables_Monthly/2014-04-09/Securities_140409.csv"
ASX200_LIST_URL = "http://www.afr.com/rw/AFR/Web/Tables/Share_Tables_Daily/2014-05-03/GGsada140503.csv"
LARGE_CAP_THRESHOLD = 5000000
MID_CAP_THRESHOLD = 250000
SECTORS = {
  "10": "Energy",
  "15": "Materials",
  "20": "Industrials",
  "25": "Consumer Discretionary",
  "30": "Consumer Staples",
  "35": "Health Care",
  "40": "Financials",
  "45": "Information Technology",
  "50": "Telecommunication Services",
  "55": "Utilities"
}

def parse_remote_csv(url):
    """Return the parsed CSV reader from remote URL"""
    file = urllib2.urlopen(url)
    return csv.reader(file)

def sector_for_gics_code(gics):
    try:
        return SECTORS[gics[:2]]
    except KeyError:
        return "Others"

def tsr_for_value(value):
    """Return total shareholder return from a input of $1000 investment value in 3 years"""
    if value == '':
        return None
    else:
        return (int(value) - 1000) / 10.0

def seed_securities_list():
    db = database.get_db()
    db.execute("delete from stocks")
    csv = parse_remote_csv(SECURITIES_LIST_URL)
    for row in csv:
        prog = re.compile('[A-Z]+\/[A-Z]')
        if len(row) >= 24 and prog.match(row[8]):  # Match ASX codes like "ONT/S". Ignore derivatives and non-stock securities.
            db.execute("insert into stocks (asx_code, company_name, sector, market_cap, div_yield, pe_ratio, franking, eps, tsr_3y) values (?,?,?,?,?,?,?,?,?)", (row[8][:3], row[7], sector_for_gics_code(row[9]), row[6], row[17], row[22], row[18], row[21], tsr_for_value(row[3])))
    db.commit()
    bin_data_by_market_cap()
    bin_data_by_franking()
    bin_data_by_div_yield()
    bin_data_by_eps()
    bin_data_by_tsr_3y()

def seed_asx200_list():
    db = database.get_db()
    csv = parse_remote_csv(ASX200_LIST_URL)
    for row in csv:
        if len(row) >= 18 and len(row[4]) == 3:   # Only take rows with valid ASX codes
            db.execute("update stocks set asx200 = 't' where asx_code = ?", (row[4],))
    db.commit()

def bin_data_by_market_cap():
    data = database.query_db("select id, market_cap from stocks")
    db = database.get_db()
    for row in data:
        if row['market_cap'] >= LARGE_CAP_THRESHOLD:
            market_cap_bin = "Large Cap"
        elif row['market_cap'] >= MID_CAP_THRESHOLD:
            market_cap_bin = "Medium Cap"
        else:
            market_cap_bin = "Small Cap"
        db.execute("update stocks set market_cap_bin = ? where id = ?", (market_cap_bin, row['id']))
    db.commit()

def bin_data_by_franking():
    data = database.query_db("select id, franking from stocks")
    db = database.get_db()
    for row in data:
        if row['franking'] == 0:
            franking_bin = "No Franking"
        elif row['franking'] == 100:
            franking_bin = "Fully Franked"
        else:
            franking_bin = "Partially Franked"
        db.execute("update stocks set franking_bin = ? where id = ?", (franking_bin, row['id']))
    db.commit()

def bin_data_by_div_yield():
    data = database.query_db("select id, div_yield from stocks")
    db = database.get_db()
    for row in data:
        if row['div_yield'] == 0 or row['div_yield'] == '':
            div_yield_bin = "0"
        if row['div_yield'] >= 10:
            div_yield_bin = ">=10"
        else:
            div_yield_bin = "%d-%d" % (int(row['div_yield']), int(row['div_yield']+1))
        db.execute("update stocks set div_yield_bin = ? where id = ?", (div_yield_bin, row['id']))
    db.commit()

def bin_data_by_eps():
    data = database.query_db("select id, eps from stocks")
    db = database.get_db()
    for row in data:
        if row['eps'] == None:
            eps_bin = None
        elif row['eps'] >= 0:
            eps_bin = "Positive Earnings"
        else:
            eps_bin = "Negative Earnings"
        db.execute("update stocks set eps_bin = ? where id = ?", (eps_bin, row['id']))
    db.commit()

def bin_data_by_tsr_3y():
    data = database.query_db("select id, tsr_3y from stocks")
    db = database.get_db()
    for row in data:
        if row['tsr_3y'] == None:
            tsr_3y_bin = None
        elif row['tsr_3y'] >= 100:
            tsr_3y_bin = "#07 TSR >= 100%"
        elif row['tsr_3y'] >= 50:
            tsr_3y_bin = "#06 50% <= TSR < 100%"
        elif row['tsr_3y'] >= 25:
            tsr_3y_bin = "#05 25% <= TSR < 50%"
        elif row['tsr_3y'] >= 0:
            tsr_3y_bin = "#04 0% <= TSR < 25%"
        elif row['tsr_3y'] >= -25:
            tsr_3y_bin = "#03 -25% <= TSR < 0%"
        elif row['tsr_3y'] >= -50:
            tsr_3y_bin = "#02 -50% <= TSR < -25%"
        else:
            tsr_3y_bin = "#01 TSR < -50%"
        db.execute("update stocks set tsr_3y_bin = ? where id = ?", (tsr_3y_bin, row['id']))
    db.commit()
