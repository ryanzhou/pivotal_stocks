from flask import render_template, request, flash, redirect, url_for
from pivotal_stocks import app, database, datasource
from pivotal_stocks.pivot_table import PivotTable

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
    if 'asx200_list' in request.form:
        datasource.seed_asx200_list()
        flash("ASX 200 List has been imported.")
    return redirect(url_for('utilities'))

@app.route("/stocks")
def stocks():
    stocks = database.query_db("select * from stocks order by market_cap desc;")
    return render_template("stocks.html", stocks=stocks)

@app.route("/pivot")
def pivot():
    data_columns = [
      ["ASX Code", "asx_code"],
      ["Company Name", "company_name"],
      ["Sector", "sector"],
      ["Market Cap ('000)", "market_cap"],
      ["Dividend Yield", "div_yield"],
      ["P/E Ratio", "pe_ratio"],
      ["Franking %", "franking"],
      ["ASX200 Constituent", "asx200"]
    ]
    group_columns = [
      ["Sector", "sector"],
      ["Market Cap (Bins)", "market_cap_bin"],
      ["Dividend Yield (Bins)", "div_yield_bin"],
      ["Franking % (Bins)", "franking_bin"],
      ["ASX200 Constituent", "asx200"]
    ]
    filter_predicates = [
      ["is anything", "any"],
      ["=", "="],
      [">", ">"],
      [">=", ">="],
      ["<", "<"],
      ["<=", "<="],
      ["!=", "!="],
      ["contains", "contain"],
      ["does not contain", "not_contain"],
      ["is True", "t"],
      ["is False", "f"]
    ]
    aggregation_functions = [
      ["Sum", "sum"],
      ["Average", "avg"],
      ["Count", "count"],
      ["Minimum", "min"],
      ["Maximum", "max"],
      ["Standard Deviation", "stdev"],
      ["Variance", "var"]
    ]
    return render_template("pivot/index.html", data_columns=data_columns, group_columns=group_columns, filter_predicates=filter_predicates, aggregation_functions=aggregation_functions)

@app.route("/pivot/build", methods=['POST'])
def pivot_build():
    if request.form['filter_predicate'] in ['any']:
        return redirect(url_for('pivot_table',
          c_label=request.form['column_label'],
          r_label=request.form['row_label'],
          a_function=request.form['aggregation_function'],
          a_field=request.form['aggregation_field'],
          f_field="any",
          f_predicate="any",
          f_value="any"
        ))
    elif request.form['filter_predicate'] in ['t', 'f']:
        return redirect(url_for('pivot_table',
          c_label=request.form['column_label'],
          r_label=request.form['row_label'],
          a_function=request.form['aggregation_function'],
          a_field=request.form['aggregation_field'],
          f_field=request.form['filter_field'],
          f_predicate="=",
          f_value=request.form['filter_predicate']
        ))
    else:
        return redirect(url_for('pivot_table',
          c_label=request.form['column_label'],
          r_label=request.form['row_label'],
          a_function=request.form['aggregation_function'],
          a_field=request.form['aggregation_field'],
          f_field=request.form['filter_field'],
          f_predicate=request.form['filter_predicate'],
          f_value=request.form['filter_value']
        ))

@app.route("/pivot/table/<c_label>/<r_label>/<a_function>/<a_field>/<f_field>/<f_predicate>/<f_value>")
def pivot_table(c_label, r_label, a_function, a_field, f_field, f_predicate, f_value):
    pivot_table = PivotTable("stocks", c_label, r_label, a_function, a_field, f_field, f_predicate, f_value)
    cursor = pivot_table.query()
    headers = list(map(lambda x: x[0], cursor.description))
    rows = cursor.fetchall()
    footers = pivot_table.footer_query()
    sql = pivot_table.sql()
    return render_template("pivot/table.html", headers=headers, rows=rows, footers=footers, sql=sql, human_name=pivot_table.human_name())
