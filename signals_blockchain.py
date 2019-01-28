# import modules
import os
import requests
import telegram
import time
from datetime import datetime
from wallets_dict import wallets
from config import limit, transactions, contract, looptime, my_token, filename, api_key


def get_OPQ_prices():
    request_ETH = requests.get(
        'https://api.kucoin.com/v1/open/tick?symbol=OPQ-ETH')
    request_BTC = requests.get(
        'https://api.kucoin.com/v1/open/tick?symbol=OPQ-BTC')

    ETH_pair = request_ETH.json()
    BTC_pair = request_BTC.json()

    OPQinETH = ETH_pair.get("data").get("lastDealPrice")
    OPQinBTC = BTC_pair.get("data").get("lastDealPrice")

    request_ETHprice = requests.get("https://api.cryptonator.com/api/ticker/eth-usd")
    request_BTCprice = requests.get("https://api.cryptonator.com/api/ticker/btc-usd")

    ETH = request_ETHprice.json()
    BTC = request_BTCprice.json()
    ETH = ETH.get("ticker")
    BTC = BTC.get("ticker")

    ETH_price = float(ETH.get("price"))
    BTC_price = float(BTC.get("price"))

    OPQinDollar = round((OPQinETH * ETH_price + OPQinBTC * BTC_price) / 2, 3)

    return OPQinBTC, OPQinETH, OPQinDollar


# defining standard telegram message
def send(chat_id, token):
    #OPQinBTC, OPQinETH, OPQinUSD = get_OPQ_prices()
    #OPQinSat = OPQinBTC * 100000000
    time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    tx_link = "https://etherscan.io/tx/" + hash
    amount_project = amount + " " + project
    block_link = "https://etherscan.io/block/" + block
    from_link = "https://etherscan.io/address/" + tx_from
    to_link = "https://etherscan.io/address/" + tx_to

    bot = telegram.Bot(token)
    bot.send_message(chat_id,
                     parse_mode='MARKDOWN',
                     disable_web_page_preview=True,
                     text="*" + time + "*\n" + \
                          "-" * len(time) + "\n" + "[Transaction Hash](" + tx_link + ")\n\n" + \
                          "*" + amount_project + "* in Block [" + block + "](" + block_link + ")\n\n" + \
                          "_From_ : [" + walletname_from + "](" + from_link + ")\n" + \
                          "_To_ : [" + walletname_to + "](" + to_link + ")\n\n",)# + \
                          #"*Value transfered*\n" + \
                          #"----------------\n" + \
                          #"ETH: " + str(OPQinETH) + "\n" + \
                          #"Sats: " + str(round(OPQinSat)) + "\n" + \
                          #"USD: " + str(OPQinUSD), )


def update_chat_ids():
    try:
        with open("chat_IDs.txt") as f:
            chat_ids = f.read()
            chat_ids = chat_ids.split("\n")
    except:
        with open("chat_IDs.txt", "a+") as f:
            pass
        chat_ids = []
    return chat_ids


# input for requests
url = "http://api.etherscan.io/api?module=account&action=tokentx&contractaddress=" + contract + "&page=1&offset=" + str(
    transactions) + "&sort=desc&apikey=" + api_key
bot_update = "https://api.telegram.org/bot"+my_token+"/getUpdates"

# create txt file to add transactions to
try:
    with open("" + filename + ".txt") as f:
        read_data = f.read()
except:
    with open("" + filename + ".txt", "w+") as f:
        f.write("block;timestamp;hash;amount\n")
    print("New file created for verifying transactions\n")

# loop per looptime
while True:
    print("Loop")

    try:
        response = requests.get(url)
        address_content = response.json()
        result = address_content.get("result")

        bot_up = requests.get(bot_update)
        bot_content = bot_up.json()
        bot_results = bot_content.get("result")

        for n, update in enumerate(bot_results):
            chat_ids = update_chat_ids()
            # print(update.get("message"))
            buffer = update.get("message")
            chat = buffer.get("chat")
            chat = chat.get("id")
            if str(chat) not in chat_ids:
                with open("chat_IDs.txt", "a+") as f:
                    f.write(str(chat) + "\n")

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
        value_raw = int(GWEI_value) / 1000000000000000000
        value = round(value_raw)
        amount = value.__str__()
        project = transaction.get("tokenSymbol")
        timestamp = int(transaction.get("timeStamp"))

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
                    for chat_id in chat_ids:
                        if chat_id != "":
                            try:
                                send(chat_id, my_token)
                            except:
                                print("Error while printing to chat_id: {}\n".format(chat_id))
                                chat_ids.remove(chat_id)
                                with open("chat_IDs.txt","w") as fh:
                                    for x in chat_ids:
                                        fh.write(x+"\n")

                    f = open("" + filename + ".txt", "a+")
                    out = ";".join([str(block), str(timestamp), str(hash), str(amount)])
                    f.write(str(out) + "\n")
                except:
                    print("Telegram error. Waiting 3 seconds.")
                    print(str(datetime.now()))
                    time.sleep(3)
                # time.sleep(5)

    # time in seconds for every loop
    time.sleep(looptime)
