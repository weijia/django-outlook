# noinspection PyMethodMayBeStatic
class MailToHandleBase(object):
    def is_valid(self):
        return False

    def get_senders(self):
        return []

    def get_entry_id(self):
        return None

    def get_recipients(self):
        return []

    def get_categories(self):
        return []

    def get_subject(self):
        return None

    def get_conversation_id(self):
        return None

    def get_receive_datetime(self):
        return None

    def get_mail_specific_link(self):
        return self.get_one_note_link()

    def get_one_note_link(self):
        return 'onenote:outlook?folder=Mail&entryid=' + str(self.get_entry_id())

    def dump_mail(self):
        # properties can be found at https://msdn.microsoft.com/en-us/library/office/dn320330.aspx
        email_info = unicode(self.get_subject()), unicode(self.get_entry_id()), \
                     unicode(self.get_sender()), \
                     "conversationID:", unicode(self.get_conversation_id()), \
                     "category:", unicode(self.get_categories())
        self.logger.info(email_info)

