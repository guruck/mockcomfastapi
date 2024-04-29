"""consumindo o servico mockado"""

import json
import logging
from typing import Union
import requests
from requests.models import Response
from consumer_interface import ConsumerInterface


class Consumer(ConsumerInterface):
    """para realizar as operacoes mockadas"""

    def __init__(self) -> None:
        self.server_uri = "http://127.0.0.1:8000"

    def req_get(self, uri, anyone: bool = False) -> Response:
        logging.debug('%s "GET %s"', self.server_uri, uri)
        if anyone:
            url = f"{self.server_uri}{uri}/anyone"
        else:
            url = f"{self.server_uri}{uri}"
        return requests.get(
            url,
            headers={"Accept": "application/json"},
            timeout=5.0,
        )

    def req_post(self, uri, json_object) -> Response:
        logging.debug('%s "POST %s"', self.server_uri, uri)
        url = f"{self.server_uri}{uri}"
        return requests.post(
            url,
            data=json_object,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            timeout=5.0,
        )

    def print_response(self, res: Response):
        print("-" * 80)
        print("Content: ", res._content)
        print("Status Code: ", res.status_code)
        print("Headers: ", res.headers)
        print("Url: ", res.url)
        print("History: ", res.history)
        print("Encoding: ", res.encoding)
        print("Reason: ", res.reason)
        print("Cookies: ", res.cookies)
        print("Elapsed: ", res.elapsed)
        print("Request: ", res.request)

    def get_data(self) -> Union[str, list, dict]:
        res = self.req_get(uri="/secret")
        if res.status_code == 200:
            if res._content is None:
                return "nenhum dado obtido na consulta"
            else:
                tasks = json.loads(res._content.decode(str(res.encoding)))
                return tasks["data"][0]
        else:
            return "dados nao obtidos com sucesso"
