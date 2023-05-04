# Email-Thon

Email-Thon is a simple library to do "all" things IR in regards to eml, msg, and live mailbox collection.
The project is currently actively under development so just assume everything is broken.

## Base Functionaility

Currently we only supporting reading .eml (text) based message exports. The immediate task will be to expand this to include .msg files.
Each message will be represented as a dataclass with various attributes for processing. 

## Current Status

**To Complete**
- [x] Add doc strings
- [x] Add logging module
- [ ] JSON repre for email data
- [ ] add support for .msg files
- [ ] Expand save to folder_name options
- [ ] Metadata file within each folder with summary of items parsed
- [ ] migrate to dataclass to represent a parsed email

**Foward Looking**
- [ ] Create CLI version
- [ ] Docker Ready
- [ ] Report generator PDF|HTML based on export folder
- [ ] add support to connect to mailboxes (protocol base support|outlook|gmail)
- [ ] Create Module for AI interaction (Context, Name Recognition)

**Considerations**
 - Should we capture duplicate messages?

**Complete**
- [x] Create simple lib with modular expansions
- [x] Class implementation
- [x] Create ReadMe
- [x] Read all messages in directory
- [x] IOC Extractor (URLS|Attachments)
- [x] Attachment Extractor
- [x] Extract only message (from,to,subject,date) within Body to assist with Context
- [x] Export to folders tracked by subject
- [x] class to represent a parsed email 
