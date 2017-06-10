from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class GreetingView(View):
    message = 'Good Day'

    def get(self, *args, **kwargs):
        return HttpResponse(self.message)

greeting = GreetingView.as_view()


class MorningGreetingView(GreetingView):
    message = 'Morning to ya'

morning_greeting = MorningGreetingView.as_view()


evening_greeting = GreetingView.as_view(message='Evening to ya')

