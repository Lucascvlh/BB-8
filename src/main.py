from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
from selenium.webdriver.common.alert import Alert
from dotenv import load_dotenv
from pyautogui import hotkey
from function import createTxt
import time
import os
import datetime

from function import confirm_action

load_dotenv()

today = datetime.date.today()
todayFormat = today.strftime("%d/%m/%y")
todayTxt = today.strftime("%d-%m-%y")

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driver.maximize_window()

#login no BL
driver.get(os.getenv('URL_BL'))
driver.find_element(By.XPATH, '//*[@id="Email"]').send_keys(os.getenv('LOGIN_BL'))
driver.find_element(By.XPATH, '//*[@id="Senha"]').send_keys(os.getenv('PASSWORD_BL') + Keys.ENTER)
driver.get(os.getenv('URL_BL_PESQUISA'))
window_BrainLaw = driver.current_window_handle

#Abrir aba BL cadastro
driver.execute_script("window.open('', '_blank');")
driver.switch_to.window(driver.window_handles[1])
driver.get(os.getenv('URL_PAINEL_CSC'))
window_cadastro = driver.current_window_handle

#Login no projudi
driver.execute_script("window.open('', '_blank');")
driver.switch_to.window(driver.window_handles[2])
driver.get(os.getenv('URL_PROJUDI'))
window_projudi = driver.current_window_handle
driver.find_element(By.XPATH, '//*[@id="login"]').send_keys(os.getenv('LOGIN_PROJUDI'))
driver.find_element(By.XPATH, '//*[@id="senha"]').send_keys(os.getenv('PASSWORD_PROJUDI') + Keys.ENTER)
time.sleep(5)
confirm_action()

processView = []

directory = 'Processos'
if not os.path.exists(directory):
  os.makedirs(directory)

if confirm_action:
  driver.get(os.getenv('URL_CITACOES_PROJUDI'))
  time.sleep(5)
  dayCienc = driver.find_element(By.XPATH, '//*[@id="Arquivos"]/div/table[2]/tbody/tr[3]/td[8]/font/strong').text
  todayFormat = '18/09/23' #Está aqui só pra maquiar o dia, depois quando terminar, excluir
  a = 0
  try:
    while todayFormat == dayCienc:
      process = driver.find_element(By.XPATH, '//*[@id="Arquivos"]/div/table[2]/tbody/tr[3]/td[1]/a').text
      driver.switch_to.window(window_BrainLaw)
      campoPesquisaBL = '//*[@id="txtNrProcesso_F"]'
      wait.until(EC.visibility_of_element_located((By.XPATH, campoPesquisaBL)))
      driver.find_element(By.XPATH, campoPesquisaBL).clear()
      driver.find_element(By.XPATH, campoPesquisaBL).send_keys(process)
      hotkey('ctrl','a')
      hotkey('ctrl','c')
      driver.find_element(By.XPATH,'//*[@id="ContentMaster"]/div/div[2]/div[4]/div/div/button').click()
      time.sleep(5)
      try:
        noData = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_ASPxGridViewProcessos_DXEmptyRow"]/td[2]/div').text
        if str(noData).strip() == 'No data to display':
          #fazendo download do processo
          driver.switch_to.window(window_projudi)
          driver.find_element(By.XPATH, '//*[@id="Arquivos"]/div/table[2]/tbody/tr[3]/td[1]/a').click()
          time.sleep(2)
          driver.find_element(By.XPATH, '/html/body/div[5]/p/a[3]').click()
          
          while True:
            try:
              wait.until(EC.alert_is_present())
              alert = Alert(driver)
              alert.accept()
              break
            except NoAlertPresentException:
              continue
          time.sleep(6)
          driver.back()
          #realizar o upload
          driver.switch_to.window(window_cadastro)
          driver.find_element(By.XPATH, '//*[@id="btnPreCadastroProcesso"]').click()
          wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="formularioPreCadastroTcg"]/div/div/div/div[4]/div/div/div/div/div/div/div/div[1]/div[1]/div')))
          driver.find_element(By.XPATH, '//*[@id="formularioPreCadastroTcg"]/div/div/div/div[2]/div/div/div/div/div/div/div[1]').click()
          hotkey('down')
          hotkey('down')
          hotkey('enter')
          driver.find_element(By.XPATH, '//*[@id="formularioPreCadastroTcg"]/div/div/div/div[3]/div/div/div/div/div/div[1]').click()
          time.sleep(0.5)
          hotkey('ctrl','v')
          driver.find_element(By.XPATH, '//*[@id="formularioPreCadastroTcg"]/div/div/div/div[4]/div/div/div/div/div/div/div/div[1]/div[1]').click()
          time.sleep(5)
          if a == 0:
            hotkey('shift','tab')
            hotkey('shift','tab')
            hotkey('down')
            hotkey('down')
            hotkey('down')
            hotkey('down')
            hotkey('down')
            hotkey('down')
            hotkey('down')
            hotkey('enter')
            time.sleep(0.5)
            hotkey('tab')
            hotkey('down')
            hotkey('up')
            hotkey('enter')
          else:
            hotkey('shift','tab')
            hotkey('shift','tab')
            hotkey('down')
            hotkey('up')
            hotkey('enter')
          a += 1 
          #Esperando carregar o arquivo para mandar
          wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="gridArquivosPreCadastroTcg"]/div/div[6]/div/div/div[1]/div/table/tbody/tr[1]/td[2]')))
          i = 0
          while True:
            archProcess = driver.find_element(By.XPATH, '//*[@id="gridArquivosPreCadastroTcg"]/div/div[6]/div/div/div[1]/div/table/tbody/tr[1]/td[2]').text
            nameWhitOutExtension, extension = os.path.splitext(archProcess)
            if nameWhitOutExtension == process:
              driver.find_element(By.XPATH, '//*[@id="btnGravarPreCadastroTcg"]/div').click()
              processView.append(f'Processo {process} cadastrado via automação.')
              print(f'Processo {process} cadastrado via automação.')
              break
            elif i < 5:
              i += 1
              time.sleep(1)
              continue
            elif i >= 5:
              print('Nome do arquivo diferente do número do processo.')
              break
          wait.until(EC.invisibility_of_element_located((By.XPATH,'//*[@id="btnGravarPreCadastroTcg"]/div')))
          time.sleep(5)
          #Botão de quando aparece o OK de processo enviado
          driver.find_element(By.XPATH, '/html/body/div[9]/div/div[3]/button[1]').click()
          time.sleep(2)
          #clicar em visualizar depois de cadastrado
          driver.switch_to.window(window_projudi)
          driver.find_element(By.XPATH, '//*[@id="Arquivos"]/div/table[2]/tbody/tr[3]/td[10]/a').click()
          driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
          driver.back()
          hotkey('f5')
          time.sleep(5)
          dayCienc = driver.find_element(By.XPATH, '//*[@id="Arquivos"]/div/table[2]/tbody/tr[3]/td[8]/font/strong').text
      except NoSuchElementException:
        driver.switch_to.window(window_projudi)
        driver.find_element(By.XPATH, '//*[@id="Arquivos"]/div/table[2]/tbody/tr[3]/td[10]/a').click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.back()
        hotkey('f5')
        processView.append(f'Processo {process} já cadastrado no BrainLaw.')
        print(f'Processo {process} já cadastrado no BrainLaw.')
        time.sleep(5)
        dayCienc = driver.find_element(By.XPATH, '//*[@id="Arquivos"]/div/table[2]/tbody/tr[3]/td[8]/font/strong').text
  except NoSuchElementException:
    print('Não tem processo para o dia.')
  createTxt(processView, directory, todayTxt)
else:
  driver.close()


