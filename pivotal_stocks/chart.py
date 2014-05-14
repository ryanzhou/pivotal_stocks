from pivotal_stocks import database
from pivotal_stocks.pivot_table import PivotTable
import pygal
from pygal.style import LightStyle

class Chart:
    def __init__(self, pivot_table):
        self.pivot_table = pivot_table
        cursor = pivot_table.query()
        self.headers = list(map(lambda x: x[0], cursor.description))
        self.rows = cursor.fetchall()

    def bar_chart(self):
        chart = pygal.Bar(style=LightStyle)
        chart.title = self.pivot_table.human_name()
        chart.x_labels = self.headers[1:-1]
        for row in self.rows:
            chart.add(row[0], list(row)[1:-1])
        return chart.render()
