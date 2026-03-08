import os.path
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from constants import CONSTANTS


class PlotGen:
    def __init__(self, save_dir_root=None):
        if save_dir_root is not None:
            self.save_dir_root = save_dir_root
        else:
            self.save_dir_root = "./figs"
        if not os.path.exists(self.save_dir_root):
            os.makedirs(self.save_dir_root)
        self.colors = CONSTANTS.pyplot_color_palette

    @staticmethod
    def save_figure(path, fig):
        """

        Args:
            path: a str
            fig: a matplotlib figure

        Returns:
            None
        """
        print(f"[Saving] {path}")
        fig.savefig(path, dpi=600)

    @staticmethod
    def set_title_and_labels(title, x_label, y_label):
        """

        Args:
            title: a str
            x_label: a str
            y_label: a str

        Returns:
            None
        """
        plt.title(title)
        if x_label is not None:
            plt.xlabel(x_label)
        if y_label is not None:
            plt.ylabel(y_label)

    def draw_trend_line_and_get_rho(self, x, y, deg=1):
        """

        Args:
            x: a list of numbers
            y: a list of numbers
            deg: a positive int

        Returns:
            a float
        """
        z = np.polyfit(x, y, deg)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="black", linewidth=2)
        rho = np.corrcoef(x, y)[0, 1]
        return rho

    def draw_scatter_plot(self, x, y, title, x_label=None, y_label=None):
        """

        Args:
            x: a list of int
            y: a list of numbers (int or float)
            title: a str
            x_label: a str
            y_label: a str

        Returns:
            None
        """
        fig = plt.figure()
        x_bef, y_bef = x[:52], y[:52]
        x_aft, y_aft = x[52:], y[52:]
        plt.scatter(x_bef, y_bef, s=20, alpha=0.5, c="blue")
        self.draw_trend_line_and_get_rho(x_bef, y_bef, deg=1)
        plt.scatter(x_aft, y_aft, s=20, alpha=0.5, c="red")
        self.draw_trend_line_and_get_rho(x_aft, y_aft, deg=1)
        self.set_title_and_labels(title, x_label, y_label)
        self.save_figure(f"{self.save_dir_root}/{title}.png", fig)
        plt.close(fig)

    def draw_scatter_plot_with_trend_line(self, x, y, title, x_label=None,
                                          y_label=None):
        """

        Args:
            x: a list of int
            y: a list of numbers (int or float)
            title: a str
            x_label: a str
            y_label: a str

        Returns:
            a float (pearson correlation)
        """
        fig = plt.figure()
        plt.scatter(x, y, c="orange", s=5, alpha=0.2)
        rho = self.draw_trend_line_and_get_rho(x, y, deg=1)
        self.set_title_and_labels(title, x_label, y_label)
        plt.ylim([-1, 1])
        self.save_figure(f"{self.save_dir_root}/{title}.png", fig)
        plt.close(fig)
        return rho

    def draw_bar_plot(self, x, y, title, x_label=None, y_label=None):
        """

        Args:
            x: a list of int
            y: a list of numbers (int or float)
            title: a str
            x_label: a str
            y_label: a str

        Returns:
            None
        """
        fig = plt.figure()
        plt.bar(x, y, c=self.colors[0])
        self.set_title_and_labels(title, x_label, y_label)
        self.save_figure(f"{self.save_dir_root}/{title}.png", fig)
        plt.close(fig)

    def draw_stacked_bar_plot(self, x, y_dict, title, x_label=None,
                              y_label=None):
        """

        Args:
            x: a list of int
            y_dict: a dict where values are list of numbers, e.g.,
                    {
                        "python": [0.3, 0.4, 0.4, ...],
                        "java": [0.3, 0.3, 0.2, ...],
                    }
            title: a str
            x_label: a str
            y_label: a str

        Returns:
            None
        """
        fig, ax = plt.subplots()
        y_length = len(list(y_dict.values())[0])
        bottom = np.array([0.0]*y_length)
        for topic, count in y_dict.items():
            p = ax.bar(x, count, bottom=bottom, label=topic)
            bottom += count
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        self.set_title_and_labels(title, x_label, y_label)
        self.save_figure(f"{self.save_dir_root}/{title}.png", fig)

    def draw_scatter_plot_with_confidence_interval(self, x, y, title,
                                                   x_label=None, y_label=None):
        """

        Args:
            x: a list of int
            y: a list of numbers (int or float)
            title: a str
            x_label: a str
            y_label: a str

        Returns:
            None
        """
        fig = plt.figure()
        sns.regplot(x=x, y=y, scatter_kws={"alpha": 0.5,
                                           "color": self.colors[0]})
        self.set_title_and_labels(title, x_label, y_label)
        self.save_figure(f"{self.save_dir_root}/{title}.png", fig)
        plt.close(fig)

if __name__ == "__main__":
    from lib.utils.data_loader import DataLoader
    from lib.utils.statistics import *
    from lib.utils.datetime_handler import *
    from lib.utils.utils import *
    dir_root_bert = "../result/bert_based/run_id_0/data"
    dir_root_lda = "../result/lda/run_id_1/data"
    def get_top_and_bottom_topics(data_dir):
        monthly_count = get_monthly_topics_counts(data_dir, list(range(0, 50)))
        before_gpt_count = {topic: sum(monthly_count[topic][:12]) for topic in monthly_count}
        sorted_topics = [k for k, v in sorted(before_gpt_count.items(),
                                              key=lambda item: item[1],
                                              reverse=True)]
        return sorted_topics[:10], sorted_topics[-10:]

    def get_topic_distribution_in_date_range(date_range, data_dir, topics):
        file_list = get_related_files(date_range)
        list_ = []
        for i in file_list:
            file_path = f"{data_dir}/{i}.json"
            json_list = DataLoader.load_json(file_path)
            list_ += json_list
        list_ = get_sublist_of_desired_date_range(list_, date_range)
        if "bert" in data_dir:
            to_return = get_topics_counts_bert(list_, topics)
        else:
            to_return = get_topics_counts_lda(list_, topics)
        to_return = get_fractional_values_dict(to_return)
        return to_return

    def collect_topic_distribution(window, data_dir, topics):
        """

        Args:
            window: window size, which is a positive int

        Returns:
            a dict, where keys are datetime str and values are distributions
        """
        date_str_list = get_datetime_strings_before_and_after_gpt(window)
        to_return = []
        for i in range(len(date_str_list)-1):
            date_range = (date_str_list[i], date_str_list[i+1])
            topic_distribution = get_topic_distribution_in_date_range(
                date_range, data_dir, list(range(0, 50)))
            to_append = {topic: topic_distribution[topic] for topic in topics}
            to_return.append(to_append)
        return to_return

    plot_gen = PlotGen()
    bert_top_10, bert_bottom_10 = get_top_and_bottom_topics(dir_root_bert)
    lda_top_10, lda_bottom_10 = get_top_and_bottom_topics(dir_root_lda)
    bert_top_10_res = collect_topic_distribution(7, dir_root_bert, bert_top_10)
    bert_top_10_res = list(map(lambda x: sum(x.values()), bert_top_10_res))
    bert_bot_10_res = collect_topic_distribution(7, dir_root_bert,
                                                 bert_bottom_10)
    bert_bot_10_res = list(map(lambda x: sum(x.values()), bert_bot_10_res))
    lda_top_10_res = collect_topic_distribution(7, dir_root_lda, lda_top_10)
    lda_top_10_res = list(map(lambda x: sum(x.values()), lda_top_10_res))
    lda_bot_10_res = collect_topic_distribution(7, dir_root_lda,
                                                lda_bottom_10)
    lda_bot_10_res = list(map(lambda x: sum(x.values()), lda_bot_10_res))
    x = list(range(104))
    plot_gen.draw_scatter_plot(x, bert_top_10_res, title="bert_top_10")
    plot_gen.draw_scatter_plot(x, lda_top_10_res, title="lda_top_10")
    plot_gen.draw_scatter_plot(x, bert_bot_10_res, title="bert_bot_10")
    plot_gen.draw_scatter_plot(x, lda_bot_10_res, title="lda_bot_10")
