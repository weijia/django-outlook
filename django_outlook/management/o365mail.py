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
        return base64.b64decode(self.raw_mail.josn["id"], '-_').encode("hex")[-140:]

    def get_conversation_id(self):
        return base64.b64decode(self.raw_mail.josn["conversationId"], '-_').encode("hex")[-32:]

    def get_categories(self):
        return self.raw_mail.josn["categories"]

    def get_subject(self):
        return self.raw_mail.json["subject"]

    def is_valid(self):
        return True

    def get_senders(self):
        return self.raw_mail.josn["sender"]["emailAddress"]["address"]

    def get_receive_datetime(self):
        return self.raw_mail.json["receivedDateTime"]