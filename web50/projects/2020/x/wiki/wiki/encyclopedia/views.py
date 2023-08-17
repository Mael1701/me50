from django.shortcuts import render, redirect
from django.urls import reverse
import random
import markdown2
from django.http import HttpResponseRedirect
from .forms import NewEntryForm
from .forms import EditEntryForm
from .forms import SearchForm
from . import util




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    markdown_content = util.get_entry(title)

    if not markdown_content:
        return render(request, "encyclopedia/error.html", {
            "message": "La page demandée n'a pas été trouvée."
        })

    html_content = markdown2.markdown(markdown_content)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })


def search(request):
    query = request.GET.get('q')

    if not query:
        return redirect('encyclopedia:index')

    query = query.lower()
    entries = util.list_entries()

    matching_entries = [entry for entry in entries if query in entry.lower()]

    if len(matching_entries) == 1:
        return redirect('encyclopedia:entry', title=matching_entries[0])
    elif matching_entries:
        return render(request, "encyclopedia/search_results.html", {
            "entries": matching_entries
        })
    else:
        return render(request, "encyclopedia/search_results.html", {
            "entries": [],
            "message": "Aucun résultat trouvé pour votre recherche."
        })


def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)

    return HttpResponseRedirect(reverse('encyclopedia:entry', args=[random_entry]))

def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                context = {
                    "form": form,
                    "error_message": "This entry already exists!"
                }
                return render(request, "encyclopedia/new_entry.html", context)
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
    else:
        return render(request, "encyclopedia/new_entry.html", {"form": NewEntryForm()})

def edit_entry(request, title):
    entry_content = util.get_entry(title)
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data["content"]
            util.save_entry(title, new_content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
    else:
        form = EditEntryForm(initial={'content': entry_content})
    return render(request, "encyclopedia/edit_entry.html", {
        "title": title,
        "form": form
    })
