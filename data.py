from SPARQLWrapper import SPARQLWrapper, JSON


class City:
    def __init__(self, name, img, population):
        self.name = name
        self.img_src = img
        self.population = population

class University:
    def __init__(self, name, img, desc, link):
        self.name = name
        self.img_src = img
        self.description = desc
        self.link = link

wrapper  = SPARQLWrapper("https://dbpedia.org/sparql")

def get_cities():
    q = """
select distinct ?name ?img ?population where
{
    ?city rdf:type dbo:City;
    rdfs:label ?name;
    dbo:thumbnail ?img;
    dbp:populationTotal ?population.
    {
        select distinct ?university_city ?university where
        {
            ?university rdf:type dbo:University;
            dbo:country dbr:Ukraine;
            dbo:city ?university_city.
        }
    }
  
    filter(?university_city = ?city)
    filter(lang(?name)="en" )
}

    """
    wrapper.setQuery(q)
    wrapper.setReturnFormat(JSON)
    result = wrapper.query().convert()["results"]["bindings"]
    return [City(item["name"]["value"],item["img"]["value"], item["population"]["value"]) for item in result]


def get_universities(city):
    q = f"""
select  ?name ?university ?img ?desc where
{{
    ?university rdf:type dbo:University;
    dbo:country dbr:Ukraine;
    dbo:city ?city;
    dbo:abstract ?desc;
    rdfs:label ?name.
    filter(lang(?name)="en" and lang(?desc) = "en" )
    filter(contains(LCASE(STR(?city)), "{str(city).lower()}"))
    OPTIONAL  {{  ?university dbo:thumbnail ?img  }}
}}
    """
    wrapper.setQuery(q)
    wrapper.setReturnFormat(JSON)
    result = wrapper.query().convert()["results"]["bindings"]

    uni_result = []
    for item in result:
        img = ""
        if (item.get("img") != None):
            img =item["img"]["value"]
        univer = University(item["name"]["value"], img, item["desc"]["value"], item["university"]["value"])
        uni_result.append(univer)
    return uni_result


print(len(get_cities()))
print(len(get_universities("kyiv")))
