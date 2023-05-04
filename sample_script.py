from src.message_parse_engine import HgMsgParser


def main():
    email_msg_parse = HgMsgParser(level="info")

    test_sort(email_msg_parse)
    test_message_properties(email_msg_parse)

def test_sort(email_msg_parse):

    email_msg_parse.read_messages_in_dir(source_directory="data/", recurse=True)

    email_msg_parse.sort_messages(output_directory="export/my_exported_emails")

def test_message_properties(email_msg_parse):
    email_msg_parse.read_messages_in_dir(source_directory="data/", recurse=True)

    for message in email_msg_parse.all_read_messages:
        print(message['message_item'].message_subject)

if __name__ =='__main__':
    main()

