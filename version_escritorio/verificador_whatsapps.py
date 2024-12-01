import sys
import pandas as pd
import time

import random
import qrcode
import os

import qrcode.constants
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

from datetime import datetime, timedelta

class VerificarWhatsApp:
  
  def __init__(self):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        driver_path = os.path.join(script_dir, "msedgedriver.exe")
        if not os.path.isfile(driver_path):
            print(f"Error: El driver 'msedgedriver.exe' no se encuentra en {script_dir}.")
            print("Por favor asegúrese de que el driver esté en la misma carpeta que el script de Python.")
            sys.exit()

        service = Service(executable_path = driver_path)
        options = webdriver.EdgeOptions()
        options.add_argument("--verbose")
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("--window-size=1920, 1200")
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Edge(service=service, options=options)
        self.file_path = os.path.join(script_dir, "base.csv")
        if not os.path.isfile(self.file_path):
            print(f"Error: El archivo '{'base.csv'}' no se encuentra.")
            print("Por favor asegúrese de que el archivo esté en la misma carpeta que el script de Python.")
            sys.exit()

        self.base = pd.read_csv(self.file_path)

        columnas_archivo = self.base.columns.tolist()
        columnas_esperadas = ["Móvil", "Está en Whatsapp?", "Fecha"]

        if columnas_archivo != columnas_esperadas:
            print("Las columnas no coinciden con las esperadas.")
            print(f"Columnas encontradas: {columnas_archivo}")
            print(f"Columnas esperadas: {columnas_esperadas}")
            sys.exit()

        self.base['Fecha'] = self.base['Fecha'] = pd.to_datetime(self.base['Fecha'], errors='coerce')
    except Exception as e:
      print(f'Error: {e}')
      sys.exit()

  def get_qr(self,i):
    if (i<6):
      self.driver.get('https://web.whatsapp.com')
      try:
        time.sleep(6)
        element = self.driver.find_element(By.CLASS_NAME, "_akau.x1n2onr6.x78zum5.x1okw0bk.x6s0dn4.xl56j7k.x1tdqgrh.x1l76qip.x6ikm8r.x10wlt62.xm3z3ea.x1x8b98j.x131883w.x16mih1h")
        data_ref_value = element.get_attribute('data-ref')

        qr = qrcode.QRCode(
          version=1,
          error_correction=qrcode.constants.ERROR_CORRECT_L,
          box_size=1,
          border=10,
        )
        qr.add_data(data_ref_value)
        qr.make(fit=True)
        qr_terminal = qr.get_matrix()
        qr = []
        for j in range(0, len(qr_terminal), 2):
          new_row = []
          if j + 1 < len(qr_terminal):
            for z in range(len(qr_terminal[0])):
              new_row.append(f"{qr_terminal[j][z]},{qr_terminal[j+1][z]}")
          else:
            for z in range(len(qr_terminal[0])):
              new_row.append(f"{qr_terminal[j][z]},False")
          qr.append(new_row)

        print(f"Escanea el QR para empezar el proceso. Intento {i}/5.")
        for row in qr:
          print("".join(['▀' if col == "True,False" else 
                   ("█" if col == "True,True" else 
                    ("▄" if col == "False,True" else " ")) 
                   for col in row]))
        if self.is_loggin():
          print("Sesion iniciada con éxito.")
        else:
          self.get_qr(i+1)
      except Exception as e:
        if self.is_loggin():
          print("Sesion iniciada con éxito.")
          print("Iniciando proceso...")
        else:
          self.get_qr(i+1)
    else:
      print("No se pudo iniciar la sesión.")
      sys.exit()

  def is_loggin(self):
    try:
      time.sleep(5)
      element = self.driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[1]')
      if element.text == "Search" or element.text == "Buscar":
        return True
      else:
        return False
    except Exception as e:
      return False

  def number_check(self):
    time.sleep(2)
    print("Procesando números de WhatsApp, esto tomará un tiempo... \n")
    url_izquierda = 'https://web.whatsapp.com/send/?phone=%2B'
    url_derecha = '&text&type=phone_number&app_absent=0'

    for index,row in self.base.iterrows():
      i = row['Móvil']
      fecha = row['Fecha']
      tiene = row['Está en Whatsapp?']
      hoy = datetime.now()
      limite = hoy - timedelta(weeks=52/2)

      if fecha<limite or tiene == "Error" or tiene == "" or pd.isnull(fecha):
        url = url_izquierda + str(i).replace("+","").replace(" ","") + url_derecha
        self.driver.get(url)
        time.sleep(random.uniform(7, 9))
        self.base.at[index, 'Fecha'] = hoy
        resultado = self.exist(1)
        if "," in resultado:
          resultado = resultado.split(",")
          self.base.at[index, 'Está en Whatsapp?'] = resultado[0]
          self.base.at[index, 'Móvil'] = resultado[1].replace(" ","").replace("(","").replace(")","").replace("-","")
        else:
          self.base.at[index, 'Móvil'] = str(i).replace(" ", "")
          self.base.at[index, 'Está en Whatsapp?'] = resultado

    self.base.to_csv(self.file_path, index=False)
    print("Finalizando proceso, espera a que se cierre la sesión.")

  def exist(self, i):
    if (i<3):
      text1 = "El número de teléfono compartido a través de la dirección URL no es válido."
      text2 = "The phone number shared via the URL is invalid."
      text3 = "Write a message"
      text4 = "Escribe un mensaje"
      text5 = "Buscar"
      text6 = "Search"
      try:
        element = None
        element2 = None
        try:
          element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{text1}') or contains(text(), '{text2}')]")
        except:
          element2 = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{text3}') or contains(text(), '{text4}') or contains(text(), '{text5}') or contains(text(), '{text6}')]")
        if element is not None:
          return "No"
        elif element2 is not None:
          '''script = """
                    var phoneNumber = document.getElementsByClassName("_amid")[0]
                                          .getElementsByTagName("span")[0]
                                          .textContent;
                    return phoneNumber;
                    """
          time.sleep(2)
          number = self.driver.execute_script(script)
          if "+" in number:
            return "Si,"+number
          else:
            time.sleep(1)
            number = self.driver.execute_script(script)
            return "Si,"+number
            if "+" in number:
              time.sleep(1)
              return self.exist(i+1)'''
          return "Si"
        else:
          time.sleep(2)
          return self.exist(i+1)
      except Exception as e:
        print(f"Error {e}")
        time.sleep(2)
        return self.exist(i+1)
    else:
      return "Error"

  def logout(self):
    try:
      logout_button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[3]/div[3]/header/header/div/span/div/span/div[2]/span/div/ul/li[5]")
      logout_button.click()
      time.sleep(2)
      logout_button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/span[2]/div/div/div/div/div/div/div[2]/div/button[2]")
      logout_button.click()
      time.sleep(8)
      print("Se cerro la sesión correctamente.")
      self.driver.quit()
    except Exception as e:
      print("Error al hacer clic en el botón de 'Cerrar sesión':", e)

  def open_menu(self):
    self.driver.get('https://web.whatsapp.com')
    time.sleep(8)
    try:
      menu_button =  self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[3]/div[3]/header/header/div/span/div/span/div[2]/div")
      menu_button.click()
    except Exception as e:
      print("Error al hacer clic en el botón de menú:", e)

scrape = VerificarWhatsApp()
scrape.get_qr(1)
scrape.number_check()
scrape.open_menu()
scrape.logout()
scrape.driver.quit()