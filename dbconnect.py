import pymysql
from pymysql.constants import CLIENT
class connectdb():
    def __init__(self):
        self.db = pymysql.connect(host='49.234.83.197',user='root',password='Biu123@',database='gx',client_flag=CLIENT.MULTI_STATEMENTS)
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
    def close(self):
        self.db.commit()
        self.cursor.close()
        self.db.close()
    def sql_format(self,a):
        return pymysql.escape_string(a)
