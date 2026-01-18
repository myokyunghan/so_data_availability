from setting_for_sda.constants import CONSTANTS
class RunnerOptions:
    #############################input the options here#############################
    model_in_run    = "bert_based"
    year_range      = "22to24"
    run_id          = 5
    #############################input the options here#############################
    
    bert_based_opt = {
        "run_id": run_id,
        "year_range" : year_range,
        "data_dir": f"{CONSTANTS.data_root_dir}/data/snapshot2/questions/python/{year_range}",    
        "save_dir": f"{CONSTANTS.data_root_dir}/result/bert_based",    
        "selected_tags": None,
        "snapshot":"2",
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
    lda_opt = {
        "run_id": run_id,
        "year_range" : year_range,
        "data_dir": f"{CONSTANTS.data_root_dir}/data/snapshot2/questions/python/{year_range}",    
        "save_dir": f"{CONSTANTS.data_root_dir}/result/lda",    
        "selected_tags": None,
        "snapshot": "2",
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
