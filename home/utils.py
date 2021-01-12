from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import *



class ObjectPostDetailMixin:
    model = None
    template = None


    def get(self, request, pk):
        obj = get_object_or_404(self.model, id=pk)
        return render(request, self.template, context={self.model.__name__.lower(): obj})


class ObjectCreateViewMixin:
    model = None
    template = None


    def get(self, request):
        form = self.model()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = self.model(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form})



class ObjectUpdateMixin:
    model = None
    form = None
    template = None

    def get(self, request, pk):
        obj_id =self.model.objects.get(id=pk)
        form = self.form(instance=obj_id)
        return render(request, self.template, context={'form': form,
                                                       self.model.__name__.lower(): obj_id})
    def post(self, request, pk):
        obj_id = self.model.objects.get(id=pk)
        form = self.form(request.POST, instance=obj_id)

        if form.is_valid():
            new_form = form.save()
            return redirect(new_form)
        return render(request, self.template, context={'form': form,
                                                       self.model.__name__.lower(): obj_id})


class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request, pk):
        obj = self.model(id=pk)
        return render(request, self.template, context={self.model.__name__.lower: obj})

    def post(self, request, pk):
        obj = self.model(id=pk)
        obj.delete()
        return redirect(reverse(self.redirect_url))


