from django.shortcuts import render

# Create your views here.
import requests
import json
from string import Template

def home(request):

    lista_tuplas=[]
    page_episodes_query="query{episodes{info{pages}}}"
    url = 'https://rickandmortyapi.com/graphql/'
    respuesta_numero_paginas = requests.post(url, json={'query': page_episodes_query})
    json_data = json.loads(respuesta_numero_paginas.text)
    numero_paginas = int(json_data["data"]["episodes"]["info"]["pages"])
    for i in range(numero_paginas):
        all_episodes_query = "query{episodes(page: "+str(i+1)+"){results{id name air_date episode}}}"
        r = requests.post(url, json={'query': all_episodes_query})
        json_data = json.loads(r.text)
        resultados=json_data["data"]["episodes"]["results"]
        for episodio in resultados:
            tupla = (episodio["id"], episodio["name"], episodio["air_date"], episodio["episode"])
            lista_tuplas.append(tupla)

    return render(request, 'home.html', {"lista_tuplas": lista_tuplas})

def episodio(request, id):
    url = "https://rickandmortyapi.com/graphql/"
    episodes_query = "query{episode(id:" + str(id) + "){name air_date episode characters{id name}}}"
    respuesta_episodio = requests.post(url, json={'query': episodes_query})
    json_data = json.loads(respuesta_episodio.text)
    resultado = json_data["data"]["episode"]
    nombre = resultado["name"]
    fecha_al_aire = resultado["air_date"]
    episodio = resultado["episode"]
    lista_personajes=resultado["characters"]
    diccionario_personajes={}
    for personaje in lista_personajes:
        nombre = personaje["name"]
        id = personaje["id"]
        diccionario_personajes[nombre]=id

    return render(request, "episodio.html", {"nombre":nombre,"fecha_al_aire":fecha_al_aire, "episodio":episodio, "personajes": diccionario_personajes})

def personaje(request, ur):
    url = "https://rickandmortyapi.com/graphql/"
    characters_query = "query{character(id:" + str(ur) + "){name status species type gender origin{id name} location{id name} image episode{id name}}}"
    respuesta_personaje = requests.post(url, json={'query': characters_query})
    json_data = json.loads(respuesta_personaje.text)
    resultado = json_data["data"]["character"]
    nombre = resultado["name"]
    estado = resultado["status"]
    especie = resultado["species"]
    tipo = resultado["type"]
    genero = resultado["gender"]
    nombre_origen = resultado["origin"]["name"]
    id_origen=resultado["origin"]["id"]
    nombre_locacion = resultado["location"]["name"]
    id_locacion=resultado["location"]["id"]
    imagen = resultado["image"]
    episodios = resultado["episode"]
    diccionario_episodios={}
    for episodio in episodios:
        nombre=episodio["name"]
        id = episodio["id"]
        diccionario_episodios[nombre]=id

    return render(request, "personaje.html",
                  {"nombre": nombre, "estado": estado, "especie": especie, "tipo": tipo, "genero": genero,
                   "origen": nombre_origen, "numero_origen": id_origen, "numero_locacion": id_locacion,
                   "locacion": nombre_locacion, "imagen": imagen, "episodios": diccionario_episodios})



def lugar(request, id):
    url = "https://rickandmortyapi.com/graphql/"
    location_query = "query{location(id:" + str(id) + "){name type dimension residents{id name}}}"
    respuesta_locacion = requests.post(url, json={'query': location_query})
    json_data = json.loads(respuesta_locacion.text)
    resultado = json_data["data"]["location"]
    nombre = resultado["name"]
    tipo = resultado["type"]
    dimension = resultado["dimension"]
    residentes = resultado["residents"]
    diccionario_residentes = {}
    for residente in residentes:
        nombre = residente["name"]
        id = residente["id"]
        diccionario_residentes[nombre] = id



    return render(request, "lugar.html",
                  {"nombre": nombre,  "tipo":tipo, "dimension":dimension, "residentes":diccionario_residentes})


def busqueda(request):
    palabra = request.GET.get('q')
    url = "https://rickandmortyapi.com/graphql/"


    # episodios
    diccionario_episodios={}
    page_episodes_query = "query{episodes{info{pages}}}"
    respuesta_numero_paginas = requests.post(url, json={'query': page_episodes_query})
    json_data = json.loads(respuesta_numero_paginas.text)
    numero_paginas = int(json_data["data"]["episodes"]["info"]["pages"])
    for pag in range(numero_paginas):
        query_template = Template("""query{episodes(page: $pag, filter: { name: "$palabra" }){results{id name}}}""")
        nueva_query = query_template.substitute(palabra=palabra, pag= str(pag+1))
        r = requests.post(url, json={'query': nueva_query})
        if "errors" in r.text:
            continue
        else:
            json_data = json.loads(r.text)
            resultados = json_data["data"]["episodes"]["results"]
            for resultado in resultados:
                nombre = resultado["name"]
                id = resultado["id"]
                diccionario_episodios[nombre] = id



    # personajes
    diccionario_personajes = {}
    page_characters_query = "query{characters{info{pages}}}"
    respuesta_numero_paginas = requests.post(url, json={'query': page_characters_query})
    json_data = json.loads(respuesta_numero_paginas.text)
    numero_paginas = int(json_data["data"]["characters"]["info"]["pages"])
    for pag in range(numero_paginas):
        query_template = Template("""query{characters(page: $pag, filter: { name: "$palabra" }){results{id name}}}""")
        nueva_query = query_template.substitute(palabra=palabra, pag=str(pag + 1))
        r = requests.post(url, json={'query': nueva_query})
        if "errors" in r.text:
            continue
        else:
            json_data = json.loads(r.text)
            resultados = json_data["data"]["characters"]["results"]
            for resultado in resultados:
                nombre = resultado["name"]
                id = resultado["id"]
                diccionario_personajes[nombre] = id


    # lugares
    diccionario_lugares = {}
    page_locations_query = "query{locations{info{pages}}}"
    respuesta_numero_paginas = requests.post(url, json={'query': page_locations_query})
    json_data = json.loads(respuesta_numero_paginas.text)
    numero_paginas = int(json_data["data"]["locations"]["info"]["pages"])
    for pag in range(numero_paginas):
        query_template = Template("""query{locations(page: $pag, filter: { name: "$palabra" }){results{id name}}}""")
        nueva_query = query_template.substitute(palabra=palabra, pag=str(pag + 1))
        r = requests.post(url, json={'query': nueva_query})
        if "errors" in r.text:
            continue
        else:
            json_data = json.loads(r.text)
            resultados = json_data["data"]["locations"]["results"]
            for resultado in resultados:
                nombre = resultado["name"]
                id = resultado["id"]
                diccionario_lugares[nombre] = id

    return render(request, "busqueda.html", {"palabra": palabra, "episodios": diccionario_episodios,
                                             "personajes": diccionario_personajes,
                                             "lugares": diccionario_lugares})
