import json
from bottle import request

import env


def json_data() -> dict:
    with open(env.ROOT_DIR+'/data/data.json') as json_file:
        data: dict = json.load(json_file)
        return data

def write_json_data(data: dict):
    with open(env.ROOT_DIR+'/data/data.json','w') as json_file:
        json.dump(data,json_file,indent=4)

def find_user(id:int, users:list) ->int:
    """
    Função que retorna o índice do usuário(ID), se não achar, retorna 0
    """
    aux: int = 1                                                   # Aux para achar a diferença entre o indice e o ID   indice do user no data.json = id - aux
    if users[len(users) - 1]["id"] >= id and id > 0:          # ID entre 0 e ID do ultimo user
        while True:
            if id - aux < len(users):                         # Se o indice em teste é menor que o numero de users
                try:
                    if users[id - aux]["id"] > id:            # Se ID do usuário com indice teste > ID
                        aux += 1
                    elif users[id - aux]["id"] < id:          # Se ID do usuário com indice teste < ID (usuário não existe)
                        return 0
                    elif users[id - aux]["id"] == id:         # Se ID == ID do usuário com indice teste
                        return aux
                except:
                    return 0
            else:
                aux += 1
    return 0

def check_permission(data:dict ,users:list, role:int) -> bool:
    """
    Função para checar pelos cookies se o usuário tem permissão "role"
    Role 1: Create User
    Role 2: Update User
    Role 3: View Users
    """
    if request.get_cookie("id", secret='some-secret-key'):
        client_id: int = request.get_cookie("id", secret='some-secret-key')
        if find_user(client_id,users):
            index: int = client_id - find_user(client_id,users)
            if role in users[index]["roles"]:
                return True
    else:
        return False