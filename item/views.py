from django.views.generic import DetailView
from .models import Item, Category
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import NewItemForm, EditItemForm
from django.shortcuts import render, redirect, get_object_or_404


class ItemDetailView(DetailView):
    model = Item
    template_name = 'detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()  # Retrieve the current item

        # Get related items
        related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=item.pk)[:3]

        # Add related items to the context
        context['related_items'] = related_items
        return context


def items(request):
    query = request.GET.get('query', '')  # This will change the url adding a query=word
    items = Item.objects.filter(is_sold=False)
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        """
        Ok, so this statement will analyze, first, if the word that the user put in the search bar matches with some
        product, or '|' if matches with the description of some product
        """
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
    })

@login_required
def new_item(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            """ This commit=False is an argument you can pass to form.save() to indicate that you want to
            create the model instance but not save it to the database immediately. This is useful when you need to
            perform additional operations or modifications on the model instance before saving it."""
            item.created_by = request.user
            item.save()
            return redirect('item:detail', pk=item.id)  # Redirect to your desired URL after successful form submission
    else:
        form = NewItemForm()

    return render(request, 'form.html', {
        'form': form,
        'title': 'Create Item',
    })


@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('core:index')


@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item:detail', pk=item.id)  # Redirect to your desired URL after successful form submission
    else:
        form = EditItemForm(instance=item)

    return render(request, 'form.html', {
        'form': form,
        'title': 'Edit Item'
    })
