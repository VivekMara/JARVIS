import httpx

def wikipedia(q):
    response =  httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }).json()
    hits = response["query"]["searchinfo"]["totalhits"]
    if hits == 0:
        return "No results found"
    else:
        result = response["query"]["search"][0]["snippet"]
        return result

def calculate(what):
    return eval(what)