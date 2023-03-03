from youtubesearchpython import *
import json
import plotly.express as px
import openai
import pandas as pd
from tasks.models import Credit
from django.contrib.auth.models import User
from tasks import config


def title_improve(title):
    # Inicializa la API de OpenAI
    openai.api_key = config.your_api_key
    # Define los argumentos que deseas usar para la generación de texto
    prompt = (f"Genera un título  Mejorado y adaptado al marketing CEO en el idioma y inspirado del titulo: {title}."
              "Tu respuesta sera un titulo mas creativo, llamativo y atractivo  que el original. El titulo debe ser diferente ya que sera mucho mejor. SOLO RESPONDERAS CON EL TITULO MEJORADO")

    # Llama a la API de OpenAI
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    # Obtén el título generado por la API
    nuevo_titulo = completions.choices[0].text

    # Imprime el título generado
    return (nuevo_titulo)


def improve_title(df):
    df = df.sort_values(by='View Count:', ascending=False)
    top_n = df.head(3)
    titles = top_n['Title']
    titulos = titles.tolist()
    random_titles = df.sample(n=3)
    titles2 = random_titles['Title']
    titles_random = titles2.tolist()
# Inicializa la API de OpenAI
    openai.api_key = "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"
    # Define los argumentos que deseas usar para la generación de texto
    prompt = (f"Generar un título  inspirado en los siguientes tres títulos: {titulos[0]}, {titulos[1]}, {titulos[2]}."
              "El título debe ser mejor; más impactante, creativo, llamativo y atractivo  que los títulos originales. Tambien debes incluir las mejores palabras claves de los titulos orinales")
    prompt2 = (f"Generar un título  inspirado en los siguientes tres títulos: {titles_random[0]}, {titles_random[1]}, {titles_random[2]}."
               "Genera el titulo mucho mejor atractivo y que llame la atencion")
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
    fig4.write_html('pie_chart.html', full_html=False)
    chart = fig4.to_html()
    return chart


def chart2(df):
    fig = px.histogram(df, x='Title', y='View Count:')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.write_html('pie_chart.html', full_html=False)
    chart2 = fig.to_html()
    return chart2


def chart3(df, dictionary):
    fig3 = px.histogram(df, x=dictionary.keys(), y=dictionary.values())
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig3.write_html('pie_chart.html', full_html=False)
    chart3 = fig3.to_html()
    return chart3


def chart4(df, dictionary2):
    fig4 = px.histogram(df, x=dictionary2.keys(), y=dictionary2.values())
    fig4.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig4.write_html('pie_chart.html', full_html=False)
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
