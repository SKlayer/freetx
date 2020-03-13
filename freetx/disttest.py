import freetx


key = freetx.Key("5KSZ5h6AvZUdavtystU7ytR5XAxVyqpzYWHp14n7XnTc1m6kaHY")
print(key.address)
print(key.get_balance())
outputs = [
        ("FREEBotD5ZXm9qhwo43RaopKo62Aq3vbAg",1000, 'satoshi'),
    ]

tx_id = key.send(outputs, fee=1, message=f"This is a test TRANSACTION created by BITCASH")
print(tx_id)
