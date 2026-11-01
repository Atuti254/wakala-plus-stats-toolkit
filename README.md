# Wakala Plus - M-Pesa Agent Deposit Statistical Toolkit

Wakala Plus operates an M-Pesa agent network across Nairobi, Thika, Machakos, and Nakuru [cite: Overview Wakala Plus runs a network of M-Pesa agents around Nairobi, Thika, Machakos and Nakuru. Its risk team watches daily deposit totals per agent: unusually high or low days can mean fraud, a float shortage or a data-entry error.  They want a small, dependable statistics toolkit they understand line by line, not a black box. You must implement every calculation yourself in plain Python first; NumPy is permitted only afterwards, to verify that your numbers agree. The data comes from agents ty]. Daily deposit totals tell a crucial story. Spike too high, and you might be looking at fraud or a decimal error [cite: Overview Wakala Plus runs a network of M-Pesa agents around Nairobi, Thika, Machakos and Nakuru. Its risk team watches daily deposit totals per agent: unusually high or low days can mean fraud, a float shortage or a data-entry error.  They want a small, dependable statistics toolkit they understand line by line, not a black box. You must implement every calculation yourself in plain Python first; NumPy is permitted only afterwards, to verify that your numbers agree. The data comes from agents ty]. Drop too low, and an agent is likely facing network downtime or running dry on float [cite: Overview Wakala Plus runs a network of M-Pesa agents around Nairobi, Thika, Machakos and Nakuru. Its risk team watches daily deposit totals per agent: unusually high or low days can mean fraud, a float shortage or a data-entry error.  They want a small, dependable statistics toolkit they understand line by line, not a black box. You must implement every calculation yourself in plain Python first; NumPy is permitted only afterwards, to verify that your numbers agree. The data comes from agents ty]. 

This project provides a custom Python statistics toolkit built from scratch. It gives the risk team complete clarity on how every metric gets computed, without relying on hidden library magic [cite: Overview Wakala Plus runs a network of M-Pesa agents around Nairobi, Thika, Machakos and Nakuru. Its risk team watches daily deposit totals per agent: unusually high or low days can mean fraud, a float shortage or a data-entry error.  They want a small, dependable statistics toolkit they understand line by line, not a black box. You must implement every calculation yourself in plain Python first; NumPy is permitted only afterwards, to verify that your numbers agree. The data comes from agents ty].

## What the Toolkit Does

The core module, `stats_toolkit.py`, handles all raw data parsing and math calculations natively:

* Cleans messy source CSV records, stripping empty entries and malformed text formats.
* Calculates central metrics including mean, median, and mode.
* Computes dispersion measures for both sample and population variance along with standard deviation.
* Finds quartiles ($Q_1$, $Q_2$, $Q_3$) and Interquartile Range ($IQR$) using linear interpolation.
* Identifies extreme transaction outliers using standard $1.5 \times IQR$ fences.
* Runs verification checks against NumPy to guarantee mathematical precision [cite: Overview Wakala Plus runs a network of M-Pesa agents around Nairobi, Thika, Machakos and Nakuru. Its risk team watches daily deposit totals per agent: unusually high or low days can mean fraud, a float shortage or a data-entry error.  They want a small, dependable statistics toolkit they understand line by line, not a black box. You must implement every calculation yourself in plain Python first; NumPy is permitted only afterwards, to verify that your numbers agree. The data comes from agents ty].
* Groups deposit statistics by individual town for regional monitoring.

## Project Structure

Here is how your workspace is laid out:

```text
Day-3/
├── data/
│   └── agent_deposits.csv    # Raw daily deposit data from agents
├── output/
│   └── stats_report.txt      # Formatted summary report and NumPy checks
├── stats_toolkit.py          # Plain Python calculations and report generation
├── test_stats_toolkit.py     # Unittest suite for validation
└── README.md                 # Project guide