import sqlite3
from datetime import datetime
import struct
import plistlib
from io import BytesIO
import re
import config

def get_handle_ids(phone_number):

    conn = sqlite3.connect(config.PATH_TO_DB)
    cursor = conn.cursor()

    query = """
    SELECT ROWID
    FROM chat
    WHERE chat_identifier = ?
    """

    cursor.execute(query, (phone_number,))
    results = cursor.fetchall()
    chat_ids = [row[0] for row in results]
    if not len(chat_ids): return []

    handle_query = """
    SELECT handle_id
    FROM chat_handle_join
    WHERE chat_id IN ({})
    """.format(','.join('?' * len(chat_ids)))

    cursor.execute(handle_query, chat_ids)
    handle_results = cursor.fetchall()
    handle_ids = [row[0] for row in handle_results]
    if not handle_ids: return []

    return list(set(handle_ids))
    conn.close()

    return chat_ids



def decode_attributed_body(attributed_body):
    if not attributed_body:
        return "No attributed body data"

    try:
        # Convert hex string to bytes
        data = bytes.fromhex(attributed_body)
        
        # Convert bytes to string
        text = data.decode('utf-8', errors='ignore')
        
        # Use regex to find the actual content
        match = re.search(r'NSString.*?(\w.*?)(?:\x00|\Z)', text, re.DOTALL)
        if match:
            content = match.group(1)
            # Remove unwanted text from the beginning and end, but keep "Loved"
            content = re.sub(r'^[\d\s]*(?=Loved|.)|(?:")?iI.*?NSDictionary$', '', content).strip()
            return content
        else:
            return "Unable to extract message content"
    except Exception as e:
        return f"Error decoding attributed body: {str(e)}"