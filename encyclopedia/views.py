from django.forms import TextInput,Textarea
from django.shortcuts import render
from markdown2 import Markdown
from . import util
from random import randint
from django import forms
from django.contrib import messages

class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'size':'110'}))
    content = forms.CharField(widget=forms.Textarea())


def NewPage(request):
    if request.method == "POST":

        form = NewPageForm(request.POST)

        if form.is_valid():

            title= form.cleaned_data["title"]
            content= form.cleaned_data["content"]

            current_entries=util.list_entries()
            for entry in current_entries:
                if entry.lower() == title.lower():
                    messages.warning(request, 'This entry already exists, please choose another title')
                    return render(request,"encyclopedia/NewPage.html", {"form": form})

            util.save_entry(title,content)
            with open(f"entries/{title}.md", "w") as file:
                hash="# "+title+"\n"
                file.write(hash)
                file.write(content)

            content = util.get_entry(title)
            return render(request,"encyclopedia/item.html",
                {"title":title, "entry": Markdown().convert(content)}
            )

        else:
            return render(request,"encyclopedia/NewPage.html", {"form": form})
    return render(request, "encyclopedia/NewPage.html", {"form": NewPageForm()})

def EditPage(request,entry):
    form = NewPageForm()
    content=util.get_entry(entry)
    title=entry
    form.fields["title"].initial=title
    form.fields["content"].initial=content.replace(("# "+title),"")

    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():
            title= form.cleaned_data["title"]
            content= form.cleaned_data["content"]

            with open(f"entries/{title}.md", "w") as file:
                hash="# "+title
                file.write(hash)
                file.write("\n")
                file.write(content)


            format = util.get_entry(title)
            return render(request,"encyclopedia/item.html",
                {"title":title, "entry": Markdown().convert(format)}
            )
        else:
            return render(request,"encyclopedia/EditPage.html", {"form": form})

    return render(request, "encyclopedia/EditPage.html", {
        "title":title,
        "form": form})


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

def searchresults(request):
    
    querystr=request.GET.get('q','')
    results=[]

    if util.get_entry(querystr) is None:
        for entry in util.list_entries():
            if querystr.lower() in entry.lower():
                results.append(entry)
        return render(request,"encyclopedia/searchresults.html", {"results": results, "querystr": querystr})

    else: 
        content = util.get_entry(querystr)
        return render(request,"encyclopedia/item.html",
            {"title":querystr, "entry": Markdown().convert(content)}
        )

def RandomPage(request):
    pages = util.list_entries()
    entry=pages[randint(0,len(pages)-1)]

    return render(request,"encyclopedia/item.html",
        {"title":entry, "entry": Markdown().convert(util.get_entry(entry))}
    )
            
