from src.message_parse_engine import HgMsgParser


def main():
    email_msg_parse = HgMsgParser()
    # email_msg_parse.read_message(source_message="data/sub1/sub2/sub3/ANOTHER LEVEL/BeProactive_BeforeThis_Springwith_LeafFilter.eml")
    email_msg_parse.read_messages_in_dir(source_directory="data/", recurse=True)
    # for message in email_msg_parse.all_read_messages:
    #     print(message['message_item'].message_subject)

    email_msg_parse.sort_messages(output_directory="export/my_exported_emails")

if __name__ =='__main__':
    main()

