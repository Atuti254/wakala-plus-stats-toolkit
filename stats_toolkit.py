"""
Day 3 - Statistical Analysis Toolkit
Squad Python Specialization - Data Science, AI & Analytics

RULE: implement every calculation yourself with plain Python.
NumPy may be imported ONLY in compare_with_numpy(), to verify your results.
Do not use the statistics module.
"""
import csv
import math
from pathlib import Path

DATA_PATH = Path("data") / "agent_deposits.csv"


def load_column(path: Path, column: str) -> tuple[list[float], list[dict]]:
    """
    Reads CSV and validates column entries.
    Returns (valid_values, rejected_details)
    where rejected_details contains dicts with row, value, and reason.
    """
    valid_values = []
    rejected = []

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_idx, row in enumerate(reader, start=2):  # Row 1 is header
            raw_val = row.get(column, "").strip()

            if not raw_val or raw_val.lower() in ("nan", "null", "none", "n/a", "-"):
                rejected.append({"row": row_idx, "value": raw_val, "reason": "missing value"})
                continue

            try:
                val = float(raw_val)
                if math.isnan(val) or math.isinf(val):
                    rejected.append({"row": row_idx, "value": raw_val, "reason": "non-finite float"})
                elif val < 0:
                    rejected.append({"row": row_idx, "value": raw_val, "reason": "negative deposit"})
                else:
                    valid_values.append(val)
            except ValueError:
                rejected.append({"row": row_idx, "value": raw_val, "reason": "invalid numeric format"})

    return valid_values, rejected


def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("Cannot calculate mean of empty list.")
    return sum(values) / len(values)


def median(values: list[float]) -> float:
    if not values:
        raise ValueError("Cannot calculate median of empty list.")
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 1:
        return float(sorted_vals[mid])
    return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2.0


def mode(values: list[float]) -> list[float]:
    if not values:
        raise ValueError("Cannot calculate mode of empty list.")
    
    counts = {}
    for val in values:
        counts[val] = counts.get(val, 0) + 1
    
    max_freq = max(counts.values())
    
    if max_freq == 1 or len(set(counts.values())) == 1:
        return []
    
    modes = [val for val, count in counts.items() if count == max_freq]
    return sorted(modes)


def variance(values: list[float], sample: bool = True) -> float:
    if not values:
        raise ValueError("Cannot calculate variance of empty list.")
    if sample and len(values) < 2:
        raise ValueError("Sample variance requires at least 2 data points.")
    
    m = mean(values)
    sq_diff_sum = sum((x - m) ** 2 for x in values)
    divisor = (len(values) - 1) if sample else len(values)
    return sq_diff_sum / divisor


def std_dev(values: list[float], sample: bool = True) -> float:
    return math.sqrt(variance(values, sample=sample))


def _percentile(sorted_vals: list[float], p: float) -> float:
    """Calculates percentile using linear interpolation matching numpy.percentile default."""
    n = len(sorted_vals)
    if n == 1:
        return float(sorted_vals[0])
    idx = p * (n - 1)
    lower = int(math.floor(idx))
    upper = int(math.ceil(idx))
    weight = idx - lower
    return sorted_vals[lower] * (1 - weight) + sorted_vals[upper] * weight


def quartiles(values: list[float]) -> tuple[float, float, float]:
    """Return (Q1, Q2, Q3) using linear interpolation matching numpy.percentile."""
    if not values:
        raise ValueError("Cannot calculate quartiles of empty list.")
    s_vals = sorted(values)
    q1 = _percentile(s_vals, 0.25)
    q2 = _percentile(s_vals, 0.50)
    q3 = _percentile(s_vals, 0.75)
    return q1, q2, q3


def iqr_outliers(values: list[float], k: float = 1.5) -> dict:
    """Return the IQR, lower/upper fences, and outlying values."""
    if not values:
        raise ValueError("Cannot find outliers in empty list.")
    q1, q2, q3 = quartiles(values)
    iqr = q3 - q1
    lower_fence = q1 - k * iqr
    upper_fence = q3 + k * iqr
    outliers = [x for x in values if x < lower_fence or x > upper_fence]
    return {
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "lower_fence": lower_fence,
        "upper_fence": upper_fence,
        "outliers": outliers,
    }


class StatisticsAnalyzer:
    """Wraps one numeric column and exposes every statistic above as a method."""

    def __init__(self, values: list[float], name: str = "daily_deposits_kes", rejected: list = None) -> None:
        if not values:
            raise ValueError("StatisticsAnalyzer requires non-empty values.")
        self.raw_values = values
        self.sorted_values = sorted(values)  # Sort once during initialization
        self.name = name
        self.rejected = rejected or []

    @classmethod
    def from_csv(cls, path: Path, column: str) -> "StatisticsAnalyzer":
        valid_vals, rejected = load_column(path, column)
        return cls(valid_vals, name=column, rejected=rejected)

    def summary(self, sample: bool = True) -> dict:
        q1, q2, q3 = quartiles(self.sorted_values)
        outlier_info = iqr_outliers(self.sorted_values)
        
        return {
            "count": len(self.sorted_values),
            "mean": mean(self.sorted_values),
            "median": median(self.sorted_values),
            "mode": mode(self.sorted_values),
            "variance": variance(self.sorted_values, sample=sample),
            "std_dev": std_dev(self.sorted_values, sample=sample),
            "min": self.sorted_values[0],
            "max": self.sorted_values[-1],
            "q1": q1,
            "q3": q3,
            "iqr": outlier_info["iqr"],
            "lower_fence": outlier_info["lower_fence"],
            "upper_fence": outlier_info["upper_fence"],
            "outliers": outlier_info["outliers"],
        }

    def without_outliers(self) -> "StatisticsAnalyzer":
        outlier_info = iqr_outliers(self.sorted_values)
        lf, uf = outlier_info["lower_fence"], outlier_info["upper_fence"]
        clean_vals = [x for x in self.sorted_values if lf <= x <= uf]
        return StatisticsAnalyzer(clean_vals, name=f"{self.name}_clean", rejected=self.rejected)

    def report(self) -> str:
        s1 = self.summary()
        clean_analyzer = self.without_outliers()
        s2 = clean_analyzer.summary()

        lines = [f"=== Statistics report: {self.name} ==="]
        lines.append(f"Rows read         : {len(self.sorted_values) + len(self.rejected)}")
        lines.append(f"Valid values      : {len(self.sorted_values)}")
        lines.append(f"Rejected values   : {len(self.rejected)}")
        for r in self.rejected:
            lines.append(f"  row {r['row']}: '{r['value']}' ({r['reason']})")
        lines.append("")

        fmt = "{:<20} {:<15} {:<15}"
        lines.append(fmt.format("", "all data", "outliers removed"))
        lines.append(fmt.format("count", s1['count'], s2['count']))
        lines.append(fmt.format("mean", f"{s1['mean']:.2f}", f"{s2['mean']:.2f}"))
        lines.append(fmt.format("median", f"{s1['median']:.2f}", f"{s2['median']:.2f}"))
        
        m1_str = ", ".join(map(str, s1['mode'])) if s1['mode'] else "none"
        m2_str = ", ".join(map(str, s2['mode'])) if s2['mode'] else "none"
        lines.append(fmt.format("mode", m1_str, m2_str))
        
        lines.append(fmt.format("variance (sample)", f"{s1['variance']:.2f}", f"{s2['variance']:.2f}"))
        lines.append(fmt.format("std dev (sample)", f"{s1['std_dev']:.2f}", f"{s2['std_dev']:.2f}"))
        lines.append(fmt.format("min / max", f"{s1['min']:.2f} / {s1['max']:.2f}", f"{s2['min']:.2f} / {s2['max']:.2f}"))
        lines.append(fmt.format("Q1 / Q3", f"{s1['q1']:.2f} / {s1['q3']:.2f}", f"{s2['q1']:.2f} / {s2['q3']:.2f}"))
        lines.append(fmt.format("IQR", f"{s1['iqr']:.2f}", f"{s2['iqr']:.2f}"))
        lines.append("")

        lines.append(f"Outlier fences      : lower {s1['lower_fence']:.2f}, upper {s1['upper_fence']:.2f}")
        outlier_str = ", ".join(f"{x:.2f}" for x in s1['outliers']) if s1['outliers'] else "none"
        lines.append(f"Outliers            : {outlier_str}")
        lines.append("")

        lines.append("Risk Team Note:")
        lines.append("Extremely high outliers likely indicate larger bulk deposits, business liquidity floats, or decimal entry errors.")
        lines.append("Extremely low outlier days may represent network downtimes, unrecorded offline transactions, or float exhaustion.")
        lines.append("Removing outliers stabilizes baseline expectations for routine agent monitoring.")

        return "\n".join(lines)


def compare_with_numpy(analyzer: StatisticsAnalyzer, tol: float = 1e-6) -> tuple[dict, str]:
    """Import numpy HERE to verify calculations."""
    import numpy as np

    vals = analyzer.sorted_values
    s = analyzer.summary()

    np_mean = np.mean(vals)
    np_median = np.median(vals)
    np_var = np.var(vals, ddof=1)
    np_std = np.std(vals, ddof=1)
    np_q1, np_q3 = np.percentile(vals, [25, 75])

    matches = {
        "mean": abs(s["mean"] - np_mean) < tol,
        "median": abs(s["median"] - np_median) < tol,
        "variance": abs(s["variance"] - np_var) < tol,
        "std_dev": abs(s["std_dev"] - np_std) < tol,
        "Q1_Q3": (abs(s["q1"] - np_q1) < tol) and (abs(s["q3"] - np_q3) < tol),
    }

    report_lines = ["=== NumPy verification ==="]
    report_lines.append(f"mean      {'MATCH' if matches['mean'] else 'MISMATCH'}")
    report_lines.append(f"median    {'MATCH' if matches['median'] else 'MISMATCH'}")
    report_lines.append(f"variance  {'MATCH' if matches['variance'] else 'MISMATCH'}  (ddof=1)")
    report_lines.append(f"std dev   {'MATCH' if matches['std_dev'] else 'MISMATCH'}  (ddof=1)")
    report_lines.append(f"Q1 / Q3   {'MATCH' if matches['Q1_Q3'] else 'MISMATCH'}  (method=linear)")

    return matches, "\n".join(report_lines)

# Quick snippet to analyze by town
import csv
from collections import defaultdict

town_data = defaultdict(list)
with open("data/agent_deposits.csv", mode="r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            val = float(row["daily_deposits_kes"])
            town_data[row["town"]].append(val)
        except (ValueError, TypeError):
            continue

for town, values in town_data.items():
    analyzer = StatisticsAnalyzer(values, name=f"Town_{town}")
    print(f"--- {town} Summary ---")
    print(f"Mean: {analyzer.summary()['mean']:.2f}")

if __name__ == "__main__":
    if DATA_PATH.exists():
        # Overall analysis
        analyzer = StatisticsAnalyzer.from_csv(DATA_PATH, "daily_deposits_kes")
        report_text = analyzer.report()
        _, numpy_text = compare_with_numpy(analyzer)

        full_output = report_text + "\n\n" + numpy_text
        print(full_output)

        out_dir = Path("output")
        out_dir.mkdir(exist_ok=True)
        (out_dir / "stats_report.txt").write_text(full_output, encoding="utf-8")

        # Analysis grouped by town
        import csv
        from collections import defaultdict

        town_data = defaultdict(list)
        with open(DATA_PATH, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    val = float(row["daily_deposits_kes"].replace(",", ""))
                    town_data[row["town"]].append(val)
                except (ValueError, TypeError, KeyError):
                    continue

        print("\n=== Town Breakdown ===")
        for town, values in town_data.items():
            town_analyzer = StatisticsAnalyzer(values, name=f"Town_{town}")
            s = town_analyzer.summary()
            print(f"{town:<12}: count={s['count']}, mean={s['mean']:.2f}, std_dev={s['std_dev']:.2f}")