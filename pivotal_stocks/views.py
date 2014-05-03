from flask import render_template, request, flash, redirect, url_for
from pivotal_stocks import app, database, datasource

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/utilities")
def utilities():
    return render_template('utilities.html')

@app.route("/utilities/init_db", methods=['POST'])
def utilities_init_db():
    if 'confirmation' in request.form:
        database.init_db()
        flash("Database reinitialized successfully.")
        return redirect(url_for('utilities'))
    else:
        error = "You must check the confirmation checkbox to initialize database."
        return render_template('utilities.html', error=error)

@app.route("/utilities/seed_data", methods=['POST'])
def utilities_seed_data():
    if 'securities_list' in request.form:
        datasource.seed_securities_list()
        flash("Securities List has been imported.")
    if 'industry_groups' in request.form:
        datasource.seed_industry_groups()
        flash("Industry Groups has been imported.")
    return redirect(url_for('utilities'))

@app.route("/stocks")
def stocks():
    stocks = database.query_db("select * from stocks order by market_cap desc;")
    return render_template("stocks.html", stocks=stocks)
