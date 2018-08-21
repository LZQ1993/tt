import pymysql

class MysqlDao(object):

    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                passwd='root',
                db='patent',
                charset='utf8'
            )
        except Exception as e:
            print(e)
        else:
            self.cur = self.conn.cursor()

    def create_table(self):
        sql = 'create table patent(id int, name varchar(10),age int)'
        res = self.cur.execute(sql)

    def close(self):
        self.cur.close()
        self.conn.close()

    def query(self,sql):
        res0 = self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def add(self,inventName,applyNum,applyDate,publicNum,publicDate,IPCnum,applyPeople,inventPeople):  # 增
        query_sql = "select * from brakingInfo where publicNum='" + publicNum + "'"
        if len(self.query(query_sql)) == 0:
            insert_sql = "insert into brakingInfo(inventName,applyNum,applyDate,publicNum,publicDate,IPCnum,applyPeople,inventPeople) VALUES ('" + inventName + "','" + applyNum + "','" + applyDate + "','" + publicNum + "','" + publicDate + "','" + IPCnum + "','" + applyPeople + "','" + inventPeople + "')"
            res = self.cur.execute(insert_sql)
            if res:
                self.conn.commit()
            else:
                self.conn.rollback()