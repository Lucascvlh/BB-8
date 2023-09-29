import easygui
import os
import time

def confirm_action():
    response = easygui.ynbox("Só confirme depois que entrar no projudi!\n \nLogin foi realizado com sucesso?", "Confirmação login")
    if response:
        print("Login realizado com sucesso.")
        return True
    else:
        return False

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