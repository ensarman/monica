#!/usr/bin/python

from time import sleep, strftime, localtime
import subprocess
from detectarConexion import detector


class ejecucion:
    delay = 0
    programas = []
    procesos = []
    log = ""

    def __init__(self, *progs):
        self.delay = 1
        self.programas = progs
        self.procesos = []
        self.log = "/home/pi/log/exec.log"

    def set_delay(self, delay):
        self.delay = delay

    def ejecutar(self):
        for programa in self.programas:
            self.procesos.append(subprocess.Popen(programa))

    def matar(self):
        for proceso in self.procesos:
            proceso.kill()

    def detectar_conexion(self):
        conexion = detector(log="/home/pi/log/detectarConexion.log",
                            interface="ttyUSB2",
                            conexion="gsm-ttyUSB2")
        self.escribirlog("Detectando conexion, log en: "
                         + conexion.getlogfile())
        if conexion.detectar():
            return True
        else:
            return False

    def escribirlog(self, txt):
        with open(self.log, 'a') as f:
            linealog = txt + "\n"
            f.write(linealog)

    def ejecutar_siempre(self):
        while True:
            sleep(1)  # cada segundo se detiene a hacer lo siguiente
            if localtime().tm_min % self.delay == 0:
                if localtime().tm_sec == 0:
                    self.escribirlog("************ " +
                                     strftime('%Y-%m-%d %H:%M:%S') +
                                     "  ***************")
                    if self.detectar_conexion():
                        self.ejecutar()
                        self.escribirlog("se ejcutaron los programas")
                        sleep(40)
                        self.matar()
                        self.escribirlog("se mataron los programas")
                    else:
                        self.escribirlog("sin conexion Reiniciando")
                        subprocess.call("sudo reboot", shell=True)


ejec = ejecucion("/home/pi/client/capture_data_IQ.py",
                 "/home/pi/client/send_data_final.py")
ejec.set_delay(1)  # Aqui definimos el tiempo de las repeticiones, en minutos

ejec.ejecutar_siempre()
