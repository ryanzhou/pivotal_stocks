from pivotal_stocks import app
from flask import Markup

@app.template_filter('big_number')
def big_number_filter(s):
    if s == None:
        return ''
    else:
        return "{:,.0f}".format(s)

@app.template_filter('number')
def number_filter(s):
    if s == None:
        return Markup('<span class="light">N/A</span>')
    elif isinstance(s, int):
        return "{:,.0f}".format(s)
    else:
        return "{:,.2f}".format(s)

@app.template_filter('percent')
def percent_filter(s):
    if s == None or s == '':
        return Markup('<span class="light">N/A</span>')
    else:
        return "{:.2f}%".format(s)

@app.template_filter('bin')
def bin_filter(s):
    if s != None and s[0] == "#":
        return s[4:]
    else:
        return s
