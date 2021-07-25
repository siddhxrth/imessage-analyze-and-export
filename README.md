# imessage conversation analyzer & exporter
### command line interface to analyze iMessage conversations and export all messages into a .csv file, perfect for data hoarders or if you want to archive old conversations!

## requirements:
* you need a computer running MacOS (either a real Mac or a Hackintosh)
  * your apple services have to be functional (including iMessage)
  
## setup

1. the ONLY setup you have to do to get this program running is to provide a path to your messages database file in [setup.py](setup.py) (```chat.db```). for most users, you can locate it here: ```Users/your-username/Library/Messages/chat.db)```
2. by default though this file is protected, so you have to either grant the application Full Disk Access in System Preferences or you can copy chat.db to a location of your choice (i found this option easier)
3. **OPTIONAL:** there are customization options available if you wish to use a different delimiter (the program uses ```,``` by default. you can also customize how you want to separate messages in the exported file (by default, the program uses a newline character (```\n```)

## how it works:
* Apple stores message history in a SQLite Database at ```/Users/your-username/Library/Messages/chat.db```
  * you can access this like a regular SQL DB & perform queries, which is how this program fetches messages
* each person you've sent/recieved a message from has their own unique ```handle_id``` - this is how Apple differentiates who the messages are for and who sent them, and this is also how the data is stored in the database (which is how this program gets the messages)
* you can open an SQL client or use the terminal to fetch recent messages and their ```handle_id``` to determine who the ```handle_id``` is associated with
  * this is pretty basic SQL so i won't go in too much detail but here is an SQL query you can run:
  
```SQL
    SELECT
        is_from_me,
        datetime(substr(date, 1, 9) + 978307200, 'unixepoch', 'localtime') as f_date,
        text,
        handle_id
    FROM MESSAGE LIMIT 100;

```

* for example, the above SQL query will return 100 records that include the values from the ```text```, ```date```, ```handle_id```, and ```is_from_me``` columns - you should be able to look at what it returns to determine which ```handle_id``` corresponds to people
* once you determine the ```handle_id``` for the conversation you want to analyze/save, you can run the program and input your name, the other person's name, and the ```handle_id```. the tool will fetch all matching messages and export them into a .csv file in the program directory with the person's name that you inputted earlier. it will contain each message, its date, and its id. the program will also print out how many total messages there were, and how many messages you've sent compared to how many messages the other person has sent.
  
## database structure:
* Apple's SQLite Database for storing message follows a typical SQL Format (nothing proprietary to Apple)! These are all of the tables in the Database, but this program currently only accesses records in the ```message``` table. Other tables contain other information as well, such as local locations to the attachments but for now this program can only access messages.
  * ```_SqliteDatabaseProperties```
  * ```deleted_messages```
  * ```sqlite_sequence```
  * ```chat_handle_join```
  * ```chat_message_join```
  * ```message_attachment_join```
  * ```handle```
  * ```message```
  * ```chat```
  * ```attachment```
  * ```sync_deleted_messages```
  * ```message_processing_task```
  * ```sync_deleted_chats```
  * ```sync_deleted_attachments```
  * ```kvtable```
  * ```sqlite_stat1```
  
* **FYI:** the ```message``` table is where Apple stores all of the messages - this is what this program queries to get all messages.

* some notable columns in the ```message``` table:
  * ```is_from_me```
  * ```date```
  * ```text```

the ```is_from_me``` value for a record is 1 if the message was sent from you or 0 if you recieved the message. the ```date``` value is the number of nanoseconds that have passed since january 1st, 2001, and the ```text``` field contains the contents of the message.

## about:
hi! i'm sid, a full stack dev from new jersey currently in highschool. i love making little scripts like this that make life more convenient :grin: if you found this useful, star the repo and give me a follow to stay updated on more scripts & tools that i make! PRs are open for this so if you would like to add a new feature, be sure to add it and open a PR.
 you can see some of the other projects i've created on my [website](https://siddharthlohani.dev) or check out my [Twitter](https://twitter.com/sidlohani)!













