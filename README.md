# Signals - Blockchain

Application to track ERC-20 transactions across the ethereum blockchain through live telegram alerts.  

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

```
pip install requests
pip install python-telegram-bot
```
### Installing

Make sure to have the dictionary file in the same directory as the applications. Fill in the variables mentioned below with your own settings. 
You can find these in the config.py file. Additionally, create a bot on telegram via the BotFather. 

```
limit = 10000 // amount of units needed to create an alert
transactions = 500 // amount of transactions 
contract = '0xb8c77482e45f1f44de1745f52c74426c631bdd52' // contract of eth token (BNB as example)
looptime = 30 // amount of sleep in seconds after finished loop
my_token = 'yourtoken' // unique telegram bot token where message will be sent from
chat_id = 'yourchatid' // telegram id where message will be sent
filename = 'yourfilename' // name of the file to log transactions
```

## Running the application

Simply execute the application. On the first execution a text file is created to log transactions. 

 ```
 python signals_blockchain.py
 ```

## Built With

* [Python 3.7.0](https://docs.python.org/3/) 

## Authors

* **Hubert Kirch** - *Initial work* - [Hubertini](https://github.com/hubertini/)

## To do

* Update dictionary
* Expand on readme
* Learn to code better
