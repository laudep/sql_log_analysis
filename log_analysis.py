#!/usr/bin/env python3
"""
Project: Logs Analysis
Udacity Full Stack Nanodegree
"""

import psycopg2


class ReportQuery:

    def __init__(self, title, query, outputForm):
        self.title = title
        self.query = query
        self.outputForm = outputForm

    def get_and_print_results(self, cursor):
        cursor.execute(self.query)
        results = cursor.fetchall()
        self.print_title()
        for result in results:
            print(self.outputForm
                  .format(result[0], result[1]))
        print('')

    def print_title(self):
        SEPARATOR_CHAR = "="
        output = "\n" + self.title + "\n"
        for i in range(len(self.title)):
            output += SEPARATOR_CHAR

        print(output)
        return


def db_connect(db_name="news"):
    """Connects to database and returns a database cursor.

     Keyword arguments:
    db_name -- name of the database to connect to (default "news")
    """
    try:
        database = psycopg2.connect("dbname={}".format(db_name))
        cursor = database.cursor()
    except psycopg2.OperationalError as e:
        print("Error connecting to database \"{0}\"!\n{1}".format(db_name, e))
        return None
    else:
        return cursor


def prepare_report_queries():
    """Returns a list with relevant ReportQuery objects for report."""
    TOP_ART_TITLE = 'Three most popular articles of all time'
    TOP_ART_QUERY = """
            SELECT articles.title,
                   count(*)
            FROM   log,
                   articles
            WHERE  log.path = '/article/' || articles.slug
            GROUP BY articles.title
            ORDER BY count(*) DESC
            LIMIT 3;
    """
    TOP_ART_OUTPUT = '"{0}" - {1} views'

    TOP_AUTHORS_TITLE = 'Most popular authors of all time'
    TOP_AUTHORS_QUERY = """
            SELECT authors.name,
                   count(*)
            FROM   log,
                   articles,
                   authors
            WHERE  log.path = '/article/' || articles.slug
              AND articles.author = authors.id
            GROUP BY authors.name
            ORDER BY count(*) DESC;
    """
    TOP_AUTHORS_OUTPUT = '{0} - {1} views'

    DAYS_ERROR_GT_1PC_TITLE = 'Days with greater than 1% errors in requests'
    DAYS_ERROR_GT_1PC_QUERY = """
            WITH request_count AS (
                SELECT time::date AS day, count(*)
                FROM log
                GROUP BY time::date
                ORDER BY time::date
              ), error_count AS (
                SELECT time::date AS day, count(*)
                FROM log
                WHERE status != '200 OK'
                GROUP BY time::date
                ORDER BY time::date
              ), error_rate AS (
                SELECT request_count.day,
                  error_count.count::float / request_count.count::float * 100
                  AS error_pc
                FROM request_count, error_count
                WHERE request_count.day = error_count.day
              )
            SELECT * FROM error_rate WHERE error_pc > 1;
    """
    DAYS_ERROR_GT_1_PC_OUTPUT = '{0:%B %d, %Y} - {1:.1f}% errors'

    return [
        ReportQuery(TOP_ART_TITLE, TOP_ART_QUERY, TOP_ART_OUTPUT),
        ReportQuery(TOP_AUTHORS_TITLE, TOP_AUTHORS_QUERY, TOP_AUTHORS_OUTPUT),
        ReportQuery(DAYS_ERROR_GT_1PC_TITLE, DAYS_ERROR_GT_1PC_QUERY,
                    DAYS_ERROR_GT_1_PC_OUTPUT)
    ]


if __name__ == "__main__":
    CURSOR = db_connect()
    if CURSOR:
        queryList = prepare_report_queries()
        for query in queryList:
            query.get_and_print_results(CURSOR)

        CURSOR.close()
