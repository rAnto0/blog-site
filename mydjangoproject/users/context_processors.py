from main_app.utils import menu


def get_main_app_context(request):
    return {'mainmenu': menu}
