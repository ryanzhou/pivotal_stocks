from pivotal_stocks import database

class PivotTable:
    def __init__(self, db_table, column_label, row_label, aggregation_function, aggregation_field, filter_field, filter_predicate, filter_value):
        self.db_table = db_table
        self.column_label = column_label
        self.row_label = row_label
        self.aggregation_function = aggregation_function
        self.aggregation_field = aggregation_field
        self.filter_field = filter_field
        self.filter_predicate = filter_predicate
        self.filter_value = filter_value

    def sql(self):
        return " ".join([self.select_sql(), self.filter_sql(), self.group_by_sql()])

    def select_sql(self):
        return "SELECT %s, %s FROM %s" % (self.row_label, self.columns_sql(), self.db_table)

    def group_by_sql(self):
        return "GROUP BY %s" % (self.row_label)

    def columns_sql(self):
        columns = self.distinct_values(self.column_label)
        sql = []
        for column in columns:
            column = column[0]
            sql.append("%s(CASE WHEN %s = '%s' THEN %s END) AS '%s'" % (self.aggregation_function, self.column_label, column, self.aggregation_field, column))
        sql.append("%s(%s) AS 'All'" % (self.aggregation_function, self.aggregation_field))
        return ", ".join(sql)

    def filter_sql(self):
        if self.filter_predicate == "any" or self.filter_predicate == None:
            return ''
        elif self.filter_predicate == "contain":
            return "where %s like '%%%s%%'" % (self.filter_field, self.filter_value)
        elif self.filter_predicate == "not_contain":
            return "where %s not like '%%%s%%'" % (self.filter_field, self.filter_value)
        else:
            return "where %s %s '%s'" % (self.filter_field, self.filter_predicate, self.filter_value)

    def distinct_values(self, column):
        return database.query_db("select distinct %s from %s order by %s" % (column, self.db_table, column))

    def query(self):
        db = database.get_db()
        return db.execute(self.sql())

    def footer_query(self):
        sql = "\n".join([self.select_sql(), self.filter_sql()])
        return database.query_db(sql, (), True)

    def human_name(self):
        output = "%s of %s by %s and %s" % (self.aggregation_function, self.aggregation_field, self.row_label, self.column_label)
        if self.filter_predicate != "any" and self.filter_predicate != None:
            output += " when %s %s %s" % (self.filter_field, self.filter_predicate, self.filter_value)
        return output
