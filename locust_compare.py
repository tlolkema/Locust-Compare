"""
Locust-Compare

This script is used to compare the results of the previous Locust run with the current one.
This can be used in a Jenkins pipeline to determine if you want to pass/fail the build step based on the differences.

A Locust run outputs 2 csv files:
prefix_distribution.csv
prefix_requests.csv

With Locust-Compare you can rename these files to a baseline.
When you have a baseline you can perform a new Locust run.
With Locust-Compare you can compare and validate these to the baseline.

The dependencies are python3, pandas.

Sample usage: create baseline
  $ python3 locust_compare.py --prefix example --option create_baseline

Sample usage: create merged results csv:
  $ locust -f example_test.py --csv=example --host https://www.github.com --no-web -t 1m
  $ python3 locust_compare.py --prefix example --option create_baseline
  $ locust -f example_test.py --csv=example --host https://www.github.com --no-web -t 1m
  $ python3 locust_compare.py --prefix example --option create_comparison_requests

Sample usage: CI/CI compare against previous run (make sure you have atleast 1 locust run)
  $ python3 locust_compare.py --prefix example --option create_baseline
  $ locust -f example_test.py --csv=example --host https://www.github.com --no-web -t 1m
  $ python3 locust_compare.py --prefix example --option compare_results_distribution --columnname 95% --factor 1.2

Sample usage: CI/CD compare against baseline (make sure you have your baseline created)
  $ locust -f example_test.py --csv=example --host https://www.github.com --no-web -t 1m
  $ python3 locust_compare.py --prefix example --option compare_results_distribution --columnname 95% --factor 1.2

"""


import pandas as pd
import argparse
import os
import sys


class LocustCompare:

    def __init__(self, prefix):
        self._prefix = prefix

    def create_baseline(self):
        if os.path.exists(f'{self._prefix}_distribution_previous.csv'):
            if os.path.exists(f'{self._prefix}_distribution.csv'):
                os.remove(f'{self._prefix}_distribution_previous.csv')
                os.remove(f'{self._prefix}_requests_previous.csv')
                print('Removed old baseline')
        if os.path.exists(f'{self._prefix}_distribution.csv'):
            os.rename(f'{self._prefix}_distribution.csv', f'{self._prefix}_distribution_previous.csv')
            os.rename(f'{self._prefix}_requests.csv', f'{self._prefix}_requests_previous.csv')
            print('Created new baseline')
        elif not os.path.exists(f'{self._prefix}_distribution_previous.csv'):
            sys.exit(
                f'An error occured\n'
                f'Make sure you first run a Locust test\n'
                f'Missing: {self._prefix}_distribution_previous.csv'
            )
        print('Baseline exists')

    def compare_results(self, columnname, factor, rtype):
        column = columnname
        fac = float(factor)
        if rtype == 'distribution': 
            df = self.return_comparison_distribution()
        elif rtype == 'requests':
            df = self.return_comparison_requests()
        df_columns = df[['Name',f'{columnname}_new',f'{columnname}_old']]
        f = df_columns[f'{columnname}_new'] / df_columns[f'{columnname}_old']
        self.validate_results(f, fac, df_columns)

    def validate_results(self, f, fac, df_columns):
        if (f > fac).any():
            raise AssertionError(
                f'One of the requests is above the given treshold factor\n'
                f'Columns: {df_columns}\n'
                f'Given Factor: {fac}\n'
                f'Factors:\n{f}\n'
            )
        elif (f < fac).all():
            print(
                f'Success!\n'
                f'Columns: {df_columns}\n'
                f'Given Factor: {fac}\n'
                f'Factors:\n{f}\n'
            )
        else:
            sys.exit(
                f'An error occured\n'
                f'Columns: {df_columns}\n'
                f'Given Factor: {fac}\n'
                f'Factors:\n{f}\n'
            )

    def return_comparison_distribution(self):
        new_df1 = pd.read_csv(f'{self._prefix}_distribution.csv')
        pre_df1 = pd.read_csv(f'{self._prefix}_distribution_previous.csv')
        merged = pd.merge(new_df1, pre_df1, on='Name', how='outer', suffixes=('_new', '_old'))
        return merged

    def return_comparison_requests(self):
        new_df2 = pd.read_csv(f'{self._prefix}_requests.csv')
        pre_df2 = pd.read_csv(f'{self._prefix}_requests_previous.csv')
        merged = pd.merge(new_df2, pre_df2, on='Name', how='outer', suffixes=('_new', '_old'))
        return merged

    def create_comparison_distribution(self):
        csv = self.return_comparison_distribution()
        csv.to_csv(f'{self._prefix}_comparison_distribution.csv')

    def create_comparison_requests(self):
        csv = self.return_comparison_requests()
        csv.to_csv(f'{self._prefix}_comparison_requests.csv')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Compare previous Locust run with the current one')

    parser.add_argument('-p', '--prefix',
                        required=True,
                        help='Prefix for the Locust CSV files')

    parser.add_argument('-o', '--option',
                        required=True,
                        help='Select an option to run, view the documentation for the possible options')

    parser.add_argument('-c', '--columnname',
                        required=False,
                        help='Which column name to compare')

    parser.add_argument('-f', '--factor',
                        required=False,
                        help='The allowed factor of difference')

    args = parser.parse_args()

    compare = LocustCompare(args.prefix)

    if args.option == 'create_baseline':
        compare.create_baseline()
    elif args.option == 'compare_results_distribution':
        compare.compare_results(args.columnname,args.factor,'distribution')
    elif args.option == 'compare_results_requests':
        compare.compare_results(args.columnname,args.factor,'requests')
    elif args.option == 'create_comparison_distribution':
        compare.create_comparison_distribution()
    elif args.option == 'create_comparison_requests':
        compare.create_comparison_requests()
    else:
        print(
            f'Invalid Option: {args.option}\n'
            'View the documentation for valid options'
        )
