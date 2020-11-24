import random
import sys
import smtplib
from email.message import EmailMessage


class Santa:
    def __init__(self, name, prev, email):
        self.name = name
        self.prev = prev
        self.email = email
        self.recipient = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def assign_recips():
    santas = []

    # Get santa info from santa.txt file
    with open('santa.txt') as santafile:
        for line in santafile:
            linesplit = line.strip().split('-')
            santas.append(Santa(linesplit[0], linesplit[1], linesplit[2]))

    # copy original list for available list
    available_recipients = santas.copy()

    for santa in santas:
        get_recipient(santa, available_recipients)

    return santas


def get_recipient(santa: Santa, available: list):
    valid = available.copy()
    for recip in available:
        if recip.name == santa.name:
            valid.remove(recip)
        if recip.name == santa.prev:
            valid.remove(recip)

    try:
        rand = random.randint(0, len(valid) - 1)
        next_recip = valid[rand]
        available.remove(next_recip)
        santa.recipient = next_recip
    except:
        print("Not enough valid recipients")
        assign_recips()


if __name__ == '__main__':
    santas = assign_recips()

    # Double check there are no duplicate recipients
    name_dict = {}
    for santa in santas:
        name_dict[santa.name] = 0

        for santa_recip in santas:
            if str(santa.name) == str(santa_recip.recipient):
                name_dict[santa.name] += 1

    # Double check no one has themselves
    for santa in santas:
        if str(santa.name) == str(santa.recipient):
            print(santa.name, 'got himself.')
            sys.exit()

    # Double check no one has their previous recipient
    for santa in santas:
        if str(santa.prev) == str(santa.recipient):
            print(santa.name, 'got their previous recipient')
            sys.exit()

    # Double check that everyone is a recipient at least once
    for recipient in name_dict.keys():
        if name_dict[recipient] == 0:
            print(recipient, 'was never selected as a recipient')
            sys.exit()

    gmail_user = 'troykollar@gmail.com'
    gmail_pass = 'password'

    msg = EmailMessage()
    msg['From'] = 'troykollar@gmail.com'
    msg['Subject'] = 'Test'
    msg.set_content('This is the test message')

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_pass)
    except:
        print('Something went wrong...')

    for santa in santas:
        print(santa.recipient)
        msg = EmailMessage()
        msg['From'] = 'troykollar@gmail.com'
        msg['Subject'] = 'Secret Santa'
        msg.set_content(
            'This message is intended for ' + santa.name + ' at ' +
            santa.email + '\n' + str(santa.name) + ' you have been assigned ' +
            str(santa.recipient) +
            ' for Secret Santa.\n\nThe following people were selected as recipients this many times\n'
            + str(name_dict))
        server.send_message(msg, gmail_user, santa.email)
