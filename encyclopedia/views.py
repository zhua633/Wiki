from django.shortcuts import render
from markdown2 import Markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def NoEntry(request):
    return render(request, "encyclopedia/NoEntry.html")

def item(request, entry):
    content = util.get_entry(entry)
    if content==None:
        return render(request,"encyclopedia/NoEntry.html")

    else:
        return render(request,"encyclopedia/item.html",
            {"title": entry, "entry": Markdown().convert(content)},
        )
