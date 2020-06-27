import pexpect
import logging
import re
import os

# creating logging file
LOGS = 'actions.log'
logging.basicConfig(filename='actions.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)
__pass = '0123'

# checking for available address
def get_client_list():
    logging.info('Get available client number from client_address.txt')

    try:

        with open('client_address.txt', 'r') as f:
            lines = f.readlines()

        for line in lines:
            global li_array
            li_array = line.split(',')
            available_address = None

            if len(li_array) < 3:
                available_address = li_array[0]
                logging.info(f"Found available ip-address at {li_array}")
                break

        if available_address is None:
            logging.info('No available addresses\n Process finished')
        else:
            cp_server_cert(available_address)

    except:
        logging.exception(Exception)


# copying ready certificate from the server
def cp_server_cert(available_address):
    logging.info('Starting copying certificate...')
    try:
        logging.info('scp command execution')

        session = pexpect.spawn(
            f'scp -P 33022 local.com:~/ccd-1/{available_address}.zip /home/niyara/test')
        session.expect("local.com's password:")
        session.sendline(__pass)
        session.expect(pexpect.EOF)

        show_output = session.before.decode('utf-8')
        logging.info(show_output)

        logging.info('Finished command execution')
        session.close()

        set_terminal_cert(available_address)

    except:
        logging.exception(Exception)


# unzipping and setting the certificate
def set_terminal_cert(available_address):
    try:
        logging.info('Starting unzip...')
        unzip_command = f'unzip -l -n /home/niyara/test/{available_address}.zip -d /home/niyara/test/{available_address}'
        session = pexpect.spawn(unzip_command)
        session.expect(pexpect.EOF)

        show_output = session.before.decode('utf-8')
        logging.info(show_output)

        session.close()
        logging.info('Unzip finished')

        set_new_config(available_address)

    except:
        logging.exception(Exception)


# changing configuration files in the terminal
def set_new_config(available_address):
    logging.info('Editing configurations in start_vpn file...')
    file_dir = '/home/niyara/test/new'

    try:
        with open(file_dir, 'rt') as f:
            file_str = f.read()
            replace = re.subn('client-[0-9]*', available_address, file_str)

            if replace[1] > 0:
                logging.info(f'Found {replace[1]} matching substring(s) and replaced with "{available_address}"')
            else:
                logging.info('No matching strings found')

            system_check()

    except:
        logging.exception(Exception)


# checking if changes are applied
def system_check():
    try:
        logging.info('Restarting OpenVPN service')

        os.popen('systemctl restart openvpn')
        status_openvpn = os.popen('systemctl status openvpn')

        logging.info(status_openvpn)
        logging.info('Restart complete')

        logging.info('Ping to server...')

        ping10 = os.popen('ping -c 1 10.10.1.1')
        ping100 = os.open('ping -c 1 100.100.1.1')

        if ping10==0:
            logging.info('Connection established 10.10.1.1')
        else:
            logging.error('No connection to server 10.10.1.1')

        resp = os.popen('ifconfig').read().split('\n')

        # searching tun0 address which identifies vpn address assigned to the device
        tun_idx = [i for i, item in enumerate(resp) if re.search('tun0:.*', item)]
        tun_idx = int(tun_idx[0])
        inet_idx = [i for i, item in enumerate(resp) if re.search('inet .*', item)]

        for idx in inet_idx:
            if idx > tun_idx:
                ip = resp[idx]
                ip = re.search('(?<=inet)(.*)(?=netmask)', ip).group(0).strip()

        if ip is li_array[1]:
            logging.info(f'Assigned ip-address {ip}')
        else:
            logging.error(f'Not matching ip-addresses\n On client_address -> {li_array[1]}\n current -> {ip}')


    except:
        logging.exception(Exception)


def mark_taken(available_address, ):
    return


if __name__ == '__main__':
    get_client_list()