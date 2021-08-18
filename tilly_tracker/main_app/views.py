from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Plant, Vessel, Watering
from .forms import WateringForm

# Create your views here.

# Class-Based-Views
class PlantCreate(LoginRequiredMixin, CreateView):
    model = Plant
    fields = "__all__"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PlantUpdate(LoginRequiredMixin, UpdateView):
    model = Plant
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ["species", "description", "age"]


class PlantDelete(LoginRequiredMixin, DeleteView):
    model = Plant
    success_url = "/plants/"


# Define the home view


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def signup(request):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
        else:
            error_message = "Invalid sign up - try again"
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "registration/signup.html", context)

@login_required
def plants_index(request):
    plants = Plant.objects.filter(owner=request.user)
    return render(request, "plants/index.html", {"plants": plants})

@login_required
def plant_detail(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    unused_containers = Vessel.objects.exclude(
        id__in=plant.vessels.all().values_list("id")
    )
    watering_form = WateringForm()
    return render(
        request,
        "plants/detail.html",
        {
            "plant": plant,
            "watering_form": watering_form,
            "vessels": unused_containers,
        },
    )

@login_required
def add_watering(request, plant_id):
    # create a ModelForm instance using the data in request.POST
    form = WateringForm(request.POST)
    # validate the form
    if form.is_valid():
        new_watering = form.save(commit=False)
        new_watering.plant_id = plant_id
        new_watering.save()
    return redirect("detail", plant_id=plant_id)


@login_required
def delete_watering(request, plant_id, w_id):
    plant = Plant.objects.get(id=plant_id)
    watering = Watering.objects.get(plant_id=plant_id, id=w_id)
    plant.watering_set.remove(watering)
    return redirect("detail", plant_id=plant_id)


@login_required
def reset_watering(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    plant.watering_set.clear()
    return redirect("detail", plant_id=plant_id)


def assoc_vessel(request, plant_id, vessel_id):
  # Note that you can pass a toy's id instead of the whole object
  Plant.objects.get(id=plant_id).vessels.add(vessel_id)
  return redirect('detail', plant_id=plant_id)

class VesselList(LoginRequiredMixin, ListView):
    model = Vessel

class VesselDetail(LoginRequiredMixin, DetailView):
    model = Vessel

class VesselCreate(LoginRequiredMixin, CreateView):
    model = Vessel
    fields = "__all__"

class VesselUpdate(LoginRequiredMixin, UpdateView):
    model = Vessel
    fields = ["name", "color"]

class VesselDelete(LoginRequiredMixin, DeleteView):
    model = Vessel
    success_url = "/vessels/"
