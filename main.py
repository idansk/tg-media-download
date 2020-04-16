import os
import shutil
from tqdm import tqdm
from telethon import TelegramClient, events, sync
from telethon.tl.types import InputMessagesFilterDocument


api_id = 000000
api_hash = "00000000000000000000000000000000"
client =  TelegramClient('tgBotSession', api_id, api_hash)

client.start()
dialogs = client.get_dialogs()
for i, dialog in enumerate(dialogs):
        if dialog.name:
            print(f"{i+1}. {dialog.name}")
        else:
            print(f"{i+1}. Deleted Account | ID={dialog.entity.id}")

while True:
        try:
            selected_dialog = int(input("\nPlease enter dialog number: "))
            if not (1 <= selected_dialog <= len(dialogs)):
                raise ValueError
            break
        except ValueError:
            print("Entered value is incorrect. Please try again...")

print()

dialog = dialogs[selected_dialog - 1]
entity = dialog.entity

messages = [
        message
        for message in client.iter_messages(entity, filter=InputMessagesFilterDocument, reverse=True)
    ]  

if messages:
        saved_filenames = list()
        directory_name = dialog.name if dialog.name else str(dialog.entity.id)

    if not os.path.exists(directory_name):
            os.makedirs(directory_name)
    #else:
            #shutil.rmtree(directory_name)
            #os.makedirs(directory_name)

    for message in tqdm(messages):
            at_least_one_media_file_present = True
            if (os.path.exists(directory_name+'/'+message.file.name)):
                    print(message.file.name + ' Already Exists, skipping')
            else:
                saved_filenames.append(message.file.name)
                message.download_media(directory_name)

    print(f"\n✅ Successfully downloaded following files to `{directory_name}` folder:")

    for filename in saved_filenames:
            print(filename)
else:
        print(f"\n❌ Could not find any media files.")
