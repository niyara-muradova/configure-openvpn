import pexpect
from pexpect import pxssh
import logging

LOGS = 'actions.log'
logging.basicConfig(filename='actions.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)


def __create_files():
    return


if __name__ == '__main__':
    try:
        s = pxssh.pxssh()
        hostname = 'local.com'
        username = 'terminal'
        password = '0123'
        if s.login(hostname, username, password, port=33022):
            logging.info(f'Successful login to {username}@{hostname}')

    except pxssh.ExceptionPxssh as e:
        logging.exception(f'Failed login to {username}@{hostname}')


# creates txt file
# with open('client_address.txt', 'w') as f:
#     for i in range(1, 60):
#         num = 200+i
#         ip = i*4+2
#         f.write(f'client-{str(num)},10.10.1.{str(ip)} \n')
