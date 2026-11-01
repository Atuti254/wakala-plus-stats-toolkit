import unittest
from pathlib import Path
from stats_toolkit import (
    mean,
    median,
    mode,
    variance,
    std_dev,
    quartiles,
    iqr_outliers,
    load_column,
)


class TestLoading(unittest.TestCase):
    def test_invalid_and_missing_values_are_rejected(self):
        p = Path("data") / "agent_deposits.csv"
        valid, rejected = load_column(p, "daily_deposits_kes")
        self.assertGreater(len(valid), 0)
        self.assertGreater(len(rejected), 0)


class TestCentralTendency(unittest.TestCase):
    def test_empty_input_raises(self):
        with self.assertRaises(ValueError):
            mean([])
        with self.assertRaises(ValueError):
            median([])
        with self.assertRaises(ValueError):
            mode([])

    def test_mean_of_known_values(self):
        self.assertAlmostEqual(mean([10.0, 20.0, 30.0]), 20.0)

    def test_median_even_and_odd_lengths(self):
        self.assertEqual(median([10.0, 20.0, 30.0]), 20.0)
        self.assertEqual(median([10.0, 20.0, 30.0, 40.0]), 25.0)

    def test_mode_with_ties(self):
        self.assertEqual(mode([1.0, 2.0, 2.0, 3.0, 3.0]), [2.0, 3.0])
        self.assertEqual(mode([1.0, 2.0, 3.0]), [])


class TestSpread(unittest.TestCase):
    def test_sample_vs_population_variance(self):
        vals = [10.0, 20.0, 30.0]
        self.assertAlmostEqual(variance(vals, sample=True), 100.0)
        self.assertAlmostEqual(variance(vals, sample=False), 200.0 / 3.0)

    def test_std_dev_single_value(self):
        with self.assertRaises(ValueError):
            variance([10.0], sample=True)


class TestOutliers(unittest.TestCase):
    def test_detects_obvious_outlier(self):
        vals = [10, 12, 11, 13, 12, 11, 100]
        res = iqr_outliers(vals)
        self.assertIn(100, res["outliers"])

    def test_no_outliers_in_uniform_data(self):
        vals = [10.0, 11.0, 12.0, 13.0, 14.0]
        res = iqr_outliers(vals)
        self.assertEqual(res["outliers"], [])


if __name__ == "__main__":
    unittest.main()