from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views import View
from .forms import CreateForm
from datetime import datetime
import os
import json


def home_page(request):
    return redirect("/news/")


def news_page(request, post_id):

    context = {}

    with open(settings.NEWS_JSON_PATH, 'r') as json_file:
        news_json = json.load(json_file)

    for index, news in enumerate(news_json):
        if news['link'] == post_id:
            context = news_json[index]
            break

    return render(request, "news/news.html", context)


def main_page(request):
    with open(settings.NEWS_JSON_PATH, 'r') as json_file:
        news_json = json.load(json_file)
        searched_word = request.GET.get('q')
        searched_dict = []
        for news in news_json:
            if searched_word is None:
                context = {"news": news_json}
            elif str(searched_word) in news["title"]:
                searched_dict.append(news)
                context = {"news": searched_dict}

        return render(request, "news/main.html", context)


class CreateNewsView(View):
    template_name = 'news/create_news.html'

    def get(self, request, *args, **kwargs):
        form = CreateForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            with open(settings.NEWS_JSON_PATH, 'r+') as json_file:
                news_json = json.load(json_file)
                new_link = news_json[-1]["link"] + 1
                new_post = {"created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "text": text, "title": title, "link": new_link}
                news_json.append(new_post)
            with open(settings.NEWS_JSON_PATH, 'w') as json_file:
                json.dump(news_json, json_file)

                return redirect('/news/')
