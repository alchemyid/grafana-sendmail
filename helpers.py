import decimal
import datetime
import subprocess
import os
import requests
import time
import secrets
import string
import json
from mail import email

class helpers:
    @staticmethod
    def jsonSerializer(obj):
        if isinstance(obj, datetime.datetime):
            return str(obj)
        elif isinstance(obj, decimal.Decimal):
            return str(obj)

        raise TypeError(
            'Cannot serialize {!r} (type {})'.format(obj, type(obj)))
    @staticmethod
    def getImage(id, receive):
        # print(id)
        today = datetime.date.today()
        day = today.day
        month = today.month
        year = today.year

        # f = "01/"+str(month)+"/"+str(year)+" 00:00:00"
        f = str(day-1)+"/"+str(month)+"/"+str(year)+" 00:00:00"
        
        if day < 31:
            d = day
        elif day == 31:
            d = 31

        to = str(d)+"/"+str(month)+"/"+str(year)+" 00:00:00"
        element_f = datetime.datetime.strptime(f,"%d/%m/%Y %H:%M:%S").timetuple()
        element_to = datetime.datetime.strptime(to,"%d/%m/%Y %H:%M:%S").timetuple()
        

        url = os.getenv('GF_URI_SCHEMA')+"://"+os.getenv('GF_USERNAME')+":"+os.getenv('GF_PASSWORD')+"@"+ \
            os.getenv('GF_HOST')+"/render/d/"+id+"?from="+str(time.mktime(element_f))[:10]+"000&to"+str(time.mktime(element_to))[:10]+"000&height=450&theme=light&kiosk"
        
        rand = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(10))

        data = requests.get(url, timeout=30).content
        file = open("assets/"+id+"_"+rand+".png","wb")
        file.write(data)
        file.close()

        api = os.getenv('GF_URI_SCHEMA')+"://"+os.getenv('GF_USERNAME')+":"+os.getenv('GF_PASSWORD')+"@"+os.getenv('GF_HOST')
        resp = requests.get(api+"/api/dashboards/uid/J0nHnl8Vz")
        resp_dict = resp.json()
        title = json.dumps(resp_dict["dashboard"]["panels"][0]["title"])

        email(id+"_"+rand, f, to, title, receive)

        
    @staticmethod
    def command(s):
        proc = subprocess.Popen([s], stdout=subprocess.PIPE, shell=True)
        out, _ = proc.communicate()
        return out.decode()

    @staticmethod
    def env():

        schema_app = os.getenv("SCHEMA_APP")
        url_app = os.getenv("URL_APP")

        host = os.getenv('GF_HOST')
        gf_user = os.getenv('GF_USERNAME')
        gf_pass = os.getenv('GF_PASSWORD')
        schema = os.getenv('GF_URI_SCHEMA')

        mail_user = os.getenv("MAIL_USER")
        mail_pass = os.getenv("MAIL_PASS")
        mail_smtp = os.getenv("MAIL_SMTP")
        mail_port = os.getenv("PORT_MAIL")

        url = schema+"://"+gf_user+":"+gf_pass+"@"+host+""
        r = requests.get(url)
        if r.status_code == 200 and (schema_app and url_app and mail_user and mail_pass and mail_smtp and mail_port) != None:
            return True
