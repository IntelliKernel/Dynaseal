import os
import smtplib
from email.mime.text import MIMEText

def send_email(smtp_server, port, username, password, sender_email, receiver_email, subject, content):
    # 邮件内容
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # 连接SMTP服务器并发送邮件
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()  # 如果服务器需要使用TLS
    server.login(username, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

# 使用示例
smtp_server = os.environ.get('SMTP_SERVER')
port = os.environ.get('SMTP_PORT')
username = os.environ.get('SMTP_USERNAME')
password = os.environ.get('SMTP_PASSWORD')

if __name__ == '__main__':

    sender_email = "noreply@thisis.plus"
    receiver_email = '3046308220@qq.com'
    subject = '邮件主题'
    content = '这是邮件内容'

    send_email(smtp_server, port, username, password, sender_email, receiver_email, subject, content)