# Creator : Vinura Yashohara (AnonyMSAV) | Contact : t.me/AnonyMSAV
# Enrollment application.
import imghdr
import os
import platform
import random
import smtplib
import sqlite3
import pathlib
import qrcode
from email.message import EmailMessage
import cv2 as cv
import pyzbar.pyzbar as pyzbar
import termcolor

# Current path.
path = pathlib.Path(__file__).parent.resolve()

# Connect database.
connecter = sqlite3.connect(f'{path}\db.sql')
cursor = connecter.cursor()


# Generate token for user.
def token(tokens):

    # Generate number between 1000 and 9999.
    number = random.randrange(1000, 9999)

    # Check the generated number already exists or not, if not it returns.
    if tokens == []:

        return number

    for i in tokens:

        if number != i:

            return number


# Generate QR code and sent it the user's email.
def sender(number, email):

    # QR code generator.
    data = number
    path = 'invitation_token.png'
    image = qrcode.make(data)
    image.save(path)

    # Emailing the generated QR code.
    sender_email = 'Your email address.'
    receiver_email = email
    email_pass = 'Go and generate App password https://myaccount.google.com/security?hl=en_GB and enter it to this space.'

    with open(path, 'rb') as file:
        img_data = file.read()
        img_type = imghdr.what(file.name)
        img_name = file.name

    # Body of the email.
    msg = EmailMessage()
    msg['Subject'] = "Invitation For EMS'ERA 21"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.add_attachment(img_data, maintype='image',
                       subtype=img_type, filename=img_name)

    # Email sending process.
    try:

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(sender_email, email_pass)
        server.sendmail(sender_email, receiver_email, msg.as_string())

        print(termcolor.colored(
            f'\nInvitaion successfully sent to {termcolor.colored(email,"red")}.', 'yellow'))

    except:

        print(termcolor.colored(
            '\nAn Error occured, check the email address again!', 'red'))

        # Delete user from the database if the details are wrong.
        cursor.execute(f'DELETE FROM data_table WHERE Number = {number};')
        connecter.commit()


# Database access.
def database(data, email):

    # Check table is already exist or not.
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS data_table(ID INTEGER PRIMARY KEY, Name TEXT, Number INTEGER, Email TEXT);')

    # SQL query.
    payload = 'INSERT INTO data_table(Name, Number, Email) VALUES(?, ?, ?);'

    # For Token Number Generating.
    check = cursor.execute('SELECT Number FROM data_table;')

    tokens = [i for i in check]

    number = token(tokens)

    cursor.execute(payload, (data, number, email))

    connecter.commit()

    result = cursor.execute(
        'SELECT * FROM data_table WHERE ID=(SELECT MAX(id) FROM data_table);')

    for i in result:

        sender(i[2], i[3])


# For add members and their emails to the database.
def add_member():

    name = input(termcolor.colored('\nName', 'blue') +
                 ' ' + termcolor.colored(':', 'yellow') + ' ')
    email = input(termcolor.colored('\nEmail Address', 'blue') +
                  ' ' + termcolor.colored(':', 'yellow') + ' ')

    if name != '' and email != '':

        database(name, email)


# For checking current database.
def check_database():

    data = []

    connecter = sqlite3.connect(f'{path}\db.sql')
    cursor = connecter.cursor()

    try:

        result = cursor.execute('SELECT * FROM data_table;')

        for i in result:

            data.append(
                f'Name : {i[1]}, Token Number : {i[2]}, Email Address : {i[3]}')

        for i in data:

            print(termcolor.colored(f'\n{i}', 'yellow'))

    except sqlite3.OperationalError:

        print(termcolor.colored('\nNothing!', 'red'))


# For access the webcam.
capture = cv.VideoCapture(0)
decorder = cv.QRCodeDetector()


# For validation of the QR code.
def qrcode_reader():

    while True:

        # Get image data from webcam.
        # Outputs of cv.VideoCapture(0) is result and image.
        # result --> Check image is captured or not (Boolean value), but now I'm not going to use it so I didn't use it.
        # image --> Capture frame(image) and return its pixel metrix.
        _, image = capture.read()

        # Show captured frames (images).
        cv.imshow('Image', image)

        # Filter data from QR code.
        data = pyzbar.decode(image, symbols=[pyzbar.ZBarSymbol.QRCODE])

        try:

            for i in data:

                data = int(i[0])

        except ValueError:
            continue

        # Access database and check the invitaion number is present or not.
        try:

            result = cursor.execute('SELECT Number FROM data_table;')

            for i in result:

                if data == i[0]:

                    print(termcolor.colored('\nAccess Granted', 'green'))

                    # Delete the user data from the database after access granted.
                    cursor.execute(
                        f'DELETE FROM data_table WHERE Number = {data};')
                    connecter.commit()

        except:

            print(termcolor.colored(
                '\nNothing in the database!', 'red'))

            break

        cv.waitKey(1)


# Check system os type.
def check_system():

    system = platform.platform()

    if 'Linux' in system:

        os.system('clear')

    elif 'Windows' in system:

        os.system('cls')


# The main function.
def main():

    check_system()

    banner = termcolor.colored('''
    
                ███████╗███╗   ███╗███████╗  ███████╗██████╗  █████╗     ██████╗  ██╗
                ██╔════╝████╗ ████║██╔════╝  ██╔════╝██╔══██╗██╔══██╗    ╚════██╗███║
                █████╗  ██╔████╔██║███████╗  █████╗  ██████╔╝███████║     █████╔╝╚██║
                ██╔══╝  ██║╚██╔╝██║╚════██║  ██╔══╝  ██╔══██╗██╔══██║    ██╔═══╝  ██║
                ███████╗██║ ╚═╝ ██║███████║  ███████╗██║  ██║██║  ██║    ███████╗ ██║
                ╚══════╝╚═╝     ╚═╝╚══════╝  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚══════╝ ╚═╝

                Created By : Vinura Yashohara                                                              
    ''', 'blue')
    print(banner)

    print(termcolor.colored(f'''\n
+=========+
| OPTIONS |
+=========+

{termcolor.colored('{1}. Add new member and send invitaion.','yellow')}
{termcolor.colored('{2}. Show current database.','yellow')}
{termcolor.colored('{3}. Check QR Code validation.','yellow')}''', 'red'))

    try:

        option = int(input(termcolor.colored('\nEnter', 'blue') + ' ' +
                     termcolor.colored(':', 'yellow') + ' '))

        if option == 1:

            add_member()

        elif option == 2:

            check_database()

        elif option == 3:

            qrcode_reader()

        else:

            print(termcolor.colored('\nHappy Hacking!', 'blue'))
            exit()

    except ValueError:

        exit()


# Entrance of the program.
if __name__ == '__main__':
    main()
