from setting_for_sda.constants import CONSTANTS
class RunnerOptions:
    def __init__(self, model_in_run, year_range, run_id, snapshot): 
        self.model_in_run   = None
        self.bert_based_opt = None
        self.lda_opt        = None

        self.chk_opt(model_in_run, year_range, run_id, snapshot)
        self.set_opt(model_in_run, year_range, run_id, snapshot)

    def chk_opt(self, model_in_run, year_range, run_id, snapshot):
        # model_in_run chk
        if model_in_run not in ["bert_based", "lda"]:
            raise ValueError("'bert_based' and 'lda' are supported")
        
        # year_range chk
        if year_range not in (["21to23", "22to24", "21to24"]):
            raise ValueError("We now offer only three options (21to23, 22to24, 21to24) for 'year_range' parameter.\n If you want to add options, please modify 'settings_for_sda.constants.py'")
        
        # snapshot chk
        if snapshot not in (["snapshot1", "snapshot2"]):
            raise ValueError("We now offer only two options (snapshot1, snapshot2 for 'snapshot' parameter.\n If you want to add options, please modify 'settings_for_sda.constants.py'")
        

    def set_opt(self, model_in_run, year_range, run_id, snapshot):
        self.model_in_run    = model_in_run
        self.bert_based_opt = {
                                    "run_id": run_id,
                                    "model" : 'BERTopic',
                                    "year_range" : year_range,
                                    "data_dir": f"{CONSTANTS.data_root_dir}/data/{snapshot}/questions/python/{year_range}",    
                                    "save_dir": f"{CONSTANTS.data_root_dir}/result/bert_based",    
                                    "selected_tags": None,
                                    "snapshot": 'f{snapshot}',
                                    "model_option": {
                                        "model_type": "text",
                                        "clustering": {
                                            "name": "kmeans",
                                            "n_clusters": 50,
                                        },
                                        "nr_topics": None,
                                        "vectorizer": "CountVectorizer",
                                        "embedding_model" : None

                                    },
                                    "visualization": {
                                        "n": 10
                                    }
                                }

        self.lda_opt = {
                            "run_id": run_id,
                            "model" : 'LDA',
                            "year_range" : year_range,
                            "data_dir": f"{CONSTANTS.data_root_dir}/data/{snapshot}/questions/python/{year_range}",    
                            "save_dir": f"{CONSTANTS.data_root_dir}/result/lda",    
                            "selected_tags": None,
                            "snapshot": 'f{snapshot}',
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