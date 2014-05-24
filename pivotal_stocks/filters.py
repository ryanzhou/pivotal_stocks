from pivotal_stocks import app
from flask import Markup
import json

@app.template_filter('big_number')
def big_number_filter(s):
    if s == None:
        return ''
    else:
        return "{:,.0f}".format(s)

@app.template_filter('number')
def number_filter(s):
    if s == None:
        return Markup('<span class="light">-</span>')
    elif isinstance(s, int):
        return "{:,.0f}".format(s)
    else:
        return "{:,.2f}".format(s)

@app.template_filter('percent')
def percent_filter(s):
    if s == None or s == '':
        return Markup('<span class="light">-</span>')
    else:
        return "{:.2f}%".format(s)

@app.template_filter('bin')
def bin_filter(s):
    if s != None and s[0] == "#":
        return s[4:]
    else:
        return s

@app.template_filter('to_json')
def to_json_filter(s):
    return json.dumps(s)

@app.template_filter('to_human')
def to_human_filter(s):
    words = []
    dict = {
        "sum": "Sum",
        "avg": "Average",
        "count": "Count",
        "min": "Minimum",
        "max": "Maximum",
        "asx_code": "ASX Code",
        "company_name": "Company Name",
        "sector": "Sector",
        'market_cap': "Market Cap",
        "div_yield": "Dividend Yield",
        "pe_ratio": "P/E Ratio",
        "franking": "Franking %",
        "tsr_3y": "3-Year TSR",
        "asx200": "ASX200 Constituent",
        "market_cap_bin": "Market Cap (Bins)",
        "div_yield_bin": "Dividend Yield (Bins)",
        "franking_bin": "Franking % (Bins)",
        "eps_bin": "Earnings (Bins)",
        "tsr_3y_bin": "3-Year TSR (Bins)",
        "contain": "contains",
        "not_contain": "does not contain",
        "t": "True",
        "f": "False"
    }
    for word in s.split():
        try:
            words.append(dict[word])
        except KeyError:
            words.append(word)
    return " ".join(words)
