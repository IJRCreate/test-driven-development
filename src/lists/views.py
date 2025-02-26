from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from lists.models import Item, List


def home_page(request):
    return render(request, "home.html")


def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    error = None
    if request.method == "POST":
        try:
            item = Item(text=request.POST["item_text"], list=our_list)
            item.full_clean()
            item.save()
            return redirect(our_list)
        except ValidationError:
            error = "You can't have an empty list item"
    return render(request, "list.html", {"list": our_list, "error": error})


def new_list(request):
    new_list_ = List.objects.create()
    item = Item.objects.create(text=request.POST["item_text"], list=new_list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        new_list_.delete()
        error = "You can't have an empty list item"
        return render(request, "home.html", {"error": error})
    return redirect(new_list_)
