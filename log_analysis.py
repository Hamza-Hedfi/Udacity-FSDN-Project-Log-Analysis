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