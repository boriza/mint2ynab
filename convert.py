import yaml 
import pandas as pd 
import numpy as np
import sys
import argparse
import os

transaction_file_name = 'mintapi-transactions.csv'
new_output_file_name = 'output-transactions.csv'
yaml_data_file = 'categories-conf.yml'

dir_path = os.path.dirname(os.path.realpath(__file__))
yaml_data_file_full_path = os.path.join(dir_path, yaml_data_file)

parser = argparse.ArgumentParser(description='Mint2Ynab')

# Parse argiments e.g., python categories.py mintapi-transactions.csv out.csv Mastercard

parser.add_argument('transaction_file_name', help='input file name')
parser.add_argument('output_file_name', help='output file name')
parser.add_argument('account_filter', nargs='?', const='', type=str)
args = parser.parse_args()

transaction_file_name = args.transaction_file_name
new_output_file_name = args.output_file_name
account_filter = args.account_filter

# Open yaml data file and store data in a variable
with open(yaml_data_file_full_path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)


def get_category(category):
    if type(category) == str:
        for key, value in data.items():
            if key.lower() == category.lower():
                return value
    else:
        # if parent category is blank, return empty string
        return ""

# read transaction file
df = pd.read_csv(transaction_file_name)

# Get parent category for eatch row or category column
df['Category Group/Category'] = df['category'].apply(get_category)
df['inflow'] = np.where(df['transaction_type']=='credit', df['amount'], df['amount'] * -1)
df = df.fillna('')

if account_filter:
    df = df.loc[df['account_name'] == account_filter]

df = df.rename(columns={'account_name': 'account', 'description': 'Payee'})
df = df.drop(columns=['original_description', 'labels', 'notes','category', 'transaction_type'])

print (df)
# save dataframe to new csv file
df.to_csv(new_output_file_name, index=False)

f.close()  # close yaml file
