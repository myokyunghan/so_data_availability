from lib.utils.datetime_handler import calc_rel_period
from lib.visualization.distribution_collector import (proportion_calc_for_topic, 
                                                      collect_top_bottom_topic,
                                                      collect_top_bottom_tags)
from lib.utils.file_io import load_df, load_json, save_json

from setting_for_sda.path_setting import path_list
from setting_for_sda.date_setting import Date_Setting

def save_list_for_topic(data_dir, option_dict, std_date): 
    tmp = load_df(data_dir, ['id' , 'creationdate' , 'title', 'tags', 'body', 'Topic'])
    tmp = calc_rel_period(tmp, std_date, date_col = 'creationdate', period = 7).reset_index()

    prop_df = proportion_calc_for_topic(tmp, 'rel_week', 'Topic')

    top10list, _ , bot10list = collect_top_bottom_topic(prop_df, 'rel_week', 'Topic', 'proportion')

    option_dict['topic_list'] = {'Top 20% Topics' : top10list, 
                'Bottom 20% Topics' : bot10list,}
    print(option_dict)
    save_json(option_dict, f'{path_list["data_root_dir"]}/result/{model_in_run}/run_id_{idx}/topic_list.json')

def save_list_for_tag(data_dir, option_dict, std_date): 
    tmp = load_df(data_dir, ['cdate' , 'id' , 'tag', 'cnt', 'tot_cnt', 'pct'])
    tmp = calc_rel_period(tmp, std_date, date_col = 'cdate', period = 7).reset_index()

    top_tag, bot_tag = collect_top_bottom_tags(tmp, 0.2)

    option_dict['tag_list'] = {'Top 20% Tags' : top_tag, 
                                'Bottom 20% tags' : bot_tag,}
    print(option_dict)
    save_json(option_dict, f'{path_list["data_root_dir"]}/result/{model_in_run}/run_id_{idx}/tag_list.json')   
    print(f'[saved] File saved in {path_list["data_root_dir"]}/result/{model_in_run}/run_id_{idx}/tag_list.json')



def save_list(idx, model_in_run): 

    data_dir = f'{path_list["data_root_dir"]}/result/{model_in_run}/run_id_{idx}/data'
    option_dict = load_json(f'{path_list["data_root_dir"]}/result/{model_in_run}/run_id_{idx}/option.json')
    std_date = Date_Setting[option_dict['year_range']]['std_date']

    if model_in_run == "tag":
        save_list_for_tag(data_dir, option_dict, std_date)
    else :
        save_list_for_tag(data_dir, option_dict, std_date)


    

    

     
if __name__ == "__main__":
    idx = 100
    model_in_run = "tag"
    save_list(idx, model_in_run)
     