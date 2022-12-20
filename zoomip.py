"""Prefix Fetcher for easing the management of objects and object groups in ACLS"""

import requests, logging, os
from ipaddress import IPv4Network
from datetime import date
# from slack_sdk.webhook import WebhookClient

logging.basicConfig(format='%(asctime)s %(message)s', 
    datefmt='%m/%d/%Y %H:%M:%S', filename='zoomacl.log', encoding='utf-8', 
    level=logging.INFO)

# Zoom recently decided in a support exchange that the z_generic list or 
# zoom.txt asset is all you need for all services

z_generic = "https://assets.zoom.us/docs/ipranges/Zoom.txt"
# z_meetings = "https://assets.zoom.us/docs/ipranges/ZoomMeetings.txt"
# z_cloud_room = "https://assets.zoom.us/docs/ipranges/ZoomCRC.txt"
# z_phone = "https://assets.zoom.us/docs/ipranges/ZoomPhone.txt"

z_prefixlists = [z_generic]

# class network_objects:
#   def __init__(self, network, mask):
#        self.network = network
#        self.mask = mask

    #def add_obj_prefix():
    #    for i in range:
    #        new = old[i].append + 

def get_zoom_iplists(zoomlist):
    """Reaches out to the URL provided in the argument to retrieve the data"""
    try:
        zoomstr = requests.get(zoomlist)
        zoomstr.raise_for_status()

        #if zoomstr.status_code != 200:
        #    logging.error('There is a problem with accessing the source URL %s', zoomlist)
        #    logging.error("Status code: %s", zoomstr.status_code)
        #    print(f'There is a problem with accessing the source URL {zoomlist}')
        #    print("Status code:", zoomstr.status_code)
        #    return None
        #else:
        #    logging.info('%s received', zoomlist)
        #    print(f'\nThere is no problem with accessing the source URL {zoomlist}')
        #    print("Status code:", zoomstr.status_code)
        #    print(zoomlist, '\tText file received\n')
        #    return zoomstr

        logging.info('%s received', zoomlist)
        print(f'\nThere is no problem with accessing the source URL {zoomlist}')
        print("Status code:", zoomstr.status_code)
        print(zoomlist, '\tText file received\n')
        return zoomstr
        
    except:
        logging.error('There is likely a problem with basic network connectivity')
        print(f'There is likely a problem with basic network connectivity')



def slash_to_dotted(listtoconvert):
    """Converts the slash notation used by Zoom to dotted notation. Mostly for the benefit of Cisco ASA Objects"""
    """https://towardsdatascience.com/do-not-use-to-join-strings-in-python-f89908307273"""
    # ref URL https://stackoverflow.com/questions/33750233/convert-cidr-to-subnet-mask-in-python
    listtoconvert = listtoconvert.text
    listtoconvert = listtoconvert.split()
    cidrtxt = ''
    for i in listtoconvert:
        #remove print statement when happy
        #print(IPv4Network(i).network_address, IPv4Network(i).netmask)
        #eachline = (IPv4Network(i).network_address.__str__, IPv4Network(i).netmask.__str__)
        eachline = "network-object " + str(IPv4Network(i).network_address) + " " + str(IPv4Network(i).netmask)
        # print(eachline)
        cidrtxt += (eachline + '\\n')
        #cidrtxt += eachline
    return cidrtxt

def send_to_file(nulist, filename):
    """Writes the list to a timestamped file in the filesystem"""
    today = str(date.today())
    try:
        print(filename)
        fo = open(today + '-' + filename, 'wt') 
        fo.write(nulist)
        fo.close()
        #logging.info(current_file, " written to disk")
    except IOError as e:
        print("I/O error occurred: ", os.strerror(e.errno))


def post_msg_to_slack(nulist):
    """ Use the block kit builder! https://app.slack.com/block-kit-builder/ """
    """ There's a limit on no. of characters per post. Says 4K , but it's less than that. Perhaps it includes all chars inc the message. ~3K seems to work need a helper function to split before posting"""
    """ Using the snippet file post seems more evolved than artificially splitting the data uploaded. https://api.slack.com/methods/files.upload """
    webhook_url = "https://hooks.slack.com/services/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"
    headers = {
        "Content-type": "application/x-www-form-urlencoded"
    }
    slack_post = {
        "blocks": [
            {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                #"text": "This is unquoted text\n>This is quoted text\n>This is still quoted text\nThis is unquoted text again"
                #"text": f"This is unquoted text\n>{nulist}\n>This is still quoted text\nThis is unquoted text again"
                #"text": f"This is unquoted text\n```{nulist}```\n>This is still quoted text\nThis is unquoted text again"
                "text": "```" + nulist + "```"
                
                }
            }
        ]
    }
    finale = requests.post(webhook_url, headers=headers, json=slack_post)
    finale.raise_for_status()

# def post_file_to_slack(slack_file, snippet_comment):
    #""" Using the snippet file post seems more evolved than artificially splitting the data uploaded. https://api.slack.com/methods/files.upload """
    #""" No use of webhooks here - that's for messages only """
    #""" https://keestalkstech.com/2019/10/simple-python-code-to-send-message-to-slack-channel-without-packages/"" "
    #slack_url = "https://slack.com/api/files.upload"
    #headers = {
    #    "Content-type": "application/json"
    #}
    # 
    #finale = requests.post(slack_url, filename=slack_file, filetype="text", initial_comment=snippet_comment, title=slack_file)
    #finale.raise_for_status()

def main():
    for i in z_prefixlists:
        last_slash = i.rfind('/') + 1
        filename = i[last_slash:]
        listtext = get_zoom_iplists(i)
        cidrtxtresult = slash_to_dotted(listtext)
        #test_two_lines = "network-object 3.7.35.0 255.255.255.128\nnetwork-object 3.21.137.128 255.255.255.128"
        test_3k = "network-object 3.7.35.0 255.255.255.128\nnetwork-object 3.21.137.128 255.255.255.128\nnetwork-object 3.22.11.0 255.255.255.0\nnetwork-object 3.23.93.0 255.255.255.0\nnetwork-object 3.25.41.128 255.255.255.128\nnetwork-object 3.25.42.0 255.255.255.128\nnetwork-object 3.25.49.0 255.255.255.0\nnetwork-object 3.80.20.128 255.255.255.128\nnetwork-object 3.96.19.0 255.255.255.0\nnetwork-object 3.101.32.128 255.255.255.128\nnetwork-object 3.101.52.0 255.255.255.128\nnetwork-object 3.104.34.128 255.255.255.128\nnetwork-object 3.120.121.0 255.255.255.128\nnetwork-object 3.127.194.128 255.255.255.128\nnetwork-object 3.208.72.0 255.255.255.128\nnetwork-object 3.211.241.0 255.255.255.128\nnetwork-object 3.235.69.0 255.255.255.128\nnetwork-object 3.235.82.0 255.255.254.0\nnetwork-object 3.235.71.128 255.255.255.128\nnetwork-object 3.235.72.128 255.255.255.128\nnetwork-object 3.235.73.0 255.255.255.128\nnetwork-object 3.235.96.0 255.255.254.0\nnetwork-object 4.34.125.128 255.255.255.128\nnetwork-object 4.35.64.128 255.255.255.128\nnetwork-object 8.5.128.0 255.255.254.0\nnetwork-object 13.52.6.128 255.255.255.128\nnetwork-object 13.52.146.0 255.255.255.128\nnetwork-object 18.157.88.0 255.255.255.0\nnetwork-object 18.205.93.128 255.255.255.128\nnetwork-object 20.203.158.80 255.255.255.240\nnetwork-object 20.203.190.192 255.255.255.192\nnetwork-object 50.239.202.0 255.255.254.0\nnetwork-object 50.239.204.0 255.255.255.0\nnetwork-object 52.61.100.128 255.255.255.128\nnetwork-object 52.202.62.192 255.255.255.192\nnetwork-object 52.215.168.0 255.255.255.128\nnetwork-object 64.125.62.0 255.255.255.0\nnetwork-object 64.211.144.0 255.255.255.0\nnetwork-object 65.39.152.0 255.255.255.0\nnetwork-object 69.174.57.0 255.255.255.0\nnetwork-object 69.174.108.0 255.255.252.0\nnetwork-object 99.79.20.0 255.255.255.128\nnetwork-object 101.36.167.0 255.255.255.0\nnetwork-object 103.122.166.0 255.255.254.0\nnetwork-object 111.33.115.0 255.255.255.128\nnetwork-object 111.33.181.0 255.255.255.128\nnetwork-object 115.110.154.192 255.255.255.192\nnetwork-object 115.114.56.192 255.255.255.192\nnetwork-object 115.114.115.0 255.255.255.192\nnetwork-object 115.114.131.0 255.255.255.192\nnetwork-object 120.29.148.0 255.255.255.0\nnetwork-object 129.151.0.0 255.255.224.0\nnetwork-object 129.151.40.0 255.255.252.0\nnetwork-object 129.151.48.0 255.255.240.0\nnetwork-object 129.159.0.0 255.255.240.0\nnetwork-object 129.159.160.0 255.255.224.0\nnetwork-object 129.159.208.0 255.255.240.0\nnetwork-object 130.61.164.0 255.255.252.0\nnetwork-object 134.224.0.0 255.255.0.0\nnetwork-object 140.238.128.0 255.255.255.0\nnetwork-object 140.238.232.0 255.255.252.0\nnetwork-object 144.195.0.0 255.255.0.0\nnetwork-object 147.124.96.0 255.255.224.0\nnetwork-object 149.137.0.0 255.255.128.0\nnetwork-object 150.230.224.0 255.255.248.0\nnetwork-object 152.67.20.0 255.255.255.0\nnetwork-object 152.67.118.0 255.255.255.0\nnetwork-object 152.67.168.0 255.255.252.0\nnetwork-object 152.67.180.0 255.255.255.0\nnetwork-object 152.67.184.0 255.255.255.0"
        #send_to_file(cidrtxtresult, filename)
        #post_to_slack(cidrtxtresult)
        post_msg_to_slack(test_3k)
        #post_file_to_slack(test_3k, filename)

if __name__ == "__main__":
    main()