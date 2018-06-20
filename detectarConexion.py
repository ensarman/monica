#!/usr/bin/python

import subprocess
from os.path import expanduser
import urllib2
from time import strftime, sleep
import argparse # para recibir parametros por cli

class detector():
	
	homeDir="/home/pi"
	log = ""
	tiempo = ""
	interface = ""
	conexion = "gsm-ttyUSB2"
	delay=5 #tiempo entre la conexion y la siguiente prueba
	
	def __init__(self, log="/home/pi/log/detectarConexion.log", interface="ttyUSB2", conexion="gsm-ttyUSB2"):
		self.log = log
		self.tiempo = strftime('%Y-%m-%d %H:%M:%S')
		self.interface=interface
		self.conexion=conexion
	
	def internet_on(self):
		try:
			#urllib2.urlopen('http://monicaresidual.com/mainPage.html', timeout=3)
			urllib2.urlopen('http://google.com', timeout=3)
			return True
		except urllib2.URLError as err: 
			return False
		except urllib2.socket.timeout as timeout:			
			self.escribirlog("se supero el tiempo de espera")
			return False
	
	def nm_up(self):
		estado = subprocess.check_output(
			"nmcli dev  status  |grep " + self.interface + " | awk '{print $3}' |tr -d '\n'"
			,shell=True)
		log = "el estado es: " + estado + "\n"
		if estado == "conectado":
			self.escribirlog(log + "no se hace nada")
			return True
		else:
			self.escribirlog(log + "El estado de Network Manager es:")
			self.escribirlog(
				subprocess.check_output(
					"nmcli device status",
					shell=True
				)
			)
			return False
	
	def nm_restart(self): #reinicia los procesos de Network Manager y Modem Manager
		self.escribirlog("reiniciando los procesos de Network Manager y Modem Manager")
		subprocess.call("sudo systemctl stop ModemManager.service NetworkManager.service", shell=True)
		sleep(2)
		subprocess.call("sudo systemctl start ModemManager.service NetworkManager.service", shell=True)
		sleep(2)
	
	def detectarUptime(self):
		uptime = 0.0
		with open("/proc/uptime", "r") as f:
			uptime = float(f.readline().split()[0])
		return uptime
	
	def escribirlog(self, txt):
		with open(self.log, 'a') as f: 
			linealog = txt + "\n"
			f.write(linealog)
	
	def getlogfile(self):
		return self.log
            
    
	def detectar(self):
		self.escribirlog('**********************************************')
		self.escribirlog(strftime('%Y-%m-%d %H:%M:%S'))
		self.escribirlog("Probando Operatividad del modem")
		
		# si el uptime es menor a 20 segundos no hacer la prueba
		if self.detectarUptime()<30.0:
			self.escribirlog("tiempo encendido insuficinte para hacer pruebas")
			return True
		else:
			if not self.nm_up():
				self.escribirlog("intentando reconectar via Network manager")
				self.nm_restart()
				log_reconexion = ""
				try:				
					log_reconexion=subprocess.check_output(
						"nmcli connection up "+ self.conexion,
						shell=True)
					log_reconexion = "reconectado satisfactoriamente"
				except Exception as ex:
					log_reconexion =  "el error es: " + str(ex) + "\n"
					log_reconexion += "no hay la interface indicada: "+self.interface
				
				sleep(self.delay)
				self.escribirlog(log_reconexion)

				
		
		self.escribirlog(strftime('%Y-%m-%d %H:%M:%S'))
		self.escribirlog("Probando desde conectividad a internet")
		
		if self.internet_on():
			self.escribirlog( 'hay internet no se hace nada')
		else:
			self.escribirlog('no hay internet')
			#subprocess.call("sudo reboot", shell=True)
			return False
		
		return  True
		    

parser = argparse.ArgumentParser(
			description="verifica si hay conexion y escrbe en log")
parser.add_argument('--log',  type=str, dest = "log", default = expanduser("~")+"/log/detectarConexion.log",
					help = "ubicacion del log")
parser.add_argument('--interface',  type=str, dest = "interface", default = "eth0",
					help = "Nombre de la Interface en linux")
parser.add_argument('--conexion',  type=str, dest = "conexion", default = "dhcp-eth0",
					help = "Nombre de la Conexion de Network Manager")
					

resultado = parser.parse_args()

#print (resultado.log)

detect = detector(log=resultado.log, interface=resultado.interface, conexion=resultado.conexion )
#detect.internet_on()
detect.detectar()

