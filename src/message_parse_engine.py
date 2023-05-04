import json
import shutil
import pathlib
import logging
import email
from email import policy
from email.parser import BytesParser
from typing import Type, List
from src.msg_exceptions.message_parse_exceptions import  UnableToLocateFile, UnableToWriteFile
from src.msg_helpers.message_logging_base import HgMessageLogger


class HgMsgParsed(HgMessageLogger):
    def __init__(self, message:email.message.EmailMessage, **kwargs):
        """
        :param message: provided email.message.EmailMessage object for processing
        """
        self.read_message = message
        self.message_type = None
        self.extended_options = kwargs
        super().__init__(self.extended_options)

    @property
    def list_available_properties(self):
        """
        using email message object view all extracted properties available
        :return: list of properties that can be called explicitly
        """
        return (self.self.read_message.keys())

    @property
    def message_subject(self) ->str:
        """
        :return: A string wiith the message subject
        """
        return self.read_message["subject"]

    @property
    def message_from(self) ->str:
        """
        :return: A string wiith the message from
        """
        return self.read_message["from"]

    @property
    def message_to(self) ->str:
        """
        :return: A string wiith the message to
        """
        return self.read_message["to"]

    @property
    def message_attachments(self) ->list:
        """
        :return: A list of attachment names in the message
        """
        ...

    @property
    def mask_sensitive_chars(self) ->str:
        ...

    def generate_metadata(self):
        ...


class HgMsgParser(HgMessageLogger):

    def __init__(self, **kwargs):
        """
        Parser class, responsible for reading and retrieving messages. Any read/retrieved messages will be stored in the
        self._all_read_messages attribute. This attribute will be a list that contains dictionaries for each read/retreived
        """

        self.all_read_messages: list[dict[str, type[HgMsgParsed]]] = []

        self.extended_options = kwargs
        super().__init__(self.extended_options)


    def remove_illegal_chars_folder(self, folder_string:str) ->str:
        """
        :param folder_string: string that will be processed to remove any illegal characters
        :return: an updated string with no illegal characters
        """
        illegal_chars = ["<",">",":","\"","/","\\","|","?","*",":"]

        for illegal_char in illegal_chars:
            updated_str=folder_string.replace(illegal_char,";")

        return updated_str

    def read_message(self, source_message:str,
                     internal_dir_call:bool=False,
                     raise_on_error:bool=True)-> email.message.EmailMessage:
        """
        :param source_message: a string pointing to the file that will be read and processing attempted
        :param internal_dir_call: an internal param to track where the call to read_message originated from
        :param raise_on_error: expanding into logging module but currently suppresses some error messages
        :return: an email.message.EmailMessage object
        """
        # only txt/eml supported for now
        try:
            if pathlib.Path(source_message).is_file():

                self.logger.info(f"Attempting to read message {source_message}")

                with open(source_message, 'rb') as message_file:
                    current_message = BytesParser(policy=policy.default).parse(message_file)

                    self.all_read_messages.append({"source_file_location":source_message,
                                                   "message_item":HgMsgParsed(current_message)
                                                   }
                                                  )
                    return current_message
            else:
                if raise_on_error:
                    raise UnableToLocateFile(f'Unable to locate or we do not have access to provided file {source_message}')
        except Exception as e:
            if raise_on_error:
                print(e)

    def read_messages_in_dir(self, source_directory:str, recurse:bool =False) ->None:
        """
        :param source_directory: a string pointing to the foldder that will be read and processing attempted
        :param recurse: will the engine recurse into subdirectories and attempt ingest of identified files
        :return: None
        """
        try:
            for item in pathlib.Path(source_directory).iterdir():
                if item.is_file():

                    self.logger.debug(f"file identified {item}")
                    self.read_message(source_message=item, internal_dir_call=True)
                if item.is_dir() and recurse:

                    self.logger.debug(f"directory identified calling recurse {item}")
                    self.read_messages_in_dir(source_directory=item, recurse=True)
        except Exception as e:
            print(e)

    def extract_attachments(self, view_only:bool=False, message_id:int=None):
        """
        will attempt to extract the attachment from the provided message or all messages currently read.
        :param message_id: attempt to export the attachments from the  provided message_id
        :param view_only: provide a view of what would be extracted
        :return: None
        """

    def sort_messages(self, output_directory:str="export/",
                      include_in_folder_name:str=["Subject"],
                      include_attachments: bool = False,
                      all_message:bool = False,
                      message_id:int=None):
        """

        :param output_directory: the output of sorted messages will be stored here
        :param include_in_folder_name: any supported string identifiers that can be added to the folder name
        :param include_attachments: should we also export all attachments from the captured messages
        :param all_message: should we process all items currently ingested
        :param message_id: attempt to sort a specific message based on id provided message_id
        :return: NOne
        """

        if self.all_read_messages:
            for message in self.all_read_messages:
                try:
                    formatted_folder = self.remove_illegal_chars_folder(folder_string=f"{output_directory}/{message['message_item'].message_subject}")
                    sanitized_output = pathlib.Path(formatted_folder)

                    if not sanitized_output.is_dir():
                        sanitized_output.mkdir(parents=True, exist_ok=True)

                    shutil.copy2(message['source_file_location'],f'{sanitized_output}/')
                # print(message['source_file_location'])
                except Exception as e:
                    print(e)


    def export_parse_stats(self):
        #What would be nice to see here
        ...

    def masked_gpt_submit(self):
        ...