import smtplib

server = smtplib.SMTP('smtp.gmail.com',587)
server.ehlo()
server.starttls()
server.ehlo()

server.login('khantaha4210@gmail.com','pjgnnbetxhxamaml')
subject = "Test"
body = 'Check the amazon link'

msg = f"Subject:{subject}\n\n{body}"

server.sendmail(
        'khantaha4210@gmail.com',
        'mtahakhan93@gmail.com',
        msg
        )