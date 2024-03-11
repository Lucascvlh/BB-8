from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
from selenium.webdriver.common.alert import Alert
from dotenv import load_dotenv
from pyautogui import hotkey
from function import createTxt, finish, confirm_action
import time
import os
from datetime import datetime, timedelta

load_dotenv()

today = datetime.now()
futureDay = today + timedelta(days=4)
futureDayFormatted = futureDay.strftime("%d/%m/%y")
futureDayDate = datetime.strptime(futureDayFormatted, "%d/%m/%y")

login = os.getenv('LOGIN')

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)
waitUpload = WebDriverWait(driver, 90)
driver.maximize_window()

def updatePageProjudi (message, directory, todayTxt):
    driver.switch_to.window(window_projudi)
    driver.find_element(By.XPATH, '//*[@id="Arquivos"]/div/table[2]/tbody/tr[3]/td[10]/a').click()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.back()
    hotkey('f5')
    time.sleep(5)
    print(message)
    createTxt(message, directory, todayTxt) 

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

confirmation = confirm_action()

countOk = 0
countRegistred = 0
preRegistred = 0

directory = 'Processos'
if not os.path.exists(directory):
  os.makedirs(directory)

if confirmation:
  driver.switch_to.window(window_projudi)
  driver.get(os.getenv('URL_CITACOES_PROJUDI'))
  time.sleep(5)
  driver.find_element(By.XPATH, '//*[@id="Arquivos"]/div/table[2]/tbody/tr[2]/th[8]/a').click()
  time.sleep(3)
  dayCienc = driver.find_element(By.XPATH, '//*[@id="Arquivos"]/div/table[2]/tbody/tr[3]/td[8]/font/strong').text
  dayCiencDate = datetime.strptime(dayCienc, "%d/%m/%y")
  searchFile = 0

  try:
    while dayCiencDate <= futureDayDate:
      todayTxt = dayCienc.replace('/','-')
      process = driver.find_element(By.XPATH, '//*[@id="Arquivos"]/div/table[2]/tbody/tr[3]/td[1]/a').text
      driver.switch_to.window(window_BrainLaw)
      campoPesquisaBL = '//*[@id="txtNrProcesso_F"]'
      wait.until(EC.visibility_of_element_located((By.XPATH, campoPesquisaBL)))
      driver.find_element(By.XPATH, campoPesquisaBL).clear()
      driver.find_element(By.XPATH, campoPesquisaBL).send_keys(process)
      hotkey('ctrl','a')
      hotkey('ctrl','c')
      driver.find_element(By.XPATH,'//*[@id="ContentMaster"]/div/div[2]/div[4]/div/div/button').click()
      time.sleep(10)
      try:
        noData = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_ASPxGridViewProcessos_DXEmptyRow"]/td[2]/div').text
        if str(noData).strip() == 'No data to display':
          driver.switch_to.window(window_cadastro)
          driver.find_element(By.XPATH, '//*[@id="btnPublicacoesTcg"]').click()
          wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ListarDadosExtraidosTcg"]/div/div[6]/div/div/div[1]/div/table/tbody')))
          driver.find_element(By.XPATH, '//*[@id="ListarDadosExtraidosTcg"]/div/div[5]/div/table/tbody/tr[2]/td[14]/div/div[2]/div/div/div[1]/input').send_keys(process)
          time.sleep(4)
          processBL = driver.find_element(By.XPATH, '//*[@id="ListarDadosExtraidosTcg"]/div/div[6]/div/div/div[1]/div/table/tbody/tr[1]/td[14]').text
          time.sleep(1)
          driver.find_element(By.XPATH, '//*[@id="btnCancelar_UcPublicacaoTcgGrid"]').click()
          while str(processBL) != str(process):
            if processBL != '':
              time.sleep(1)
            else:
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
              downloadDirectory = f'C:\\Users\\{login}\\Downloads'
              expectedFile = f'{process}.pdf'
              while not os.path.exists(os.path.join(downloadDirectory, expectedFile)):
                time.sleep(1)
              driver.back()
              #realizar o upload
              driver.switch_to.window(window_cadastro)
              driver.find_element(By.XPATH, '//*[@id="btnPreCadastroProcesso"]').click()
              wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="formularioPreCadastroTcg"]/div/div/div/div[4]/div/div/div/div/div/div/div/div[1]/div[1]/div')))
              driver.find_element(By.XPATH, '//*[@id="formularioPreCadastroTcg"]/div/div/div/div[2]/div/div/div/div/div/div/div[1]').click()
              time.sleep(2.5)
              hotkey('down')
              hotkey('down')
              hotkey('enter')
              driver.find_element(By.XPATH, '//*[@id="formularioPreCadastroTcg"]/div/div/div/div[3]/div/div/div/div/div/div[1]').click()
              time.sleep(0.5)
              hotkey('ctrl','v')
              driver.find_element(By.XPATH, '//*[@id="formularioPreCadastroTcg"]/div/div/div/div[4]/div/div/div/div/div/div/div/div[1]/div[1]').click()
              time.sleep(5)
              if searchFile == 0:
                hotkey('shift','tab')
                hotkey('shift','tab')
                count = os.getenv('COUNT_DOWN')
                for _ in range(int(count)):
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
              searchFile += 1 
              #Esperando carregar o arquivo para mandar
              wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="gridArquivosPreCadastroTcg"]/div/div[6]/div/div/div[1]/div/table/tbody/tr[1]/td[2]')))
              i = 0
              while True:
                archProcess = driver.find_element(By.XPATH, '//*[@id="gridArquivosPreCadastroTcg"]/div/div[6]/div/div/div[1]/div/table/tbody/tr[1]/td[2]').text
                nameWhitoutExtension, extension = os.path.splitext(archProcess)
                if nameWhitoutExtension == process:
                  driver.find_element(By.XPATH, '//*[@id="btnGravarPreCadastroTcg"]/div').click()
                  countRegistred += 1
                  break
                elif i < 5:
                  i += 1
                  time.sleep(1)
                  continue
                elif i >= 5:
                  print('Nome do arquivo diferente do número do processo.')
                  createTxt(f'Nome do arquivo diferente do número do processo {process}.', directory, todayTxt) 
                  driver.quit()
                  break
              waitUpload.until(EC.invisibility_of_element_located((By.XPATH,'//*[@id="btnGravarPreCadastroTcg"]/div')))
              time.sleep(5)
              #Botão de quando aparece o OK de processo enviado
              driver.find_element(By.XPATH, '/html/body/div[19]/div/div[3]/button[1]').click()
              time.sleep(2)
              #clicar em visualizar depois de cadastrado
              updatePageProjudi(f'Processo {process} cadastrado via automação.', directory, todayTxt)
              break
            processBL = driver.find_element(By.XPATH, '//*[@id="ListarDadosExtraidosTcg"]/div/div[6]/div/div/div[1]/div/table/tbody/tr[1]/td[14]').text
          if str(processBL) == str(process):
            preRegistred += 1
            updatePageProjudi(f'Processo {process} já está na TCG.', directory, todayTxt)
          dayCienc = driver.find_element(By.XPATH, '//*[@id="Arquivos"]/div/table[2]/tbody/tr[3]/td[8]/font/strong').text
          dayCiencDate = datetime.strptime(dayCienc, "%d/%m/%y")
      except NoSuchElementException:
        updatePageProjudi(f'Processo {process} já cadastrado no BrainLaw.', directory, todayTxt)      
        time.sleep(5)
        dayCienc = driver.find_element(By.XPATH, '//*[@id="Arquivos"]/div/table[2]/tbody/tr[3]/td[8]/font/strong').text
        dayCiencDate = datetime.strptime(dayCienc, "%d/%m/%y")
        countOk += 1
    todayFormat = datetime.strftime(today, "%d/%m/%y")
    if countRegistred + countOk != 0:  
      percentage = (countRegistred / (countRegistred + countOk)) * 100
      percentageRounded = round(percentage,2)
      createTxt(f'Início semana: {todayFormat}\nProcesso já cadastrado: {countOk}\nProcesso cadastrado via automação: {countRegistred}\nProcessos já na TCG: {preRegistred}\nPorcentagem aproveitamento: {percentageRounded}%\n--------------------------------------', directory, 'Resumo semanal')
    else:
      createTxt(f'Início semana: {todayFormat}\nProcesso já cadastrado: {countOk}\nProcesso cadastrado via automação: {countRegistred}\nProcessos já na TCG: {preRegistred}\nPorcentagem aproveitamento: 0%\n--------------------------------------', directory, 'Resumo semanal')
    finish('Processo finalizado.')
    driver.quit()
  except NoSuchElementException:
    finish('Processo não encontrado.')
    driver.quit()
else:
  finish('Login não confirmado.')
  driver.quit()


