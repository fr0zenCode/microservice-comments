import asyncio

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from message_brokers.core import KafkaMessageBroker


kafka_message_broker = KafkaMessageBroker(
    consumer=AIOKafkaConsumer(
        "test",
        bootstrap_servers="localhost:9092",
        group_id="comments"
    ),
    producer=AIOKafkaProducer()
)


async def consume():
    consumer = AIOKafkaConsumer(
        "test",
        bootstrap_servers="localhost:9092",
        group_id="comments"
    )

    await consumer.start()
    try:
        async for msg in consumer:
            print(msg)
            print(f"\n\n{'-' * 30}\n"
                  f"CONSUMED:"
                  f"\n"
                  f"msg.topic: {msg.topic}, \n"
                  f"msg.partition: {msg.partition}, \n"
                  f"msg.offset: {msg.offset}, \n"
                  f"msg.key: {msg.key}, \n"
                  f"msg.value: {msg.value}, \n"
                  f"msg.timestamp: {msg.timestamp} \n")
    finally:
        await consumer.stop()


asyncio.run(consume())
