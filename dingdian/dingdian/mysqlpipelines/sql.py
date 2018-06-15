import pymysql
from dingdian import settings

MYSQL_HOST = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB


cnx = pymysql.connect(host=MYSQL_HOST, port=int(MYSQL_PORT), user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB, charset='utf8')
cur = cnx.cursor()


class Sql:
    @classmethod
    def insert_dd_name(cls, xs_name, xs_author, category, name_id):
        sql = "INSERT INTO dd_name (xs_name, xs_author, category, name_id) values (%s, %s, %s, %s)"
        value = (xs_name, xs_author, category, name_id)
        print(sql)
        cur.execute(sql, value)
        cnx.commit()


    @classmethod
    def select_name(cls, name_id):
        sql = "SELECT EXISTS (SELECT 1 FROM dd_name WHERE name_id = %(name_id)s)"
        value = {
            "name_id" : name_id
        }
        cur.execute(sql, value)
        return cur.fetchall()[0]

    @classmethod
    def insert_dd_chaptername(cls, xs_chaptername, xs_content, id_name, num_id, url):
        sql = "INSERT INTO dd_chaptername(xs_chaptername, xs_content, id_name, num_id, url)values(%(xs_chaptername)s, %(xs_content)s, %(id_name)s, %(num_id)s, %(url)s)"
        value = {
            "xs_chaptername" : xs_chaptername,
            "xs_content" : xs_content,
            "id_name" : id_name,
            "num_id" : num_id,
            "url" : url
        }
        cur.execute(sql, value)
        cnx.commit()


    @classmethod
    def select_chapter(cls, url):
        sql = "SELECT EXITST(SELECT 1 FROM dd_chaptername WHERE url=%(url)s)"
        value={
            "url": url
        }
        return cur.fetchall(sql, value)[0]

