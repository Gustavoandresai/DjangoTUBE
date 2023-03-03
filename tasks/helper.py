from youtubesearchpython import *
import json
import plotly.express as px
import openai
import pandas as pd
from tasks.models import Credit
from django.contrib.auth.models import User
from tasks import config


def title_improve(title, language):
    # Inicializa la API de OpenAI
    openai.api_key = config.your_api_key
    # Define los argumentos que deseas usar para la generación de texto
    prompt = (f"I want you to respond only in language {language}, Generate a title Improved and adapted to SEO marketing and inspired by the title: {title}."
              "Your answer would be a more creative, striking and attractive title than the original. The title should be different as it will be much better. the video title has to be  better and catchy no more than 70 characters.")

    # Llama a la API de OpenAI
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    # Get de api title
    nuevo_titulo = completions.choices[0].text

    # title
    return (nuevo_titulo)


def improve_title(df, language):
    df = df.sort_values(by='View Count:', ascending=False)
    # Top 3 title with more views for the inspiration
    top_n = df.head(3)
    titles = top_n['Title']
    titulos = titles.tolist()
    # inspire by title random
    random_titles = df.sample(n=3)
    titles2 = random_titles['Title']
    titles_random = titles2.tolist()
# Inicializa la API de OpenAI
    openai.api_key = "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"
    # Define los argumentos que deseas usar para la generación de texto
    prompt = (f"I want you to respond only in language {language}, be inspired by the following titles and make the words dramatic based on: {titulos[0]}, {titulos[1]}, {titulos[2]}."
            "take on the role of professional copywriter and YouTube video content creator And make the title compelling and captivating, the video title has to be different, better and catchy no more than 70 characters.")
    prompt2 = (f"I want you to respond only in language {language}, be inspired by the following titles and make the words dramatic based on: {titles_random[0]}, {titles_random[1]}, {titles_random[2]}."
            "take on the role of professional copywriter and YouTube video content creator And make the title compelling and captivating, the video title has to be catchy no more than 70 characters.")
    # Llama a la API de OpenAI
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    completions2 = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt2,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    # Obtén el título generado por la API
    nuevo_titulo = completions.choices[0].text
    nuevo_titulo2 = completions2.choices[0].text

    # Imprime el título generado
    return (nuevo_titulo, nuevo_titulo2)


def value_credits(request, *args):
    user = User.objects.get(username=request.user)
    credit = Credit.objects.get(user=user)
    if args:
        subtract = int(args[0])
        credit.value -= subtract  # we subtract the credits
        credit.save()
    return credit.value


def process_results(search, number_result):
    # Exactact data
    videosSearch = VideosSearch(search, limit=number_result)
    results = videosSearch.result(mode=ResultMode.json)
    # Convert to json for handle it better
    json_response = json.loads(results)
    data = json_response['result']
    datos = {}
    none = 0
    for idx, text in enumerate(data):
        #text = json_response['result'][idx]
        # data more exactly

        video = Video.getInfo(text['link'], mode=ResultMode.json)
        miniaturahd = "https://img.youtube.com/vi/" + \
            video['id'] + "/maxresdefault.jpg"
        canal = Channel.get(video['channel']['id'])
        # If any data is not found, leave the box blank
        try:
            datos[idx] = {'Title': text['title'], 'Search': search, 'Link': text['link'], 'Thumbnail': miniaturahd, 'View Count:': video['viewCount']['text'], 'Keywords Tags': video['keywords'], 'Duration Seconds': video['duration']['secondsText'], 'Duration Minuts': text['duration'], 'Upload Date': video['uploadDate'], 'published Time': text['publishedTime'], 'Category': video['category'],
                          'All Video Description': video['description'], 'Description': text['descriptionSnippet'][0]['text'], 'Channel': text['channel']['name'], 'Subscribers': canal['subscribers']['simpleText'], 'Channel Description': canal['description'], 'Banner Chanel': canal['banners'][5]['url'], 'Keywords channel': canal['keywords'], 'Channel Total Views': canal['views'], 'Channel Join': canal['joinedDate'], 'Country': canal['country']}
        except TypeError:
            none += 1
            print(TypeError)
            print('\n we have', none, ' blank boxes nonetype')
        #link = text['link']
    return datos


def chart(df):
    fig4 = px.pie(df, values=df['View Count:'], names='Country',
                  title='Population of European continent')
    fig4.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    chart = fig4.to_html()
    return chart


def chart2(df):
    fig = px.histogram(df, x='Title', y='View Count:')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    chart2 = fig.to_html()
    return chart2


def chart3(df, dictionary):
    fig3 = px.histogram(df, x=dictionary.keys(), y=dictionary.values())
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    chart3 = fig3.to_html()
    return chart3


def chart4(df, dictionary2):
    fig4 = px.histogram(df, x=dictionary2.keys(), y=dictionary2.values())
    fig4.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    chart4 = fig4.to_html()
    return chart4


def count_words(value):
    # create a cycle For count the words and get what are de the most used word
    diccionario = dict()
    for i in range(len(value)):
        cadena = value[i]
        palabras = cadena.split(" ")
        for p in palabras:
            diccionario[p] = diccionario.get(p, 0) + 1
    return diccionario


def count_words2(value):
    # create a cycle For count the words and get what are de the most used word
    diccionario = dict()
    for i in range(len(value)):
        cadena = value[i]
        palabras = str(cadena).split("'")
        for p in palabras:
            diccionario[p] = diccionario.get(p, 0) + 1
    diccionario.pop(", ")
    del diccionario['[']
    del diccionario[']']

    return diccionario
