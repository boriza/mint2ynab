# mint2ynab
mint.com to youneedabudget.com migration script including categories

Export mint.com
mint.com export can be generated with https://github.com/mrooney/mintapi

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

Usage filter account name
```
python categories.py mintapi-transactions.csv out.csv Mastercard
```
