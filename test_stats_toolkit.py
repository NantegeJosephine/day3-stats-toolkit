"""Write unit tests
Fill in test_stats_toolkit.py with at least eight passing tests using unittest or pytest, 
covering empty input, even/odd lengths, ties in mode, sample vs population variance, 
outlier detection and rejected values. Use small hand-checkable inputs, not the dataset.

Unit tests for the toolkit. Run with:  python -m unittest -v   (or pytest).
"""
import json
import unittest
from pathlib import Path
from statistics import StatisticsError

_notebook = Path(__file__).with_name("analysis.ipynb")
_namespace = {"__name__": "analysis"}
with _notebook.open(encoding="utf-8") as _file:
    _notebook_data = json.load(_file)
for _cell in _notebook_data.get("cells", []):
    if _cell.get("cell_type") == "code":
        exec("".join(_cell.get("source", [])), _namespace)

# mean = _namespace["mean"]
# median = _namespace["median"]
# mode = _namespace["mode"]
# variance = _namespace["variance"]
# std_dev = _namespace["std_dev"]
# iqr_outliers = _namespace["iqr_outliers"]


# class TestCentralTendency(unittest.TestCase):
#     def test_mean_of_known_values(self):
#         self.assertEqual(mean([1, 2, 3, 4, 5]), 3)

#     def test_median_even_and_odd_lengths(self):
#         self.assertEqual(median([1, 3, 5]), 3)
#         self.assertEqual(median([1, 2, 3, 4]), 2.5)

#     def test_mode_with_ties(self):
#         self.assertEqual(set(mode([1, 1, 2, 2, 3])), {1, 2})

#     def test_empty_input_raises(self):
#         for statistic in (mean, median, mode, variance, std_dev):
#             with self.assertRaises((ValueError, StatisticsError)):
#                 statistic([])


# class TestSpread(unittest.TestCase):
#     def test_sample_vs_population_variance(self):
#         self.assertAlmostEqual(variance([1, 2, 3], sample=False), 2 / 3)
#         self.assertAlmostEqual(variance([1, 2, 3], sample=True), 1)

#     def test_std_dev_single_value(self):
#         self.assertEqual(std_dev([7]), 0)


# class TestOutliers(unittest.TestCase):
#     def test_no_outliers_in_uniform_data(self):
#         result = iqr_outliers([2, 2, 2, 2, 2])
#         self.assertEqual(result["Outliers"], [])

#     def test_detects_obvious_outlier(self):
#         result = iqr_outliers([1, 2, 2, 3, 4, 100])
#         self.assertEqual(result["Outliers"], [100])


# class TestLoading(unittest.TestCase):
#     def test_invalid_and_missing_values_are_rejected(self):
#         for values in ([1, None, 3], [1, "bad", 3]):
#             with self.assertRaises((TypeError, ValueError)):
#                 mean(values)


# if __name__ == "__main__":
#     unittest.main()
