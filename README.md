# mint2ynab 
### mint.com to youneedabudget.com migration script including categories

This script is designed to migrate your mint.com data to ynab.com (you need a budget). At this point in time ynab UI does not allow you to migrate categories. This script uses ynab api and your developer bearer token to import your data into your ynab account. You would need to run it per each account

Pre-requisites
1) csv mint export generated with https://github.com/mrooney/mintapi
2) categories-map-cong.yml categories provided is a superset of what mint.com has. If you have used default categories then you will be ok, otherwise you would need to adjust
3) categories-ynab.json, which can be obtained via https://api.youneedabudget.com/v1#/Categories/getCategories

in migrate.py set
```
# YNAB API https://api.youneedabudget.com/v1#/
api_token = 'replace_me'
budget_id = 'replace_me'
```

## dependencies

install dependencies 
```
pip install pyyaml
pip install pandas
pip install numpy
pip install requests
pip install logging
```


Run 
```
  python convert.py [replace_this_with_ynapapi_account_id] path-to/mint-transactions.csv path-to/transactions.csv '[account_name in input mint csv]'
```
