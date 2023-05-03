import json
import shutil
import pathlib
import logging
import email
from email import policy
from email.parser import BytesParser
from typing import Type, List
from src.msg_exceptions.message_parse_exceptions import  UnableToLocateFile, UnableToWriteFile


class MSG_PARSED:
    def __init__(self, message:email.message.EmailMessage):

        self.message_ = message

    @property
    def list_available_properties(self):
        return (self.message_.keys())

    @property
    def message_subject(self):
        return self.message_["subject"]

    @property
    def message_from(self):
        return self.message_["from"]

    @property
    def message_to(self):
        return self.message_["to"]

    @property
    def message_attachments(self):
        ...

    @property
    def mask_sensitive_chars(self) ->str:
        ...

    def generate_metadata(self):
        ...


class MSG_PARSER:

    def __init__(self):
        self.all_read_messages:list[dict[str, MSG_PARSED]]= [] #list of MSG_PARSED items

    @property
    def message_viewer(self) -> MSG_PARSED:

        return MSG_PARSED(self.current_message)

    def remove_illegal_chars_folder(self, folder_string:str) ->str:
        illegal_chars = ["<",">",":","\"","/","\\","|","?","*",":"]

        for illegal_char in illegal_chars:
            updated_str=folder_string.replace(illegal_char,";")

        return updated_str

    def read_message(self, source_message:str,
                     internal_dir_call:bool=False,
                     raise_on_error:bool=True)-> email.message.EmailMessage:
        # only txt/eml supported for now
        try:
            if pathlib.Path(source_message).is_file():
                with open(source_message, 'rb') as message_file:
                    current_message = BytesParser(policy=policy.default).parse(message_file)

                    self.all_read_messages.append({"source_file_location":source_message,
                                                   "message_item":MSG_PARSED(current_message)
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
        try:
            for item in pathlib.Path(source_directory).iterdir():
                if item.is_file():
                    self.read_message(source_message=item, internal_dir_call=True)
                if item.is_dir() and recurse:
                    self.read_messages_in_dir(source_directory=item, recurse=True)
        except Exception as e:
            print(e)

    def extract_attachments(self, view_only:bool=False):
        ...

    def sort_messages(self, output_directory:str="export/",
                      include_in_folder_name:str=["Subject"],
                      include_attachments: bool = False,
                      all_message:bool = False):

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