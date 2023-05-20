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
import logging
import boto3
from botocore.exceptions import ClientError

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
        print(id)

        today = datetime.date.today()
        day = today.day
        month = today.month
        year = today.year

        f = "01/"+str(month)+"/"+str(year)+" 00:00:00"
        # f = str(day-1)+"/"+str(month)+"/"+str(year)+" 00:00:00"
        
        if day < 31:
            d = day
        elif day == 31:
            d = 31

        to = str(d)+"/"+str(month)+"/"+str(year)+" 00:00:00"
        element_f = datetime.datetime.strptime(f,"%d/%m/%Y %H:%M:%S").timetuple()
        element_to = datetime.datetime.strptime(to,"%d/%m/%Y %H:%M:%S").timetuple()
        

        url = os.getenv('GF_URI_SCHEMA')+"://"+os.getenv('GF_USERNAME')+":"+os.getenv('GF_PASSWORD')+"@"+ \
            os.getenv('GF_HOST')+"/render/d/"+id+"?from="+str(time.mktime(element_f))[:10]+"000&to"+str(time.mktime(element_to))[:10]+"000&width=1450&height=1240&theme=light&kiosk"
        
        rand = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(10))

        data = requests.get(url, timeout=300).content
        file = open("assets/"+id+"_"+rand+".png","wb")
        file.write(data)
        file.close()

        helpers.upload_file("assets/"+id+"_"+rand+".png", os.getenv("BUCKET_NAME"), id+"/"+rand+".png")

        api = os.getenv('GF_URI_SCHEMA')+"://"+os.getenv('GF_USERNAME')+":"+os.getenv('GF_PASSWORD')+"@"+os.getenv('GF_HOST')
        resp = requests.get(api+"/api/dashboards/uid/"+id+"")
        resp_dict = resp.json()
        title = json.dumps(resp_dict["dashboard"]["panels"][0]["title"])

        # width render 1450
        # cpu usage top left &w=730&h=435&c=tl
        # memory usage top right &w=730&h=435&c=tl 
        # center storage + count nodes 1240 &w=1450&h=390&c=center
        # network max &w=730&h=435&c=bl
        # network avg &w=730&h=435&c=br

        email(id ,rand, f, to, title, receive)

        
    @staticmethod
    def command(s):
        proc = subprocess.Popen([s], stdout=subprocess.PIPE, shell=True)
        out, _ = proc.communicate()
        return out.decode()

    @staticmethod
    def env():
        # return True
        aws_access = os.getenv("AWS_ACCESS_KEY")
        aws_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        bucket_name = os.getenv("BUCKET_NAME")

        host = os.getenv('GF_HOST')
        gf_user = os.getenv('GF_USERNAME')
        gf_pass = os.getenv('GF_PASSWORD')
        schema = os.getenv('GF_URI_SCHEMA')

        mail_user = os.getenv("MAIL_USER")
        mail_pass = os.getenv("MAIL_PASS")
        mail_smtp = os.getenv("MAIL_SMTP")
        mail_port = os.getenv("MAIL_PORT")


        url = schema+"://"+gf_user+":"+gf_pass+"@"+host+""
        r = requests.get(url)
        
        if r.status_code == 200 and (aws_access and aws_key and bucket_name and mail_user and mail_pass and mail_smtp and mail_port) != None:
            return True
    
    @staticmethod
    def upload_file(file_name, bucket, object_name=None):

        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None: 
            object_name = os.path.basename(file_name)
            
        # session = boto3.Session(profile_name='reporting-grafana')

        # Upload the file
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )

        # s3_client = session.client('s3')

        try:
            s3_client.upload_file(
                file_name, 
                bucket, os.getenv("BUCKET_NAME"), 
                object_name,
                ExtraArgs={
                    "ACL": "public-read",
                    "ContentType": "image/png"
                    }
            )
            
        except ClientError as e:
            logging.error(e)
            return False
        return True
