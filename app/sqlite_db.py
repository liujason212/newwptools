import sqlite3
from config import sqlite_db_pth
def initial_db():
    #尝试连接数据库
    conn=sqlite3.connect(sqlite_db_pth)
    cursor=conn.cursor()
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='web_config'")
    if_table_exsit=cursor.fetchall()
    print ('web_config exsit or not')
    print(if_table_exsit)
    #判断是表是否已经存在
    if if_table_exsit[0][0] <1:
        cursor.execute('create table web_config (id varchar(20) primary key, password varchar(20),token varchar(20))')
    cursor.execute('SELECT *from web_config where id=?',('1',))
    values = cursor.fetchall()
    print(len(values))
    #判断默认值是否已经产生
    if len(values)<1:
        cursor.execute('INSERT into web_config(id,password,token)values(\'1\',\'add your password\',\'add your token\')')
    else:
        print('已经完成初始化')
    cursor.close()
    conn.commit()
    cursor=conn.cursor()
    cursor.execute('SELECT *from web_config where id=?',('1',))
    values=cursor.fetchall()
    print(values)
    cursor.close()
    conn.close()
    print('success')

def update_db_password(web_password):
    conn = sqlite3.connect(sqlite_db_pth)
    cursor = conn.cursor()
    cursor.execute('UPDATE web_config SET password="%s" WHERE ID=1' % (web_password))
    cursor.execute('SELECT *from web_config where id=?', ('1',))
    values = cursor.fetchall()
    print(values)
    cursor.close()
    conn.commit()
    conn.close()
    print('password setting success')

def update_db_token(token):
    conn = sqlite3.connect(sqlite_db_pth)
    cursor = conn.cursor()
    cursor.execute('UPDATE web_config SET token="%s" WHERE ID=1' % (token))
    cursor.execute('SELECT *from web_config where id=?', ('1',))
    values = cursor.fetchall()
    print(values)
    cursor.close()
    conn.commit()
    conn.close()
    print('token setting success')


def get_db_password():
    conn = sqlite3.connect(sqlite_db_pth)
    cursor = conn.cursor()
    cursor.execute('SELECT *from web_config where id=?', ('1',))
    values = cursor.fetchall()
    values=values[0][1]
    print(values)
    return values

def get_db_token():
    conn = sqlite3.connect(sqlite_db_pth)
    cursor = conn.cursor()
    cursor.execute('SELECT *from web_config where id=?', ('1',))
    values = cursor.fetchall()
    values = values[0][2]
    print(values)
    return values


#update_db_password('noway')
#initial_db()



