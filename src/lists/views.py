from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from lists.models import Item, List


def home_page(request):
    return render(request, "home.html")


def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"], list=our_list)
        return redirect(f"/lists/{our_list.id}/")
    return render(request, "list.html", {"list": our_list})


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
    return redirect(f"/lists/{new_list_.id}/")
