import yaml 
import pandas as pd 
import sys
import argparse
import os

transaction_file_name = 'mintapi-transactions.csv'
new_output_file_name = 'output-transactions.csv'
yaml_data_file = 'categories-conf.yml'

dir_path = os.path.dirname(os.path.realpath(__file__))
yaml_data_file_full_path = os.path.join(dir_path, yaml_data_file)


parser = argparse.ArgumentParser(description='Mint parent category')
parser.add_argument('transaction_file_name', help='input file name')
parser.add_argument('output_file_name', help='output file name')
parser.add_argument('account_filter', help='only process records with a matching filter')

args = parser.parse_args()
transaction_file_name = args.transaction_file_name
new_output_file_name = args.output_file_name

# Open yaml data file and store data in a variable
with open(yaml_data_file_full_path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)


def get_my_parent_category(category):
    """
    get parent category from chield
    :param: category:child category name
                type: <str> for category file, <float> for blank category
    : retrun: parent category name or blank
        type: str
    """
    if type(category) == str:
        for key, value in data.items():
            if key.lower() == category.lower():
                # if category have no parent
                if value == 'Root':
                    return key
                return value
    else:
        # if parent category is blank, return empty string
        return ""

# read transaction file
df = pd.read_csv(transaction_file_name)

# Get parent category for eatch row or category column
# and store to new column 'parent_category'
df['parent_category'] = df['category'].apply(get_my_parent_category)

# save dataframe to new csv file
df.to_csv(new_output_file_name, index=False)
f.close()  # close yaml file
