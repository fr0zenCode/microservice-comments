import asyncio

from aiokafka import AIOKafkaProducer


async def send_one():
    producer = AIOKafkaProducer(bootstrap_servers="localhost:9092")
    await producer.start()
    try:
        await producer.send_and_wait("test",
                                     key="true".encode("utf-8"),
                                     value="TEST MESSAGE".encode("utf-8"))
    finally:
        await producer.stop()

asyncio.run((send_one()))
