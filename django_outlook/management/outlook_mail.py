

class OutlookMail(object):
    pre_check_attr_list = ["EntryID", "To"]

    def __init__(self, mail):
        super(OutlookMail, self).__init__()
        self.mail = mail
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

    def __getattr__(self, name):
        try:
            return self.__dict__[name]
        except:
            pass
        return getattr(self.mail, name)



