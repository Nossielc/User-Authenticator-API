import json
import os

from bottle import Bottle, run, request, response

from libs.api import funcs

app = Bottle()

def run(local:str, port:int, debug:bool, reloader:bool):
    app.run(local = local, port = port, debug = debug, reloader = reloader)
#ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

"""
/api/user
"""

#VER TODOS OS USUÁRIOS
@app.get("/api/user")
def show_all_users():
    data:  dict = funcs.json_data()
    users: list = data["users"]
    if funcs.check_permission(data,users,3):
        users: str = json.dumps(users)
        return users
    else:
        return "Unauthorized"

#INSERIR UM NOVO USUÁRIO
@app.post("/api/user")
def add_user():
    data: dict = funcs.json_data()
    users:list = data["users"]
    if funcs.check_permission(data,users,1):
        error: int = 0                                                           #Variavel para saber se houve alguma incompatibilidade com o request.json e o data.json
        new_user: dict = request.json
        new_user_id: int = users[len(users)-1]["id"] + 1                         #ID do último usuário + 1
        user: dict = {}                                                           #Dicionário novo vazio auxiliar
        user["id"] = new_user_id
        user["roles"] = []
        if new_user:
            if len(new_user)==4:
                for key in new_user:
                    if key in ("name","email","password","roles"):              #Checa as keys do request.json
                        if key == "roles" and type(new_user[key]) == list:      #Checa se a key "roles" é do tipo list
                            for r in new_user[key]:
                                if 1<=r<=3:
                                    user["roles"].append(r)                     #Adiciona a nova role para o novo usuário somente se a role for 1,2 e/ou 3
                        elif key == "email" and "@" in new_user[key]:           #Checa se é um email válido
                            user[key]=new_user[key]
                        elif key =="name" or key == "password":
                            user[key]=new_user[key]
                        else:
                            error = 1
                    else:
                        error = 1
            else:
                error = 1 
        else:
            error = 1                       
        if error == 0:                      #Caso não ocorreu nenhum erro
            users.append(user)              #Adiciona o novo usuário na lista de usuários
            data["users"] = users           #Atualiza os usuários do data
            funcs.write_json_data(data)           #Escreve no arquivo data.json o novo data
        else:
            #error
            pass
    #else:
        #Unauthorized


"""
/api/user/<id:int>
"""

#VER APENAS O USUÁRIO DE ID (id)
@app.get("/api/user/<id:int>")
def show_user_by_id(id:int):
    data: dict = funcs.json_data()
    users:list = data["users"]
    if funcs.check_permission(data,users,3):          #Se tiver a permissão "view_users":
        if funcs.find_user(id,users):                 #Se existir o usuário com esse ID:
            index:int =id-funcs.find_user(id,users)        #Índice desse usuário é o ID - o aux da função "funcs.find_user"
            user :dict = users[index]
            user = json.dumps(user)
            return user
        else:
            return "USER NOT FOUND"
    else:
        return "Unauthorized"

                
                
#ATUALIZANDO O USUÁRIO DE ID (id)
@app.put("/api/user/<id:int>")
def update_user_by_id(id:int):
    data: dict = funcs.json_data()
    users:list = data["users"]
    if funcs.check_permission(data,users,2):                                      #Se tiver a permissão "update_user":
        if funcs.find_user(id, users):                                            #Se existir o usuário com esse ID:
            index: int = id - funcs.find_user(id, users)                               #Índice desse usuário é o ID - o aux da função "funcs.find_user"
            user: dict = users[index]
        to_update_data: dict = request.json
        if to_update_data:
            for key in to_update_data:                                              #For loop para testar todas as key do to_update_data
                if key in ("name","email","password","roles"):                  #Se a key do to_update_data for nome,email,password ou roles:
                    try:
                        if key == "roles" and type(to_update_data[key]) == list:    #Checa se a key é "roles" e é do tipo list
                            for r in to_update_data[key]:                           #Testa as roles e adiciona na lista "roles" do novo usuário
                                if 1<=r<=3 and r not in user["roles"]:          
                                    user["roles"].append(r)                     #Adiciona a nova role para o novo usuário somente se a role for 1,2 e/ou 3
                        elif key == "email" and "@" in to_update_data[key]:         #Checa se é um email válido
                            user[key]=to_update_data[key]
                        elif key =="name" or key == "password":
                            user[key]=to_update_data[key]
                    except:
                        pass
            user["roles"].sort()                                                #Ordena as roles do usuário selecionado
            data["users"][index] = user                                         #Atualiza o usuário selecionado 
            funcs.write_json_data(data)                                               #Atualiza o arquivo data.json com o data atualizado
    #else:
        #Unauthorized user


#EXCLUIR O USUÁRIO DE ID (id)
@app.delete("/api/user/<id:int>")
def delete_user_by_id(id:int):
    data:  dict = funcs.json_data()
    users: list =data["users"]
    if funcs.check_permission(data,users,2):              #Se tiver a permissão "update_user":
        if funcs.find_user(id, users):                    #Se existir o usuário com esse ID:
            index: int = id - funcs.find_user(id, users)       #Índice desse usuário é o ID - o aux da função "funcs.find_user"
            del users[index]                        #Deleta o usuário selecionado
            data["users"]=users                     #Atualiza a data
            funcs.write_json_data(data)                   #Atualiza o arquivo data.json com o data atualizado
    #else:
        #Unauthorized user


"""
/api/user/<id:int>/role
"""

#VER TODAS AS PERMISSÕES DO USUÁRIO DE ID (id)
@app.get("/api/user/<id:int>/role")
def show_user_roles_by_id(id:int):
    data:  dict = funcs.json_data()
    users: list =data["users"]
    if funcs.check_permission(data,users,3):              #Se tiver a permissão "view_users":
        roles: list = data["roles"]
        user_roles: list = []                             #Lista auxiliar para as roles do usuário selecionado
                
        if funcs.find_user(id, users):                    #Se existir o usuário com esse ID:
            index: int = id - funcs.find_user(id, users)       #Índice desse usuário é o ID - o aux da função "funcs.find_user"
            num_user_roles: int = users[index]["roles"]  #num_user_roles = roles do usuário selecionado

            for r in num_user_roles:                #Para cada role no num_user_roles:
                user_roles.append(roles[r-1])       #Adiciona na lista user_roles o role de id  r-1
            user_roles: str = json.dumps(user_roles)     #Transforma a lista user_roles em json
            return user_roles
        else:
            return "USER NOT FOUND"
    else:
        return "Unauthorized"

                
#ADICIONAR UMA PERMISSÃO AO USUÁRIO DE ID (id)
@app.post("/api/user/<id:int>/role")
def add_user_roles_by_id(id:int):
    data:  dict = funcs.json_data()
    users: list =data["users"]
    if funcs.check_permission(data,users,1):                          #Se tiver a permissão "create_user":         
        if funcs.find_user(id, users):                                #Se existir o usuário com esse ID:
            index: int  = id - funcs.find_user(id, users)                   #Índice desse usuário é o ID - o aux da função "funcs.find_user"
            user:  dict = users[index]                                 #User = usuário com id (ID)
        post_data: dict = request.json
        try:
            new_user_role = post_data["roles"]
            if new_user_role and type(new_user_role) == list:   #Se new_user_role não estiver vazia e for do tipo lista:
                for r in new_user_role:                         #Para cada role no new_user_role:
                    if r not in user["roles"] and 1<=r<=3:      #Se o usuário já não tiver essa role e for 1,2 e/ou 3
                        user["roles"].append(r)                 #Adiciona a role para o usuário
        except:
            pass
        else:
            user["roles"].sort()                                #Ordena as roles
            data["users"][index] = user                         #Atualiza o data
            funcs.write_json_data(data)                               #Atualiza o arquivo data.json com o data atualizado
            
    #else:
        #Unauthorized user
               

#EXCLUIR A PERMISSÃO DE ID 1 DO USUÁRIO DE ID (id)
@app.delete("/api/user/<id:int>/role/<role_num:int>")
def delete_user_role_by_id(id:int, role_num:int):
    data :dict = funcs.json_data()
    users:list = data["users"]
    if funcs.check_permission(data,users,2):                  #Se tiver a permissão "update_user":
        if funcs.find_user(id, users):                        #Se existir o usuário com esse ID:
            index: int = id - funcs.find_user(id, users)           #Índice desse usuário é o ID - o aux da função "funcs.find_user"
            try:
                users[index]["roles"].remove(role_num)  #Remove a role (role_num) do usuário selecionado
            except:
                pass
        else:
            pass
        data["users"] = users                           #Atualiza o data
        funcs.write_json_data(data)                           #Atualiza o arquivo data.json com o data atualizado
    #else:
        #Unauthorized user


"""
/api/login
"""

@app.post("/api/login")
def create_cookie():
    data :dict = funcs.json_data()
    users:list = data["users"]
    post_data :dict = request.json
    for u in users:                                                             #Para cada usuário no arquivo data.json:
        if u["email"] == post_data["email"]:                                    #Se o email der match:
            if u["password"] == post_data["password"]:                          #Se a senha também dar match:
                #print("Success")
                response.set_cookie("id", u["id"], secret='some-secret-key')    #Seta um cookie com o ID do usuário


app.run(local = "localhost", port = 8080, debug = True, reloader = True)