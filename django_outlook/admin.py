import models
from djangoautoconf.auto_conf_admin_tools.admin_register import AdminRegister

r = AdminRegister()
r.register_all_models(models)

