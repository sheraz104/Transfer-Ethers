from web3 import Web3, HTTPProvider
from requests import get
import json
import struct

coinbase_address = '0xB06cEF6B14dd249f5a0977F645436cC4f4095325'
receiver_address = '0x22741e8eE26E83AaCBf098a31DE5af1b1231920e'
GETH_HOST = 'http://localhost:8545'

web3 = Web3(HTTPProvider(GETH_HOST))


def main():

    coinbase_balance = getBalance(coinbase_address)

    if isGreaterThanZero(coinbase_balance):
        print("Transfering balance of ", coinbase_balance, " Ether")
        gasPrice = getGasPrice()
        if isZero(gasPrice):
            print("Could not get gas price")
        else:
            print("Gas Price: ", gasPrice)
            amount_to_send = calculateBalanceToSend(coinbase_balance, gasPrice)
            gasPrice_bytes = gasPriceToBytes(gasPrice)

            txHash = makeTransaction(amount_to_send, gasPrice_bytes)
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


def gasPriceToBytes(gasPrice):
    return bytearray(struct.pack("f", gasPrice))


def makeTransaction(amount_to_send, gasPrice_bytes):
    return web3.eth.sendTransaction({'to': receiver_address, 'from': coinbase_address, 'value': amount_to_send, 'gas': 21000, 'gasPrice': web3.toHex(gasPrice_bytes)})


def isGreaterThanZero(amount):
    return amount > 0


def isZero(amount):
    return amount == 0


main()
