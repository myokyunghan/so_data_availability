from setting_for_sda.path_setting import path_list
class RunnerOptions:
    def __init__(self, model_in_run, language, year_range, run_id, snapshot): 
        self.model_in_run   = None
        self.bert_based_opt = None
        self.lda_opt        = None
        self.tag_opt        = None
        self.user_opt       = None

        self.chk_opt(model_in_run, language, year_range, run_id, snapshot)
        self.set_opt(model_in_run, language, year_range, run_id, snapshot)

    def chk_opt(self, model_in_run, language,  year_range, run_id, snapshot):
        # model_in_run chk
        if model_in_run not in ["bert_based", "lda", "tag"]:
            raise ValueError("'bert_based' and 'lda' are supported")
        
        # year_range chk
        if year_range not in (["2019to2021", "2020to2022", "2021to2023", "2022to2024", "2023to2025", "2021to2024", "2021to2025", "2020to2025"]):
            raise ValueError("We now offer only three options (2021to2023, 2022to2024, 2023to2025, 2021to2024, 2021to2025, 2020to2025) for 'year_range' parameter.\n If you want to add options, please modify 'settings_for_sda.constants.py'")
        
        # snapshot chk
        if snapshot not in (["snapshot1", "snapshot2", "snapshot3", "public_for_260105"]):
            raise ValueError("We now offer only three options (snapshot1, snapshot2, snapshot3) for 'snapshot' parameter.\n If you want to add options, please modify 'settings_for_sda.constants.py'")
        

    def set_opt(self, model_in_run,  language, year_range, run_id, snapshot):
        self.model_in_run    = model_in_run
        if self.model_in_run == "bert_based":
            self.user_opt = {
                                        "run_id": run_id,
                                        "model" : 'BERTopic',
                                        "year_range" : year_range,
                                        "data_dir": f"{path_list['data_root_dir']}/data/{snapshot}/questions/{language}/{year_range}",    
                                        "save_dir": f"{path_list['data_root_dir']}/result/bert_based/run_id_{run_id}",    
                                        "selected_tags": language,
                                        "snapshot": f"{snapshot}",
                                        "model_option": {
                                            "model_type": "text",
                                            "clustering": {
                                                "name": "kmeans",
                                                "n_clusters": 20,
                                            },
                                            "nr_topics": None,
                                            "vectorizer": "CountVectorizer",
                                            "embedding_model" : 'all-MiniLM-L6-v2'

                                        },
                                        "visualization": {
                                            "n": 10
                                        }
                                    }
        elif self.model_in_run == "lda":
            self.user_opt = {
                                "run_id": run_id,
                                "model" : 'LDA',
                                "year_range" : year_range,
                                "data_dir": f"{path_list['data_root_dir']}/data/{snapshot}/questions/{language}/{year_range}",    
                                "save_dir": f"{path_list['data_root_dir']}/result/lda/run_id_{run_id}",    
                                "selected_tags": language,
                                "snapshot": f"{snapshot}",
                                "model_option": {
                                    "n_components": 50,
                                    "max_df": 0.8,
                                    "min_df": 10,
                                    "attach_suffix": False
                                },
                                "visualization": {
                                    "html": True,
                                    "n": 10
                                }
                            }
        elif self.model_in_run == "tag":
            self.user_opt = {
                                "run_id": run_id,
                                "model" : 'tag',
                                "year_range" : year_range,
                                "data_dir": f"{path_list['data_root_dir']}/data/{snapshot}/questions/{language}/{year_range}",    
                                "save_dir": f"{path_list['data_root_dir']}/result/tag/run_id_{run_id}",    
                                "selected_tags": language,
                                "snapshot": f"{snapshot}"
                            }