from src.utils.gantt_utils import load_tasks, group_tasks_by_group, plot_gantt
import argparse


def run(path, sheet, out=None):
    
    tasks = load_tasks(path, sheet)
    grouped_tasks = group_tasks_by_group(tasks)
    plot_gantt(grouped_tasks, output_path=None)
    

if __name__ == "__main__":
    # Setup Argument Parser
    parser = argparse.ArgumentParser(description='Generate Gnatt chart from Excel data file.')
    parser.add_argument('path', help='use this Excel file path.')
    parser.add_argument('-s', '--sheet', help='use this Excel sheet.')
    parser.add_argument('-o', '--out', help='output path of gnatt chart as figure.')
    args = vars(parser.parse_args())
    
    # Run Gnatt Task
    run(path=args['path'], sheet=args['sheet'], out=args['out'])
    