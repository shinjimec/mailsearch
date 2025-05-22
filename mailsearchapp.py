import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import os
import signal

def web_handler(search_term):
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_experimental_option("excludeSwitches", ['enable-automation', 'load-extension'])
    prefs = {
        "credentials_enable_service": False,
        "download_bubble.partial_view_enabled": False,
        "plugins.always_open_pdf_externally": True,
    }
    options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver=browser, timeout=60)

    try:
        url = 'https://secure.xserver.ne.jp/xapanel/login/xbiz/mail/'
        browser.get(url)
        browser.maximize_window()
        browser.find_element(By.ID,'email').send_keys('gomibako@gomec.co.jp')
        browser.find_element(By.ID,'mail_password').send_keys('9SQLnZTqy5')
        browser.find_element(By.XPATH,'//*[@id="login_area"]/div[2]/div/input').click()

        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mailIndex"]/div[1]/section/div[1]/div/ul/li[2]/a')))
        browser.find_element(By.XPATH,'//*[@id="mailIndex"]/div[1]/section/div[1]/div/ul/li[2]/a').click()

        sleep(2)
        handles = browser.window_handles
        browser.switch_to.window(handles[0])
        browser.close()
        browser.switch_to.window(handles[1])

        wait.until(EC.presence_of_element_located((By.XPATH, '//a[@id="searchmenulink"]')))
        browser.find_element(By.XPATH,'//a[@id="searchmenulink"]').click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="s_scope_all"]')))
        browser.find_element(By.XPATH,'//input[@id="s_scope_all"]').click()

        browser.find_element(By.XPATH,'//a[@id="searchmenulink"]').click()
        sleep(1)
        elem_search = browser.find_element(By.ID,'quicksearchbox')
        elem_search.send_keys(search_term)
        sleep(4)
        elem_search.send_keys(Keys.ENTER)

    finally:
        os.kill(browser.service.process.pid, signal.SIGTERM)

st.title('迷惑メール検索ツール')
st.write('検索するワードを入力して[検索]ボタン押してください')
st.write('(例：@smc-card.com)')
st.write('※ワードを指定しない場合はそのまま[検索]ボタンを押してください')
st.write('※GoogleChromeで起動します')

search_term = st.text_input('検索ワード', '')

if st.button('検索'):
    try:
        web_handler(search_term)
        st.success('検索が完了しました。')
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        st.error(traceback.format_exc())
