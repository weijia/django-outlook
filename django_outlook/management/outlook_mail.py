class OutlookMail(object):
    pre_check_attr_list = ["EntryID", "To"]

    def __init__(self, mail):
        super(OutlookMail, self).__init__()
        self.outlook_mail = mail
        self._is_valid = True
        try:
            for attr in self.pre_check_attr_list:
                getattr(mail, attr)
        except AttributeError:
            self._is_valid = False
        except Exception, e:
            self._is_valid = False

    def is_valid(self):
        return self._is_valid

    def get_categories(self):
        try:
            return unicode(self.outlook_mail.Categories).split(",")
        except AttributeError:
            return []

    def get_sender(self):
        try:
            sender = self.outlook_mail.SenderName
        except:
            sender = "No sender"
        return sender

    def get_mail_subject(self):
        return self.outlook_mail.Subject

    def get_receive_datetime(self):
        return self.outlook_mail.receivedTime

    def __getattr__(self, name):
        try:
            return self.__dict__[name]
        except:
            pass
        return getattr(self.outlook_mail, name)

    def dump_mail(self):
        # properties can be found at https://msdn.microsoft.com/en-us/library/office/dn320330.aspx
        email_info = unicode(self.get_subject()), unicode(self.get_entry_id()), \
                     unicode(self.get_sender()), \
                     unicode(self.outlook_mail.BodyFormat), "session: ", unicode(self.outlook_mail.Session), \
                     "conversationID:", unicode(self.get_conversation_id()), \
                     "c index:", unicode(self.outlook_mail.ConversationIndex), \
                     "topic:", unicode(self.outlook_mail.ConversationTopic), \
                     "category:", unicode(self.get_categories()), \
                     "unread:", unicode(self.outlook_mail.Unread), \
                     "receivedTime", unicode(self.get_receive_datetime())
        self.logger.info(email_info)


