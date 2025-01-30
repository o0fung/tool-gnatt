import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import mplcursors
from matplotlib import rcParams

from config.settings import (
    TITLE, TITLE_SIZE, TITLE_FONT_WEIGHT,
    FONT_FAMILY, FONT_SANS_SERIF, FONT_COLOR,
    LABEL_SIZE, Y_LABEL_FONT_SIZE, DAY_FONT_SIZE, MONTH_FONT_SIZE, MONTH_FONT_WEIGHT,
    X_LABEL, Y_LABEL, 
    BAR_COLOR, TEAM_BAR_COLORS,
    DATE_FORMAT
)

# style confs
rcParams['font.family'] = FONT_FAMILY
rcParams['font.sans-serif'] = FONT_SANS_SERIF
rcParams['axes.titlesize'] = TITLE_SIZE
rcParams['axes.labelsize'] = LABEL_SIZE

def load_tasks(file_path, sheet_name, header, nrows, skiprows):
    """
    This function loads data from an Excel spreadsheet into a Pandas dataframe.
    """
    try:
        tasks = pd.read_excel(file_path, sheet_name=sheet_name, header=header, 
                              nrows=nrows, skiprows=skiprows)
        tasks.columns = [
            'task_id', 'team', 'dependencies', 'task_group', 'task_description',
            'start_date', 'end_date'
        ]
        tasks['start_date'] = pd.to_datetime(tasks['start_date'], format=DATE_FORMAT)
        tasks['end_date'] = pd.to_datetime(tasks['end_date'], format=DATE_FORMAT)
        tasks.set_index(pd.DatetimeIndex(tasks['start_date'].values), inplace=True)
        return tasks
    except Exception as e:
        print(f"Error when trying to load tasks: {e}")

def group_tasks_by_group(tasks):
    grouped = tasks.groupby(by=['team', 'task_group']).agg({
        'start_date': 'min',
        'end_date': 'max'
    }).reset_index().sort_values(by=['start_date', 'task_group'], ascending=False)
    return grouped

def plot_gantt(tasks, output_path):
    """
    """
    if tasks.empty:
        print("No tasks to plot.")
        return
    
    tasks.sort_values(by=['start_date', 'task_group'], ascending=False, inplace=True)
    start_date = tasks['start_date'].min()
    end_date = tasks['end_date'].max()

    bars = []
    for task in tasks.itertuples():
        bar = plt.barh(
                task.task_group,
                (task.end_date - task.start_date).days,
                left=task.start_date,
                color=TEAM_BAR_COLORS.get(task.team, "#000000")
        )
        
        for rect in bar:
            rect.annotation = (
                f"{start_date.strftime('%d/%b/%y')} - {end_date.strftime('%d/%b/%y')}\n"
                f"Duration: {(task.end_date - task.start_date).days}\n"
                f"Task group: {task.task_group}\n"
                f"Team: {task.team}"
            )
            bars.append(rect)

    all_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    week_labels = []
    week_positions = []

    for date in all_dates:
        if date.weekday() == 0:
            week_labels.append(date.strftime('%d'))
            week_positions.append(date)

    ax = plt.gca()
    ax.set_title(TITLE, fontsize=TITLE_SIZE, color=FONT_COLOR).set_fontweight(TITLE_FONT_WEIGHT)
    ax.set_xlabel(X_LABEL, fontsize=LABEL_SIZE, color=FONT_COLOR)
    ax.set_ylabel(Y_LABEL, fontsize=LABEL_SIZE, color=FONT_COLOR)
    ax.tick_params(axis='x', colors=FONT_COLOR)
    ax.tick_params(axis='y', colors=FONT_COLOR)
    ax.set_xticks(week_positions)
    ax.set_xticklabels(week_labels, fontsize=DAY_FONT_SIZE, color=FONT_COLOR)
    ax.set_yticklabels("", fontsize=Y_LABEL_FONT_SIZE, color=FONT_COLOR)

    sec_ax = ax.secondary_xaxis('bottom')
    sec_ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))
    sec_ax.xaxis.set_major_locator(mdates.MonthLocator())
    sec_ax.spines['bottom'].set_position(('outward', 20))

    for label in sec_ax.get_xticklabels():
        label.set_fontsize(MONTH_FONT_SIZE)
        label.set_weight(MONTH_FONT_WEIGHT)
        label.set_color(FONT_COLOR)

    ax.grid(axis='x', linestyle='--', alpha=0.6)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    sec_ax.spines['top'].set_visible(False)
    sec_ax.spines['right'].set_visible(False)

    cursor = mplcursors.cursor(bars, hover=True)
    @cursor.connect("add")
    def on_add(sel):
        task_annotation = sel.artist.annotation
        sel.annotation.set_text(task_annotation)
        sel.annotation.get_bbox_patch().set_facecolor("white")
        sel.annotation.get_bbox_patch().set_alpha(0.8)
        sel.annotation.set_fontsize(10)
    
    legend_patches = []
    for team, color in TEAM_BAR_COLORS.items():
        patch = mpatches.Patch(color=color, label=team)
        legend_patches.append(patch)

    ax.legend(
        handles=legend_patches,
        loc='best'
    )

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()