#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__author__  = "Romain Schwab - Kevin Bedin"
__version__ = "1.0.1"
__date__    = "2020-02-02"
__status__  = "Development"
"""
"""
    The ``ulysse_gnss_compass`` module
    ======================
    
    Use it to :
        - get RTK positions from u-blox GNSS receivers
        - compute heading
        - broadcast data for SBG Systems Ekinox1-U
    
    Context
    -------------------
    Ulysse Unmaned Surface Vehicle
    
    Information
    ------------------------
    Points a reprendre :
        - modification de la trame GST
        - resynchronisation des trames
        - decouper les fichiers apres une certaine taille
    
"""


import os
import re
import serial
import socket
import time
import struct
import numpy as np

import rospy
import rospkg
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus

from datetime import datetime


BASENAME="gps"
DIAG_BASENAME="GPS -"

HEADING_BIAS = 1.895 # biais en degres entre axe des GPS et axe de la centrale

# On lit sur port serie les positions RTK :
COM_UBLOX_2 = '/dev/ttyACM0'#Arriere
COM_UBLOX_1 = '/dev/ttyACM1'#Avant
BD = 115200
COM_TIMEOUT = 1e-4 # 100us


PATH = rospkg.RosPack().get_path("ublox_gps")+'/LOGS/GNSS_DATA/'

zda_count = 0


def checksum(s):
    """
        NMEA frame checksum computation
    """
    result   = re.search('\$(.*)\*', s) # everything between '$' and '*' (escaped with '\')

    # https://rietman.wordpress.com/2008/09/25/how-to-calculate-the-nmea-checksum/
    # see also https://forum.u-blox.com/index.php/14618/python-generate-checksums-validate-coming-serial-interface

    checksum = 0
    for thing in result.group(1):
        checksum = checksum ^ ord(thing)  # Xor

    ck  = hex(0x100 + checksum)[-2:].upper()
    return ck

# =============================================================================
#  ATTENTION : ERREUR QUAND LA VARIABLE dm EST VIDE
# =============================================================================
def DM2DD(dm, sign):
    """
        Passage de la convention degre/minute a la convention degre pour 
        les donnees de longitude et latitude.
        
        Convention de signe : positif si Nord ou Est
        
        Format des donnees d'entree : 7 chiffres apres la virgule
        
        Exemple : '4825.0876539' devient '48.418127565'
    """
    # Conversion des coordonnees degre-minute en degre :
    dd = np.float((dm[:-10])) + np.float((dm[-10:]))/60.
    
    # Convention de signe :
    if sign in ['S', 'W']:
        dd *= -1
    
    return dd

def ublox_connection(serial_port):
    """
        Open a connection with u-blox (serial port)
    """
    # Connect to serial ports
    try:
        port = serial.Serial(port=serial_port, baudrate=BD, timeout=COM_TIMEOUT)
    except:
        port = None
        
    return port

def get_nmea_data(port):
    """
        Listen to u-blox serial port
        
        If frame is incomplete, infinite loop waiting for next complete frame
    """
    
#    q = 1 # quality factor
    
    # Wait for RMC message :
    rmc = port.readline().decode("utf-8")
    while not 'RMC' in rmc:
        if rmc: print("Wait for RMC : ", rmc)
        rmc = port.readline().decode("utf-8")
    
    # Read GGA+GST+ZDA messages :
    gga = port.readline().decode("utf-8")
    gst = port.readline().decode("utf-8")
    zda = port.readline().decode("utf-8")
    
    t = np.float(rmc[7:16])
    
    # Print messages :
    print("Trames :")
    print(" RMC: ",rmc)
    print(" GGA: ",gga)
    print(" GST: ",gst)
    print(" ZDA: ",zda)
    
    # Quality check :
    if not 'GGA' in gga or not 'GST' in gst or not 'ZDA' in zda:
        print("Issue with GGA/GST/ZDA frame decoding !\nMessage:\nGGA:{0}\nGST:{1}\nZDA:{2}".format(gga, gst, zda))
        rmc, gga, gst, zda, t = get_nmea_data(port)
    
    return rmc, gga, gst, zda, t
    

def get_heading_data(port):
    """
        Listen to u-blox ZED-F9H serial port
        
        If frame is incomplete, infinite loop waiting for next complete frame
    """
    
    
    # Wait for RMC message :
    data = port.readline().decode("utf-8")

    intData = struct.Struct("<i")#I4
    charData = struct.Struct("<b")#I1
    uintData = struct.Struct("<I")#U4

    length = intData.unpack(data[26:30])+charData.unpack(data[41:42])*0.1 # distance between the 2 antennas in cm.
    heading = intData.unpack(data[30:34])# in degrees
    acc_length = uintData.unpack(data[54:58])# in mm 
    acc_heading = uintData.unpack(data[58:62])# in degrees

    return length, acc_length, heading, acc_heading

def complete_gst(gst_in, gga_in):
    """
        Write NMEA GST frame according to a given position
    """
    
    gst_out = gst_in.split(',')
    gga_in = gga_in.split(',')
    hdop = np.float(gga_in[8])
    hdop = 0.05
    gst_out[2] = str(hdop)
    gst_out[3] = str(hdop)
    gst_out[4] = str(hdop)
    gst_out[5] = str(0.1)
    gst = ','.join(gst_out)
    
    # Apply new checksum :
    gst = gst[:-4] + checksum(gst) + gst[-2:]
    
    return gst

def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        theta = atan2(sin(dlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(dlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")
        
    lat1 = np.radians(pointA[0])
    lat2 = np.radians(pointB[0])
    
    diffLong = np.radians(pointB[1] - pointA[1])
    
    x = np.sin(diffLong) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - (np.sin(lat1)
            * np.cos(lat2) * np.cos(diffLong))
    
    initial_bearing = np.arctan2(x, y)
    
    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = np.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    
    return compass_bearing


def send_nmea(udp_port, rmc, gga, gst, zda, hdt):
    """
        Send GNSS data to SBG Systems Ekinox-1 using UDP protocol
    """
    
    # Send data :
    udp_port.sendto(rmc.encode('utf-8'), (UDP_IP, UDP_PORT))
    udp_port.sendto(gga.encode('utf-8'), (UDP_IP, UDP_PORT))
    udp_port.sendto(gst.encode('utf-8'), (UDP_IP, UDP_PORT))
    udp_port.sendto(hdt.encode('utf-8'), (UDP_IP, UDP_PORT))
    if zda:
        udp_port.sendto(zda.encode('utf-8'), (UDP_IP, UDP_PORT))
        
def write_nmea(rmc_1, gga_1, gst_1, zda_1, hdt, heading, acc_heading, length, acc_length, f1, fh):
    """
        Save GNSS data into ascii files
    """
    f1.write(rmc_1)
    f1.write(gga_1)
    f1.write(gst_1)
    if zda_1:
        f1.write(zda_1)
    
    line = "%s %f %f %f %f"%(hdt, heading,acc_heading,length,acc_length)
    fh.write(line)
    
    
def set_hdt_nmea_frame(heading, rmc_1):
    
    # Create HDT NMEA sentence :
    prefix = rmc_1[:3] + 'HDT'
    suffix = 'T*00\r\n' # default checksum
    hdt_nmea = ','.join([prefix, str(heading), suffix])
    
    # Apply correct checksum :
    hdt = hdt_nmea[:-4] + checksum(hdt_nmea) + hdt_nmea[-2:]
    return hdt

def create_empty_logfiles(path):
    
    file_prefix = datetime.utcnow().strftime('%Y%m%d_%H%M%S_')
    # Fichiers de sauvegarde des donnees
    f1 = open(path+file_prefix+'data_ublox1.txt', 'a')
    fh = open(path+file_prefix+'data_cap.txt', 'a')
    
    return f1, fh


if __name__ == '__main__':

    rospy.init_node(BASENAME, anonymous=False, log_level=rospy.DEBUG)
    diag=rospy.Publisher("diagnostics",DiagnosticArray, queue_size=5)

    # Connect to serial ports
    port_ubh = ublox_connection(COM_UBLOX_1) # HEADING
    port_ub1 = ublox_connection(COM_UBLOX_2) # GNSS


    # On diffuse par protocole ethernet UDP les trames NMEA GGA, GST, RMC, ZDA, HDT
    UDP_IP = "10.255.255.255"
    UDP_PORT = 1010
    # Creation d'un serveur UDP :
    udp_server = socket.socket(socket.AF_INET, # Internet
                                   socket.SOCK_DGRAM) # UDP
    udp_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    f1, fh = create_empty_logfiles(PATH)
    



# =============================================================================
#     LECTURE 
# =============================================================================
    count_missing_data = 0
    while not(rospy.is_shutdown()):

        try:
            # trouver l'ordre des trames : par exemple : RMC, GGA, GST, ZDA
            # bien regler le timeout en fonction de la cadence d'emission (5Hz)
            
            # Create new files if max size limit is reached :
            if os.stat(f1.name).st_size >= 10e7 or os.stat(fh.name).st_size >= 10e7:
                f1.close()
                fh.close()
                f1, fh = create_empty_logfiles(PATH)
            
            # Start
            t0 = time.time()
            
            # Listen COM ports :
            rmc_1, gga_1, gst_1, zda_1, t_f1 = get_nmea_data(port_ub1)
            length, acc_length, heading, acc_heading = get_heading_data(port_ubh)
            
            hdt = set_hdt_nmea_frame(heading, rmc_1)
            
            t1 = time.time()
            
            
            print("\nDonnees :\n   Cap GNSS : {0:.2f}°+/-{0:.2f}°".format(heading, acc_heading))
            print("\nDonnees :\n   Distance entre GNSS : {0:.2f}cm+/-{0:.2f}mm".format(length, acc_length))
            print("Temps de calcul :")
            print("   Temps calcul total : {0:.1f}ms".format((t1-t0)*1e3))

            send_nmea(udp_server, rmc_1, gga_1, gst_1, zda_1, hdt)
            
            write_nmea(rmc_1, gga_1, gst_1, zda_1, hdt, length, acc_length, heading, acc_heading, fh)
            
            arr=DiagnosticArray()
            arr.status.append(DiagnosticStatus(level=0,name=DIAG_BASENAME+" Calcul Time",message="{0:.1f}ms".format((t1-t0)*1e3)))
            arr.status.append(DiagnosticStatus(level=0,name=DIAG_BASENAME+" Cap",message="{0:.2f}".format(heading)))
            arr.header.stamp= rospy.Time.now()
            diag.publish(arr)

        except:

            arr=DiagnosticArray()
            arr.status.append(DiagnosticStatus(level=1,name=DIAG_BASENAME+" Calcul Time",message="ERROR"))
            arr.status.append(DiagnosticStatus(level=1,name=DIAG_BASENAME+" Cap",message="ERROR"))
            arr.header.stamp= rospy.Time.now()
            diag.publish(arr)


    print("Script arrete par l'utilisateur.")
    f1.close()
    fh.close()

