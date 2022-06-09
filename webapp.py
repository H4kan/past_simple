from crypt import methods
from flask import Flask, render_template, request, redirect, url_for
from generator import fun
import json
from language import *
from probs import *
from generator import *
from queue import PriorityQueue
from random import randint
from hypothesis import Hypothesis
from algorithm import *
from language import *
from decode_utils import *

def generate_translation_options():
    # TODO: zmienic strukture maxP i bestTrans
    d = {}
    for key, value in probs_rev.trans.items():
        if (len(value) > MAX_SINGLE_TRANSLATION):
            maxP = []
            bestTrans = []
            for key2, value2 in value.items():
                if key2 == '\x00':
                    continue
                if len(maxP) < MAX_SINGLE_TRANSLATION:
                    maxP.append(value2)
                    bestTrans.append(key2)
                elif value2 > min(maxP):
                    i = maxP.index(min(maxP))
                    maxP.pop(i)
                    bestTrans.pop(i)
                    maxP.append(value2)
                    bestTrans.append(key2)
            d[key] = dict(zip(bestTrans, maxP))
        else:
            d[key] = value
    return d


with open('probs_rev.json') as json_file:
    probs_revJSON = json.load(json_file)

with open('probs.json') as json_file:
    probsJSON = json.load(json_file)

with open('lang.json') as json_file:
    langsJSON = json.load(json_file)

langs = langFromJson(langsJSON)

probs_rev = Probs(None, None,
                  probs_revJSON["allPlWords"],
                  probs_revJSON["allEnWords"],
                  probs_revJSON["fert"],
                  probs_revJSON["dist"],
                  probs_revJSON["trans"])
probs = Probs(None, None,
              probsJSON["allPlWords"],
              probsJSON["allEnWords"],
              probsJSON["fert"],
              probsJSON["dist"],
              probsJSON["trans"])
translation_options = generate_translation_options()
# Example sentence in German


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        entxt = request.form["entxt"]
        
        en = entxt.split(" ")
        en.append("\x00")
        # en = ["climate", "change", "are", "dangerous","\x00" ]

        res = fun(probs, probs_rev, langs, en,translation_options)
        pltxt = " ".join(res)
        
        return render_template("index.html", pltxt=pltxt, entxt=entxt)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port = 4444)
