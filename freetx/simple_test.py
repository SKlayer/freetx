import freetx


my_key = freetx.Key("5KSZ5h6AvZUdavtystU7ytR5XAxVyqpzYWHp14n7XnTc1m6kaHY")
print(my_key.get_balance("mbch"))


tx_id = my_key.sweep("bitcoincash:qr2vny04sxzqn7zeuufgr3wh7gs89uvzvu6jgfd3ge")
# Sweep your all bch to dest address
print(tx_id)
outputs = [
        ("bitcoincash:qr2vny04sxzqn7zeuufgr3wh7gs89uvzvu6jgfd3ge",1000, 'satoshi'),
    ]
tx_id = my_key.send(outputs, fee=1, message=f"This is a test TRANSACTION created by BITCASH CN")
print(tx_id)

tx_id = my_key.send_op_return([bytes.fromhex('6d01'),  # encode hex to bytes
                         'BitCash CN!'.encode('utf-8')])
print(tx_id)
tx_id = my_key.send_op_return([bytes.fromhex('6d02'),  # encode hex to bytes
                         'https://github.com/SKlayer/bitcashcn'.encode('utf-8')])
print(tx_id)