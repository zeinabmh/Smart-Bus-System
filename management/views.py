from argparse import Action
from pickletools import pystring
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from firebase_admin import firestore
# Create your views here.
def index(request):
    return render(request, 'management/index.html')
def options(request):
    return render(request, 'management/options.html')
def adddriver(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        bus=request.POST.get("bus_name")
        if not name or not email:
            return HttpResponse("Name and email are required.", status=400)

       
        db = firestore.client()

        
        data = {
            'name': name,
            'email': email,
            'password': password,
            'phone number': phone,
            'Bus Name': bus
           
        }

       
        
        doc_ref = db.collection('Drivers').document()

        try:
            # Set data to Firestore document
            doc_ref.set(data)

            # Provide feedback to the user
            return HttpResponse("Registration successful. Document ID: " + doc_ref.id)
        except Exception as e:
            # Handle errors gracefully
            return HttpResponse("An error occurred: " + str(e), status=500)
    return render(request, 'management/adddriver.html')
def deletedriver(request):
    db = firestore.client()
    
        





    email = request.POST.get('email')
    
            # Query Firestore to find the driver document with the provided email
    drivers_ref = db.collection('Drivers')
    query = drivers_ref.where('email', '==', email).limit(1)
    docs = query.stream()
    for doc in docs:
            doc.reference.delete()
            return  HttpResponse("deleted!")
            
        
    return render(request, 'management/deletedriver.html')



def showdriver(request):
    db = firestore.client()
    
       
    db = firestore.client()
    doc_ref = db.collection("Drivers").document('73tQyRBMUorp9SyCpCcN')

    doc = doc_ref.get()
    if doc.exists:
         c= doc.to_dict()
         return render(request, 'management/showdriver.html', {'c': c})
    return render(request, 'management/showdriver.html')