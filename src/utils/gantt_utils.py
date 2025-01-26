import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
from config.settings import (
    TITLE, X_LABEL, Y_LABEL, BAR_COLOR, FONT_FAMILY, FONT_SANS_SERIF,
    TITLE_SIZE, LABEL_SIZE, DAY_FONT_SIZE, MONTH_FONT_SIZE, MONTH_FONT_WEIGHT,
    Y_LABEL_FONT_SIZE
)

rcParams['font.family'] = FONT_FAMILY
rcParams['font.sans-serif'] = FONT_SANS_SERIF
rcParams['axes.titlesize'] = TITLE_SIZE
rcParams['axes.labelsize'] = LABEL_SIZE

def load_tasks(file_path):
    tasks = pd.read_csv(file_path, encoding='latin1', delimiter=';')
    tasks.columns = [
        'Área', 'ID da tarefa', 'Dependências', 'Grupo tarefas', 'Tarefa',
        'Tamanho', 'Dias úteis', 'Devs dedicados', 'Horas', 'Início', 'Fim'
    ]
    tasks['Início'] = pd.to_datetime(tasks['Início'], format='%d/%m/%Y')
    tasks['Fim'] = pd.to_datetime(tasks['Fim'], format='%d/%m/%Y')
    tasks = tasks.set_index(pd.DatetimeIndex(tasks['Início'].values))
    tasks.sort_index(inplace=True)
    return tasks

def group_tasks_by_group(tasks):
    grouped = tasks.groupby('Grupo tarefas').agg({
        'Início': 'min',
        'Fim': 'max'
    }).reset_index()
    return grouped

def plot_gantt(tasks, output_path=None):
    start_date = tasks['Início'].min()
    end_date = tasks['Fim'].max()
    timeline_length = (end_date - start_date).days

    #base_width = 5
    #width_per_week = 0.1
    #figure_width = base_width + ((timeline_length / 7) * width_per_week)
    #figure_height = max(7, len(tasks) * 0.5)
    #plt.figure(figsize=(figure_width, figure_height))
    plt.figure()

    y_positions = range(len(tasks))
    group_labels = tasks['Grupo tarefas'].tolist()

    tasks = tasks.sort_values(by='Início', ascending=True)

    for task in tasks.itertuples():
        plt.barh(
            task._1,
            (task.Fim - task.Início).days,
            left=task.Início,
            color=BAR_COLOR
        )

    ax = plt.gca()
    all_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    week_labels = []
    week_positions = []

    for date in all_dates:
        if date.weekday() == 0:
            week_labels.append(date.strftime('%d'))
            week_positions.append(date)

    ax.set_xticks(week_positions)
    ax.set_xticklabels(week_labels, fontsize=DAY_FONT_SIZE)
    ax.tick_params(axis='y', labelsize=Y_LABEL_FONT_SIZE)

    sec_ax = ax.secondary_xaxis('bottom')
    sec_ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))
    sec_ax.xaxis.set_major_locator(mdates.MonthLocator())
    sec_ax.spines['bottom'].set_position(('outward', 20))

    for label in sec_ax.get_xticklabels():
        label.set_fontsize(MONTH_FONT_SIZE)
        label.set_weight(MONTH_FONT_WEIGHT)

    ax.grid(axis='x', linestyle='--', alpha=0.6)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    sec_ax.spines['top'].set_visible(False)
    sec_ax.spines['right'].set_visible(False)

    plt.xlabel(X_LABEL, labelpad=10)
    #sec_ax.set_xlabel('Mês/Ano', labelpad=10)
    plt.ylabel(Y_LABEL, labelpad=10)
    plt.title(TITLE, pad=15)

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()