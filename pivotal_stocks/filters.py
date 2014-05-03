from pivotal_stocks import app

@app.template_filter('big_number')
def big_number_filter(s):
    return "{:,.0f}".format(s)

@app.template_filter('percent')
def percent_filter(s):
    if len(str(s)) > 0:
        return "{:.2f}%".format(s)
    else:
        return ""
