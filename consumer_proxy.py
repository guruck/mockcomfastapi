import json
from typing import Union
from consumer_interface import ConsumerInterface
from consumer import Consumer


class ConsumerProxy(ConsumerInterface):
    def __init__(self) -> None:
        super().__init__()
        self._client = Consumer()
        self._data = "None"

    def get_data(self) -> Union[str, list, dict]:

        if self._data == "None":
            res = self._client.req_get(uri="/secret")
            if res.status_code == 200:
                if res._content is None:
                    self._data = "nenhum dado obtido na consulta"
                else:
                    tasks = json.loads(res._content.decode(str(res.encoding)))
                    self._data = tasks["data"][0]
            else:
                self._data = "dados nao obtidos com sucesso"

        return self._data
