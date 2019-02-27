import imaplib
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

connection = imaplib.IMAP4_SSL(config.get('Server', 'Host'))

try:
    connection.login(config.get('Server', 'User'), config.get('Server', 'Pass'))
except:
    print('Login failed.')

print (connection)
connection.logout()