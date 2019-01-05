import psycopg2

DBNAME = "news"


def most_popular_three_articles():
    """returns the most popular three articles of all time"""

    # Query to fetch the most populr three articles of all tume
    query = """select title as article_title, count(*) as article_views
    from log, articles where path = '/article/' || articles.slug
    and status = '200 OK' group by articles.title
    order by article_views desc limit 3"""

    # Create connection object
    db = psycopg2.connect(database=DBNAME)

    # Create cursor
    c = db.cursor()

    # Execute the query
    c.execute(query)

    # Get the query result
    popular_articles = c.fetchall()

    # Print the result
    print "The most popular three articles of all time are :\n"
    for article in popular_articles:
        print '\t"', article[0], '" -- ', article[1], 'views'
    print "\n"
    db.close()


def most_popular_article_authors():
    """returns the most popular article authors of all time"""

    # Query to fetch the most popular article authors of all time
    query = """select authors.name, count(*)
    from log, articles, authors
    where path = '/article/' || articles.slug
        and (authors.id = articles.author)
    group by authors.id order by count desc"""

    # Create connection object
    db = psycopg2.connect(database=DBNAME)

    # Create cursor
    c = db.cursor()

    # Execute the query
    c.execute(query)

    # Get the query result
    popular_authors = c.fetchall()

    # Print the result
    print "The most popular article authors of all time are :\n"
    for author in popular_authors:
        print '\t', author[0], ' -- ', author[1], 'views'
    print "\n"
    db.close()


def day_s_more_than_1percent_of_requests_lead_to_errors():
    """returns which days did more than 1% of requests lead to errors"""

    # Query to fetch which days did more than 1% of requests lead to errors
    query = """select day, percentage
    from
    (
        select (round((not_found::numeric/total)*100.0,3)) as Percentage, day
        from
        (
        select
        count(case when status = '404 NOT FOUND' then 1 end) as not_found,
        count(status) as total, date(time) as day
            from log group by date(time)
            order by date(time)
        )as q
    )
    as q where percentage > 1.0"""

    # Create connection object
    db = psycopg2.connect(database=DBNAME)

    # Create cursor
    c = db.cursor()

    # Execute the query
    c.execute(query)

    # Get the query result
    results = c.fetchall()

    # Print the result
    print "day(s) did more than 1% of requests lead to errors :\n"
    for res in results:
        print '\t', res[0], ' -- ', res[1], '% errors'
    print "\n"
    db.close()


print "\n"
most_popular_three_articles()

print "\n"
most_popular_article_authors()

print "\n"
day_s_more_than_1percent_of_requests_lead_to_errors()
