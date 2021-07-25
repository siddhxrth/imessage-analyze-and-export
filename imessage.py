import sqlite3
from datetime import datetime
import setup

# CONNECT TO DATABASE
conn = sqlite3.connect(setup.PATH_TO_DB)
cur = conn.cursor()

YOUR_NAME = input("Hello! To begin, what is your name? ")

while True:

    NAME_OF_CONTACT = input("What is the sender's name? ")
    HANDLE_ID = input("What is %s's handle_id? " % NAME_OF_CONTACT)

    # QUERY SENDER, DATE/TIME, AND TEXT FOR EACH RECORD IN MESSAGE TABLE FROM SPECIFIED SENDER
    cur.execute( 
    '''
    SELECT
    is_from_me,
    datetime(substr(date, 1, 9) + 978307200, 'unixepoch', 'localtime') as f_date,
    text
    FROM MESSAGE
    WHERE handle_id = %s;
    ''' % HANDLE_ID
    ) 

    # VARIABLES THAT HOLDS NUMBER OF MESSAGES FOUND
    id = 0
    your_messages = 0
    recieved_messages = 0


    # CLEAR OUTPUT.CSV FILE
    with open('./%s.csv' % NAME_OF_CONTACT.replace(" ", ''), 'w') as output:
        output.write('')
        output.close()

    # ITERATE THROUGH EACH RECORD AND WRITE A NEW LINE WITH DATE, TEXT & MESSAGE ID
    with open('./%s.csv' % NAME_OF_CONTACT.replace(" ", ''), 'a') as output:
        
        output.write('date, message, id')

        for record in cur.fetchall():
            if(record[0] == 0):
                if not(record[2] == ' '):
                    output.write(setup.NEWLINE + str(record[1]) + setup.DELIMITER + NAME_OF_CONTACT + ": " + str(record[2]).replace("\n", ' ') + setup.DELIMITER + str(id))
                    recieved_messages += 1
            else:
                if not(record[2] == ' '):
                    output.write(setup.NEWLINE + str(record[1]) + setup.DELIMITER + YOUR_NAME + ": " + str(record[2]).replace("\n", ' ') + setup.DELIMITER + str(id))
                    your_messages += 1
            id += 1
        
        output.close()

    print("Found %s messages between %s and %s! Check \"./%s.csv\" for a list of them. Out of the %s total messages, you sent %s of them and %s sent %s of them." % (id, YOUR_NAME , NAME_OF_CONTACT, NAME_OF_CONTACT.replace(" ", '') ,id, your_messages, NAME_OF_CONTACT, recieved_messages))

    loop = input("Do you want to analyze another conversation? (y/n) ")

    if not (loop.lower() == 'y'):
        print("Thank you for using this tool! Check out more of my projects on GitHub: https://github.com/siddhxrth")
        conn.close()
        cur.close()
        break