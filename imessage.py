import utils
import sqlite3
from datetime import datetime
import config

def get_messages(phone_number, output, sender, recipient):
    handle_ids = utils.get_handle_ids(phone_number)
    if not handle_ids:
        print(f"No handle IDs found for {phone_number}")
        return

    handle_id = handle_ids[0]

    conn = sqlite3.connect(config.PATH_TO_DB)
    cursor = conn.cursor()

    query = """
    SELECT datetime(message.date / 1000000000 + strftime('%s', '2001-01-01'), 'unixepoch', 'localtime') as date,
           message.text,
           message.is_from_me,
           message.attributedBody
    FROM message
    WHERE handle_id = ?
    ORDER BY date ASC
    """

    cursor.execute(query, (handle_id,))
    messages = cursor.fetchall()

    conn.close()

    if not messages:
        print(f"No messages found for handle ID {handle_id}")
        return

    for date, text, is_from_me, attributed_body in messages:
        msg_sender = sender if is_from_me else recipient
        if is_from_me:
            global sender_msg_count
            sender_msg_count += 1
        else:
            global recipient_msg_count
            recipient_msg_count += 1
        formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %I:%M:%S %p")
        decoded = False
        if text is None:
            if attributed_body is not None:
                text = utils.decode_attributed_body(attributed_body.hex())
                decoded = True
        
        # Replace newlines and commas with escape characters
        if text:
            text = text.replace('\n', '\\n').replace('\r', '\\r').replace('"', "'")
            text = f"\"{text}\""
        
        output.append(f"{formatted_date}{config.DELIMITER}{msg_sender}{config.DELIMITER}{text}{config.DELIMITER}{decoded}")



while True:
    output = ["time,sender,message,decoded"]

    sender = input("Your name: ")
    recipient = input("Recipient's name: ")
    phone_number = input("Phone number: ")

    sender_msg_count = 0
    recipient_msg_count = 0

    get_messages(phone_number, output, sender, recipient)

    with open(f"output/{sender}-{recipient}.csv", "w") as f:
        f.write(config.NEWLINE.join(output))

    print(f"Wrote {sender_msg_count} messages from {sender} to {recipient} to output/{sender}-{recipient}.csv")
    print(f"Wrote {recipient_msg_count} messages from {recipient} to {sender} to output/{sender}-{recipient}.csv")

    continue_option = input("Do you want to continue? (y/n): ")
    if continue_option.lower() != 'y':
        print("Thank you for using this tool! Check out my other projects at https://github.com/siddhxrth !")
        break