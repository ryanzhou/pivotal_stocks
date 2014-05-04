Pivotal Stocks
==============

Pivotal Stocks is a ASX stocks data explorer and pivot table generator based on Flask microframework. It's written in Python, with a bit of SQL, HTML5 (Jinja2) and CSS.

## Running the web app

There are two ways to run Pivotal Stocks: the built-in WSGI server or CGI.

If possible, running the built-in WSGI server is much more performant than CGI:

    python run.py

Then open the browser at http://localhost:5000 to use the web application.

Otherwise, the `cgi.py` file can be used in CGI (such as in IVLE). You can optionally configure URL rewrites to generate "pretty URLs", but that's not possible in IVLE.

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

## Security

Pivotal Stocks is an assignment project and not a commercial product. It's designed with functionality and proof of concepts in mind, not security. Please do not run Pivotal Stocks as a public web service in a mission-critical production server yet.

There's still a lot to do to make this app more secure, for example, by adding user input sanitizing and authentication.
