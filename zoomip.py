import requests, logging, os
from ipaddress import IPv4Network
from datetime import date

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', filename='zoomacl.log', encoding='utf-8', level=logging.INFO)

z_generic = "https://assets.zoom.us/docs/ipranges/Zoom.txt"
z_meetings = "https://assets.zoom.us/docs/ipranges/ZoomMeetings.txt"
z_cloud_room = "https://assets.zoom.us/docs/ipranges/ZoomCRC.txt"
z_phone = "https://assets.zoom.us/docs/ipranges/ZoomPhone.txt"

z_prefixlists = [z_generic, z_meetings, z_cloud_room, z_phone]

# class network_objects:
#   def __init__(self, network, mask):
#        self.network = network
#        self.mask = mask

    #def add_obj_prefix():
    #    for i in range:
    #        new = old[i].append + 

def get_zoom_iplists(zoomlist):
    try:
        zoomstr = requests.get(zoomlist)
        if zoomstr.status_code != 200:
            logging.error('There is a problem with accessing the source URL %s', zoomlist)
            logging.error("Status code: %s", zoomstr.status_code)
            print(f'There is a problem with accessing the source URL {zoomlist}')
            print("Status code:", zoomstr.status_code)
            return None
        else:
            logging.info('%s received', zoomlist)
            print(f'\nThere is no problem with accessing the source URL {zoomlist}')
            print("Status code:", zoomstr.status_code)
            print(zoomlist, '\tText file received\n')
            return zoomstr
    except:
        logging.error('There is likely a problem with basic network connectivity')
        print(f'There is likely a problem with basic network connectivity')



def slash_to_dotted(listtoconvert):
    #ref URL https://stackoverflow.com/questions/33750233/convert-cidr-to-subnet-mask-in-python
    listtoconvert = listtoconvert.text
    listtoconvert = listtoconvert.split()
    cidrtxt = ''
    for i in listtoconvert:
        #remove print statement when happy
        #print(IPv4Network(i).network_address, IPv4Network(i).netmask)
        #eachline = (IPv4Network(i).network_address.__str__, IPv4Network(i).netmask.__str__)
        eachline = "network-object " + str(IPv4Network(i).network_address) + " " + str(IPv4Network(i).netmask)
        print(eachline)
        cidrtxt += (eachline + '\n')
    return cidrtxt

def send_to_file(nulist, filename):
    today = str(date.today())
    try:
        print(filename)
        fo = open(today + '-' + filename, 'wt') 
        fo.write(nulist)
        fo.close()
        #logging.info(current_file, " written to disk")
    except IOError as e:
        print("I/O error occurred: ", os.strerror(e.errno))

def runme():
    for i in z_prefixlists:
        last_slash = i.rfind('/') + 1
        filename = i[last_slash:]
        listtext = get_zoom_iplists(i)
        cidrtxtresult = slash_to_dotted(listtext)
        send_to_file(cidrtxtresult, filename)
    
if __name__ == "__main__":
    runme()