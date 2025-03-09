from twilio.rest import Client
from values import needed
values=needed()
def twilio_alert(X, Y, ngrok_link, name, alert_type,index, device_no, fm):
    #print(X, Y)
    client = Client(X, Y)
    face_details = "None"
    if fm is not None and len(fm)>0:
        face_details = "\n".join(fm)

    urls=['/screenshots/','/screen_recordings/', face_details]
    devices = ['whatsapp:+918328044665', 'whatsapp:+919951280286']
    url = ngrok_link + urls[index] + name
    if alert_type==3:
        url = face_details
    print(url)
    print(name)
    alert = ["We found someone roaming at your place, face recognition details will be updated soon", "🔴EMERGENCY AT House No 123 Main Street, Anytown, CA 12345🔴", "This is the screen recording.", "Face recognition details"]
    message = client.messages.create(
    from_='whatsapp:+14155238886',
    to=devices[device_no],
    #body= '🔴EMERGENCY AT House No 123 Main Street, Anytown, CA 12345🔴',
    #media_url= ngrok_link + '/screenshots/' + name
    body = alert[alert_type] + "\n\n" + url,
    )
    print(message.sid)




import time

def user_reply(X, Y):
    client = Client(X, Y)
    time.sleep(3)
    
    last_message = client.messages.list(to='whatsapp:+918328044665', limit=1)
    
    if not last_message: 
        return None
    
    text = last_message[0].body.strip().lower()    
    if "yes" in text:
        return "yes"
        twilio_alert(values['device1_x'], values['device1_y'], values['ngrok_link'], 0, 2)  
    elif "no" in text:
        return "no"
    
    return None