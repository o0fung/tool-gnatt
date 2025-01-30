import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.utils.gantt_utils import load_tasks, group_tasks_by_group, plot_gantt

class TestGanttUtils(unittest.TestCase):
    def setUp(self):
        """Set up test data."""
        self.sample_data = pd.DataFrame({
            'task_id': [1, 2, 3],
            'team': ['Team A', 'Team B', 'Team A'],
            'dependencies': [None, None, None],
            'task_group': ['Group 1', 'Group 2', 'Group 1'],
            'task_description': ['Task 1', 'Task 2', 'Task 3'],
            'start_date': ['2023-10-01', '2023-10-05', '2023-10-03'],
            'end_date': ['2023-10-04', '2023-10-07', '2023-10-06']
        })

    @patch('pandas.read_excel')
    def test_load_tasks(self, mock_read_excel):
        """Test the load_tasks function."""
        # Mock the return value of pd.read_excel
        mock_read_excel.return_value = self.sample_data

        # Call the function
        tasks = load_tasks('dummy_path.xlsx', header=0, nrows=None, skiprows=None)

        # Assertions
        self.assertIsInstance(tasks, pd.DataFrame)
        self.assertEqual(len(tasks), 3)
        self.assertIn('task_group', tasks.columns)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(tasks['start_date']))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(tasks['end_date']))

    def test_group_tasks_by_group(self):
        """Test the group_tasks_by_group function."""
        # Convert dates to datetime
        self.sample_data['start_date'] = pd.to_datetime(self.sample_data['start_date'])
        self.sample_data['end_date'] = pd.to_datetime(self.sample_data['end_date'])

        # Call the function
        grouped_tasks = group_tasks_by_group(self.sample_data)

        # Assertions
        self.assertIsInstance(grouped_tasks, pd.DataFrame)
        self.assertEqual(len(grouped_tasks), 2)  # 2 unique groups
        self.assertEqual(grouped_tasks.iloc[0]['task_group'], 'Group 1')
        self.assertEqual(grouped_tasks.iloc[1]['task_group'], 'Group 2')

    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.savefig')
    def test_plot_gantt(self, mock_savefig, mock_show):
        """Test the plot_gantt function."""
        # Convert dates to datetime
        self.sample_data['start_date'] = pd.to_datetime(self.sample_data['start_date'])
        self.sample_data['end_date'] = pd.to_datetime(self.sample_data['end_date'])

        # Call the function with output_path
        plot_gantt(self.sample_data, output_path='test_gantt.png')

        # Assertions
        mock_savefig.assert_called_once_with('test_gantt.png', dpi=300, bbox_inches='tight')

        # Call the function without output_path
        plot_gantt(self.sample_data, output_path=None)
        mock_show.assert_called_once()

if __name__ == '__main__':
    unittest.main()