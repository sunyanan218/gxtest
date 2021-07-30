from dbconnect import connectdb
class a(connectdb):
    def selectrobot(self):
        c=connectdb()
        result=c.cursor.execute('''select taskid from task where robotid=1 and date(begintime)= "2021-07-27" ''')
        print(c.cursor.fetchall())
        c.close()

a=a()
a.selectrobot()
