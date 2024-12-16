import configparser
import mysql.connector
from mysql.connector import MySQLConnection

# 创建配置解析器
config = configparser.ConfigParser()
# 读取配置文件
config.read('E:\\git_project\\bind-news-recommender-flask\\config\\config.ini')
# 使用示例
db_config = {
    "host": config.get('database', 'db_host'),
    "port": config.getint('database', 'db_port'),
    "user": config.get('database', 'db_user'),
    "password": config.get('database', 'db_password'),
    "database": config.get('database', 'db_name')
}

## 修改版本
class mysql_utils:
    _conn:MySQLConnection = None
    _cursor = None

    def __init__(self):
        '''
        初始数据库的连接对象
        '''
        self._conn =  mysql.connector.connect(**db_config)
        self._cursor = self._conn.cursor(dictionary=True)

    def __del__(self):
        self.close_connection()

    def close_connection(self):
        '''
        关闭连接
        :return:
        '''
        if getattr(self, '_cursor', None):
            self._cursor.close()
        if getattr(self, '_conn', None):
            self._conn.close()
            self._conn = None


    def do_execute(self, query_str, values=None, isSingle=False):
        """
        Execute database operations.
        :param query_str: SQL query string to be executed.
        :param values: Parameters for the SQL query, if any.
        :param is_single: Whether the query result should return a single record.
        :return: Last row ID for insert queries, a single record, or a list of records based on the query and parameters.
        """
        if not query_str:
            return None

        # Ensure values is a tuple if provided
        if values is not None and not isinstance(values, tuple):
            values = tuple(values)

        # Execute the query with or without parameters
        if values:
            self._cursor.execute(query_str, values)
        else:
            self._cursor.execute(query_str)

        # Commit if it's an insert query
        if query_str.strip().lower().startswith("insert"):
            self._conn.commit()
            return self._cursor.lastrowid

        # Fetch results based on is_single flag
        result = self._cursor.fetchone() if isSingle else list(self._cursor.fetchall())
        return result
