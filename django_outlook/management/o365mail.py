import base64

from django_outlook.management.mail_to_handle_base import MailToHandleBase
import urllib
from bs4 import BeautifulSoup


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
        return self._html_to_text(self.raw_mail.json["body"]["content"])

    def _html_to_text(self, html):
        # https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
        soup = BeautifulSoup(html, "lxml")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text

    def move_to_folder(self, target_folder):
        self.raw_mail.moveToFolder(target_folder)
