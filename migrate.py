import yaml 
import pandas as pd 
import numpy as np
import sys
import argparse
import os
import logging
import requests

#conversion
transaction_file_name = 'mintapi-transactions.csv'
new_output_file_name = 'transactions.csv'
categories_map_file_path = 'categories-map-conf.yml'
categories_ynab_map_file_path = 'pathto/categories-ynab.json'

# YNAB API https://api.youneedabudget.com/v1#/
api_token = 'replace_me'
budget_id = 'replace_me'

dir_path = os.path.dirname(os.path.realpath(__file__))
categories_map_full_path = os.path.join(dir_path, categories_map_file_path)

parser = argparse.ArgumentParser(description='Mint2Ynab')

# Parse argiments e.g., python categories.py mintapi-transactions.csv out.csv Mastercard

parser.add_argument('account_id', help='input account id from ynab API')
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
f.close()  # close yaml file

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


# ------- json category ids

import json
import collections

categories_mint_ynab = {}

def get_ynab_categories(categories_ynab_map_file_path):
    
    cat = collections.defaultdict(lambda : '') 
    # read file
    with open(categories_ynab_map_file_path, 'r') as myfile:
        data=myfile.read()

    # parse file
    categories_dict = json.loads(data)

    for category_group in categories_dict['data']["category_groups"]:
        for category in category_group['categories']:
            cat[category['name']] = category['id']

    return cat

categories_mint_ynab = get_ynab_categories(categories_ynab_map_file_path)

def get_category_id(category_name):
    return categories_mint_ynab[category_name]

df['Category_ID'] = df['Category'].apply(get_category_id)

# save dataframe to new csv file
df.to_csv(new_output_file_name, index=False)

print (df)

# API logic



import uuid 

def amount_conversion(str1):

    try:
        num1 = float(str1)
    except ValueError:
        num1 = 0.0
    
    amount = int(1000 * num1)
    return amount

def create_json_transactions(df):
    transactions = []
    

    for index, row in df.iterrows(): 

        Category = row['Category']
        Category_ID = row['Category_ID']
        if not Category_ID :
            Category = None
            Category_ID = None

        transaction = {
            "account_id": args.account_id, 
            "date": row['Date'],
            "payee_name": row['Payee'], 
            "amount": amount_conversion(row['Inflow']), 
            "memo": row['Memo'], 
            "category": Category, 
            "category_id": Category_ID, 
            "cleared": "cleared",
            "import_id": uuid.uuid1().time_low,
            "payee_id": None,
            "approved": False,
            "flag_color": None
        }
        transactions.append(transaction)
    
    data = {
        "transactions": transactions
    }

    return data

def post_transactions(data):
    # send our data to API
    logging.info("Uploading transactions to YNAB...")
    url = ("https://api.youneedabudget.com/v1/budgets/" +
            "{}/transactions?access_token={}".format(
                budget_id,
                api_token))

    post_response = requests.post(url, json=data)
    print(post_response.text)

json = create_json_transactions(df)
print(json)
post_transactions(json)

