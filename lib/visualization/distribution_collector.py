from lib.utils.datetime_handler import *
from lib.utils.statistics import (get_monthly_topics_counts, get_topics_counts,
                              get_tags_counts, get_fractional_values_dict)
from lib.utils.file_io import *
from lib.utils.sublist import get_sublist_of_desired_date_range
import numpy as np


def get_top_and_bottom_topics(data_dir):
    """

    Args:
        data_dir: a str

    Returns:
        a couple of
            index of top 10 topics,
            index of bottom 10 topics
    """
    monthly_count = get_monthly_topics_counts(data_dir, list(range(0, 50)))
    before_gpt_count = {topic: sum(monthly_count[topic][:12]) for topic in
                        monthly_count}
    sorted_topics = [k for k, v in sorted(before_gpt_count.items(),
                                          key=lambda item: item[1],
                                          reverse=True)]
    return sorted_topics[:10], sorted_topics[-10:]


def get_topic_distribution_in_date_range(date_range, data_dir, topics):
    """

    Args:
        date_range: a couple of datetime strings
        data_dir: a str
        topics: a list of int

    Returns:
        a topic distribution in given date range
    """
    file_list = get_related_files(date_range)
    list_ = []
    for i in file_list:
        file_path = f"{data_dir}/{i}.json"
        json_list = load_json(file_path)
        list_ += json_list
    list_ = get_sublist_of_desired_date_range(list_, date_range)
    to_return = get_topics_counts(list_, topics)
    to_return = get_fractional_values_dict(to_return)
    return to_return


def collect_topic_distributions(window, data_dir):
    """

    Args:
        window: a window size (unit: date)
        data_dir: a str

    Returns:
        a list of dict
    """
    all_topics = CONSTANTS.all_topics_list
    date_str_list = get_datetime_strings_before_and_after_gpt(window)
    to_return = []
    for i in range(len(date_str_list)-1):
        date_range = (date_str_list[i], date_str_list[i+1])
        topic_distribution = get_topic_distribution_in_date_range(
            date_range, data_dir, all_topics)
        to_return.append(topic_distribution)
    return to_return


def extract_specific_topics(dict_, topics):
    """

    Args:
        dict_: a topic distribution dict
        topics: a list of int

    Returns:
        a topic distribution dict (only containing desired topics)
    """
    to_return = {topic: dict_[topic] for topic in topics}
    return to_return


def get_tag_distribution_in_date_range(date_range, data_dir, tags):
    """

    Args:
        date_range: a couple of datetime strings
        data_dir: a str
        tags: a list of str

    Returns:
        a topic distribution in given date range
    """
    file_list = get_related_files(date_range)
    list_ = []
    for i in file_list:
        file_path = f"{data_dir}/{i}.json"
        json_list = load_json(file_path)
        list_ += json_list
    list_ = get_sublist_of_desired_date_range(list_, date_range)
    to_return = get_tags_counts(list_, tags)
    to_return = get_fractional_values_dict(to_return)
    return to_return


def collect_tag_distributions(window, data_dir):
    """

    Args:
        window: a window size (unit: date)
        data_dir: a str

    Returns:
        a list of dict
    """
    tag_info = load_json("./result/tag/tag_info.json")
    all_tags = list(tag_info.keys())
    date_str_list = get_datetime_strings_before_and_after_gpt(window)
    to_return = []
    for i in range(len(date_str_list)-1):
        date_range = (date_str_list[i], date_str_list[i+1])
        topic_distribution = get_tag_distribution_in_date_range(
            date_range, data_dir, all_tags)
        to_return.append(topic_distribution)
    return to_return

def collect_top_mid_bottom_tags(df, pct_cut = 0.2):
    """

    Args:
        df: calculated dataframe for tag distribution (columns: 'cdate', 'id', 'tag', 'cnt', 'tot_cnt', 'pct')
        
    Returns:
        a list of dict
    """
    df_bf_pro = (df[df['rel_week']<0].groupby(['tag']).sum(['pct'])['pct'].sort_values().reset_index())
    tagnum = int(np.floor(df_bf_pro.shape[0]*pct_cut))
    bot_tag = list(df_bf_pro.iloc[:tagnum, 0])
    top_tag = list(df_bf_pro.iloc[-tagnum:, 0])
    mid_tag = list(df_bf_pro.iloc[tagnum:-tagnum, 0])
    

    df_bot = df[df['tag'].isin(bot_tag)].groupby(['rel_week'])['pct'].sum().reset_index(name = 'weekly_pct')
    df_top = df[df['tag'].isin(top_tag)].groupby(['rel_week'])['pct'].sum().reset_index(name = 'weekly_pct')
    df_mid = df[df['tag'].isin(mid_tag)].groupby(['rel_week'])['pct'].sum().reset_index(name = 'weekly_pct')


    df_tot = df.groupby(['rel_week']).sum(['pct'])['pct'].reset_index(name = 'tot_pct')

    result = {}
    for label, df_sub in [('Top', df_top), ('Middle', df_mid), ('Bottom', df_bot)]:
        df_merged = pd.merge(df_tot, df_sub, on='rel_week', how='left').fillna(0)
        df_merged['pct_pct'] = df_merged['weekly_pct'] / df_merged['tot_pct']
        pct_label = int(pct_cut * 100)
        if label == 'Middle':
            key = f'Middle {100 - pct_label*2}% Tags'
        else:
            key = f'{label} {pct_label}% Tags'
        result[key] = df_merged[['rel_week', 'pct_pct']]

    return result

def collect_pareto_tags(df, pct_cut = 0.2):
    """

    Args:
        df: calculated dataframe for tag distribution (columns: 'cdate', 'id', 'tag', 'cnt', 'tot_cnt', 'pct')
        
    Returns:
        a list of dict
    """
    df_bf_pro = (df[df['rel_week']<0].groupby(['tag']).sum(['pct'])['pct'].sort_values().reset_index())
    tagnum = int(np.floor(df_bf_pro.shape[0]*pct_cut))
    
    top_tag = list(df_bf_pro.iloc[-tagnum:  , 0]) # top pct_cut% tag
    bot_tag = list(df_bf_pro.iloc[0:-tagnum , 0]) # rest of the topic
    

    df_bot = df[df['tag'].isin(bot_tag)].groupby(['rel_week'])['pct'].sum().reset_index(name = 'weekly_pct')
    df_top = df[df['tag'].isin(top_tag)].groupby(['rel_week'])['pct'].sum().reset_index(name = 'weekly_pct')


    df_tot = df.groupby(['rel_week']).sum(['pct'])['pct'].reset_index(name = 'tot_pct')

    result = {}
    for label, df_sub in [('Top', df_top), ('Bottom', df_bot)]:
        df_merged = pd.merge(df_tot, df_sub, on='rel_week', how='left').fillna(0)
        df_merged['pct_pct'] = df_merged['weekly_pct'] / df_merged['tot_pct']
        pct_label = int(pct_cut * 100)
        if label == 'Middle':
            key = f'Middle {100 - pct_label*2}% Tags'
        else:
            key = f'{label} {pct_label}% Tags'
        result[key] = df_merged[['rel_week', 'pct_pct']]

    return result

def proportion_calc_for_topic(df, period, topic):
       
    prop_df = pd.merge( df.groupby([period, topic]).count()['id'].reset_index().rename(columns={'id': 'cnt'}),
                        df.groupby([period]).count()['id'].reset_index().rename(columns={'id': 'tot_cnt'}), on = period)
    prop_df['proportion'] = prop_df['cnt']/prop_df['tot_cnt']

    return prop_df


def collect_top_bottom_topic(df, period, topic, proportion):
    topic_list = list(df[df[period] <0].groupby(topic).sum()[proportion].reset_index().sort_values(by = proportion, ascending=False)[topic])
    top10list = topic_list[:10]
    bot10list = topic_list[-10:]
    mid30list = np.setdiff1d(np.arange(0,50), top10list)
    mid30list = np.setdiff1d(mid30list, bot10list)

    return top10list, mid30list, bot10list


def sort_distribution_by_list(df, sort_list):
    order_map = {v: i for i, v in enumerate(sort_list)}
    
    return_df = df[df['Topic'].isin(sort_list)].copy() 
    
    return (
            return_df
            .assign(topic_order=return_df['Topic'].map(order_map))
            .sort_values(by=['rel_week', 'topic_order'])
            .drop(columns='topic_order')
        )