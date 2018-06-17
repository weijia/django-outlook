

class O365Mail(object):

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
