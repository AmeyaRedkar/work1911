import paramiko
from configparser import ConfigParser

config=ConfigParser()
config.read("C:\\Users\\appam\\Desktop\\work1911\\configuration.txt")
ip=config["paramiko"]["ip"]
user=config["paramiko"]["username"]
passwd=config["paramiko"]["password"]
time=config["paramiko"]["time"]


session=paramiko.SSHClient()

session.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())

session.connect(ip, username = user, password = passwd,timeout=int(time))

stdin, stdout, stderr = session.exec_command(#insert commands here)

output=stdout.readlines()

for x in output:
	print "/n {} /n".format(x)