# Locust-Compare

Locust-Compare compares and validates the result of a Locusio.io run with the previous result.

## Features

- Written in uncomplicated python3
- Easy of installation and use
- Merge your Locust.io runs and generate a merged .csv
- Specify which column to compare and set your own tresholds
- Great for integration in your CI/CD pipelines (Jenkins, Travis)

## Installation

### Prerequisites

You just need python3 to get started

### Installation

```bash
$ python3 -m pip install -r requirements.txt
```

## Usage

### Commands:

Arguments to run Locust-Compare:
```
-p    Prefix for the Locust CSV files
-o    Select an option to run, view the documentation for the possible options
-c    Which column name to compare
-f    The allowed factor of difference
```

All possible options:
```
create_baseline
compare_results_distribution (also provide a columnname and factor)
compare_results_requests (also provide a columnname and factor)
create_comparison_distribution
create_comparison_requests
```

### Basic usage CI/CD

First we need atleast a Locust run to have some baseline results:

```bash
$ locust -f example_test.py --csv=example --host https://www.github.com --no-web -t 1m
```

Add a pre build step to create a baseline with Locust Compare based on the previous run:

```bash
$ python3 locust_compare.py --prefix example --option create_baseline
```

Run your actual Locust script:

```bash
$ locust -f example_test.py --csv=example --host https://www.github.com --no-web -t 1m
```

Add a post build step to compare the results on a given column and specify the allowed factor of difference

```bash
$ python3 locust_compare.py --prefix example --option compare_results_distribution --columnname 95% --factor 1.2
```

## Development

#### Bug Reports & Feature Requests

Please use the [issue tracker](https://github.com/tlolkema/locust-compare/issues) to report any bugs or feature requests.
