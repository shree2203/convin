from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from oauth2client.client import OAuth2WebServerFlow


class GoogleCalendarInitView(TemplateView):
    template_name = 'google_calendar_init.html'

    def get(self, request):
        flow = OAuth2WebServerFlow(
            client_id='YOUR_CLIENT_ID',
            client_secret='YOUR_CLIENT_SECRET',
            scope='https://www.googleapis.com/auth/calendar',
            redirect_uri=reverse('google_calendar_redirect'))

        auth_url = flow.step1_get_authorize_url()

        return HttpResponseRedirect(auth_url)


class GoogleCalendarRedirectView(TemplateView):
    template_name = 'google_calendar_redirect.html'

    def get(self, request):
        flow = OAuth2WebServerFlow(
            client_id='YOUR_CLIENT_ID',
            client_secret='YOUR_CLIENT_SECRET',
            scope='https://www.googleapis.com/auth/calendar',
            redirect_uri=reverse('google_calendar_redirect'))

        # Get the code from the query string
        code = request.GET.get('code')

        # Exchange the code for an access token
        access_token, refresh_token = flow.step2_exchange(code)

        # Save the access token and refresh token in the user's profile
        user = User.objects.get(username=request.user.username)
        user.google_access_token = access_token
        user.google_refresh_token = refresh_token
        user.save()

        # Redirect the user back to the home page
        return HttpResponseRedirect(reverse('home'))

