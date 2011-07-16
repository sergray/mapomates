from annoying.decorators import render_to


@render_to('home.html')
def home(request):
    """ Logs user in and greets """
    return {}

