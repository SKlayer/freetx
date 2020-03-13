import logging
import requests
from decimal import Decimal

from freetx.network import currency_to_satoshi
from freetx.network.meta import Unspent
from freetx.network.transaction import Transaction,TxPart

DEFAULT_TIMEOUT = 30

BCH_TO_SAT_MULTIPLIER = 100000000


def set_service_timeout(seconds):
    global DEFAULT_TIMEOUT
    DEFAULT_TIMEOUT = seconds


class InsightAPI:
    MAIN_ENDPOINT = ''
    MAIN_ADDRESS_API = ''
    MAIN_BALANCE_API = ''
    MAIN_UNSPENT_API = ''
    MAIN_TX_PUSH_API = ''
    MAIN_TX_API = ''
    MAIN_TX_AMOUNT_API = ''
    TX_PUSH_PARAM = ''

    @classmethod
    def get_balance(cls, address):
        r = requests.get(cls.MAIN_BALANCE_API.format(
            address), timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        return r.json()

    @classmethod
    def get_transactions(cls, address):
        r = requests.get(cls.MAIN_ADDRESS_API.format(
            address), timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        return r.json()['transactions']

    @classmethod
    def get_tx_amount(cls, txid, txindex):
        r = requests.get(cls.MAIN_TX_AMOUNT_API.format(
            txid), timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        response = r.json(parse_float=Decimal)
        return (Decimal(response['vout'][txindex]['value']) * BCH_TO_SAT_MULTIPLIER).normalize()

    @classmethod
    def get_unspent(cls, address):
        r = requests.get(cls.MAIN_UNSPENT_API.format(
            address), timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        return [
            Unspent(currency_to_satoshi(tx['amount'], 'bch'),
                    tx['confirmations'],
                    tx['scriptPubKey'],
                    tx['txid'],
                    tx['vout'])
            for tx in r.json()
        ]

    @classmethod
    def broadcast_tx(cls, tx_hex):  # pragma: no cover
        r = requests.post(cls.MAIN_TX_PUSH_API, json={
                          cls.TX_PUSH_PARAM: tx_hex, 'network': 'mainnet', 'coin': 'BCH'}, timeout=DEFAULT_TIMEOUT)
        return True if r.status_code == 200 else False


class IFBlockAPI():
    """ fchapi.ifwallet.com API """
    MAIN_ENDPOINT = 'https://fchapi.ifwallet.com:8225/api/'
    MAIN_ADDRESS_API = MAIN_ENDPOINT + 'address/{}/'
    MAIN_UNSPENT_API = MAIN_ENDPOINT + 'address/utxo/list/'
    MAIN_TX_PUSH_API = MAIN_ENDPOINT + 'tool/tx/broadcast/'
    MAIN_TX_API = MAIN_ENDPOINT + 'tx/{}/'
    MAIN_TX_AMOUNT_API = MAIN_TX_API
    MAIN_RAW_API = MAIN_TX_API


    TX_PUSH_PARAM = 'rawtx'

    TEST_ENDPOINT = 'https://tfchapi.ifwallet.com:8222/'
    TEST_ADDRESS_API = TEST_ENDPOINT + 'address/{}/'
    TEST_UNSPENT_API = TEST_ENDPOINT + 'address/utxo/list/'
    TEST_TX_PUSH_API = TEST_ENDPOINT + 'tool/tx/broadcast/'
    TEST_TX_API = TEST_ENDPOINT + 'tx/{}/'
    TEST_TX_AMOUNT_API = TEST_TX_API
    TEST_RAW_API = MAIN_TX_API
    @classmethod
    def get_tx_script(cls, txid, address):
        r = requests.get(cls.MAIN_TX_API.format(txid),
                         timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        response = r.json(parse_float=Decimal)["data"]
        print(response)
        for tx in response["vout"]:
            if address in tx["addrs"]:
                return tx["script_hex"]

    @classmethod
    def get_balance(cls, address):
        r = requests.get(cls.MAIN_ADDRESS_API.format(address),
                         timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        data = r.json()
        balance = data["data"]['balance']
        return balance

    @classmethod
    def get_balance_testnet(cls, address):
        r = requests.get(cls.TEST_ADDRESS_API.format(address),
                         timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        data = r.json()
        balance = data["data"]['balance']
        return balance

    @classmethod
    def get_transactions(cls, address):
        r = requests.get(cls.MAIN_ADDRESS_API.format(address),
                         timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        return r.json()["data"]['tx_count']

    @classmethod
    def get_transactions_testnet(cls, address):
        r = requests.get(cls.TEST_ADDRESS_API.format(address),
                         timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        return r.json()["data"]['tx_count']

    @classmethod
    def get_transaction(cls, txid):
        r = requests.get(cls.MAIN_TX_API.format(txid),
                         timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        response = r.json(parse_float=Decimal)["data"]

        tx = Transaction(response['txid'],
                         (Decimal(response['in_value'])
                          ).normalize(),
                         (Decimal(response['out_value'])
                          ).normalize())

        for txin in response['vin']:
            part = TxPart(txin['addrs'],
                          txin['value'],
                          txin['script'])
            tx.add_input(part)

        for txout in response['vout']:
            addr = None
            if 'addrs' in txout and txout['addrs'] != [""]:
                addr = txout['addrs'][0]

            part = TxPart(addr,
                          (Decimal(txout['value'])
                           ).normalize(),
                          txout['script'])
            tx.add_output(part)

        return tx

    @classmethod
    def get_transaction_testnet(cls, txid):
        r = requests.get(cls.TEST_TX_API.format(txid),
                         timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        response = r.json(parse_float=Decimal)["data"]

        tx = Transaction(response['txid'],
                         (Decimal(response['in_value'])
                          ).normalize(),
                         (Decimal(response['out_value'])
                          ).normalize())

        for txin in response['vin']:
            part = TxPart(txin['addrs'],
                          txin['value'],
                          txin['script'])
            tx.add_input(part)

        for txout in response['vout']:
            addr = None
            if 'addrs' in txout and txout['addrs'] != [""]:
                addr = txout['addrs'][0]

            part = TxPart(addr,
                          (Decimal(txout['value'])).normalize(),
                          txout['script'])
            tx.add_output(part)

        return tx

    @classmethod
    def get_tx_amount(cls, txid, txindex):
        r = requests.get(cls.MAIN_TX_AMOUNT_API.format(
            txid), timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        response = r.json(parse_float=Decimal)["data"]
        return response['vout'][txindex]['value']

    @classmethod
    def get_tx_amount_testnet(cls, txid, txindex):
        r = requests.get(cls.MAIN_TX_AMOUNT_API.format(
            txid), timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        response = r.json(parse_float=Decimal)["data"]
        return response['vout'][txindex]['value']

    @classmethod
    def get_unspent(cls, address):
        req_args = {
            "addresses": address,
            "confirmations": -1
        }

        r = requests.get(cls.MAIN_UNSPENT_API,
                         timeout=DEFAULT_TIMEOUT,data=req_args)
        r.raise_for_status()  # pragma: no cover
        return [
            Unspent(tx['value'],
                    tx['confirmations'],
                    None,
                    tx['txid'],
                    tx['vout'])
            for tx in r.json()['data']

        ]

    @classmethod
    def get_unspent_testnet(cls, address):
        req_args = {
            "addresses": address,
            "confirmations": -1
        }
        r = requests.get(cls.TEST_UNSPENT_API,data=req_args,
                         timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        #cls.get_transaction("20293ed2b52726baeb9b2b5b60f5dd50f5b294c824d98a46b4068d5cdbedfc3f")


        return [
            Unspent(tx['value'],
                    tx['confirmations'],
                    None,
                    tx['txid'],
                    tx['vout'])
            for tx in r.json()['data']

        ]

    @classmethod
    def get_raw_transaction(cls, txid):
        r = requests.get(cls.MAIN_RAW_API.format(
            txid), timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        response = r.json(parse_float=Decimal)["data"]
        return response

    @classmethod
    def get_raw_transaction_testnet(cls, txid):
        r = requests.get(cls.TEST_RAW_API.format(
            txid), timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        response = r.json(parse_float=Decimal)["data"]
        return response

    @classmethod
    def broadcast_tx(cls, tx_hex):  # pragma: no cover
        r = requests.post(cls.MAIN_TX_PUSH_API, data={"raw_tx": tx_hex})
        #print(r.json(),tx_hex)
        return True if "OK" == r.json()["message"] else False

    @classmethod
    def broadcast_tx_testnet(cls, tx_hex):  # pragma: no cover

        r = requests.post(cls.TEST_TX_PUSH_API,data={"raw_tx": tx_hex})
        return True if "OK" == r.json()["message"] else False


class NetworkAPI:
    IGNORED_ERRORS = (ConnectionError,
                      requests.exceptions.ConnectionError,
                      requests.exceptions.Timeout,
                      requests.exceptions.ReadTimeout)

    GET_BALANCE_MAIN = [IFBlockAPI.get_balance]
    GET_TRANSACTIONS_MAIN = [IFBlockAPI.get_transactions]
    GET_UNSPENT_MAIN = [IFBlockAPI.get_unspent]
    BROADCAST_TX_MAIN = [IFBlockAPI.broadcast_tx]
    GET_TX_MAIN = [IFBlockAPI.get_transaction]
    GET_TX_AMOUNT_MAIN = [IFBlockAPI.get_tx_amount]
    GET_RAW_TX_MAIN = [IFBlockAPI.get_raw_transaction]

    GET_BALANCE_TEST = [IFBlockAPI.get_balance_testnet]
    GET_TRANSACTIONS_TEST = [IFBlockAPI.get_transactions_testnet]
    GET_UNSPENT_TEST = [IFBlockAPI.get_unspent_testnet]
    BROADCAST_TX_TEST = [IFBlockAPI.broadcast_tx_testnet]
    GET_TX_TEST = [IFBlockAPI.get_transaction_testnet]
    GET_TX_AMOUNT_TEST = [IFBlockAPI.get_tx_amount_testnet]
    GET_RAW_TX_TEST = [IFBlockAPI.get_raw_transaction_testnet]

    @classmethod
    def get_balance(cls, address):
        """Gets the balance of an address in satoshi.

        :param address: The address in question.
        :type address: ``str``
        :raises ConnectionError: If all API services fail.
        :rtype: ``int``
        """

        for api_call in cls.GET_BALANCE_MAIN:
            try:
                return api_call(address)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def get_balance_testnet(cls, address):
        """Gets the balance of an address on the test network in satoshi.

        :param address: The address in question.
        :type address: ``str``
        :raises ConnectionError: If all API services fail.
        :rtype: ``int``
        """

        for api_call in cls.GET_BALANCE_TEST:
            try:
                return api_call(address)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def get_transactions(cls, address):
        """Gets the ID of all transactions related to an address.

        :param address: The address in question.
        :type address: ``str``
        :raises ConnectionError: If all API services fail.
        :rtype: ``list`` of ``str``
        """

        for api_call in cls.GET_TRANSACTIONS_MAIN:
            try:
                return api_call(address)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def get_transactions_testnet(cls, address):
        """Gets the ID of all transactions related to an address on the test
        network.

        :param address: The address in question.
        :type address: ``str``
        :raises ConnectionError: If all API services fail.
        :rtype: ``list`` of ``str``
        """

        for api_call in cls.GET_TRANSACTIONS_TEST:
            try:
                return api_call(address)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def get_transaction(cls, txid):
        """Gets the full transaction details.

        :param txid: The transaction id in question.
        :type txid: ``str``
        :raises ConnectionError: If all API services fail.
        :rtype: ``Transaction``
        """

        for api_call in cls.GET_TX_MAIN:
            try:
                return api_call(txid)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def get_transaction_testnet(cls, txid):
        """Gets the full transaction details on the test
        network.

        :param txid: The transaction id in question.
        :type txid: ``str``
        :raises ConnectionError: If all API services fail.
        :rtype: ``Transaction``
        """

        for api_call in cls.GET_TX_TEST:
            try:
                return api_call(txid)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def get_tx_amount(cls, txid, txindex):
        """Gets the amount of a given transaction output.

        :param txid: The transaction id in question.
        :type txid: ``str``
        :param txindex: The transaction index in question.
        :type txindex: ``int``
        :raises ConnectionError: If all API services fail.
        :rtype: ``Decimal``
        """

        for api_call in cls.GET_TX_AMOUNT_MAIN:
            try:
                return api_call(txid, txindex)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def get_tx_amount_testnet(cls, txid, txindex):
        """Gets the amount of a given transaction output on the
        test network.

        :param txid: The transaction id in question.
        :type txid: ``str``
        :param txindex: The transaction index in question.
        :type txindex: ``int``
        :raises ConnectionError: If all API services fail.
        :rtype: ``Decimal``
        """

        for api_call in cls.GET_TX_AMOUNT_TEST:
            try:
                return api_call(txid, txindex)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def get_unspent(cls, address):
        """Gets all unspent transaction outputs belonging to an address.

        :param address: The address in question.
        :type address: ``str``
        :raises ConnectionError: If all API services fail.
        :rtype: ``list`` of :class:`~bitcash.network.meta.Unspent`
        """

        for api_call in cls.GET_UNSPENT_MAIN:
            try:
                return api_call(address)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def get_unspent_testnet(cls, address):
        """Gets all unspent transaction outputs belonging to an address on the
        test network.

        :param address: The address in question.
        :type address: ``str``
        :raises ConnectionError: If all API services fail.
        :rtype: ``list`` of :class:`~bitcash.network.meta.Unspent`
        """

        for api_call in cls.GET_UNSPENT_TEST:
            try:
                return api_call(address)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def get_raw_transaction(cls, txid):
        """Gets the raw, unparsed transaction details.

        :param txid: The transaction id in question.
        :type txid: ``str``
        :raises ConnectionError: If all API services fail.
        :rtype: ``Transaction``
        """

        for api_call in cls.GET_RAW_TX_MAIN:
            try:
                return api_call(txid)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def get_raw_transaction_testnet(cls, txid):
        """Gets the raw, unparsed transaction details on the test
        network.

        :param txid: The transaction id in question.
        :type txid: ``str``
        :raises ConnectionError: If all API services fail.
        :rtype: ``Transaction``
        """

        for api_call in cls.GET_RAW_TX_TEST:
            try:
                return api_call(txid)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def broadcast_tx(cls, tx_hex):  # pragma: no cover
        """Broadcasts a transaction to the blockchain.

        :param tx_hex: A signed transaction in hex form.
        :type tx_hex: ``str``
        :raises ConnectionError: If all API services fail.
        """
        success = None

        for api_call in cls.BROADCAST_TX_MAIN:
            try:
                success = api_call(tx_hex)
                if not success:
                    continue
                return
            except cls.IGNORED_ERRORS:
                pass

        if success is False:
            raise ConnectionError('Transaction broadcast failed, or '
                                  'Unspents were already used.')

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def broadcast_tx_testnet(cls, tx_hex):  # pragma: no cover
        """Broadcasts a transaction to the test network's blockchain.

        :param tx_hex: A signed transaction in hex form.
        :type tx_hex: ``str``
        :raises ConnectionError: If all API services fail.
        """
        success = None

        for api_call in cls.BROADCAST_TX_TEST:
            try:
                success = api_call(tx_hex)
                if not success:
                    continue
                return
            except cls.IGNORED_ERRORS:
                pass

        if success is False:
            raise ConnectionError('Transaction broadcast failed, or '
                                  'Unspents were already used.')

        raise ConnectionError('All APIs are unreachable.')
