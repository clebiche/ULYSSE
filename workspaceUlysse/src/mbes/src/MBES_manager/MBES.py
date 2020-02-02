import struct
import time
import socket
from SVP import calculateXYsvp

BUFFER_SIZE=65535 #Taille maximale d'un message UDP
UDP_PORT = 1030


def date():
    t=time.localtime()
    m=t[1]
    j=t[2]
    a=t[0]
    hh=t[3]
    mm=t[4]
    ss=t[5]
    date=str(j)+"_"+str(m)+"_"+str(a)+"-"+str(hh)+"H"+str(mm)+"m"+str(ss)+"s"
    return(date)

def initMBESsocket(path):
    f = open(path+"/LOGS/R2SONIC/trames_"+date()+".raw","wb")
    sock = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
    sock.bind(('', UDP_PORT))
    return sock, f


def closeMBESsocket(sock,saving_file):
    close(sock)
    close(saving_file)

def getMBESdata(sock, saving_file):

    addr = sock.recvfrom(BUFFER_SIZE)
    print("New raw data")

    message = addr[0]
    address = addr[1]
    saving_file.write(message)

    angle=[]
    time=[]
    try:
        s = struct.Struct(">ccccIIccHccccccccccccccccccccccccIIIfffffffffHhfffffffIHHccHf")
        record,message = message[:s.size],message[s.size:]
        p1=s.unpack(record)
        #print p1
        N=p1[56]#Nbr de points
        N=(N+(N&1))
        dateS=int(p1[33])
        dateNS=int(p1[34])
        pingNum=int(p1[35])

        #Section R0 - R0_Range[H0_Points] - [second two-way] = R0_Range * R0_ScalingFactor (=p1[-1])
        str1="H"*(N)
        s2=struct.Struct(">"+str1)
        record2 = message[:s2.size],message[s2.size:]
        p2=s2.unpack(record2)
        #print p2

        #A0 ou A2 section
        s3=struct.Struct(">ccHffffffff")
        record3 = message[:s3.size],message[s3.size:]
        p3=s3.unpack(record3)
        #print p3

        if p3[1]=='2':#Si section A2
            str1="H"*N
            s4=struct.Struct(">"+str1)
            record4 = message[:s4.size],message[s4.size:]
            p4=s4.unpack(record4)
            #print p4

#        #Section I1 et G0
#        s5=struct.Struct(">ccHf")
#        record5 = message[:s5.size],message[s5.size:]
#        p5=s5.unpack(record5)
#        #print p5
#        if p5[0]=="I":#Si section I1
#            s6=struct.Struct(">"+str1)
#            record6 = message[:s6.size],message[s6.size:]
#            p6=s6.unpack(record6)
#            #print(p6)
#            s7=struct.Struct(">ccHfff")
#            record7 = message[:s7.size],message[s7.size:]
#            p7=s7.unpack(record7)


#        else: #section G0
#            s7=struct.Struct(">ff")
#            record7 = message[:s7.size],message[s7.size:]
#            p7=s7.unpack(record7)

#        
#        #Section G1 et Q0
#        s8=struct.Struct(">ccH")
#        record8= message[:s8.size],message[s8.size:]
#        p8 = s8.unpack(record8)
#        #print p8

#        str2="I"*int((N+7)/8)
#        if p8[0]=="G":#Si section G1
#            s9=struct.Struct(">f")
#            record9=message[:s9.size],message[s9.size:]
#            p9=s9.unpack(record9)
#            #print p9
#            s10=struct.Struct(">BB")
#            for i in range(N):
#                record10=message[:s10.size],message[s10.size:]
#                p10=s10.unpack(record10)
#                #print p10
#            s11=struct.Struct(">ccH"+str2)#Section Q0
#        else:#Section Q0
#            s11=struct.Struct(">"+str2)
#            
#        record11=message[:s11.size],message[s11.size:]
#        p11= s11.unpack(record11)
#        #print p11
        
                
        scaleFactor=p1[-1]
        i = 0
        sumDelt = 0
        X = []
        Y = []
        
        if (p3[1] == '2'):
            for time in p2:
                sumDelt += p4[i]
                angles.append(p3[3]+sumDelt*p3[4])
                times.append(time*scaleFactor)
                i+=1
        return(angles,times,dateS,dateNS,pingNum)
    except:
        print("Error in unpacking socket")
        return(None,None,None,None,None)

def readMBESdata(f):

    angles = []
    times = []
    try:
        # > Big endian et < Little endian
        #Section BEGIN et H0 et debut R0
        #print("\n\n##### Packet "+str(n_packet)+" #####\n")
        s = struct.Struct(">ccccIIccHccccccccccccccccccccccccIIIfffffffffHhfffffffIHHccHf")
        record = f.read(s.size)
        p1=s.unpack(record)
        #print p1
        N=p1[56]#Nbr de points
        N=(N+(N&1))
        dateS=int(p1[33])
        dateNS=int(p1[34])
        pingNum=int(p1[35])

        #Section R0 - R0_Range[H0_Points] - [second two-way] = R0_Range * R0_ScalingFactor (=p1[-1])
        str1="H"*(N)
        s2=struct.Struct(">"+str1)
        record2 = f.read(s2.size)
        p2=s2.unpack(record2)
        #print p2

        #A0 ou A2 section
        s3=struct.Struct(">ccHffffffff")
        record3 = f.read(s3.size)
        p3=s3.unpack(record3)
        #print p3

        if p3[1]=='2':#Si section A2
            str1="H"*N
            s4=struct.Struct(">"+str1)
            record4 = f.read(s4.size)
            p4=s4.unpack(record4)
            #print p4
#            ret = 4

        #Section I1 et G0
        s5=struct.Struct(">ccHf")
        record5 = f.read(s5.size)
        p5=s5.unpack(record5)
        #print p5
        if p5[0]=="I":#Si section I1
            s6=struct.Struct(">"+str1)
            record6 = f.read(s6.size)
            p6=s6.unpack(record6)
            #print(p6)
            s7=struct.Struct(">ccHfff")
            record7 = f.read(s7.size)
            p7=s7.unpack(record7)
#            if (ret == 4):
#                ret = 467
#            else:
#                ret = 67

        else: #section G0
            s7=struct.Struct(">ff")
            record7 = f.read(s7.size)
            p7=s7.unpack(record7)
#            if (ret == 4):
#                ret = 47
#            else:
#                ret = 7
        #print p7
        
        #Section G1 et Q0
        s8=struct.Struct(">ccH")
        record8= f.read(s8.size)
        p8 = s8.unpack(record8)
        #print p8

        str2="I"*int((N+7)/8)
        if p8[0]=="G":#Si section G1
            s9=struct.Struct(">f")
            record9=f.read(s9.size)
            p9=s9.unpack(record9)
            #print p9
            s10=struct.Struct(">BB")
            for i in range(N):
                record10=f.read(s10.size)
                p10=s10.unpack(record10)
                #print p10
            s11=struct.Struct(">ccH"+str2)#Section Q0
        else:#Section Q0
            s11=struct.Struct(">"+str2)
            
        record11=f.read(s11.size)
        p11= s11.unpack(record11)
        #print p11
        
                
        scaleFactor=p1[-1]
        i = 0
        sumDelt = 0
        X = []
        Y = []
        #f = open("data.txt", "w")
        
        #f.write("Time_two-way[seconds];Angle[radians];x[m];y[m]\n")
        if (p3[1] == '2'):
            for time in p2:
                sumDelt += p4[i]
                angles.append(p3[3]+sumDelt*p3[4])
                times.append(time*scaleFactor)
                i+=1
        return(angles,times,dateS,dateNS,pingNum)
    except:
            return(None,None,None,None,None)
                
                
                
def loadMBESdata(f,svp):

    end_data=False
    n_packet=0
    X = []
    Y = []
    ret = 0

    while not end_data:
        try:
            # > Big endian et < Little endian
            #Section BEGIN et H0 et debut R0
            #print("\n\n##### Packet "+str(n_packet)+" #####\n")
            s = struct.Struct(">ccccIIccHccccccccccccccccccccccccIIIfffffffffHhfffffffIHHccHf")
            record = f.read(s.size)
            p1=s.unpack(record)
            #print p1
            N=p1[56]#Nbr de points
            N=(N+(N&1))

            #Section R0 - R0_Range[H0_Points] - [second two-way] = R0_Range * R0_ScalingFactor (=p1[-1])
            str1="H"*(N)
            s2=struct.Struct(">"+str1)
            record2 = f.read(s2.size)
            p2=s2.unpack(record2)
            #print p2

            #A0 ou A2 section
            s3=struct.Struct(">ccHffffffff")
            record3 = f.read(s3.size)
            p3=s3.unpack(record3)
            #print p3

            if p3[1]=='2':#Si section A2
                str1="H"*N
                s4=struct.Struct(">"+str1)
                record4 = f.read(s4.size)
                p4=s4.unpack(record4)
                #print p4
                ret = 4

            #Section I1 et G0
            s5=struct.Struct(">ccHf")
            record5 = f.read(s5.size)
            p5=s5.unpack(record5)
            #print p5
            if p5[0]=="I":#Si section I1
                s6=struct.Struct(">"+str1)
                record6 = f.read(s6.size)
                p6=s6.unpack(record6)
                #print(p6)
                s7=struct.Struct(">ccHfff")
                record7 = f.read(s7.size)
                p7=s7.unpack(record7)
                if (ret == 4):
                    ret = 467
                else:
                    ret = 67

            else: #section G0
                s7=struct.Struct(">ff")
                record7 = f.read(s7.size)
                p7=s7.unpack(record7)
                if (ret == 4):
                    ret = 47
                else:
                    ret = 7
            #print p7
            
            #Section G1 et Q0
            s8=struct.Struct(">ccH")
            record8= f.read(s8.size)
            p8 = s8.unpack(record8)
            #print p8

            str2="I"*int((N+7)/8)
            if p8[0]=="G":#Si section G1
                s9=struct.Struct(">f")
                record9=f.read(s9.size)
                p9=s9.unpack(record9)
                #print p9
                s10=struct.Struct(">BB")
                for i in range(N):
                    record10=f.read(s10.size)
                    p10=s10.unpack(record10)
                    #print p10
                s11=struct.Struct(">ccH"+str2)#Section Q0
                if(ret == 467):
                    ret = 467910
                if(ret == 67):
                    ret = 67910
                if(ret == 47):
                    ret = 47910
                if(ret==7):
                    ret = 7910
                if (ret==0): 
                    ret = 910
            else:#Section Q0
                s11=struct.Struct(">"+str2)
                
            record11=f.read(s11.size)
            p11= s11.unpack(record11)
            #print p11
            n_packet+=1

            x_pack,y_pack = calculateXYsvp(svp,p1[-1], p1, p2, p3, p4)

            X.append(x_pack)
            Y.append(y_pack)
            
            
        except:
                print(" /!\ not complete\n\n#######################")
                end_data=True
                print("\n\nTotal complete packets: "+str(n_packet)+"\n\n")
                f.close()
                pass

    if (ret == 0):
        return p1,p2,p3,-1,p5,-1,-1,p8,-1,-1,p11,X,Y
    if (ret == 4):
        return p1,p2,p3,p4,p5,-1,-1,p8,-1,-1,p11,X,Y
    if (ret == 67):
        return p1,p2,p3,-1,p5,p6,p7,p8,-1,-1,p11,X,Y
    if (ret == 7):
        return p1,p2,p3,-1,p5,-1,p7,p8,-1,-1,p11,X,Y
    if (ret == 910):
        return p1,p2,p3,-1,p5,-1,-1,p8,p9,p10,p11,X,Y
    if(ret == 467):
        return p1,p2,p3,p4,p5,p6,p7,p8,-1,-1,p11,X,Y
    if(ret == 67910):
        return p1,p2,p3,-1,p5,p6,p7,p8,p9,p10,p11,X,Y
    if(ret == 467910):
        return p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,X,Y
    if(ret == 47):
        return p1,p2,p3,p4,p5,-1,p7,p8,-1,-1,p11,X,Y
    if(ret==47910):
        return p1,p2,p3,p4,p5,-1,p7,p8,p9,p10,p11,X,Y
    if (ret==7910): 
        return p1,p2,p3,-1,p5,-1,p7,p8,p9,p10,p11,X,Y
    return -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,X,Y


def printMBESdata(p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,X,Y):
    print(p1)
    print(p2)
    print(p3)
    print(p4)
    print(p5)
    print(p6)
    print(p7)
    print(p8)
    print(p9)
    print(p10)
    print(p11)
    print(X)
    print(Y)





