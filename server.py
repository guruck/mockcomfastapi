"""Mock de serviço de api para testes"""

import json
from typing import Any
import locale
import logging
from logging.handlers import TimedRotatingFileHandler  # , RotatingFileHandler
import uvicorn
from fastapi import FastAPI, Request

locale.setlocale(locale.LC_ALL, "Portuguese")
handlertime = TimedRotatingFileHandler("server.log", when="d", interval=1, backupCount=5)
# handlersize = RotatingFileHandler("server.log", maxBytes=2048, backupCount=5)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[handlertime]  # , handlersize]
)

app = FastAPI()

# minimamente no dadosMockados deve conter o parametro "id" para funcionamento das funcoes
dadosMockados = [
    {"id": 0, "owner": "Tiago", "task": "desenvolver GET", "status": "concluido"},
    {"id": 1, "owner": "Rodrigues", "task": "desenvolver POST", "status": "pendente"},
    {"id": 2, "owner": "Tiago", "task": "desenvolver teste", "status": "teste"},
    {"id": 3, "owner": "Tiago", "task": "desenvolver teste", "status": "teste"},
    {"id": 4, "owner": "Jonas", "task": "desenvolver teste", "status": "pendente"},
    {"id": 5, "owner": "Jorel", "task": "desenvolver teste", "status": "teste"},
    {"id": 6, "owner": "Irmao do Jorel", "task": "desenvolver teste", "status": "concluido"},
]


def find_secret(params: dict[str, str]):
    """funcao que resgata nos dados mockados nenhum, um ou mais registros
    dependendo dos parametros passados para realizar a busca
    """
    collecteds_secrets: list[dict[str, Any]] = []
    finder: list[dict[str, Any]] = []

    def __resume_list():
        """funcao interna apenas para o caso de existir registro duplicado
        quando encontrado mais de uma vez existindo mais de um filtro
        """
        if len(finder) <= 1:
            return finder
        else:
            for item in finder:
                if item not in collecteds_secrets:
                    collecteds_secrets.append(item)
            return collecteds_secrets

    if len(params.keys()) == 1 and "id" in params.keys():
        try:
            num = int(str(params.get("id")))
            aux_value = dadosMockados[num]
            if "deleted" in aux_value.keys():
                return {"status": "failed", "data": "Id ja deletado"}

            return aux_value
        except ValueError as e:
            logging.error(e)
            return {"status": "failed", "data": "Id especificado invalido"}

    for secret in dadosMockados:
        putsecret = True
        check = 0
        for param, value in params.items():
            if param in ("param", "last_param"):  # parametro unico ou ultimo parametro
                if value == "anyone" and check > 0:
                    logging.info("%s[%s]: %s", param, str(len(params)), value)
                    putsecret = True
                    break
                if value != "anyone" and len(params) == 1:
                    logging.info("%s[%s]: %s", param, str(len(params)), value)
                    return {"status": "sucesso", "data": ""}

            teste = f"{param} in {secret.keys()}: {param in secret.keys()}"
            logging.info(teste)
            if param in secret.keys():
                teste = f"secret.get({param}) {secret.get(param)} == {value}: {str(secret.get(param)).lower() == str(value).lower()}"  # noqa: E501, pylint: disable=fixme, line-too-long
                logging.info(teste)
                if str(secret.get(param)).lower() == str(value).lower():
                    logging.info("achei")
                    check += 1
                else:
                    logging.info("nao achei")
                    putsecret = False
            else:
                putsecret = False

        if putsecret:
            logging.warning("anyone: %s", str(len(params)))
            finder.append(secret)

    teste = f"len(finder) < len(params)>> {len(finder)} < {len(params)}"
    logging.info(teste)

    return {"status": "sucesso", "data": __resume_list()}


def get_params(path: str) -> dict[str, str]:
    """transforma o path da url para um dicionario de parametros
    os parametros sao quebrados pela / se existirem
    devem ser fornecidos como: URI/parametro/valor
    """
    res_dict: dict[str, str] = {}
    lparams = path.split("/")
    term = len(lparams)
    logging.info("quantidade de parametros %s", term)

    if term == 1:
        res_dict = {"param": str(lparams[0])}
    else:
        for i in range(0, term - 1, 2):
            res_dict[str(lparams[i])] = str(lparams[i + 1])

        if term % 2 != 0:
            res_dict["last_param"] = str(lparams[term - 1])

    logging.info("dparams: %s", str(res_dict))
    return res_dict


async def print_request(request: Request) -> None:
    """para realizar dump da request"""
    data = await request.body()
    payload = json.loads(data.decode("utf-8")) if data != b"" else "body: None"
    # print(
    #     "{}\n{}\r\n{}\r\n\r\n{}".format(
    #         "-----------START-----------",
    #         request.method + " " + request.url.path,
    #         "\r\n".join("{}: {}".format(k, v) for k, v in request.headers.items()),
    #         payload,
    #     )
    # )
    logging.info("%s %s", request.method, request.url.path)
    for k, v in request.headers.items():
        logging.info("%s: %s", k, v)
    logging.info("payload: %s", payload)
    # print("data: ", data.decode("utf-8"))


@app.api_route("/secret/{full_path:path}", methods=["GET", "POST", "DELETE", "PUT"])
async def secret(request: Request, full_path: str):
    """metodo simples para simular o CRUD"""
    logging.info("-" * 80)
    await print_request(request)
    if request.method == "POST":
        # inserir um novo valor, despresa fullpath
        data = await request.body()
        payload = json.loads(data.decode("utf-8")) if data != b"" else None
        if payload is not None and payload != {}:
            # pode ser necessario realizar um modelo de entrada para validar os dados
            payload["id"] = len(dadosMockados)
            dadosMockados.append(payload)
            response = {"status": "sucesso", "data": f"Tarefa inserida: {payload['id']}"}
        else:
            response = {"status": "failed", "data": "Tarefa vazia"}

        return response
    elif request.method == "GET":
        # busca determinado valor, despresa fullpath para all
        if full_path.strip() == "":
            return {"status": "sucesso", "data": dadosMockados}
        else:
            dparams = get_params(path=full_path.strip())
            return find_secret(params=dparams)
    elif request.method == "DELETE":
        # deve ser fornecido no body o parametro adequado para filtro id
        data = await request.body()
        payload = json.loads(data.decode("utf-8")) if data != b"" else None
        if payload is not None and payload != {}:
            if len(payload.keys()) == 1 and "id" in payload.keys():
                num = payload.get("id")
                if not isinstance(num, int):
                    return {"status": "failed", "data": "Id especificado invalido"}

                if num < 0 or num > len(dadosMockados):
                    return {"status": "failed", "data": "Id fora do intervalo"}

                aux_value = dadosMockados[num]
                if "deleted" in aux_value.keys():
                    return {"status": "failed", "data": "Id ja deletado"}

                aux_str_value = ";".join("_{}: _{}".format(k, v) for k, v in aux_value.items())
                logging.info(aux_str_value)
                dadosMockados.pop(num)
                dadosMockados.insert(num, {"deleted": aux_str_value})
                return {"status": "success", "data": f"deleted {num}"}
        else:
            return {"status": "failed", "data": "Tarefa vazia"}
    elif request.method == "PUT":
        # deve ser fornecido no body o parametro adequado para filtro id
        data = await request.body()
        payload = json.loads(data.decode("utf-8")) if data != b"" else None
        if payload is not None and payload != {}:
            if len(payload.keys()) >= 1 and "id" in payload.keys():
                num = payload.get("id")
                if not isinstance(num, int):
                    return {"status": "failed", "data": "Id especificado invalido"}

                if num < 0 or num > len(dadosMockados):
                    return {"status": "failed", "data": "Id fora do intervalo"}

                dadosMockados.pop(num)
                dadosMockados.insert(num, payload)
                return {"status": "success", "data": f"updated {num}"}
            else:
                return {"status": "failed", "data": "Id nao informado para UPDATE"}
        else:
            return {"status": "failed", "data": "Tarefa vazia"}


if __name__ == "__main__":
    uvicorn.run(app, port=8088)
