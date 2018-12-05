'''Module used to generate report of log analysis
Report is genrated by executing sql queries on log database tables'''

import psycopg2

# sql queries to answer specific questions

query1 = '''SELECT articles.title, COUNT(articles.title) AS views
            FROM articles, log
            WHERE log.path LIKE '%'||articles.slug||'%' AND
            log.status = '200 OK'
            GROUP BY articles.title ORDER BY views DESC
            LIMIT 3;'''

query2 = '''SELECT t.name, COUNT(t.name) AS views FROM
            (SELECT authors.name, articles.slug FROM
                authors JOIN articles ON
                authors.id = articles.author
            ) AS t, log
            WHERE log.path LIKE '%'||t.slug||'%'
            AND log.status='200 OK'
            GROUP BY t.name
            ORDER BY views DESC;'''

query3 = '''SELECT temp.day, temp.perc FROM
            (SELECT all_count_t.day,
                ROUND((error_count_t.count::decimal)/all_count_t.count *100,2)
                AS perc
                FROM
                    (SELECT date(time) AS day, count(*) AS count
                        FROM log WHERE
                        log.status != '200 OK'
                        GROUP BY day ORDER BY day) AS error_count_t,
                    (SELECT date(time) AS day, count(*) AS count
                        FROM log WHERE
                        log.status = '200 OK'
                        GROUP BY day ORDER BY day) AS all_count_t
                WHERE error_count_t.day = all_count_t.day) AS temp
            WHERE temp.perc > 1;'''


def execute_query(query):
    '''Function used to connect to database and execute query'''
    conn = psycopg2.connect(dbname='news')
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    conn.close()
    return results


def print_result1():
    '''Prints result of query1'''
    results = execute_query(query1)
    print('Most popular three articles of all time..!!')
    print('Article Title'+' \t \t \t '+'Number of Views')
    print('-----------------------------------------------')
    for result in results:
        print(result[0] + ' - '+str(result[1]) + ' views')


def print_result2():
    '''Prints result of query2'''
    results = execute_query(query2)
    print('Most popular authors of all time..!!')
    print('Author name'+'\t\t'+'Number of Views')
    print('----------------------------------------')
    for result in results:
        print(result[0] + '-\t' + str(result[1]) + ' views')


def print_result3():
    '''Prints result of query3'''
    results = execute_query(query3)
    print('Day when more than 1% requests lead to error..!!')
    print('Date' + '\t' + 'Error percentage')
    print('----------------------------')
    for result in results:
        print(str(result[0]) + ' - ' + str(result[1]) + '%')


print_result1()
print('\n\n')
print_result2()
print('\n\n')
print_result3()
