import os.path
import sys
from dotenv import load_dotenv
import pymysql
import io

def count_perf(f):
    import datetime
    def wraper(*args, **kwargs):
        time_init = datetime.datetime.now()
        result = f(*args, **kwargs)
        time_end = datetime.datetime.now()
        total = time_end - time_init
        print('Time: {}'.format(total))
        return result
    return wraper


def prepare_for_multiple_insert(table, columns, raws):
    VALUES = []
    #create string struct like (%s %s)
    SQL_VALUES_COLS = '(%s)' % (', '.join("%s" for _ in columns))

    #create column struct
    SQL_COLS = ', '.join(columns)

    #create SQL struct
    SQL_REQUEST = "INSERT INTO %s (%s) VALUES %s" % (table,
                                                     SQL_COLS,
                                                     ', '.join(SQL_VALUES_COLS for _ in raws))

    return SQL_REQUEST


def db_connection_echo():
    connection = pymysql.connect(host=os.environ.get('MYSQL_HOST'),
                                 user=os.environ.get('MYSQL_USER'),
                                 password=os.environ.get('MYSQL_PASS'),
                                 db=os.environ.get('MYSQL_DB'),
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        query = """
                SELECT * FROM MYSQL.USER
                """
        cursor.execute(query)
        connection.commit()
        for row in cursor:
            print(row)
    connection.close()


def check_params():
    if len(sys.argv) <= 1:
        return print('No file to upload, Need: python uploader.py file.csv')

    file = sys.argv[1]
    if os.path.exists(file):
        try:
            source, url = input('Enter source info (name and url) over space: ').split(" ")
        except:
            print('Source name wrong, set default')

        if len(source) <= 3 or len(source) <= 3:
            print('[-] Error params')
            sys.exit(-1)

        connection = pymysql.connect(host=os.environ.get('MYSQL_HOST'),
                                     user=os.environ.get('MYSQL_USER'),
                                     password=os.environ.get('MYSQL_PASS'),
                                     db=os.environ.get('MYSQL_DB'),
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            cursor.execute("select `id` FROM leaker.source where url='%s' and name='%s'" % (url, source))
            connection.commit()
            source_id = cursor.fetchone()

            if not source_id or source_id == 0 or source_id == '':
                cursor.execute("INSERT IGNORE INTO `source` (`name`, `url`) VALUES (%s, %s)", [source, url])
                connection.commit()
                source_id = cursor.lastrowid
            else:
                source_id = source_id['id'] if 'id' in source_id else ''

    return file, source, url, connection, source_id

def string_post_processing(string):

    '''force all to lower case '''
    try:
        string = string.lower()
    except:
        pass
    '''remove unknown element'''
    try:
        string = string.replace('\\n', '').strip()
    except:
        pass
    '''limit to 128 symbols'''
    try:
        string = string[:128]
    except:
        pass

    return string

@count_perf
def read_from_file():
        file, source, url, connection, source_id = check_params()

        print('[+] Load file: "%s"' % (file))
        splitter = input('Enter splitter ("=" or "," or " " etc): ')
        columns = input('Enter columns index for [phone, email, fio] over space (ex: 1 3 5 6): ')
        MAX_INSERT_DATA = int(os.environ.get('TABLE_PERFORMANCE_SIZE')) or 1000


        BUFFER = []
        with io.open(file, encoding='utf-8', mode='r') as f:
            cnt = 0

            for line in (f):
                tmp = []
                raw = line.strip()
                if len(line) == 0: continue
                raw = raw.split(splitter) if len(splitter) >= 1 else raw.split('\t')
                if len(columns) == 0:
                    print(raw)
                else:
                    for column in columns.split(' '): # [9 7 6+5+11]
                            if '+' in column:
                                el_buf = column.split('+') # [6 5 1]
                                for i, x in enumerate(el_buf):
                                    try:
                                        el_buf[i] = raw[int(x) - 1] if int(x) <= len(raw) else ''
                                    except:
                                        pass
                                el = ' '.join(el_buf)
                            else:
                                el = raw[int(column) - 1] if int(column) <= len(raw) else ''

                            el = string_post_processing(el)
                            tmp.append(el)

                    tmp.append(source_id)
                    BUFFER.append(tuple(tmp))
                    cnt += 1

                if cnt >= MAX_INSERT_DATA:
                        sql = prepare_for_multiple_insert("leaker.data", ["phone", "email", "fio", "source"], BUFFER)
                        values = [_ for r in BUFFER for _ in r]
                        with connection.cursor() as cursor:
                             cursor.execute(sql, values)
                             connection.commit()
                        BUFFER.clear()

            print('[+] Wrote {} records'.format(cnt))
            return cnt
        return print('[-] General error 0')

if __name__ == '__main__':
    load_dotenv()
    read_from_file()
