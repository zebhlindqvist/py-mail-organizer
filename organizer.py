import imaplib
import configparser

def getEmailByAlias(alias):
    return '%s@%s' % (alias[1], domain)

def getFolderByAlias(alias):
    return '%s/%s@%s' % (inbox, alias[1], domain)

config = configparser.ConfigParser()
config.read('settings.ini')
domain = config.get('Server', 'User').split('@')[1]
connection = imaplib.IMAP4_SSL(config.get('Server', 'Host'))
inbox = 'Inbox'

try:
    connection.login(config.get('Server', 'User'), config.get('Server', 'Pass'))
except:
    exit('Login failed.')

aliases = config.items('Aliases')
typ, resp = connection.list(inbox)
if typ != 'OK':
    exit('Folder listing failed.')
folders = str(resp)

for alias in aliases:
    folder = getFolderByAlias(alias)
    if folder.lower() not in folders.lower():
        typ, resp = connection.create(folder)
        print('%s missing on server, creating... %s' % (folder, typ))
        if typ != 'OK':
            exit()

try:
    typ, resp = connection.select(inbox)
    if typ != 'OK':
        raise Exception()
except:
    exit('Failed to select %s.' % inbox)

for alias in aliases:
    email = getEmailByAlias(alias)
    folder = getFolderByAlias(alias)
    msg_ids = ''

    try:
        typ, [resp] = connection.search(None, 'HEADER TO', email)
        if typ != 'OK':
            raise Exception()
        msg_ids = ','.join(resp.decode('utf-8').split(' '))
    except Exception as err:
        exit('Failed to search %s. Err: %s' % (inbox, err))

    if msg_ids != '':
        try:
            typ, resp = connection.copy(msg_ids, folder)
            if typ != 'OK':
                raise Exception()
        except Exception as err:
            exit('Failed to copy messages to %s. Err: %s' % (folder, err))

        try:
            typ, resp = connection.store(msg_ids, '+FLAGS', r'(\Deleted)')
            if typ != 'OK':
                raise Exception()
        except Exception as err:
            exit('Failed to flag messages. Err: %s' % (err))

        try:
            typ, resp = connection.expunge()
            if typ != 'OK':
                raise Exception()
        except Exception as err:
            exit('Failed to expunge messages. Err: %s' % (err))

exit('Finished without errors.')
connection.logout()