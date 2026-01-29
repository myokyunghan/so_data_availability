import os
import pprint
from glob import glob
from topic_modeling.bert_based_models import load_bert_based_model_from_option
from topic_modeling.lda_model import load_lda_model_from_option
from topic_modeling.options import RunnerOptions
from setting_for_sda.constants import CONSTANTS
from utils.file_io import load_json, save_json
from utils.sublist import (get_sublist_of_desired_date_range,
                         get_sublist_of_desired_tags)



class ModelRunner:
    def __init__(self, runner_opt):
        self.runner_opt = runner_opt

        self.model_in_run = None
        self.model = None
        
        self.option = None

        self.data_dir = None
        self.data_dir_for_fit = None
        self.save_dir = None
        self.save_length = 10000
        self.load_option_and_topic_model()
        self.load_dirs_from_option()

    def __call__(self):
        self.run()

    def run(self):
        pprint.pp(self.option)
        self.run_model_and_save_data()
        self.save_option()

    def load_option_and_topic_model(self):
        """

        Returns:
            None
        """
        self.model_in_run = self.runner_opt.model_in_run
        if self.model_in_run == "bert_based":
            self.option = self.runner_opt.bert_based_opt
            self.model = load_bert_based_model_from_option(
                self.option["model_option"]
            )
        elif self.model_in_run == "lda":
            self.option = self.runner_opt.lda_opt
            self.model = load_lda_model_from_option(
                self.option["model_option"]
            )
        else:
            raise ValueError("'bert_based' and 'lda' are supported")

    def load_dirs_from_option(self):
        """

        Returns:
            None
        """
        run_id = self.option['run_id']
        self.data_dir = self.option['data_dir']
        self.save_dir = f"{self.option['save_dir']}/run_id_{run_id}"
        os.makedirs(f"{self.save_dir}/data", exist_ok=True)

    def load_all_files(self):
        """

        Returns:
            a list of dict
        """
        file_list = glob(f'{self.data_dir}/*.json')
        to_return = []
        for file in file_list:
            loaded = load_json(file)
            to_return += loaded
        return to_return
    

    def load_all_files_for_fit(self):
        """

        Returns:
            a list of dict
        """
        if self.data_dir_for_fit is not None : 
            file_list = glob(f'{self.data_dir_for_fit}/*.json')
            to_return = []
            for file in file_list:
                loaded = load_json(file)
                to_return += loaded
        else : 
            to_return = None    
        return to_return


    def run_model_and_save_data(self):
        """

        Returns:
            None
        """
        data = self.load_all_files()
        fit_data = self.load_all_files_for_fit()
        if self.option["selected_tags"] is not None:
            data = get_sublist_of_desired_tags(data,
                                               self.option["selected_tags"])
        result = self.model.run_model_and_get_output_list(data)
        topic_info = self.model.get_topic_info()
        save_json(topic_info, f"{self.save_dir}/topic_info.json")
        self.save_data(result)

    def save_data(self, list_):
        """

        Args:
            list_: a list of dict

        Returns:
            None
        """
        length = len(list_)
        iters = length // self.save_length
        for i in range(iters):
            start_idx = i * self.save_length
            end_idx = (i + 1) * self.save_length
            to_save = list_[start_idx:end_idx]
            save_json(to_save, f"{self.save_dir}/data/{i}.json")
        if length - iters * self.save_length > 0:
            start_idx = iters * self.save_length
            to_save = list_[start_idx:]
            save_json(to_save, f"{self.save_dir}/data/{iters}.json")

    def save_option(self):
        """

        Returns:
            None
        """
        save_json(self.option, f'{self.save_dir}/option.json')


## for test
if __name__ == '__main__':
    runner = ModelRunner()
    runner()
