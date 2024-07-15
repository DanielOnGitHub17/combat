from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages as msg

from game.views import GamePlay

# Create your views here.

def home(request):
    # return GamePlay().get(request)
# https://www.onthisday.com/date/2010/june/21 -> Scrape to get daily insights!
    return render(request, "landing.html", {"user": request.user})

def leaders(request):
    return render(request, "leaders.html", {"user": request.user})

def game_help(request):
    return render(request, "game_help.html", {"user": request.user})

class Support(View):
    def post(self, request):
        with open("../issues.html", 'a') as file:
            file.write(f"\n<li>{request.user}: {request.POST['issue']} | {datetime.now()}</li>")
        # Email devs
        msg.add_message(request, msg.INFO, "Thanks for sending a message!")
        return redirect("/support/")
    
    def get(self, request):
        return render(request, "support.html")

def dev(request):
    return render(request, "dev.html", {"user": request.user})
