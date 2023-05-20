import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def email(id, filename, datefrom, dateto, title, receive):

  sender_email = os.getenv("MAIL_USER")
  receiver_email = receive
  password = os.getenv("MAIL_PASS")

  #Create MIMEMultipart object
  msg = MIMEMultipart("alternative")
  msg["Subject"] = "Monthly Report "+ title
  msg["From"] = sender_email
  msg["To"] = receiver_email
  # filename = "assets/"+id+".png"
  # img = os.getenv("SCHEMA_APP")+"://"+os.getenv("URL_APP")+"/assets/"+id
  img = "https://"+os.getenv("BUCKET_NAME")+".s3.ap-southeast-1.amazonaws.com/"+id+"/"+filename+".png"
  
  #HTML Message Part
  html = """\
  <!DOCTYPE html>
  <html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta name="x-apple-disable-message-reformatting">
    <title></title>
    <!--[if mso]>
    <noscript>
      <xml>
        <o:OfficeDocumentSettings>
          <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
      </xml>
    </noscript>
    <![endif]-->
    <style>
      table, td, div, h1, p {font-family: Arial, sans-serif;}
    </style>
  </head>
  <body style="margin:0;padding:0;">
    <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;background:#ffffff;">
      <tr>
        <td align="center" style="padding:0;">
          <table role="presentation" style="width:850px;border-collapse:collapse;border:1px solid #cccccc;border-spacing:0;text-align:left;">
            <tr>
              <td align="center" style="padding:40px 0 30px 0;background:#70bbd9;">
                <img src="https://xti-reporting-grafana-prod.s3.ap-southeast-1.amazonaws.com/xti_white.png" alt="" width="300" style="height:auto;display:block;" />
              </td>
            </tr>
            <tr>
              <td style="padding:36px 30px 42px 30px;">
                <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                  <tr>
                    <td style="padding:0 0 36px 0;color:#153643;">
                      <h1 style="font-size:20px;margin:0 0 20px 0;font-family:Arial,sans-serif;">Report """+datefrom+""" - """+dateto+"""</h1>
                      <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. In tempus adipiscing felis, sit amet blandit ipsum volutpat sed. Morbi porttitor, eget accumsan et dictum, nisi libero ultricies ipsum, posuere neque at erat.</p>
                      <p style="margin:0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"><a href="http://www.example.com" style="color:#ee4c50;text-decoration:underline;">In tempus felis blandit</a></p>
                    </td>
                  </tr>

                <tr>
                  <td style="padding:0;">
                    <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                      <tr>
                        <td style="width:400px;padding:0;vertical-align:top;color:#153643;">
                          <p style="margin:0;font-size:16px;line-height:10px;font-family:Arial,sans-serif;"><h1 style="font-size:20px;margin:0 0 20px 0;font-family:Arial,sans-serif;">CPU Usages</h1></p>  
                          <p style="margin:0 0 25px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"><img src="https://thumb.xti.app/?url="""+img+"""&w=730&h=435&c=tl&q=50" alt="CPU Usage" width="390" style="height:auto;display:block;" /></p>
                          <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. In tempus adipiscing felis, sit amet blandit ipsum volutpat sed. Morbi porttitor, eget accumsan dictum, est nisi libero ultricies ipsum, in posuere mauris neque at erat.</p>
                          <p style="margin:0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"><a href="http://www.example.com" style="color:#ee4c50;text-decoration:underline;">Blandit ipsum volutpat sed</a></p>
                        </td>
                        <td style="width:20px;padding:0;font-size:0;line-height:0;">&nbsp;</td>
                        <td style="width:400px;padding:0;vertical-align:top;color:#153643;">
                          <p style="margin:0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"><h1 style="font-size:20px;margin:0 0 20px 0;font-family:Arial,sans-serif;">Memory Usage</h1></p>
                          <p style="margin:0 0 25px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"><img src="https://thumb.xti.app/?url="""+img+"""&w=730&h=435&c=tr&q=50" alt="Memory Usage" width="390" style="height:auto;display:block;" /></p>
                          <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;">Morbi porttitor, eget est accumsan dictum, nisi libero ultricies ipsum, in posuere mauris neque at erat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. In tempus adipiscing felis, sit amet blandit ipsum volutpat sed.</p>
                          <p style="margin:0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"><a href="http://www.example.com" style="color:#ee4c50;text-decoration:underline;">In tempus felis blandit</a></p>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>

                <tr><td style="height:30px;padding:0;font-size:0;line-height:0;">&nbsp;</td></tr>

                <tr>
                  <td style="padding:0;">
                    <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                      <tr>
                        <td style="width:400px;padding:0;vertical-align:top;color:#153643;">
                          <p style="margin:0;font-size:16px;line-height:10px;font-family:Arial,sans-serif;"><h1 style="font-size:20px;margin:0 0 20px 0;font-family:Arial,sans-serif;">Storage Usage & Total Nodes</h1></p> 
                          <p style="margin:0 0 25px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"><img src="https://thumb.xti.app/?url="""+img+"""&w=1450&h=390&c=center&q=50" alt="Storage Usage & Total Nodes" width="800" style="height:auto;display:block;" /></p>
                          <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. In tempus adipiscing felis, sit amet blandit ipsum volutpat sed. Morbi porttitor, eget accumsan dictum, est nisi libero ultricies ipsum, in posuere mauris neque at erat.</p>
                          <p style="margin:0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"><a href="http://www.example.com" style="color:#ee4c50;text-decoration:underline;">Link Storage</a></p>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
                <tr><td style="height:30px;padding:0;font-size:0;line-height:0;">&nbsp;</td></tr>
                <tr>
                  <td style="padding:0;">
                    <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                      <tr>
                        <td style="width:400px;padding:0;vertical-align:top;color:#153643;">
                          <p style="margin:0;font-size:16px;line-height:10px;font-family:Arial,sans-serif;"><h1 style="font-size:20px;margin:0 0 20px 0;font-family:Arial,sans-serif;">Network Maximum</h1></p>  
                          <p style="margin:0 0 25px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"><img src="https://thumb.xti.app/?url="""+img+"""&w=730&h=435&c=bl&q=50" alt="Network Maximum" width="390" style="height:auto;display:block;" /></p>
                          <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. In tempus adipiscing felis, sit amet blandit ipsum volutpat sed. Morbi porttitor, eget accumsan dictum, est nisi libero ultricies ipsum, in posuere mauris neque at erat.</p>
                          <p style="margin:0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"><a href="http://www.example.com" style="color:#ee4c50;text-decoration:underline;">Blandit ipsum volutpat sed</a></p>
                        </td>
                        <td style="width:20px;padding:0;font-size:0;line-height:0;">&nbsp;</td>
                        <td style="width:400px;padding:0;vertical-align:top;color:#153643;">
                          <p style="margin:0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"><h1 style="font-size:20px;margin:0 0 20px 0;font-family:Arial,sans-serif;">Network Average</h1></p>
                        
                          <p style="margin:0 0 25px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"><img src="https://thumb.xti.app/?url="""+img+"""&w=730&h=435&c=br&q=50" alt="" width="390" style="height:auto;display:block;" /></p>
                          <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;">Morbi porttitor, eget est accumsan dictum, nisi libero ultricies ipsum, in posuere mauris neque at erat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. In tempus adipiscing felis, sit amet blandit ipsum volutpat sed.</p>
                          <p style="margin:0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"><a href="http://www.example.com" style="color:#ee4c50;text-decoration:underline;">In tempus felis blandit</a></p>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>


                </table>
              </td>
            </tr>
            <tr>
              <td style="padding:30px;background:#ee4c50;">
                <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;font-size:9px;font-family:Arial,sans-serif;">
                  <tr>
                    <td style="padding:0;width:50%;" align="left">
                      <p style="margin:0;font-size:14px;line-height:16px;font-family:Arial,sans-serif;color:#ffffff;">
                        &reg; Someone, Somewhere 2021<br/><a href="http://www.example.com" style="color:#ffffff;text-decoration:underline;">Unsubscribe</a>
                      </p>
                    </td>
                    <td style="padding:0;width:50%;" align="right">
                      <table role="presentation" style="border-collapse:collapse;border:0;border-spacing:0;">
                        <tr>
                          <td style="padding:0 0 0 10px;width:38px;">
                            <a href="http://www.twitter.com/" style="color:#ffffff;"><img src="https://assets.codepen.io/210284/tw_1.png" alt="Twitter" width="38" style="height:auto;display:block;border:0;" /></a>
                          </td>
                          <td style="padding:0 0 0 10px;width:38px;">
                            <a href="http://www.facebook.com/" style="color:#ffffff;"><img src="https://assets.codepen.io/210284/fb_1.png" alt="Facebook" width="38" style="height:auto;display:block;border:0;" /></a>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
  </html>
  """

  part = MIMEText(html, "html")
  msg.attach(part)

  # Add Attachment
  with open("assets/"+id+"_"+filename+".png", "rb") as attachment:
      part = MIMEBase("application", "octet-stream")
      part.set_payload(attachment.read())
    
  encoders.encode_base64(part)

  # Set mail headers
  part.add_header(
      "Content-Disposition",
      "attachment", filename= "assets/"+id+"_"+filename+".png"
  )
  msg.attach(part)
  connection = smtplib.SMTP(host=os.getenv("MAIL_SMTP"), port=os.getenv("MAIL_PORT"))
  connection.starttls()
  connection.login(sender_email,password)
  connection.send_message(msg)
  connection.quit()
