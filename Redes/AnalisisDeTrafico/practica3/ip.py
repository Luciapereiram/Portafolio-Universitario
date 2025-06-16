'''
    ip.py

    Funciones necesarias para implementar el nivel IP
    Autor: Javier Ramos <javier.ramos@uam.es>
    2022 EPS-UAM
'''
from math import *
from ethernet import *
from arp import *
from fcntl import ioctl
import subprocess
SIOCGIFMTU = 0x8921
SIOCGIFNETMASK = 0x891b
#Diccionario de protocolos. Las claves con los valores numéricos de protocolos de nivel superior a IP
#por ejemplo (1, 6 o 17) y los valores son los nombres de las funciones de callback a ejecutar.
protocols={}
#Tamaño mínimo de la cabecera IP
IP_MIN_HLEN = 20
#Tamaño máximo de la cabecera IP
IP_MAX_HLEN = 60
def chksum(msg):
    '''
        Nombre: chksum
        Descripción: Esta función calcula el checksum IP sobre unos datos de entrada dados (msg)
        Argumentos:
            -msg: array de bytes con el contenido sobre el que se calculará el checksum
        Retorno: Entero de 16 bits con el resultado del checksum en ORDEN DE RED
    '''
    s = 0
    y = 0x27af
    for i in range(0, len(msg), 2):
        if (i+1) < len(msg):
            a = msg[i]
            b = msg[i+1]
            s = s + (a+(b << 8))
        elif (i+1)==len(msg):
            s += msg[i]
        else:
            raise 'Error calculando el checksum'
    y = y & 0x00ff
    s = s + (s >> 16)
    s = ~s & 0xffff
    return s

def getMTU(interface):
    '''
        Nombre: getMTU
        Descripción: Esta función obteiene la MTU para un interfaz dada
        Argumentos:
            -interface: cadena con el nombre la interfaz sobre la que consultar la MTU
        Retorno: Entero con el valor de la MTU para la interfaz especificada
    '''
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    ifr = struct.pack('16sH', interface.encode("utf-8"), 0)
    mtu = struct.unpack('16sH', ioctl(s,SIOCGIFMTU, ifr))[1]

    s.close()

    return mtu

def getNetmask(interface):
    '''
        Nombre: getNetmask
        Descripción: Esta función obteiene la máscara de red asignada a una interfaz
        Argumentos:
            -interface: cadena con el nombre la interfaz sobre la que consultar la máscara
        Retorno: Entero de 32 bits con el valor de la máscara de red
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = fcntl.ioctl(
        s.fileno(),
       SIOCGIFNETMASK,
        struct.pack('256s', (interface[:15].encode('utf-8')))
    )[20:24]
    s.close()
    return struct.unpack('!I',ip)[0]


def getDefaultGW(interface):
    '''
        Nombre: getDefaultGW
        Descripción: Esta función obteiene el gateway por defecto para una interfaz dada
        Argumentos:
            -interface: cadena con el nombre la interfaz sobre la que consultar el gateway
        Retorno: Entero de 32 bits con la IP del gateway
    '''
    p = subprocess.Popen(['ip r | grep default | awk \'{print $3}\''], stdout=subprocess.PIPE, shell=True)
    dfw = p.stdout.read().decode('utf-8')
    print(dfw)
    return struct.unpack('!I',socket.inet_aton(dfw))[0]



def process_IP_datagram(us,header,data,srcMac):
    '''
        Nombre: process_IP_datagram
        Descripción: Esta función procesa datagramas IP recibidos.
            Se ejecuta una vez por cada trama Ethernet recibida con Ethertype 0x0800
            Esta función debe realizar, al menos, las siguientes tareas:
                -Extraer los campos de la cabecera IP (includa la longitud de la cabecera)
                -Calcular el checksum y comprobar que es correcto
                -Analizar los bits de de MF y el offset. Si el offset tiene un valor != 0 dejar de procesar el datagrama (no vamos a reensamblar)
                -Loggear (usando logging.debug) el valor de los siguientes campos:
                    -Longitud de la cabecera IP
                    -IPID
                    -TTL
                    -Valor de las banderas DF y MF
                    -Valor de offset
                    -IP origen y destino
                    -Protocolo
                -Comprobar si tenemos registrada una función de callback de nivel superior consultando el diccionario protocols y usando como
                clave el valor del campo protocolo del datagrama IP.
                    -En caso de que haya una función de nivel superior registrada, debe llamarse a dicha funciñón
                    pasando los datos (payload) contenidos en el datagrama IP.

        Argumentos:
            -us: Datos de usuario pasados desde la llamada de pcap_loop. En nuestro caso será None
            -header: cabecera pcap_pktheader
            -data: array de bytes con el contenido del datagrama IP
            -srcMac: MAC origen de la trama Ethernet que se ha recibido
        Retorno: Ninguno
    '''
    version = (data[0] & 0xf0) >> 4
    ihl = (data[0] & 0x0f)
    # Tam cabecera = ihl * 4
    tam_header = ihl * 4
    
    typeService = data[1]
    length = data[2:4]
    ipID = int.from_bytes(data[4:6], "big")
    flags_offset = data[6:8]

    # Obtener únicamente los 3 primeros bits
    flags = flags_offset[0]  & 0xe0

    # obtener los 13 bits de offset
    aux = (flags_offset[0] & 0x1f) << 8
    offset = ((0x0000 | aux) | flags_offset[1])*8

    if offset != 0:
        return


    timeToLive = data[8]
    protocol = data[9]
    header_cs = data[10:12]
    orgIP = int.from_bytes(data[12:16], 'big')
    dstIP = int.from_bytes(data[16:20], 'big')

    if tam_header >= IP_MIN_HLEN:
        # Cabecera con opciones
        difference = tam_header - IP_MIN_HLEN
        options = data[IP_MIN_HLEN: difference]
        payload = data[tam_header:]
        header_aux = data[0:10] + bytes([0, 0]) + data[12:IP_MIN_HLEN+difference]
        cs = chksum(header_aux)
    else:
        # Cabecera sin opciones
        payload = data[IP_MIN_HLEN:]
        header_aux = data[0:10] + bytes([0, 0]) + data[12:IP_MIN_HLEN]
        cs = chksum(header_aux)

    if header_cs != cs.to_bytes(2, "little"):
        print("checksum incorrecto en process_IP_datagram")
        return
    # Loggear valor de los siguientes campos
    print()
    logging.debug("(process_IP_datagram) Valor longitud cabecera: " + str(tam_header))
    logging.debug("(process_IP_datagram) Valor IPID: " + str(ipID))
    logging.debug("(process_IP_datagram) Valor TTL: " + str(timeToLive))
    logging.debug("(process_IP_datagram) Valor banderas: " + str(flags))
    logging.debug("(process_IP_datagram) Valor offset: " + str(offset))
    logging.debug("(process_IP_datagram) Valor IP origen: " + str(orgIP))
    logging.debug("(process_IP_datagram) Valor IP destino: " + str(dstIP))
    logging.debug("(process_IP_datagram) Valor protocolo: " + str(protocol))

    # Comprobar que hay una funcion registrada para dicho protocolo
    if protocol not in protocols:
        print("Protocolo no registrado")
    else:
        protocols[protocol](us, header, payload, orgIP)

    return

def registerIPProtocol(callback,protocol):
    '''
        Nombre: registerIPProtocol
        Descripción: Esta función recibirá el nombre de una función y su valor de protocolo IP asociado y añadirá en la tabla
            (diccionario) de protocolos de nivel superior dicha asociación.
            Este mecanismo nos permite saber a qué función de nivel superior debemos llamar al recibir un datagrama IP  con un
            determinado valor del campo protocolo (por ejemplo TCP o UDP).
            Por ejemplo, podemos registrar una función llamada process_UDP_datagram asociada al valor de protocolo 17 y otra
            llamada process_ICMP_message asocaida al valor de protocolo 1.
        Argumentos:
            -callback_fun: función de callback a ejecutar cuando se reciba el protocolo especificado.
                La función que se pase como argumento debe tener el siguiente prototipo: funcion(us,header,data,srcIp):
                Dónde:
                    -us: son los datos de usuarios pasados por pcap_loop (en nuestro caso este valor será siempre None)
                    -header: estructura pcap_pkthdr que contiene los campos len, caplen y ts.
                    -data: payload del datagrama IP. Es decir, la cabecera IP NUNCA se pasa hacia arriba.
                    -srcIP: dirección IP que ha enviado el datagrama actual.
                La función no retornará nada. Si un datagrama se quiere descartar basta con hacer un return sin valor y dejará de procesarse.
            -protocol: valor del campo protocolo de IP para el cuál se quiere registrar una función de callback.
        Retorno: Ninguno
    '''
    protocols[protocol] = callback

def initIP(interface,opts=None):
    global myIP, MTU, netmask, defaultGW, ipOpts, IPID
    '''
        Nombre: initIP
        Descripción: Esta función inicializará el nivel IP. Esta función debe realizar, al menos, las siguientes tareas:
            -Llamar a initARP para inicializar el nivel ARP
            -Obtener (llamando a las funciones correspondientes) y almacenar en variables globales los siguientes datos:
                -IP propia
                -MTU
                -Máscara de red (netmask)
                -Gateway por defecto
            -Almacenar el valor de opts en la variable global ipOpts
            -Registrar a nivel Ethernet (llamando a registerCallback) la función process_IP_datagram con el Ethertype 0x0800
            -Inicializar el valor de IPID con el número de pareja
        Argumentos:
            -interface: cadena de texto con el nombre de la interfaz sobre la que inicializar ip
            -opts: array de bytes con las opciones a nivel IP a incluir en los datagramas o None si no hay opciones a añadir
        Retorno: True o False en función de si se ha inicializado el nivel o no
    '''
    if initARP(interface) == -1:
        return False
    myIP = getIP(interface)
    MTU = getMTU(interface)
    netmask = getNetmask(interface)
    defaultGW = getDefaultGW(interface)
    ipOpts = opts
    registerCallback(process_IP_datagram, 0x0800)
    IPID = 1

def sendIPDatagram(dstIP,data,protocol):
    '''
        Nombre: sendIPDatagram
        Descripción: Esta función construye un datagrama IP y lo envía. En caso de que los datos a enviar sean muy grandes la función
        debe generar y enviar el número de fragmentos IP que sean necesarios.
        Esta función debe realizar, al menos, las siguientes tareas:
            -Determinar si se debe fragmentar o no y calcular el número de fragmentos
            -Para cada datagrama o fragmento:
                -Construir la cabecera IP con los valores que corresponda.Incluir opciones en caso de que ipOpts sea distinto de None
                -Calcular el checksum sobre la cabecera y añadirlo a la cabecera
                -Añadir los datos a la cabecera IP
                -En el caso de que sea un fragmento ajustar los valores de los campos MF y offset de manera adecuada
                -Enviar el datagrama o fragmento llamando a sendEthernetFrame. Para determinar la dirección MAC de destino
                al enviar los datagramas se debe hacer unso de la máscara de red:
            -Para cada datagrama (no fragmento):
                -Incrementar la variable IPID en 1.
        Argumentos:
            -dstIP: entero de 32 bits con la IP destino del datagrama
            -data: array de bytes con los datos a incluir como payload en el datagrama
            -protocol: valor numérico del campo IP protocolo que indica el protocolo de nivel superior de los datos
            contenidos en el payload. Por ejemplo 1, 6 o 17.
        Retorno: True o False en función de si se ha enviado el datagrama correctamente o no

    '''
    global IPID, netmask, defaultGW, ipOpts, MTU, myIP
    dstMac = bytes()

    # Obtener MAC destino
    if myIP & netmask == dstIP & netmask:
        # Misma mascara de red -> ARP(ipDestino)
        dstMac = ARPResolution(dstIP)
    else:
        # Distinta mascara de red -> ARP(defaultGateway)
        dstMac = ARPResolution(defaultGW)

    # Comprobar que no es erronea
    if dstMac is None:
        return False

    # Obtener tam cabecera
    if ipOpts is None:
        # Sin opciones
        tam_header = IP_MIN_HLEN
    else:
        # Con opciones
        if len(ipOpts) > 40:
            return False
        tam_header = IP_MIN_HLEN + len(ipOpts) + (len(ipOpts) % 4)

    # Calcular maximo de datos en cada fragmento
    maxData = MTU - tam_header
    # Comprobar que es multiplo de 8, si no lo es, buscar el multiplo de 8 mas cercano por debajo
    maxData = maxData - (maxData % 8)

    # Calcular numero de fragmentos
    if len(data) < maxData:
        num_fragments = 1
    else:
        num_fragments = ceil(len(data)/maxData)

    for i in range(num_fragments):
        datagram = bytes()
        ip_header = bytes()

        version = 0x40
        ihl = int(tam_header/4) # Numero que multiplicado por 4 te de el tamanyo de la cabecera

        # Agregar version (siempre es 4) + ihl
        version_ihl = version | ihl
        ip_header += version_ihl.to_bytes(1, "little")

        # Agregar tipo de servicio (siempre 0x10)
        typeOfService = bytes([0x10])
        ip_header += typeOfService

        # Agregar campo longitud total del datagrama (se calcula al final)
        ip_header += bytes([0,0])

        # Agregar IPID
        ip_header += IPID.to_bytes(2, "big")

        # Calcular flags (Reservado = 0, DF = 0, MF = 1/0)
        if i == (num_fragments - 1):
            # Ultimo fragmento
            flags = bytes([0x00, 0x00])
        else:
            flags = bytes([0x20, 0x00]) # 0010 0000 ...

        # Calcular offset
        offset = (i * maxData)/8


        # Agregar flags + offset
        flags_offset = (int.from_bytes(flags, 'big') ) | (int(offset))
        ip_header += flags_offset.to_bytes(2, "big")

        # Agregar timeToLive (por defecto 64)
        timeToLive = bytes([0x40])
        ip_header += timeToLive

        # Agregar protocolo
        ip_header += protocol.to_bytes(1, "little")

        # Agregar campo checksum (se calcula al final)
        ip_header += bytes([0x0, 0x0])

        # Agregar ip origen e ip destino
        ip_header += myIP.to_bytes(4, 'big')
        ip_header += dstIP.to_bytes(4, 'big')

        # Agregar opciones + padding (si se necesitara)
        if ipOpts is not None:
                ip_header += ipOpts + bytes([0b0000] * (len(ipOpts) % 4))
        
        # Formar datagrama entero
        if i == (num_fragments - 1):
            # Ultimo fragmento
            datagram = ip_header + data[i * maxData:]
        else:
            datagram = ip_header + data[i * maxData:(i + 1) * maxData]

        # Añadir longitud
        datagram = datagram[0:2] + len(datagram).to_bytes(2, "big") + datagram[4:]

		# Calcular el checksum y terminar de formar el datagram
        ip_header = datagram[0:tam_header]

        cs = chksum(ip_header)
        ip_header = ip_header[:10] + cs.to_bytes(2, "little") + ip_header[12:tam_header]
        datagram = ip_header + datagram[tam_header:]

        sendEthernetFrame(datagram, len(datagram), 0x0800, dstMac)

    IPID += 1

    return True