from confluent_kafka import Consumer, KafkaError, KafkaException
import sys

conf = {
    "bootstrap.servers": "host1:9092,host2:9092",
    "group.id": "foo",
    "auto.offset.reset": "smallest",
}


running = True


def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write(
                        "%% %s [%d] reached end at offset %d\n"
                        % (msg.topic(), msg.partition(), msg.offset())
                    )
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                print("Received message: " + msg.value().decode("utf-8"))
    finally:
        consumer.close()


def shutdown():
    global running
    running = False


if __name__ == "__main__":
    consumer = Consumer(conf)
    basic_consume_loop(consumer=consumer, topics=["cli"])