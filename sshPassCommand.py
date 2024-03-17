#!usr/bin/python

# This program is written by Venujan Malaiyandi
# Lets connect -> https://www.linkedin.com/in/venujan-malaiyandi-924381227/

import pexpect

PROMPT = ['# ', '>>> ', '> ', '\$ ']


# This command attempts to connect with the host via ssh
# And if successfull, returns the connection
# Parameters : username of the host, ip of the host, password of the host
def connect(username,ip,credential):
	ssh_newkey = 'Are you sure you want to continue connecting'
	connection_string = 'ssh ' + username + '@' + ip
	child = pexpect.spawn(connection_string)
	return_result = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword: '])
	if return_result == 0:
		print ('[-] Error Connecting via SSH')
		return
	if return_result == 1:
		child.sendline('yes')
		return_result = child.expect([pexpect.TIMEOUT,'[P|p]assword: '])
		if return_result == 0:
			print("[-] Error Connecting")
			return
	child.sendline(credential)
	child.expect(PROMPT)
	return child 

# Formats outputs for better visibility
def format_output(output):
    output = output.decode().lstrip('b')
    output = output.replace('\r', '').replace('\n', '')
    commands = output.split(';')
    for command_output in commands:
        print(command_output)

# Sends the commands passed via the params
# Params: connection, commands that you want to pass
def sendCommand(shell, command):
	shell.sendline(command)
	shell.expect(PROMPT)
	format_output(shell.before)

# Main function
def startMain():
	host = input('[*] Enter target host: ') 
	user = input('[*] Enter target user: ') 
	password =input('[*] Enter password: ') 
	child_shell = connect(user,host,password)
	sendCommand(child_shell, 'cat /etc/shadow | grep root;ps') # Change the commands passed to your needs 

# Main
startMain()
