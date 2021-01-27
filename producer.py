from confluent_kafka import Producer

from prompt_toolkit import PromptSession
import socket

conf = {"bootstrap.servers": "host1:9092,host2:9092", "client.id": socket.gethostname()}


producer = Producer(
    conf,
)
if __name__ == "__main__":
    session = PromptSession()
    while True:
        try:
            text = session.prompt("Send a message >>> ")
        except KeyboardInterrupt:
            break
        except EOFError:
            break

        producer.produce(
            "cli",
            key="key",
            value=text,
        )

    print("GoodBye!")
