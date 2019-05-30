from web3 import Web3, HTTPProvider
from requests import get
import json
import struct

# Set the address of your Geth Node
GETH_HOST = 'http://localhost:8545'

# web3 is initialized in main method
web3 = None

# set your receiving address where you want to receive your withdrawn Ethers from coinbase address.
receiver_address = '0xB06cEF6B14dd249f5a0977F645436cC4f4095325'


def main():

    global web3
    web3 = Web3(HTTPProvider(GETH_HOST))

    # set your coinbase address that you want to withdraw Ethers from.
    # For successful mining of transaction make sure this address is unlocked in your Geth Node.
    coinbase_address = web3.eth.coinbase
    coinbase_balance = getBalance(coinbase_address)

    if isGreaterThanZero(coinbase_balance):
        print("Transfering balance of ", web3.fromWei(
            coinbase_balance, 'ether'), " Ether")
        gasPrice = getGasPrice()
        if isZero(gasPrice):
            print("Could not get gas price")
        else:
            print("Gas Price: ", gasPrice)
            amount_to_send = calculateBalanceToSend(coinbase_balance, gasPrice)

            txHash = makeTransaction(
                amount_to_send, gasPrice, coinbase_address)
            print("Transaction has been successull. TxHash: ", txHash.hex())
    else:
        print("coinbase has zero balance")


def getBalance(address):
    balance_wei = web3.eth.getBalance(address)
    return balance_wei


def getGasPrice():
    response = get('https://ethgasstation.info/json/ethgasAPI.json')
    if response.status_code != 200:
        return 0
    data = response.json()
    return data['safeLow']


def calculateBalanceToSend(amount, gasPrice):
    return amount - (web3.toWei(gasPrice, 'gwei') * 21000)


def makeTransaction(amount_to_send, gasPrice, coinbase_address):
    return web3.eth.sendTransaction({'to': receiver_address, 'from': coinbase_address, 'value': amount_to_send, 'gas': 21000, 'gasPrice': web3.toWei(gasPrice, 'gwei')})


def isGreaterThanZero(amount):
    return amount > 0


def isZero(amount):
    return amount == 0


main()
