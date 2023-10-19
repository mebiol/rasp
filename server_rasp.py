import netifaces as ni

ip = 'wlan0'
#ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['wlan0']
if ip in ni.interfaces():
	name = ni.ifaddresses(ip).get(ni.AF_INET)
	if name:
		ip_address = ip[0]['addr']
		print(ip_address)
	else:
		print(f"no ip found{ip}")
else:
	print(f"interface{ip} not found on system")
