from pivotal_stocks import app
app.run(debug=True)

@app.route("/")
def hello():
    return "Hello World!"
