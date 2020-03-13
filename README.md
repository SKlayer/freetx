<h3 align="center">BitCash CN</h3>
<h4 align="center">Bitcoin Cash made easy</h4>

Forked from [sporestack's Bitcash library](https://github.com/sporestack/bitcash).

**BitCash is so easy to use, in fact, you can do this:**


```python
>>> from freetx import Key
>>>
>>> k = Key()
>>> k.address
'bitcoincash:qp0hamw9rpyllkmvd8047w9em3yt9fytsunyhutucx'
>>>
>>> k.get_balance('usd')
'2'
>>>
>>> # Let's donate a dollar to CoinSpice.io
>>> outputs = [
>>>     ('bitcoincash:qz69e5y8yrtujhsyht7q9xq5zhu4mrklmv0ap7tq5f', 1, 'usd'),
>>>     # you can add more recipients here
>>> ]
>>>
>>> k.send(outputs)
'6aea7b1c687d976644a430a87e34c93a8a7fd52d77c30e9cc247fc8228b749ff'
>>> tx_id = my_key.sweep("bitcoincash:qr2vny04sxzqn7zeuufgr3wh7gs89uvzvu6jgfd3ge")
# Sweep your all bch to dest address
>>> print(tx_id)
>>> outputs = [
        ("bitcoincash:qr2vny04sxzqn7zeuufgr3wh7gs89uvzvu6jgfd3ge",1000, 'satoshi'),
    ]
>>> tx_id = my_key.send(outputs, fee=1, message=f"This is a test TRANSACTION created by BITCASH CN")
>>> print(tx_id)
Let's create a memo! Protocol: https://memo.cash/protocol
Set Username First
>>> tx_id = my_key.send_op_return([bytes.fromhex('6d01'),  # encode hex to bytes
                         'BitCash CN!'.encode('utf-8')])
>>> print(tx_id)
Send A Memo
>>> tx_id = my_key.send_op_return([bytes.fromhex('6d02'),  # encode hex to bytes
                         'https://github.com/SKlayer/bitcashcn'.encode('utf-8')])
>>> print(tx_id)
"566e8b90e1c5f02f3717804d73b979e92e8a598616ff5f16e68dd94e48c05ea5"

```

Done. Here is the transaction:
https://explorer.bitcoin.com/bch/tx/6aea7b1c687d976644a430a87e34c93a8a7fd52d77c30e9cc247fc8228b749ff
https://memo.cash/explore/tx/566e8b90e1c5f02f3717804d73b979e92e8a598616ff5f16e68dd94e48c05ea5

## Features

- Python's fastest available implementation (100x faster than closest library)
- Seamless integration with existing server setups
- Supports keys in cold storage
- Fully supports 32 different currencies
- First class support for storing data in the blockchain
- Deterministic signatures via RFC 6979
- Access to the blockchain (and testnet chain) through multiple APIs for redundancy
- Exchange rate API, with optional caching
- Compressed public keys by default
- Multiple representations of private keys; WIF, PEM, DER, etc.
- Standard P2PKH transactions

If you are intrigued, continue reading. If not, continue all the same!

## Installation

BitCash is distributed on `PyPI` as a universal wheel and is available on Linux/macOS
and Windows and supports Python 3.5+ and PyPy3.5-v5.7.1+. `pip` >= 8.1.2 is required.


```shell
$ python setup.pp install  
```

## Documentation

Docs are hosted by Github Pages and are automatically built and published
by Travis after every successful commit to BitCash's ``master`` branch.

[Read the documentation](https://sporestack.github.io/bitcash/)

## Credits

- [ofek](https://github.com/ofek/bit) for the original bit codebase.
- [Additional](AUTHORS.rst)
