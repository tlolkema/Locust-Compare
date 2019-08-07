"""
LocustCompare

This script is used to compare the results of the previous Locust run with the current one.
This can be used in a Jenkins pipeline to determine if you want to pass/fail the build step based on the differences.

The dependencies are python3, pandas.

Sample usage:
  $ locust -f example_test.py --csv=example --host https://www.github.com --no-web -t 1m
  $ python3 locust_compare.py --prefix example --option write_previous_results
  $ locust -f example_test.py --csv=example --host https://www.github.com --no-web -t 1m
  $ python3 locust_compare.py --prefix example --option compare_results_distribution --columnname 95% --allowed 20

"""


import pandas as pd
import argparse
import os
import sys


class LocustCompare:

    def __init__(self, prefix):
        self._prefix = prefix

    def write_previous_results(self):
        os.rename(f'{self._prefix}_distribution.csv', f'{self._prefix}_distribution_previous.csv')
        os.rename(f'{self._prefix}_requests.csv', f'{self._prefix}_requests_previous.csv')

    def compare_results_distribution(self, columnname, factor):
        column = columnname
        fac = float(factor)
        df = self.return_comparison_distribution()
        df_columns = df[['Name',f'{columnname}_new',f'{columnname}_old']]
        f = df_columns[f'{columnname}_new'] / df_columns[f'{columnname}_old']
        if (f > fac).any():
            sys.exit(
                f'One of the requests is above the given treshold factor\n'
                f'Columns: {df_columns}\n'
                f'Given Factor: {fac}\n'
                f'Factors: {f}\n'
            )
        elif (f > fac).all():
            print(
                f'Success!\n'
                f'Columns: {df_columns}\n'
                f'Given Factor: {fac}\n'
                f'Factors: {f}\n'
            )
        else:
            sys.exit(
                f'An error occured\n'
            )

    def compare_results_requests(self, columnname, factor):
        column = columnname
        fac = float(factor)
        df = self.return_comparison_requests()
        df_columns = df[['Name',f'{columnname}_new',f'{columnname}_old']]
        f = df_columns[f'{columnname}_new'] / df_columns[f'{columnname}_old']
        if (f > fac).any():
            sys.exit(
                f'One of the requests is above the given treshold factor\n'
                f'Columns: {df_columns}\n'
                f'Given Factor: {fac}\n'
                f'Factors: {f}\n'
            )
        elif (f > fac).all():
            print(
                f'Success!\n'
                f'Columns: {df_columns}\n'
                f'Given Factor: {fac}\n'
                f'Factors: {f}\n'
            )
        else:
            sys.exit(
                f'An error occured\n'
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

    if args.option == 'write_previous_results':
        compare.write_previous_results()
    elif args.option == 'compare_results_distribution':
        compare.compare_results_distribution(args.columnname,args.factor)
    elif args.option == 'compare_results_requests':
        compare.compare_results_requests(args.columnname,args.factor)
    elif args.option == 'create_comparison_distribution':
        compare.create_comparison_distribution()
    elif args.option == 'create_comparison_requests':
        compare.create_comparison_requests()
    else:
        print(
            f'Invalid Option: {args.option}\n'
            'View the documentation for valid options'
        )
