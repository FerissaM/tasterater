from django.contrib.auth.forms import UserCreationForm
from .yelp_api import search_businesses, get_business_details
from .models import Restaurant, Review
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
  if 'term' in request.GET and 'location' in request.GET:
    term = request.GET['term']
    location = request.GET['location']
    results = search_businesses(term, location)
    return render (request, 'home.html', {'results': results['businesses']})
  return render(request, 'home.html')

@login_required
def add_review(request, yelp_id):
    restaurant = Restaurant.objects.filter(yelp_id=yelp_id).first()
    if not restaurant:
        business = get_business_details(yelp_id)
        if business and 'name' in business and 'location' in business and 'rating' in business:
            restaurant = Restaurant.objects.create(
                yelp_id=yelp_id,
                name=business['name'],
                location=business['location']['address1'],
                rating=business['rating']
            )
        else:
            return render(request, 'home.html', {'error_message': 'Failed to retrieve restaurant details from Yelp.'})
    if request.method == 'POST':
        text = request.POST['text']
        rating = request.POST['rating']
        Review.objects.create(user=request.user, restaurant=restaurant, text=text, rating=rating)
        return redirect('home')
    return render(request, 'add_review.html', {'restaurant': restaurant})

@login_required
def edit_review(request, review_id):
  review = get_object_or_404(Review, id=review_id)
  if request.method == 'POST':
    review.text = request.POST['text']
    request.rating = request.POST['rating']
    review.save()
    return redirect('home')
  return render(request, 'edit_review.html', {'review': review})  

@login_required
def delete_review(request, review_id):
  review = get_object_or_404(Review, id=review_id)
  review.delete()
  return redirect('home')  

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else : error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)