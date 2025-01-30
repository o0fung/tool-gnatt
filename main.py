from src.utils.gantt_utils import load_tasks, group_tasks_by_group, plot_gantt

def main():
    
    file_path = 'data/project_tasks.xlsx'
    sheet_name = 'data'
    header = 0
    nrows = 31
    skiprows = None 

    tasks = load_tasks(file_path, sheet_name, header, nrows, skiprows)
    grouped_tasks = group_tasks_by_group(tasks)
    plot_gantt(grouped_tasks, None)

if __name__ == "__main__":
    main()