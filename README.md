# mint2ynab 
### mint.com to youneedabudget.com migration script including categories

mint export can be generated with https://github.com/mrooney/mintapi

## dependencies

install yaml module 
```
pip install pyyaml
```
install pandas
```
pip install pandas
```

install numpy 
```
pip install numpy
```



Usage
```
python categories.py mintapi-transactions.csv out.csv
```

Filter by account name
```
python categories.py mintapi-transactions.csv transactions.csv Mastercard
```
