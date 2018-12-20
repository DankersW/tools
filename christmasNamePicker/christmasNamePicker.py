import smtplib
from random import shuffle

# Login credentials email
own_email = 'secret.santa.fam.dankers@gmail.com'
own_pwd = 'wouterdankers'

receiver_email = []
names = []
names_copy = []

stdMessage = ", u moet een cadautje ter waarde van 20 euro kopen voor: "

# Setup email server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(own_email, own_pwd)


def shuffle_and_compare():
    global names_copy
    names_copy = list(names)
    shuffle(names_copy)

    for j in range(len(names)):
        if names[j] == names_copy[j]:
            return False
    return True


with open('emailFile.txt', 'r') as f:
    appendData = []
    for line in f:
        receiver_email.append(line.strip())
        buffer = line.strip().split('@', 1)[0]
        buffer = buffer.replace(".", " ")
        names.append(buffer)

while not (shuffle_and_compare()):
    pass

# send email
for i in range(len(receiver_email)):
    message = "\n\n" + names[i] + stdMessage + names_copy[i]
    server.sendmail(own_email, receiver_email[i], str(message))

server.quit()
