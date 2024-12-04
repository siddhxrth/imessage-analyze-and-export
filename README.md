# iMessage Conversation Analyzer & Exporter
### Command Line Interface to Analyze iMessage Conversations and Export All Messages into a .csv File, Perfect for Data Hoarders or If You Want to Archive Old Conversations!

[![Star History Chart](https://api.star-history.com/svg?repos=siddhxrth/imessage-analyze-and-export&type=Date)](https://star-history.com/#siddhxrth/imessage-analyze-and-export&Date)

## Requirements:
* You need a computer running MacOS (either a real Mac or a Hackintosh)
  * Your Apple services have to be functional (including iMessage)
  
## Setup

1. The ONLY setup you have to do to get this program running is to provide a path to your messages database file in [config.py](config.py) (`PATH_TO_DB`). For most users, you can locate it here: `Users/your-username/Library/Messages/chat.db)`
2. By default, though, this file is protected, so you have to either grant the application Full Disk Access in System Preferences or you can copy chat.db to a location of your choice (I found this option easier)
3. **OPTIONAL:** There are customization options available in [config.py](config.py) if you wish to use a different delimiter (the program uses `,` by default). You can also customize how you want to separate messages in the exported file (by default, the program uses a newline character (`\n`))

## How to Run:
1. Ensure you have Python installed on your system
2. Navigate to the directory containing the script in your terminal
3. Run the script using the command: `python imessage.py`
4. Follow the prompts to enter your name, the recipient's name, and the phone number for the conversation you want to analyze

## How It Works:
* Apple stores message history in a SQLite Database at `/Users/your-username/Library/Messages/chat.db`
  * You can access this like a regular SQL DB & perform queries, which is how this program fetches messages
* Each person you've sent/received a message from has their own unique `handle_id` - this is how Apple differentiates who the messages are for and who sent them, and this is also how the data is stored in the database (which is how this program gets the messages)
* To analyze and save a conversation, simply run the program and input your name, the other person's name, and their phone number. The tool will automatically determine the correct `handle_id` internally. It will then fetch all matching messages and export them into a .csv file in the program directory with the names you inputted earlier. The file will contain each message, its date, and whether it was decoded from attributed body. The program will also print out how many total messages there were, and how many messages you've sent compared to how many messages the other person has sent.
  
## Database Structure:
* Apple's SQLite Database for storing message follows a typical SQL Format (nothing proprietary to Apple)! These are all of the tables in the Database, but this program currently only accesses records in the `message` table. Other tables contain other information as well, such as local locations to the attachments but for now this program can only access messages.
  * `_SqliteDatabaseProperties`
  * `deleted_messages`
  * `sqlite_sequence`
  * `chat_handle_join`
  * `chat_message_join`
  * `message_attachment_join`
  * `handle`
  * `message`
  * `chat`
  * `attachment`
  * `sync_deleted_messages`
  * `message_processing_task`
  * `sync_deleted_chats`
  * `sync_deleted_attachments`
  * `kvtable`
  * `sqlite_stat1`
  
* **FYI:** The `message` table is where Apple stores all of the messages - this is what this program queries to get all messages.

* Some notable columns in the `message` table:
  * `is_from_me`
  * `date`
  * `text`
  * `attributedBody`

The `is_from_me` value for a record is 1 if the message was sent from you or 0 if you received the message. The `date` value is message timestamp, and the `text` field contains the contents of the message. 


**Update:** For many messages, the `text` field may be empty. In these cases, the program decodes the message content from the `attributedBody` field to ensure all messages are captured.



## About:
Hi! I'm Sid, a software engineer studying CS at Georgia Tech. I love making little scripts like this that make life more convenient :grin: If you found this useful, star the repo and give me a follow to stay updated on more scripts & tools that I make! PRs are open for this so if you would like to add a new feature, be sure to add it and open a PR.
You can see some of the other projects I've created on my [website](https://siddharthlohani.dev)!
