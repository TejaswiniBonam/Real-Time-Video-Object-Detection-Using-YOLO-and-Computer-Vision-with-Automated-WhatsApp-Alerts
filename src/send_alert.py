from twilio.rest import Client
from values import needed
import time

values=needed()
devices = ['whatsapp:+918328044665', 'whatsapp:+919951280286', 'whatsapp:+919951280286', 'whatsapp:+919951280286']

def twilio_alert(X, Y, ngrok_link, name, alert_type, index, device_no, fm):
    #print(X, Y)
    client = Client(X, Y)
    face_details = "None"
    if fm is not None and len(fm)>0:
        face_details = "\n".join(fm)

    urls=['/screenshots/','/screen_recordings/', face_details]
    
    url = ngrok_link + urls[index] + name
    if alert_type==3:
        url = face_details
    if alert_type==4:
        url=''
    #print(url)
    #print(name)
    alert = ["We found someone roaming at your place, Please reply with 'yes' if there is a need for emergency act or else 'no' ",
              "🔴EMERGENCY AT House No 123 Main Street, Anytown, CA 12345🔴", 
              "This is the screen recording.",
              "Face recognition details",
              "Oh it's you!! Dont worry we are still On guard and watching everything."]
    message = client.messages.create(
    from_='whatsapp:+14155238886',
    to=devices[device_no],
    #body= '🔴EMERGENCY AT House No 123 Main Street, Anytown, CA 12345🔴',
    #media_url= ngrok_link + '/screenshots/' + name
    body = alert[alert_type] + "\n\n" + url,
    )
    print("Message sid: ", message.sid)



def user_reply(X, Y, device_no):
    client = Client(X, Y)
    time.sleep(3)
    
    last_message = client.messages.list(to=devices[device_no], limit=1)
    #print(last_message[0].body)

    
    if not last_message: 
        return "-"
    
    text = last_message[0].body.strip().lower()    
    if "yes" in text[10:13]:
        return "yes"
        twilio_alert(values['device1_x'], values['device1_y'], values['ngrok_link'], 0, 2)  
    elif "no" in text[10:12]:
        return "no"
    
    return "-"

#print(user_reply(values['device1_x'], values['device1_y']))