import os.path
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from setting_for_sda.color_setting import Color_Setting
from lib.utils.statistics import *
import lib.stats.chowtest as st
import lib.visualization.figure_setting as figure_setting
from setting_for_sda.path_setting import path_list
from setting_for_sda.date_setting import Date_Setting


class PlotGen:
    def __init__(self, save_dir_root=None):
        if save_dir_root is not None:
            self.save_dir_root = save_dir_root
        else:
            self.save_dir_root = "./fig"
        if not os.path.exists(self.save_dir_root):
            os.makedirs(self.save_dir_root)    

    def draw_line_plot(self, ax, x, y, label=None, color=None, opt=None):
        if color is None:
            color = figure_setting.PALETTE['neutral']
        if opt == 'overall':
            ax.plot(x, y,
            color=color, lw=0.9, ls='--',
            alpha=0.65, zorder=4, label=label)    
        else :
            ax.plot(x, y,
            color=color, lw=2.0,
            zorder=5, label=label)
    


    def fill_confidence_interval(self, ax, x, ci_low, ci_high, label=None, color = None):
        if color is None:
            color = figure_setting.PALETTE['primary']
        ax.fill_between(x,
                            ci_low,
                            ci_high,
                            color=color, alpha=0.25, lw=0, zorder=4, label=label)

    def draw_topic_stack(self, ax, title, proportion, order_list, c, alpha=0.9, panel_label = ''):
        
        x = sorted(list(proportion['rel_week'].unique()))
        bottom = np.zeros(len(x))
        
        for idx, topic in enumerate(order_list):
            t_p = proportion[proportion['Topic'] == topic].copy()

            count_full = np.zeros(len(x))
            for i, rw in enumerate(t_p['rel_week']):
                if rw in x:
                    rw_idx = x.index(rw)
                    count_full[rw_idx] = t_p.loc[t_p['rel_week'] == rw, 'proportion'].values[0]
            ax.bar(
                x,
                count_full,
                bottom=bottom,
                label=topic,
                color=c[idx],
                width=1.0,
                align='center',
                alpha=alpha,
                linewidth=0,         
            )
            
            bottom += count_full

        # draw chatgpt line
        self.draw_chatgpt_line(ax)
        
        # set panel label
        # self.set_panel_label(ax, panel_label)
        
        # set title
        self.set_title(ax, title)

        # set tick size
        # self.set_tick_size(ax)
        
        # set_spine_visible 
        self.set_spine_visible(ax, False)

        # # set_grid_visible
        # self.set_grid_visible(ax, True)

        # Y축 범위
        ax.set_ylim(0, bottom.max() * 1.05)

    def draw_tag_bar(self, ax, title, x, y, c, alpha=0.9, panel_label = '', set_ylim = True, p_value = None):
            
            # draw bar plot
            ax.bar(x, y, width=1.0, align='center', alpha=alpha, linewidth=0, color = c)
            
            # draw chatgpt line
            self.draw_chatgpt_line(ax)
            
            # set ylim
            if set_ylim : 
                self.set_ylim_range(ax, x, y)
            
            # set panel label
            # self.set_panel_label(ax, panel_label)
            
            # set title
            self.set_title_two_lines(ax, title_text = title, p_value= p_value)

            # # set tick size
            # self.set_tick_size(ax)

            self.set_xticks(ax, [-104, -52, 0, 52, 104, 152])
            
            # set_spine_visible 
            self.set_spine_visible(ax, False)

            # # set_grid_visible
            # self.set_grid_visible(ax, False)

    def draw_chatgpt_line(self, ax, linestype = '--', linewidth = 1.2, zorder=5):
        ax.axvline(x=0, color=Color_Setting.std_pallet['event'], linestyle=linestype, linewidth=linewidth, zorder = zorder)

    
    def set_ylim_range(self, ax, x, y, gap = 0.001, bin = 0.025):
        y_min = min(y)
        y_max = max(y)

        bot = np.floor((y_min - gap) * 100) / 100
        top = np.ceil((y_max + gap) * 100) / 100

        bot = max(0, bot)
        top = min(1, top)

        ax.set_ylim(bot-gap, top+gap)

        bot_tick = np.floor(bot * 10) / 10
        top_tick = np.ceil(top * 10) / 10
        bin = ((top_tick-bot_tick)/4*100)/100
        ax.set_yticks(np.arange(bot_tick, top_tick+0.000000001, bin))

    
    def set_panel_label(self, ax, panel_label):
        ax.text(-0.08, 1.08, panel_label,
                transform=ax.transAxes,
                fontsize=figure_setting.FONT['panel'], fontweight='bold',
                va='bottom', ha='left')
    
    def set_title(self, ax, title):
        ax.text(0.5, 1.08, f'{title}',
            transform=ax.transAxes,
            fontsize=figure_setting.FONT['title'], ha='center', va='bottom')
        
    def set_tick_size(self, ax):
        ax.tick_params(axis='both', labelsize=figure_setting.FONT['label'], width=0.8, length=3, pad=2)

    def set_spine_visible(self, ax, is_visible=True):
        ax.tick_params(width=0.6, length=2.5, pad=2) 

        for s in ['top', 'right']:
            ax.spines[s].set_visible(False)
        ax.spines['left'].set_linewidth(0.6)
        ax.spines['bottom'].set_linewidth(0.6)
        ax.spines['left'].set_position(('outward', 3))
        ax.spines['bottom'].set_position(('outward', 3))

        ax.grid(False)


    def set_xticks(self, ax, x_tick_list):
        # ── set x lim
        ax.set_xticks(x_tick_list)

    
    def set_grid_visible(self, ax, is_visible=True):
        ax.yaxis.grid(is_visible, linestyle=':', linewidth=0.5, color='gray', alpha=0.5, zorder=0)
        ax.set_axisbelow(is_visible)

    def set_legend(self, ax, is_visible=True):
        if is_visible:
            ax.legend(fontsize=figure_setting.FONT['legend'], frameon=False)


    def get_title(self, prefix=None, title_text=None, p_value=None):
        if p_value is not None:
            p_txt = '$p$ < 0.001' if p_value < 0.001 else ( 'n.s.' if p_value >= 0.05 else f'$p$ = {p_value:.3f}')
        else:
            p_txt = None

        full_title = ''
        if prefix:
            full_title += f'{prefix}.  '
        if title_text:
            full_title += title_text
        if p_txt:
            full_title += f'  ({p_txt})'

        return full_title
    

    def set_title_two_lines(self, ax, prefix=None, title_text=None, p_value=None, gap=0.04):
        if p_value is not None:
            p_txt = '($p$ < 0.001)' if p_value < 0.001 else ( '(n.s.)' if p_value >= 0.05 else f'($p$ < 0.05)')
        else:
            p_txt = None

        ax.text(0.0, 1.0 + gap + 0.08, title_text,
                transform=ax.transAxes,
                fontsize=figure_setting.FONT['title'],
                ha='left', va='bottom',
                color='#222', fontweight='normal')
        
        # 둘째 줄 (아래, 조금 작게)
        if p_txt:
            ax.text(0.0, 1.0 + gap, f'{p_txt}',
                    transform=ax.transAxes,
                    fontsize=figure_setting.FONT['title'] - 2,
                    ha='left', va='bottom',
                    color='#555', fontweight='normal')
            

    def draw_scatter_plot(self, ax, x, y):
            ax.scatter(x, y, s=1.5, color=figure_setting.PALETTE['neutral'],
            alpha=0.50, lw=0, zorder=2, clip_on=False)
