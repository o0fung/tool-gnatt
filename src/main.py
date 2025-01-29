from utils.gantt_utils import load_tasks, group_tasks_by_group, plot_gantt

def main():
    file_path = 'data/project_tasks.xlsx'
    tasks = load_tasks(file_path)
    grouped_tasks = group_tasks_by_group(tasks)
    plot_gantt(grouped_tasks)

if __name__ == "__main__":
    main()