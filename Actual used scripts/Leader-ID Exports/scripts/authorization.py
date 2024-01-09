import requests
import smtplib
import http.client
import json
from email.mime.text import MIMEText
from email.header import Header


class Auth:
    @staticmethod
    def pre_auth(token):
        headers = {'Authorization': f'Bearer {token}'}
        params = {'id': 292338}
        url = 'https://leader-id.ru/api/v4/admin/users'
        response = requests.get(url, params=params, headers=headers)
        return response.status_code

    @staticmethod
    def send_success_email(name, token, ip):
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login('xxxx@xxx.xxx', 'password')
        message = MIMEText(f'IP: {ip} {name} с токеном {token} только что запросил выгрузку данных пользователей через '
                           f'Leader-ID Export.\nСтатус: успешно.', 'plain', 'utf-8')
        message['Subject'] = Header('Успешная выгрузка контактных данных', 'utf-8')
        smtpObj.sendmail('xxxx@xxxx.xxx', 'xxxx@xxxx.xxx', message.as_string())

    @staticmethod
    def send_failed_email(name, token, ip):
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login('xxxx@xxx.xxx', 'password')
        message = MIMEText(f'IP: {ip} {name} с токеном {token} только что запросил выгрузку данных пользователей через '
                           f'Leader-ID Export.\nСтатус: ошибка, неверный bearer.', 'plain', 'utf-8')
        message['Subject'] = Header('Неудачная выгрузка контактных данных', 'utf-8')
        smtpObj.sendmail('xxxx@xxxx.xxx', 'xxxx@xxxx.xxx', message.as_string())

    def get_ip(self):
        conn = http.client.HTTPConnection("ifconfig.me")
        conn.request("GET", "/ip")
        return conn.getresponse().read().decode()

    @staticmethod
    def get_api_key() -> object:
        api_url = 'https://leader-id.ru/api/v4/auth/refresh-token'
        data = {
            'refreshToken': 'refresh_token'
        }
        refresh_response = requests.post(api_url, json=data)
        api_key = refresh_response.json()['data']['access_token']
        return api_key

    @staticmethod
    def get_owner_token(org_id):
        api_key = Auth.get_api_key()
        api_url = 'https://leader-id.ru/api/v4/admin/users/auth'
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'}
        data = json.dumps({
            'userId': org_id
        })

        token_response = requests.post(api_url, headers=headers, data=data)
        token = token_response.json()['data']['token']
        return token
