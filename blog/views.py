from django.http import HttpResponse

def greeting_view(message):
    def view_fn(request):
        return HttpResponse(message)
    return view_fn

greeting = greeting_view('Good Day')

morning_greeting = greeting_view('Morning to ya')

evening_greeting = greeting_view('Evening to ya')

