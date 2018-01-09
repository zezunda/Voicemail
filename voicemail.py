#!/usr/bin/env python

import os
import ConfigParser

MSG_DATA = ConfigParser.RawConfigParser(allow_no_value=True)
PATH = "/var/spool/asterisk/voicemail/"


def main(voicemails):
    file_list = get_files()
    blast_dict = get_blast_msgs(file_list)
    remove_files(blast_dict, file_list, voicemails)

def get_files():
    file_list = []
    for roots, dirs, files in os.walk(PATH):
        file_list += [roots + '/' + item for item in files]
    return file_list


def get_blast_msgs(file_list):
    blast_dict = {}
    for item in file_list:
        filename, file_extension = os.path.splitext(item)
        if file_extension == ".txt":
            MSG_DATA.read(item)
            msg_context = MSG_DATA.get("message", "context")
            if msg_context == "app-vmblast":
                msg_id = MSG_DATA.get("message", "msg_id")
                blast_dict[msg_id] = blast_dict.get(msg_id, 0) + 1
    return blast_dict


def remove_files(blast_dict, file_list, voicemails):
    for item in blast_dict:
        if blast_dict.get(item) < voicemails:
            for msg in file_list:
                filename, file_extension = os.path.splitext(msg)
                if file_extension == ".txt":
                    MSG_DATA.read(msg)
                    msg_id = MSG_DATA.get("message", "msg_id")
                    if msg_id in item:
                        print("Deleting %s..." % filename)
                        try:
                            os.remove(filename + '.txt')
                            os.remove(filename + '.wav')
                        except Exception as ex:
                            print(ex)


if __name__ == "__main__":
    main(4)