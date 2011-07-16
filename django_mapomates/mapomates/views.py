from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to

@login_required
@render_to('home.html')
def home(request):
    """ Logs user in and greets """
    return {}

