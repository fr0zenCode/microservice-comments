from dataclasses import dataclass

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


@dataclass
class KafkaMessageBroker:
    consumer: AIOKafkaConsumer
    producer: AIOKafkaProducer

    async def start_consuming(self):
        yield self.consumer.start()

    async def start_producer(self):
        await self.producer.start()

    async def send_message(self, key: bytes, topic: str, value: bytes):
        await self.producer.send(topic=topic, key=key, value=value)

    async def stop_consuming(self):
        await self.consumer.stop()

    async def stop_producer(self):
        await self.producer.stop()
