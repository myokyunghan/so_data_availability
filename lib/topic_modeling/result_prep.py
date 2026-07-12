import pandas as pd
import numpy as np
from datetime import datetime
import os
import re
from setting_for_sda.path_setting import path_list
from setting_for_sda.date_setting import Date_Setting
from lib.utils.file_io import *

from lib.utils.datetime_handler import calc_rel_period

class Result_Prep: 
    def __init__(self, target_idx , model_in_run = None) : 
        self.idx = target_idx
        self.visualization_target = f'run_id_{target_idx}'

        if model_in_run is not None:
            self.model_in_run = model_in_run
        else:
            self.model_in_run = 'tag'


        self.viz_dir = f'{path_list["data_root_dir"]}/result/{model_in_run}/{self.visualization_target}'

        self.data_dir = f"{self.viz_dir}/data"
        self.option_dict = load_json(f"{self.viz_dir}/option.json")
        self.std_date = Date_Setting[self.option_dict['year_range']]['std_date']

    
    def data_prep(self) : 
        return_ = load_df(self.data_dir, ['id' , 'creationdate' , 'title', 'tags', 'body', 'Topic'])
        return_ = calc_rel_period(return_, self.std_date, date_col = 'creationdate', period = 7).reset_index()
        return return_
    
