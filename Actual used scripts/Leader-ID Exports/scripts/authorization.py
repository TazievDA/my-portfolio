import json
import requests
import smtplib
import http.client
import selenium.webdriver.support.ui as ui
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from email.mime.text import MIMEText
from email.header import Header

class Auth:

    @staticmethod
    def send_success_email(name, token, ip):
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login('email', 'password')
        message = MIMEText(f'IP: {ip} {name} с токеном {token} только что запросил выгрузку данных пользователей через '
                           f'Leader-ID Export.\nСтатус: успешно.', 'plain', 'utf-8')
        message['Subject'] = Header('Успешная выгрузка контактных данных', 'utf-8')
        smtpObj.sendmail('email', 'email', message.as_string())

    @staticmethod
    def send_failed_email(name, token, ip):
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login('email', 'password')
        message = MIMEText(f'IP: {ip} {name} с токеном {token} только что запросил выгрузку данных пользователей через '
                           f'Leader-ID Export.\nСтатус: ошибка, неверный bearer.', 'plain', 'utf-8')
        message['Subject'] = Header('Неудачная выгрузка контактных данных', 'utf-8')
        smtpObj.sendmail('email', 'email', message.as_string())

    @staticmethod
    def get_ip():
        conn = http.client.HTTPConnection("ifconfig.me")
        conn.request("GET", "/ip")
        return conn.getresponse().read()

    @staticmethod
    def log_in():
        browser = webdriver.Chrome()
        token = ''
        browser.get('https://admin.leader-id.ru/')
        wait = ui.WebDriverWait(browser, 120)
        result = wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'default-layout')))
        browser.get('https://admin.leader-id.ru/events')
        for request in browser.requests:
            if 'api/v4/themes' in request.url:
                if request.response:
                    token = request.headers.get('Authorization')
        browser.close()
        return token

    @staticmethod
    def get_owner_token(org_id, token):
        api_url = 'https://leader-id.ru/api/v4/admin/users/auth'
        headers = {'Content-Type': 'application/json', 'Authorization': f'{token}'}
        data = json.dumps({
            'userId': org_id
        })

        token_response = requests.post(api_url, headers=headers, data=data)
        api_key = token_response.json()['data']['token']
        return api_key