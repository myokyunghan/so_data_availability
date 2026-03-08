from utils.datetime_handler import *
from utils.statistics import (get_monthly_topics_counts, get_topics_counts,
                              get_tags_counts, get_fractional_values_dict)
from utils.file_io import *
from utils.sublist import get_sublist_of_desired_date_range


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
