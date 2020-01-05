import datetime
import json
import dropbox
import paramiko


def get_data(host, port, usr, pwd):
    """Return the content of the backup from given router."""
    content = ''
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)
        client.connect(host, port, usr, pwd, timeout=1)
        _, stdout, __ = client.exec_command('export compact')
        content = stdout.read()
    finally:
        client.close()
        return content


def save_into_dropbox(backup, file_name, dbx_key):
    """Save the given content into dropbox."""
    file_to_upload = backup
    dbx = dropbox.Dropbox(dbx_key)
    try:
        dbx.files_upload(file_to_upload,
                         file_name,
                         dropbox.files.WriteMode.add)
        return True
    except Exception as err:
        print(err)
        return False


def main():
    """Read config.json file, get data and then upload into dropbox."""
    with open('config.json') as config_file:
        config = json.load(config_file)
        dbx_key = config['dropboxKey']
        for router in config['routers']:
            backup = get_data(router['host'],
                            router['port'],
                            router['usr'],
                            router['pwd'])
            if backup ==  '':
                print('Could not get the router backup from '
                     + router['name'])
            else:
                current_date = datetime.datetime \
                                       .now() \
                                       .strftime('%d-%m-%Y %H-%M')
                file_name = '/' + router['name'] +' ' + current_date + '.txt'
                if save_into_dropbox(backup, file_name, dbx_key):
                    print(file_name[1:] + ' saved into dropbox.')
                else:
                    print('Could not save ' + file_name[1:] + ' into dropbox.')


if __name__ == '__main__':
    main()