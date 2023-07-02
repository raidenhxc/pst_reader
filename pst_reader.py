import pypff
import os
from pathlib import Path
import pst_pb2 as PstFileFormat
from datetime import datetime

def main(path):
    # pypff.open only admits str
    path = str(Path(r''+path))

    if len(path) == 0:
        return "Empty path."
    elif not os.path.exists(path):
        return path + " not found"
    else:
        content = pypff.open(path)
        rootFolder = content.get_root_folder()

        # Is this the final object to return?
        protoRootFolder = PstFileFormat.ProtoFolder()
        setProtoFolderProperties(rootFolder, protoRootFolder)
        getFolders(rootFolder, protoRootFolder)

        return(protoRootFolder)


#####################
# folders functions #
#####################
def getFolders(rootFolder, protoRootFolder):
    for folder in rootFolder.sub_folders:
        protoSubfolder = None
        protoSubfolder = protoRootFolder.subfolders.add()
        setProtoFolderProperties(folder, protoSubfolder)    

        # recursive call if there are subfolders
        if folder.number_of_sub_folders:
            getFolders(folder, protoSubfolder)

        # messages in folder
        if rootFolder.get_number_of_sub_messages:
            getMessages(folder, protoSubfolder)  


def setProtoFolderProperties(folder, protoFolder):
    if folder and protoFolder:
        protoFolder.id = folder.get_identifier()

        # Root folder has no name attribute
        if folder.get_name() is not None:
            protoFolder.name = folder.get_name()
        else:
            protoFolder.name = "Root folder"

        protoFolder.num_of_subfolders = folder.get_number_of_sub_folders()
        protoFolder.num_of_messages = folder.get_number_of_sub_messages()


#####################
# message functions #
#####################
def getMessages(folder, protoFolder):
    for message in folder.sub_messages:
        protoMessage = None
        protoMessage = protoFolder.messages.add()
        setProtoMessageProperties(message, protoMessage)
        getAttachments(message, protoMessage)


def setProtoMessageProperties(message, protoMessage):
    if message and protoMessage:
        protoMessage.id = message.get_identifier()

        # Email name can return none if subject is empty
        if message.get_subject() is not None:
            protoMessage.subject = message.get_subject()
        else:
            protoMessage.subject = "No subject"

        # Delivery time
        protoMessage.delivery_time_timestamp = int(round(message.get_delivery_time().timestamp()))

        # Transport headers can be empty
        if message.get_transport_headers() is not None:
            protoMessage.transport_headers = message.get_transport_headers()
        else:
            protoMessage.transport_headers = ""

        # html_body and plain text body
        #if message.get_html_body() is not None:
        #    protoMessage.html_body = message.get_html_body()

        if message.get_plain_text_body() is not None:
            protoMessage.plain_text_body = message.get_plain_text_body()

#########################
# attachments functions #
#########################
def getAttachments(message, protoMessage):
    for attachment in message.attachments:
        protoAttachment = None
        protoAttachment = protoMessage.attachments.add()
        setProtoAttachmentProperties(attachment, protoAttachment)


def setProtoAttachmentProperties(attachment, protoAttachment):
    if attachment and protoAttachment:
        protoAttachment.size = attachment.get_size()
        #protoAttachment.buffer = attachment.read_buffer(attachment.get_size())


if __name__ == "__main__":
    main("test.pst")







