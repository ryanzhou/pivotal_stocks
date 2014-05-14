from pivotal_stocks import database
import matplotlib
import StringIO
from pylab import *

class Chart:
    def __init__(self, db_table, group_field, aggregation_function, aggregation_field):
        self.db_table = db_table
        self.group_field = group_field
        self.aggregation_function = aggregation_function
        self.aggregation_field = aggregation_field

    def horizontal_axis(self):
        output = []
        for column in database.query_db("select distinct %s from %s order by %s" % (self.group_field, self.db_table, self.group_field)):
            output.append(column[0])
        return output

    def values(self):
        query = "select %s(%s) from %s group by %s order by %s" % (self.aggregation_function, self.aggregation_field, self.db_table, self.group_field, self.group_field)
        output = []
        for row in database.query_db(query):
            output.append(row[0])
        return output

    def bar_chart(self):
        clf()
        barh(arange(len(self.values())), self.values())
        yticks(arange(1.0/2, len(self.horizontal_axis())), self.horizontal_axis(), rotation=0, fontsize=11)
        ylim(0, len(self.horizontal_axis()))
        title(self.human_name(), fontsize=18)
        png_out = StringIO.StringIO()
        savefig(png_out)
        return png_out.getvalue()

    def human_name(self):
        output = "%s of %s by %s" % (self.aggregation_function, self.aggregation_field, self.group_field)
        return output
