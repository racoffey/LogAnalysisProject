#!/usr/bin/env python3
#
# The program extracts reports from the "Udacity News DB".
# The scripts report on the most popular articles, authors and
# also the HTTP errors reported back to users accessing the articles.

import psycopg2


# This method opens the DB connection and requests the three reports.
def log_analysis():
    """
        This method opens the DB connection to the "Udacity News DB"
        and then requests three reports:
        1. Top 3 most popular articles
        2. Authors ordered by number of views
        3. HTTP error report, showing days with more than 1% errors
    """
    # Open connection to "news" DB

    try:
        connection = psycopg2.connect("dbname=news")
    except psycopg2.Error as e:
        print ("Error: Unable to connect to news DB")
        print e.pgerror
        print e.diag.message_detail
    else:
        cursor = connection.cursor()

        # Request three reports
        get_most_popular_articles(cursor)
        get_authors_views(cursor)
        get_error_report(cursor)

        # Close DB connection
        connection.close()


# This method generates a report showing the 3 most popular articles
def get_most_popular_articles(cursor):
    """
        This method gets the 3 most popular articles and prints them
        together with the number of views.

        Parameters
        ---------
        cursor : Cursor
            DB connections cursor for safely running queries towards the DB.
    """
    # Join log and articles table by finding articles.slug in the log.path
    # string. Use this linkage to find the number of views for each article
    # and then select the top 3.
    cursor.execute("""select articles.title, count(*) as views
                   from log, articles
                   where log.path like CONCAT('%',articles.slug)
                   group by articles.title
                   order by views desc
                   limit 3;""")
    results = cursor.fetchall()

    # Print results in a structured format.
    print("-----------------------------------------------------")
    print("|      Top 3 most popular articles      |   Views   |")
    print("-----------------------------------------------------")
    for item in results:
        print("|   " + str(item[0]) + "    |  " + str(item[1])) + "   |"
    print("-----------------------------------------------------")


# This methods generates a report showing the authors by number of views
def get_authors_views(cursor):
    """
        This method get the authors and prints them in order of
        their articles views.

        Parameters
        ---------
        cursor : Cursor
            DB connections cursor for safely running queries towards the DB.
    """

    # Join log and articles table by finding articles.slug in the log.path
    # string and also articles and authors table using the author.id.
    # This linkage is used to find the number of article views by author.
    # The list of authors ordered by views is then printed.
    cursor.execute("""select authors.name, count(*) as views
                   from log, articles, authors
                   where log.path like CONCAT('%',articles.slug)
                   and articles.author = authors.id
                   group by authors.name
                   order by views desc;""")
    results = cursor.fetchall()

    # Print results in a structured format.
    print("-----------------------------------------------------")
    print("|                Author                 |   Views   |")
    print("-----------------------------------------------------")
    for item in results:
        string = "|                                        |            |"
        string = string[:4] + item[0] + string[5+len(item[0]):]
        string = string[:44] + str(item[1]) + string[45+len(str(item[1])):]
        print(string)
    print("-----------------------------------------------------")


# This method generates a report showing the percentage of HTTP errors
def get_error_report(cursor):
    """
        This method generates a report showing the percentage of HTTP errors
        for days when over 1% of responses are erroneus

        Parameters
        ---------
        cursor : Cursor
            DB connections cursor for safely running queries towards the DB.
    """

    # Needed views are created
    create_successes_view(cursor)
    create_failures_view(cursor)

    # Views are combined to provide % errors per day.  Days with over 1% errors
    # are extracted.
    cursor.execute("""select failures.time as date,
                   round(CAST(failures.num as decimal)/
                   CAST((successes.num+failures.num) as decimal)*100, 2)
                   as percent_errors from successes,failures
                   where successes.time = failures.time
                   and round(CAST(failures.num as decimal)/
                   CAST((successes.num+failures.num) as decimal)*100, 2) > 1;
""")
    results = cursor.fetchall()

    # Print results in a structured format.
    print("-----------------------------------------------------")
    print("|            Date              |   Percent Errors   |")
    print("-----------------------------------------------------")
    for item in results:
        string = "|                               |                     |"
        string = string[:10] + str(item[0]) + string[11+len(str(item[0])):]
        string = string[:40] + str(item[1]) + string[41+len(str(item[1])):]
        print(string)
    print("-----------------------------------------------------")

    # Clean up views
    clean_up(cursor)


def create_successes_view(cursor):
    """Create view with number of successful requests grouped by day"""
    cursor.execute("""create view successes as
                   select status, CAST(time As DATE), count(*) as num
                   from log where status like '2__ OK'
                   group by status, CAST(time AS DATE)
                   order by CAST(time AS DATE);""")


# Create view with number of failed requests grouped by day
def create_failures_view(cursor):
    """Create view with number of failed requests grouped by day"""
    cursor.execute("""create view failures as
                   select status, CAST(time As DATE), count(*) as num
                   from log
                   where status not like '2__ OK'
                   group by status, CAST(time AS DATE)
                   order by CAST(time AS DATE);""")


# Clean up views
def clean_up(cursor):
    """Delete the view tables to clean up"""
    cursor.execute("""drop view successes""")
    cursor.execute("""drop view failures""")

# Run program
log_analysis()
