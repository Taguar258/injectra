from .get_app import get_app_name
from .logic import check_app_path, check_injection


def check_for_app_injection(args):

    # 1 | Check for valid folder
    check_app_path(args)

    # 2 | Get the application name
    get_app_name(args)

    # 3 | Check for injection
    check_injection(verbose_mode=True)

    quit()
