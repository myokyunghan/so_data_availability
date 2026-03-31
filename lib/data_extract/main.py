import setting_for_sda.config as conf
from setting_for_sda.date_setting import Date_Setting
from setting_for_sda.path_setting import path_list

from lib.database.DBInterface import DBInterface
from lib.utils.file_io import save_json, create_dir
from datetime import datetime

class ExtractData : 

    def __init__(self, dict_):
        # setting for the data extraction
        self.db_if = DBInterface()
        self.lang=dict_['lang']
        self.year_start = dict_['year_start']
        self.year_end = dict_['year_end']
        self.schema = conf.database_info['schema']

        self.year_range = f'{self.year_start}to{self.year_end}'
        self.monthly_timestamps = Date_Setting[self.year_range]["monthly_timestamps"]
        self.save_dir = f"{path_list['data_root_dir']}/data/{self.schema}/questions/{self.lang}/{self.year_range}/"
        print("Data will be saved in ", self.save_dir)
        print("monthly_timestamps is", self.monthly_timestamps)
        

    def __call__(self):
        self.run()
    
    def run(self):
        create_dir(self.save_dir)
        self.extract_data()

    def extract_data(self):
        print(f'Start {self.lang} Data Extraction from {self.year_start} to {self.year_end}')
        for idx in range(len(self.monthly_timestamps)-1):
            st_dt = datetime.strptime(self.monthly_timestamps[idx], "%Y.%m.%d")
            end_dt = datetime.strptime(self.monthly_timestamps[idx+1], "%Y.%m.%d")



            sql = """select p.id, p.creationdate, p.title, p.tags, p2.body from posts p , postsbody p2 where p.id = p2.id and p.posttypeid = '1' and p.tags like %s and p.creationdate >=  %s and p.creationdate < %s """
            rows = self.db_if.execute_query(sql, (f"%<{self.lang}>%", st_dt, end_dt))
        
            dict_q = [{ 'id' : row[0], 
                        'creationdate' : row[1].isoformat(),
                        'title' : row[2],
                        'tags' : row[3],
                        'body' : row[4]
                    } for row in rows]
            if len(dict_q) > 0 : 
                save_json(dict_q, f'{self.save_dir}{idx}.json')
        print(f'End {self.lang} Data Extraction from {self.year_start} to {self.year_end}')

