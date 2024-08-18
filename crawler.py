import re
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class Crawler:
  def __init__(self, url_to_crawl, input_name, logs=False, driver=None):
    """_doc_
    Args:
        url_to_crawl (_string_): url to collect data
        input_name (_string_): field element's name to insert the process number
        logs (_bool_, optional): Logs = True, will show performance logs. Defaults to False.
        driver (_webdriver.[DRIVER_], optional): Browser will be used to crawl. Defaults to Chrome Driver.
    """
    if driver is None and logs == False:
      options = ChromeOptions()
      options.add_argument("--log-level=3")  # Ocultar logs de desempenho
      options.add_argument("--disable-logging")  # Desativar logs
      service = ChromeService(log_path='NUL')  # Desativar logs de stacktrace
      driver = webdriver.Chrome(options=options, service=service)
    if driver is None and logs == True:
      driver = webdriver.Chrome()
    self._driver = driver
    self._url_to_crawl = url_to_crawl
    self._input_name = input_name
    self._process_number = None
    self._fields_target = {}
    
  def clean_text(self, text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
    
  def set_process_number(self, process_number):
    self._process_number = process_number

  def set_fields_target(self, fields_target):
    """_summary_

    Args:
        fields_target (['new_field_name', 'element_name', 'element_type']): 
    """
    self._fields_target = {field[0]: (field[1], field[2]) for field in fields_target}
    
  def get_values_by_selector(self):
    # Coletar os valores desejados dos campos
    # Exemplo: coletar o texto de um elemento com id 'result'
    result_text = {}
    page_source = self._driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    
    for field_name, (element_name, by_str) in self._fields_target.items():
      if by_str == 'ID':
        elements = soup.find_all(id=element_name)
      elif by_str == 'CLASS_NAME':
        elements = soup.find_all(class_=element_name)
      else:
        elements = soup.find_all(element_name)

      result_text[field_name] = [self.clean_text(element.get_text()) for element in elements]
    return result_text

  def init(self, peek=False):
    try:
      if (type(self._url_to_crawl) != str):
        raise ValueError("Uma única URL deve ser fornecida e no formato string.")
      # Navegar até a página desejada
      self._driver.get(self._url_to_crawl)

      # Esperar até que o campo de entrada esteja presente
      wait = WebDriverWait(self._driver, 100)
      input_field = wait.until(EC.presence_of_element_located((By.NAME, self._input_name)))

      # Digitar o código no campo de entrada
      input_field.send_keys(self._process_number)

      # Submeter o formulário (ajuste o seletor conforme necessário)
      input_field.send_keys(Keys.RETURN)

      # Esperar até que a página de resultados esteja carregada
      for element_name, by_str in self._fields_target.values():
        by = getattr(By, by_str)
        try:
          if peek:
            logger.debug(f"Waiting for element: {element_name} by {by_str}")
          WebDriverWait(self._driver, 2).until(EC.presence_of_element_located((by, element_name)))
          if peek:
            logger.debug(f"Element {element_name} loaded.")
        except Exception as e:
          logger.error(f"Element {element_name} not found: {e}")
          continue
      if peek:
        logger.debug("Collecting desired values...")
        
      # Coletar os valores desejados
      values = self.get_values_by_selector()
      if peek:
        logger.debug("Values collected:", values)
      return values
    except Exception as e:
      logger.debug(f"An error occurred: {e}")
    finally:
      self._driver.quit()

  