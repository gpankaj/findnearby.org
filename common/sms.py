#!/usr/bin/python

import urllib2
import cookielib
from getpass import getpass
import sys

class send_sms :
    url = 'http://site24.way2sms.com/Login1.action?'
    username = '7259255869'
    passwd = 'le99m46'
    send_sms_url = 'http://site24.way2sms.com/smstoss.action?'

    def __init__(self,number ,message):
        self.number = number
        message = "+".join(message.split(' '))
        self.message = message

        #Logging into the SMS Site
        self.data = 'username='+send_sms.username+'&password='+self.passwd+'&Submit=Sign+in'



    def send(self):
        #For Cookies:
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

        # Adding Header detail:
        opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')]

        try:
            usock = opener.open(send_sms.url, self.data)
        except IOError:
            #return("Error while logging in")
            return 1
        jession_id = str(cj).split('~')[1].split(' ')[0]

        send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+self.number+'&message='+self.message+'&msgLen=136'
        opener.addheaders = [('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]


        try:
            sms_sent_page = opener.open(send_sms.send_sms_url,send_sms_data)
        except IOError:
            #print "Error while sending message"
            return (2)

        return 0


if __name__ == "__main__":
    sms = send_sms('9845204336','Pikuhomes Code : \n\n\nContact Piku Technical Dept 9845204336 for technical issue.\n\n')
    if(sms.send() == 0):
        print "Succeed"
    else :
        print "Failed with exit code .."



#reference https://www.quora.com/How-do-I-send-text-messages-from-a-python-script-to-a-mobile-number-if-possible-with-a-free-gateway - Sumit