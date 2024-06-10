from fastapi import FastAPI, Query
import requests
from restcountries import RestCountryApiV2 as rapi
import os
from typing import Annotated
from dotenv import load_dotenv
from config import langchain_helper as lch
from models.schemas import Strategy, Base
import random


load_dotenv()



app = FastAPI()


@app.get("/font")
async def create_font():
    API_KEY = os.getenv("GOOGLE_FONTS_API_KEY")
    url = "https://www.googleapis.com/webfonts/v1/webfonts?key=" + API_KEY
    response =  requests.get(url, timeout=5)

    fonts = response.json()
    list_of_fonts = fonts['items']

    # Select 3 random fonts
    random_fonts = random.sample(list_of_fonts, 3)

    return {"fonts": random_fonts}

#new stuff not working yet .. 
@app.post("/problem")
def create_problem(base: Base):
    response = generate_problem(industry=base.industry, niche=base.niche)
    return {"response" : response}


@app.post("/color")
async def create_color_pallete(base: Base):
    response = lch.generate_brand_color(niche=base.niche, industry=base.industry)
    return {"response" : response}


@app.post("/messaging")
def create_brand_messaging(base: Base):
    response = lch.generate_brand_messaging(industry=base.industry, niche=base.niche)
    return {"response" : response}

@app.post("/strategy")
def create_brand_strategy(brand_strategy: Strategy):
    industry = brand_strategy.industry
    niche = brand_strategy.niche
    country = brand_strategy.country
    response = lch.generate_business_strategy(industry=industry, niche=niche, country=country)
    return {"response" : response}

@app.post("/brand_name")
def generate_brand_name(base: Base):
    response = lch.generate_brand_name(niche=base.niche, industry=base.industry)
    return {"response" : response}


@app.post("/logo")
def create_logo(base: Base):
    response = lch.generate_logo(industry=base.industry, niche=base.niche)
    return {"response" : response}

@app.post("/photography")
def create_photography(base: Base):
    response = lch.generate_pics(industry=base.industry)
    return {"response" : response}


@app.post("/illustration")
def create_illustration(base: Base):
    response = lch.generate_pattern(industry=base.industry)
    return {"response" : response}


@app.get("/all-countries/")
def get_all_countries(country_name: Annotated[str | None, Query(max_length=50)] = None ):
    all = rapi.get_all()
    countries = {}
    for country in all:
            countries[country.name] = {
                "name": country.name,
                "flag": country.flag
            }
    if country_name:
        return countries[country_name]
    else:
        return countries