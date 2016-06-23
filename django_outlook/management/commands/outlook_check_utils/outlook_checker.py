from django_outlook.management.commands.outlook_check_utils.outlook_reader import OutlookReader
from iconizer.iconizer_consts import ICONIZER_SERVICE_NAME
from iconizer.msg_service.msg_service_interface.msg_service_factory_interface import MsgServiceFactory


class OutlookChecker(OutlookReader):
    def __init__(self):
        super(OutlookChecker, self).__init__()
        f = MsgServiceFactory()
        self.msg_service = f.get_msg_service()

    def notify(self, msg):
        self.msg_service.send_to(ICONIZER_SERVICE_NAME, {"command": "notify", "msg": msg})
