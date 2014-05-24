from pivotal_stocks import database
from pivotal_stocks.pivot_table import PivotTable

class Chart:
    def __init__(self, pivot_table):
        self.pivot_table = pivot_table
        cursor = pivot_table.query()
        self.headers = list(map(lambda x: x[0], cursor.description))
        self.rows = cursor.fetchall()

    def categories(self):
        return self.headers[1:]

    def series(self):
        output = []
        for row in self.rows:
            output.append({
                'name': row[0],
                'data': list(row)[1:-1]
            })
        return output

    def title(self):
        return self.pivot_table.human_name()

    def y_title(self):
        return "%s of %s" % (self.pivot_table.aggregation_function, self.pivot_table.aggregation_field)

    def series_data(self):
        return map(lambda row: { 'name': row[0], 'y': list(row)[-1], 'drilldown': row[0] } , self.rows)

    def drilldown_series(self):
        output = []
        for row in self.rows:
            output.append({ 'name': row[0], 'id': row[0], 'data': map(lambda h: [h, row[h]], self.headers[1:-1])})
        return output
