pivotal_stocks
==============

Pivotal Stocks is a pivot table generator for ASX companies.

## Vendoring packages

As this project is going to be run in a shared CGI environment (IVLE), all packages are vendored into the `/vendor` directory using pip:

    pip install -r requirements.txt -t vendor/

In `pivotal_stocks/__init__.py`, the `vendor` and `lib` directory is added to the Python PATH:

    import sys, os
    # Add /vendor and /lib to python PATH
    sys.path.append(os.path.join(os.path.dirname(__file__), "../vendor"))
    sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))
