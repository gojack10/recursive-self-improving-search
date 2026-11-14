import json
import time
import urllib.parse
import urllib.request

from .config import ROOT

DATA = ROOT / "data" / "hunts"

# Each hunt's full answer is computed from Wikidata. Searchers only have the web through Telem,
# with wikidata.org blocked. Pools keep improvement, selection and held-out testing on different hunts.
HUNTS = {
    "hugo_nebula": dict(x='won the Hugo Award for Best Novel', y='won the Nebula Award for Best Novel',
        kind="works", pool="train",
        question="Find every novel that won both the Hugo Award for Best Novel and the Nebula Award for Best Novel.",
        criterion="novel that won both the Hugo Award for Best Novel and the Nebula Award for Best Novel",
        where='?h rdfs:label "Hugo Award for Best Novel"@en. ?n rdfs:label "Nebula Award for Best Novel"@en. ?x p:P166/ps:P166 ?h; p:P166/ps:P166 ?n. FILTER NOT EXISTS {?x wdt:P31 wd:Q5}'),
    "astronaut_physicians": dict(x='astronaut', y='physician / medical doctor',
        kind="people", pool="train",
        question="Find every astronaut who is also a trained physician (medical doctor).",
        criterion="astronaut who is also a physician / medical doctor",
        where="?x wdt:P106 wd:Q11631; wdt:P106 wd:Q39631."),
    "calatrava_bridges": dict(x='bridge', y='designed by Santiago Calatrava',
        kind="structures", pool="train",
        question="Find every bridge designed by the architect Santiago Calatrava.",
        criterion="bridge designed by Santiago Calatrava",
        where='?a rdfs:label "Santiago Calatrava"@en. ?x wdt:P84 ?a; wdt:P31/wdt:P279* wd:Q12280.'),
    "women_chem_nobel": dict(x='woman', y='won the Nobel Prize in Chemistry',
        kind="people", pool="train",
        question="Find every woman who has won the Nobel Prize in Chemistry.",
        criterion="woman who won the Nobel Prize in Chemistry",
        where="?x p:P166/ps:P166 wd:Q44585; wdt:P21 wd:Q6581072."),
    "abel": dict(x='mathematician', y='won the Abel Prize',
        kind="people", pool="select",
        question="Find every mathematician who has won the Abel Prize.",
        criterion="Abel Prize laureate",
        where='?a rdfs:label "Abel Prize"@en. ?x p:P166/ps:P166 ?a.'),
    "caspian_rivers": dict(x='river', y='flows directly into the Caspian Sea',
        kind="structures", pool="select",
        question="Find every river that flows directly into the Caspian Sea.",
        criterion="river whose mouth is the Caspian Sea",
        where="?x wdt:P403 wd:Q5484; wdt:P31/wdt:P279* wd:Q4022."),
    "turing_uk": dict(x='won the Turing Award', y='born in the United Kingdom',
        kind="people", pool="select",
        question="Find every Turing Award winner who was born in the United Kingdom.",
        criterion="Turing Award winner born in the United Kingdom",
        where='?a rdfs:label "Turing Award"@en. ?x p:P166/ps:P166 ?a; wdt:P19/wdt:P17 wd:Q145.'),
    "wirth_languages": dict(x='programming language', y='designed by Niklaus Wirth',
        kind="works", pool="select",
        question="Find every programming language designed by Niklaus Wirth.",
        criterion="programming language designed by Niklaus Wirth",
        where="?x wdt:P287 wd:Q92604."),
    "hadid": dict(x='building or structure', y='designed by Zaha Hadid',
        kind="structures", pool="test",
        question="Find every building or structure designed by the architect Zaha Hadid.",
        criterion="building or structure designed by Zaha Hadid (or Zaha Hadid Architects)",
        where='?a rdfs:label "Zaha Hadid"@en; wdt:P31 wd:Q5. ?x wdt:P84 ?a.'),
    "fields_france": dict(x='won the Fields Medal', y='French citizen',
        kind="people", pool="test",
        question="Find every Fields Medal winner who holds French citizenship.",
        criterion="Fields Medal winner with French citizenship",
        where="?x p:P166/ps:P166 wd:Q28835; wdt:P27 wd:Q142."),
    "nobel_lit_women": dict(x='woman', y='won the Nobel Prize in Literature',
        kind="people", pool="test",
        question="Find every woman who has won the Nobel Prize in Literature.",
        criterion="woman who won the Nobel Prize in Literature",
        where="?x p:P166/ps:P166 wd:Q37922; wdt:P21 wd:Q6581072."),
    "palme_bestpicture": dict(x="won the Palme d'Or", y='won the Academy Award for Best Picture',
        kind="works", pool="test",
        question="Find every film that won both the Palme d'Or and the Academy Award for Best Picture.",
        criterion="film that won both the Palme d'Or and the Academy Award for Best Picture",
        where="?x p:P166/ps:P166 wd:Q179808; p:P166/ps:P166 wd:Q102427; wdt:P31/wdt:P279* wd:Q11424."),
}


def sparql(where):
    q = ("SELECT ?x ?label (GROUP_CONCAT(DISTINCT ?alt; separator='|') AS ?alts) WHERE { " + where +
         ' ?x rdfs:label ?label. FILTER(lang(?label) IN ("en", "mul")) OPTIONAL { ?x skos:altLabel ?alt. FILTER(lang(?alt) IN ("en", "mul")) } }'
         " GROUP BY ?x ?label")
    url = "https://query.wikidata.org/sparql?" + urllib.parse.urlencode({"query": q, "format": "json"})
    req = urllib.request.Request(url, headers={"User-Agent": "searchhack-referee/0.1 (hackathon prototype)"})
    with urllib.request.urlopen(req, timeout=120) as r:
        rows = json.load(r)["results"]["bindings"]
    items = {}
    for b in rows:
        qid = b["x"]["value"].rsplit("/", 1)[1]
        names = [b["label"]["value"], *[a for a in b.get("alts", {}).get("value", "").split("|") if a]]
        if qid not in items:
            items[qid] = {"qid": qid, "label": names[0], "aliases": []}
        items[qid]["aliases"] += [n for n in names if n != items[qid]["label"] and n not in items[qid]["aliases"]]
    return list(items.values())


def build(names=None):
    DATA.mkdir(parents=True, exist_ok=True)
    for name, h in HUNTS.items():
        if names and name not in names:
            continue
        truth = sparql(h["where"])
        (DATA / f"{name}.json").write_text(json.dumps({"name": name, **h, "truth": truth,
                                                       "built": time.strftime("%Y-%m-%d")}, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"{name}: {len(truth)}")
        time.sleep(1)


def load(name):
    return {**json.loads((DATA / f"{name}.json").read_text(encoding="utf-8")), **HUNTS[name], "name": name}


def pool(p):
    return [n for n, h in HUNTS.items() if h["pool"] == p]
