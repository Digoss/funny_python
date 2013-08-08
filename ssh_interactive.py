import pexpect
import argparse

PROMPT = ['#', '>>>', '>', '\$']

def argParseFunction():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="specify the user to connect", required=True)
    parser.add_argument("-p", "--password", help="specify the password to connect", required=True)
    parser.add_argument("-H", "--host", help="specify the host to connect", required=True)
    return parser.parse_args()

def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print child.before

def connect(user, host, password):
    ssh_newkey = 'Are you sure you want to continuse connectiong'
    connStr = 'ssh '+ user+ '@'+host
    child = pexpect.spawn(connStr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    if ret == 0:
        print '[-] Error Connecting'
        return
    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
    if ret == 0:
        print '[-] Error Connecting'
        return
    child.sendline(password)
    return child

def main():
    args = argParseFunction()
    child = connect(args.user, args.host, args.password)
    send_command(child, 'rm ashk')

if __name__ == '__main__':
    main()