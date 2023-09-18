import easygui
import os
import requests
import time

def confirm_action():
    response = easygui.ynbox("Só confirme depois que entrar no projudi!\n \nLogin foi realizado com sucesso?", "Confirmação login")
    if response:
        print("Login realizado com sucesso.")
        return True
    else:
        print("Login cancelado.")
        print("Saindo do sistema...")
        time.sleep(3)
        return False
    
def statusCode200(message):
    while True:
        response = requests.get(os.getenv('URL_CITACOES_PROJUDI'))
        if response.status_code == 200:
            print(message)
            break
        else:
            time.sleep(1)

def createTxt(result, directory, day):
    nameArch = os.path.join(directory, f'{day}.txt')
    with open(nameArch, 'a') as archTxt:
        archTxt.write(f'{result}\n')

def finish(message):
    print(message)
    print('Saindo do sistema...')
    for i in range(3, 0, -1): 
        print(f'{i}...')
        time.sleep(1)