Pivotal Stocks
==============

Pivotal Stocks is a ASX stocks data explorer and pivot table generator based on Flask microframework. It's written in Python, with a bit of SQL, HTML5 (Jinja2) and CSS.

## Running the web app

There are two ways to run Pivotal Stocks: the built-in WSGI server or CGI.

If possible, running the built-in WSGI server is much more performant than CGI:

    python run.py

Then open the browser at http://localhost:5000 to use the web application.

Otherwise, the `cgi.py` file can be served in CGI (such as in IVLE), thanks to `CGIHandler` in `wsgiref`. You can optionally configure URL rewrites to generate "pretty URLs", but that's not possible in IVLE.

## Dependency management

As this project is designed to be fully self-contained, all packages have been vendored into the `/vendor` directory using pip:

    pip install -r requirements.txt -t vendor/

In `pivotal_stocks/__init__.py`, the `vendor` and `lib` directory is added to the Python PATH:

    import sys, os
    # Add /vendor and /lib to python PATH
    sys.path.append(os.path.join(os.path.dirname(__file__), "../vendor"))
    sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

## Utilities

To make system maintenance easier, there are a few built-in utilities in the web interface for easy-to-use management. For example, you can initialize the entire sqlite database or seed data from external sources.

After the app is running, you can find a link to `/utilities` in the navigation bar.

## Features

Pivotal Stocks offers many features that exceed the minimum project requirements:

* **Data Explorer**: The built-in Data Explorer allows users to sort and search data interactively, using JavaScript. This is powered by jQuery plugin dataTables.
* **Filter Predicates**: Users can build pivot tables with 10 different filter predicates. Making filters like "Market Cap >= 5000000" or "Company Name contains 'Bank'" possible.
* **Meaningfulness Detection**: Pivotal Stocks will return an error if the combination of Pivot Table parameters doesn't make meaningful sense.
* **Pivot Chart**: In Pivot Stocks, Pivot Charts are derived from Pivot Tables of the same parameters. Available in bar chart and pie chart format, Pivot Charts allow users to visualise any generated Pivot Table.
* **Bubble Chart**: Bubble Chart offers the best way to explore data visually with multiple dimensions of information. In Pivot Stocks, P/E Ratio, Dividend Yield, Market Cap and Sector of all ASX 200 companies can all be viewed in a single screen.
* **Observations**: Pivot Stocks includes 5 examples of applying Pivot Table parameters to get useful output. Each example includes a link to the relevant Pivot Table, and also the appropriate Pivot Chart based on the context.
* **Natural Language Titles**: Even though database columns are named in short-codes (such as `franking_bin`), Pivotal Stocks automatically translates column names to user-friendly English words (such as "Franking % (Bins)"). This way, chart titles can be automatically generated (e.g. "Average of Dividend Yield by Franking % (Bins) and Sector when ASX200 Constituent = True").
* **SQL Queries**: All Pivot Tables are generated directly by querying the database with constructed SQL queries that don't depend on the `pivot` SQL function (which isn't supported in SQLite).


## Security

Pivotal Stocks is an assignment project and not a commercial product. It's designed with functionality and proof of concepts in mind, not security. Please do not run Pivotal Stocks as a public web service in a mission-critical production server yet.

There's still a lot to do to make this app more secure, for example, by adding user input sanitizing and authentication.
