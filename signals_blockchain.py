# import modules
import requests
import telegram
import time
from datetime import datetime
from wallets_dict import wallets
from variables import msg, amount, project, walletname_from, walletname_to
from config import limit, transactions, contract, looptime, my_token, chat_id, filename, api_key

# defining standard telegram message
def send(msg, chat_id, token=my_token):
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id,
    parse_mode='HTML',
    text = "" + amount + " " + project + " in block " + block + "\nFrom " + walletname_from + " to " + walletname_to,)

# input for requests
url = "http://api.etherscan.io/api?module=account&action=tokentx&contractaddress=" + contract + "&page=1&offset=" + str(transactions) + "&sort=desc&apikey=" + api_key

# create txt file to add transactions to
try:
    with open("" + filename + ".txt") as f:
        read_data = f.read()
except:
    f = open("" + filename + ".txt", "w+")
    f.write("hash amount\n")
    print("New file created for verifying transactions\n")

# loop per looptime
while True:

    try:
        response = requests.get(url)
        address_content = response.json()
        result = address_content.get("result")
    except:
        print("Request error. Waiting 10 seconds.\n" + str(datetime.now()))
        time.sleep(10)
        continue

    # retrieve blockchain information
    for n, transaction in enumerate(result):
        hash = transaction.get("hash")
        tx_from = transaction.get("from")
        tx_to = transaction.get("to")
        GWEI_value = transaction.get("value")
        block = transaction.get("blockNumber")
        value_raw = int(GWEI_value)/1000000000000000000
        value = round(value_raw)
        amount = value.__str__()
        project = transaction.get("tokenSymbol")

        # comparing transaction to known wallets
        if tx_from in wallets:
            walletname_from = wallets[tx_from]
        else:
            walletname_from = "Unknown Wallet"

        if tx_to in wallets:
            walletname_to = wallets[tx_to]
        else:
            walletname_to = "Unknown Wallet"

        # check if transaction has already been added
        with open("" + filename + ".txt") as f:
            read_data = f.read()

        if hash not in read_data:

            if int(value_raw) > limit:
                print("Transaction ID: ", n)
                print("hash: ", hash)
                print("from: ", tx_from)
                print("to: ", tx_to)
                print("value: ", value)
                print("block: ", block)
                print(str(datetime.now()))
                print("\n")
                try:
                    send(msg, chat_id, token=my_token)
                    f = open("" + filename + ".txt", "a+")
                    f.write("" + hash + " " + amount + "\n")
                except:
                    print("Telegram error. Waiting 10 seconds.")
                    print(str(datetime.now()))
                    time.sleep(10)
                time.sleep(5)

    # time in seconds for every loop
    time.sleep(looptime)
