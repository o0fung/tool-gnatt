# gantt-plotter
This project generates a Gantt chart from an Excel file.

1. Clone the repository:
   ```bash
   git clone https://github.com/anacds/gantt-plotter.git
   cd gantt-plotter

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate

3. Install the dependencies
   ```bash
   pip install -r requirements.txt

## Requirements
- Python 3.8+
- pandas
- matplotlib
- openpyxl
- mplcursors

## Usage
1. Prepare your Excel file (`data/project_tasks.xlsx`) with columns:
   - task_id, team, dependencies, task_group, task_description, start_date, end_date

2. Run the visualization:
```bash
python main.py
```

3. To save the chart, modify `output_path` in `main.py`

## Configuration
Modify `config/settings.py` to customize:
```python
# Chart appearance
TITLE = "Project Synergy Horizon"  # Chart title
BAR_COLOR = "#30C7DC"  # Default bar color
TEAM_BAR_COLORS = {  # Team-specific colors
    "Technology": "#56778f",
    "Business": "#91be6f",
    "Finance": "#ff6e61",
    "Marketing": "#f9c54e"
}

# Date formatting
DATE_FORMAT = '%Y-%m-%d'  # Excel date format

# Typography
TITLE_SIZE = 12            # Chart title size
FONT_FAMILY = "sans-serif" # Base font family
FONT_COLOR = "#6C6C6C"     # Text color
```

## Project Structure
```
.
├── README.md
├── config
│   ├── __init__.py
│   └── settings.py
├── data
│   └── project_tasks.xlsx
├── output
├── main.py
├── requirements.txt
└── src
    └── utils
        ├── __init__.py
        └── gantt_utils.py
```

## Key Functions
- `load_tasks()`: Loads and preprocesses Excel data
- `group_tasks_by_group()`: Organizes tasks by team and group
- `plot_gantt()`: Generates the interactive visualization
- `build_week_ticks()`: Creates dual-axis date markers