'''
    practica1.py
    Muestra el tiempo de llegada de los primeros 50 paquetes a la interfaz especificada
    como argumento y los vuelca a traza nueva con tiempo actual

    Autor: Javier Ramos <javier.ramos@uam.es>
    2020 EPS-UAM
    
    Autores: Iker Perez Villa, Lucia Pereira Menchero
'''

from rc1_pcap import *
import sys
import binascii
import signal
import argparse
from argparse import RawTextHelpFormatter
import time
import logging

ETH_FRAME_MAX = 1514
PROMISC = 1
NO_PROMISC = 0
TO_MS = 10
num_paquete = 0
pdump = None
pdumpARP = None
TIME_OFFSET = 45*60


def signal_handler(nsignal,frame):
	logging.info('Control C pulsado')
	if handle:
		pcap_breakloop(handle)
		

def procesa_paquete(us,header,data):
	global num_paquete
	global pdump
	global pdumpARP

	logging.info('Nuevo paquete de {} bytes capturado en el timestamp UNIX {}.{}'.format(header.len, header.ts.tv_sec, header.ts.tv_sec))
	# Modificar tiempo de captura
	header.ts.tv_sec += TIME_OFFSET
	logging.info('Nuevo paquete de {} bytes capturado en el timestamp UNIX MODIFICADO {}.{}'.format(header.len, header.ts.tv_sec, header.ts.tv_sec))

	# Actualizar num de paquetes
	num_paquete += 1
	# Imprimir los N primeros bytes
	fin = 0
	if args.nbytes > len(data):
		fin = len(data)
	else:
		fin = args.nbytes
	for i in range(0, fin, 2):
		if i == len(data)-1:
			print(hex(data[i]), end = '')
			break
		print(hex(data[i]),hex(data[i+1]), ' ', end = '')
	# Salto de linea
	print("")
	if args.interface is not False:
		# Escribir el trafico al fichero de captura con el offset temporal
		if data[12] == '0x08' and data[13] == '0x06':
			pcap_dump(pdumpARP, header, data)
		else:
			pcap_dump(pdump, header, data)
	
if __name__ == "__main__":
	global args, handle
	parser = argparse.ArgumentParser(description='Captura trafico de una interfaz ( o lee de fichero) y muestra la longitud y timestamp de los 50 primeros paquetes',formatter_class=RawTextHelpFormatter)
	parser.add_argument('--file', dest='tracefile', default=False,help='Fichero pcap a abrir')
	parser.add_argument('--itf', dest='interface', default=False,help='Interfaz a abrir')
	parser.add_argument('--nbytes', dest='nbytes', type=int, default=14,help='Numero de bytes a mostrar por paquete')
	parser.add_argument('--debug', dest='debug', default=False, action='store_true',help='Activar Debug messages')
	parser.add_argument('--npkts', dest='npkts', type=int, default=-1, help='Numero de paquetes a procesar')
	args = parser.parse_args()

	if args.debug:
		logging.basicConfig(level = logging.DEBUG, format = '[%(asctime)s %(levelname)s]\t%(message)s')
	else:
		logging.basicConfig(level = logging.INFO, format = '[%(asctime)s %(levelname)s]\t%(message)s')

	if args.tracefile is False and args.interface is False:
		logging.error('No se ha especificado interfaz ni fichero')
		parser.print_help()
		sys.exit(-1)

	signal.signal(signal.SIGINT, signal_handler)

	errbuf = bytearray()
	handle = None

	if args.interface is not False:
		print(args.interface)
		# Abrir la interfaz especificada para captura o la traza
		handle = pcap_open_live(args.interface, ETH_FRAME_MAX, NO_PROMISC, 100, errbuf)
		if handle is None:
			logging.error('Error al abrir la traza {}: {}'.format(args.interface, errbuf))

		# Abrir un dumper para volcar el trafico
		descr = pcap_open_dead(DLT_EN10MB, ETH_FRAME_MAX)
		fecha = time.time()
		pdumpARP = pcap_dump_open(descr, 'capturaARP'+ args.interface + str(fecha) + '.pcap')
		if pdumpARP is None:
			logging.error('Error al abrir el dumperARP')
		pdump = pcap_dump_open(descr,'captura'+ args.interface + str(fecha) + '.pcap')
		if pdump is None:
			logging.error('Error al abrir el dumper')

	elif args.tracefile is not False:
		# Abrir traza ya capturada
		handle = pcap_open_offline(args.tracefile, errbuf)
		if handle is None:
			logging.error('Error al abrir la traza {}: {}'.format(args.tracefile, errbuf))

	# Leer trafico
	ret = pcap_loop(handle, args.npkts, procesa_paquete, None)
	if ret == -1:
		logging.error('Error al capturar un paquete')
	elif ret == -2:
		logging.debug('pcap_breakloop() llamado')
	elif ret == 0:
		logging.debug('No mas paquetes o limite superado')
	# Mostrar num de paquetes recibidos
	logging.info('{} paquetes procesados'.format(num_paquete))

	# Cerrar dumpers creados
	if pdumpARP is not None and pdump is not None:
		pcap_dump_close(pdump)
		pcap_dump_close(pdumpARP)
