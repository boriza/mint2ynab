import yaml 
import pandas as pd 
import numpy as np
import sys
import argparse
import os

transaction_file_name = 'mintapi-transactions.csv'
new_output_file_name = 'transactions.csv'
categories_map_file_path = 'categories-map-conf.yml'
categories_ynab_map_file_path = '/Users/boriza/Documents/dev/projects_workspaces/projects/mint/mint2ynab/categories-ynab.json'

dir_path = os.path.dirname(os.path.realpath(__file__))
categories_map_full_path = os.path.join(dir_path, categories_map_file_path)

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
with open(categories_map_full_path) as f:
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
df['Category'] = df['category'].apply(get_category)
df['Inflow'] = np.where(df['transaction_type']=='credit', df['amount'], df['amount'] * -1)
df = df.fillna('')

if account_filter:
    df = df.loc[df['account_name'] == account_filter]

df = df.rename(columns={'account_name': 'AccountName', 'description': 'Payee', 'notes': 'Memo' ,'date': 'Date'})
df = df.drop(columns=['original_description', 'labels',  'transaction_type','category','amount'])

def get_category_id(category_name):
    return "2cd11394-803f-47a8-9cd8-6ea5457b2938"

df['Category_ID'] = df['Category'].apply(get_category_id)

# save dataframe to new csv file
df.to_csv(new_output_file_name, index=False)

print (df)

f.close()  # close yaml file
