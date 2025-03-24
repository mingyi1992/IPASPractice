import psycopg2
import pandas as pd
import warnings
from dotenv import load_dotenv
import os

class PostgreSQL_DB:
    def __init__(self) -> None:
        """
        讀取設定檔資訊
        """
        load_dotenv()
        
        self.host = os.getenv('DB_HOST')
        self.database = os.getenv('DB_DATABASE')
        self.username = os.getenv('DB_USERNAME')
        self.password = os.getenv('DB_PASSWORD')
        self.port = os.getenv('DB_PORT', 5432)
        self.cnxn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.username,
            password=self.password,
            port=self.port
        )

    def sql_list(self, sql: str, params: tuple = ()) -> list:
        """
        以list的格式讀取sql資料
        -
        params  
        sql : sql指令 (str)  
        params : 傳入的參數 (tuple)
        """
        with self.cnxn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def sql_df(self, sql: str, params: tuple = ()) -> pd.DataFrame:
        """
        以dataframe的格式讀取sql資料
        -
        params  
        sql : sql指令 (str)  
        params : 傳入的參數 (tuple)
        """
        warnings.filterwarnings("ignore", category=UserWarning)
        return pd.read_sql_query(sql, self.cnxn, params=params)

    def sql_upsert(self, sql: str, params: tuple = ()) -> None:
        """
        新增或寫入資料進sql
        -
        params  
        sql : sql指令 (str)  
        params : 傳入的參數 (tuple)
        """
        try:
            with self.cnxn.cursor() as cursor:
                cursor.execute(sql, params)
                self.cnxn.commit()
        except Exception as e:
            print(f"Error executing SQL statement: {e}")
            # 重新連接
            self.cnxn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.username,
                password=self.password,
                port=self.port
            )

    def close_connection(self):
        """
        關閉資料庫連線
        """
        if self.cnxn:
            self.cnxn.close()

class Databuilder:
    def __init__(self, postgre : PostgreSQL_DB):
        self.postgre = postgre
    def inputdata(self, file_name : str):
        """
        讀取資料並寫入資料庫
        """
        try:
            excel_file = pd.ExcelFile(f'./data_input/{file_name}.xlsx')
            sheet_name_list = excel_file.sheet_names
            
            for sheet in sheet_name_list:
                sql_query = f"""insert into "{sheet}" (id, question, A, B, C, D, answer) values (%s, %s, %s, %s, %s, %s, %s)"""
                df = pd.read_excel(f'./data_input/{file_name}.xlsx',sheet_name=sheet)
                for row in range(len(df)):
                    self.postgre.sql_upsert(sql_query, 
                                            (int(df.loc[row,'id']), str(df.loc[row,'question']), str(df.loc[row,'A'])
                                            , str(df.loc[row,'B']), str(df.loc[row,'C']), str(df.loc[row,'D']), str(df.loc[row,'answer'])))
        except Exception as e:
            print(e)

if __name__=='__main__':
    postgre = PostgreSQL_DB()
    data = Databuilder(postgre)
    data.inputdata('IPAS')
