# import json
import locale
import logging
from logging.handlers import TimedRotatingFileHandler  # , RotatingFileHandler

from consumer import Consumer
from consumer_proxy import ConsumerProxy

locale.setlocale(locale.LC_ALL, "Portuguese")
handlertime = TimedRotatingFileHandler("client.log", when="d", interval=1, backupCount=5)
# handlersize = RotatingFileHandler("server.log", maxBytes=2048, backupCount=5)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[handlertime]  # , handlersize]
)


def main():
    """principal funcao"""

    # teste = Consumer()
    # dados = teste.req_get(uri="/secret/owner/tiago")
    # teste.print_response(dados)
    # if dados.status_code == 200:
    #     tasks = json.loads(dados._content.decode(dados.encoding))
    #     print(tasks, type(tasks))
    #     print(tasks["data"], type(tasks["data"]))

    # teste = Consumer()
    # for i in range(50):
    #     print(f"-----{i}-----")
    #     result = teste.get_data()
    #     if isinstance(result, str) or isinstance(result, dict):
    #         print(result)
    #     elif isinstance(result, list):
    #         for item in result:
    #             print(item)

    teste = ConsumerProxy()
    for i in range(50):
        print(f"-----{i}-----")
        result = teste.get_data()
        if isinstance(result, str) or isinstance(result, dict):
            print(result)
        elif isinstance(result, list):
            for item in result:
                print(item)


if __name__ == "__main__":
    main()
