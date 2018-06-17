import base64

from django_outlook.management.mail_to_handle_base import MailToHandleBase


class O365Mail(MailToHandleBase):

    def __init__(self, raw_mail):
        super(O365Mail, self).__init__()
        self.raw_mail = raw_mail
    #
    # def get_categories(self):
    #     return self.raw_mail["Categories"]

    def __getattr__(self, name):
        try:
            return self.raw_mail.json[name]
        except:
            pass
        return getattr(self.raw_mail, name)

    def get_entry_id(self):
        # Ref: https://stackoverflow.com/questions/2941995/python-ignore-incorrect-padding-error-when-base64-decoding
        return base64.b64decode(str(self.raw_mail.json["id"]), '-_').encode("hex")[-140:]

    def get_conversation_id(self):
        # Ref https://stackoverflow.com/questions/2941995/python-ignore-incorrect-padding-error-when-base64-decoding
        return base64.b64decode(str(self.raw_mail.json["conversationId"]), '-_').encode("hex")[-32:]

    def get_categories(self):
        return self.raw_mail.json["categories"]

    def get_subject(self):
        return self.raw_mail.json["subject"]

    def is_valid(self):
        return True

    def get_sender(self):
        return self.raw_mail.json["sender"]["emailAddress"]["address"]

    def get_receive_datetime(self):
        return self.raw_mail.json["receivedDateTime"]

    def get_recipients(self):
        res = []
        for to in self.raw_mail.json["toRecipients"]:
            res.append(to["emailAddress"]["address"])
        return res

    def get_mail_specific_link(self):
        return "%s\n%s" % (self.get_one_note_link(), self.raw_mail.json["webLink"])

    def get_body(self):
        return self.raw_mail.json["body"]["content"]

