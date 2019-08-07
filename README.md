# Locust-Compare

Locust-Compare compares the result of a Locusio.io run with the previous result.

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
write_previous_results
compare_results_distribution
compare_results_requests
create_comparison_distribution
create_comparison_requests
```

### Basic usage CI/CD

First create a baseline by running your Locust script and saving the initial reports:

```bash
$ locust -f example_test.py --csv=example --host https://www.github.com --no-web -t 1m
```

Add a pre build step rename the previous results:

```bash
$ python3 locust_compare.py --prefix example --option write_previous_results
```

Run your actual Locust script:

```bash
$ locust -f example_test.py --csv=example --host https://www.github.com --no-web -t 1m
```

Add a post build step compare the results on a given column and specify the allowed factor of difference

```bash
$ python3 locust_compare.py --prefix example --option compare_results_distribution --columnname 95% --allowed 20
```

## Development

#### Bug Reports & Feature Requests

Please use the [issue tracker](https://github.com/tlolkema/locust-compare/issues) to report any bugs or feature requests.
