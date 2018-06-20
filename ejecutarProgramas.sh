#!/bin/bash


######## MAtamos a los programas  #########
sudo kill `ps aux| grep capture_data_IQ.py | awk 'NR==1{print $2}'|tr -d '\n'` ;
sudo kill `ps aux| grep send_data_final.py | awk 'NR==1{print $2}'|tr -d '\n'` ;

#sudo ifconfig eth0 192.168.2.1
#sudo sysctl vm.drop_caches=3 &

####### comprobamos conexion ##########

python ~/bin/detectarConexion.py --interface ttyUSB2 --conexion gsm-ttyUSB2 ; 

####### Ejecutamos los programas ########
echo ejecutar Programas:  `date` >> /home/pi/log/log.log &
python ~/client/capture_data_IQ.py >> ~/log/capture_data_IQ.log &
python ~/client/send_data_final.py >> ~/log/send_data_final.log &

