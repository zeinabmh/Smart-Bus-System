from datetime import datetime
import json
import random
import re
import string
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
import requests
from .decorators import firebase_login_required
import requests  
from django.shortcuts import render, redirect
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import requests
import json
from django.http import HttpResponse
import firebase_admin
from firebase_admin import credentials, messaging

def index(request):
    token= generate_token()
    return render(request, 'driver/index.html',{'token': token})
def generate_token(length=16):
    """Generate a random token."""
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(length))
    return token
def homepage(request):
    

    if request.method == 'POST':
        # Get the token from the POST data
        email = request.POST.get('email')
        request.session['email'] = email
        token = request.POST.get('token')
        # Get the token stored in the session (for comparison if needed)
        
        print(token)
        # Check if the tokens match
        if token == None:
            return HttpResponseForbidden("Access Denied")
        
        # Continue rendering the incomes page if tokens match
        return render(request, 'driver/homepage.html')
    else:
        return HttpResponseForbidden("Access Denied")
def reservations(request):
    if request.method == 'POST':
        db = firestore.client()
        email = request.session.get('email')
        print(email)
        drivers_ref = db.collection('Drivers').where('email', '==', email).limit(1)
        
        # Get the documents returned by the query
        driver_docs = drivers_ref.get()

        # Initialize busname variable
        busname = None

        # Check if any documents were found
        for doc in driver_docs:
            # Extract the 'busname' field from the document
            busname = doc.to_dict().get('busname')
            print(busname)
            request.session['busname'] = busname

        if busname is not None:
            trips_ref = db.collection('Trips').where('busName', '==', busname)
            
            # List to store dates
            dates = []

            # Get the documents returned by the query
            trips_docs = trips_ref.get()

            # Iterate over the documents
            for doc in trips_docs:
                # Extract the 'dates' field from the document
                trip_data = doc.to_dict()
                if trip_data.get('busName') == busname:
                    dates.append(trip_data.get('date', ''))
            

            d=list(set(dates))
            
            context = {'busname': busname,'d':d}
            return render(request, 'driver/reservations.html', context)
        else:
            return HttpResponseForbidden("No busname found for the given email.")
    else:
        return HttpResponseForbidden("Access Denied")                                                                                                                                        
def payments(request):
    if request.method == 'POST':
   
         return render(request, 'driver/payments.html')
    else:
        return HttpResponseForbidden("Access Denied")
def sendnot(request):
    if request.method == 'POST':
        db = firestore.client()
        email = request.session.get('email')
        print(email)
        drivers_ref = db.collection('Drivers').where('email', '==', email).limit(1)
        
        # Get the documents returned by the query
        driver_docs = drivers_ref.get()

        # Initialize busname variable
        busname = None

        # Check if any documents were found
        for doc in driver_docs:
            # Extract the 'busname' field from the document
            busname = doc.to_dict().get('busname')
            print(busname)

        if busname is not None:
            trips_ref = db.collection('Trips').where('busName', '==', busname)
            
            # List to store dates
            dates = []

            # Get the documents returned by the query
            trips_docs = trips_ref.get()

            # Iterate over the documents
            for doc in trips_docs:
                # Extract the 'dates' field from the document
                trip_data = doc.to_dict()
                if trip_data.get('busName') == busname:
                    dates.append(trip_data.get('date', ''))
            

            d=list(set(dates))
            
            context = {'busname': busname,'d':d}
            return render(request, 'driver/sendnot.html', context)
        else:
            return HttpResponseForbidden("No busname found for the given email.")
    else:
        return HttpResponseForbidden("Access Denied")     
def resetpassword(request):
    if request.method == 'POST':
        password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')
        email = request.session.get('email')
        
        # Validate password format
        if not is_valid_password(password):
            error_message = "Password must be at least 8 characters long and contain at least one digit and one special character (@#$%^&*)"
            return render(request, 'driver/resetpassword.html', {'error_message': error_message})

        if password == confirm_password:
            # Check if the user exists
            user = auth.get_user_by_email(email)
            if user:
                # Update the user's password
                auth.update_user(
                    user.uid,
                    password=password
                )

                message = "Password is updated successfully!"
                return render(request, 'driver/resetpassword.html', {'message': message})
            else:
                error_message = "User does not exist."
                return render(request, 'driver/resetpassword.html', {'error_message': error_message})
        else:
            # Passwords don't match, display error message
            error_message = "Passwords don't match."
            return render(request, 'driver/resetpassword.html', {'error_message': error_message})
    
    return render(request, 'driver/resetpassword.html')

def is_valid_password(password):
    # Validate password format: at least 8 characters with at least one digit and one special character
    if len(password) < 8:
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*]', password):
        return False
    return True
def forgetpass(request):
    return render(request, 'driver/forgetpass.html')
def payments(request):
    email = request.session.get('email')
    
    # Initialize Firestore client
    db = firestore.client()
    
    # Query Firestore collection for document containing the email
    drivers_ref = db.collection('Drivers').where('email', '==', email).limit(1).get()
    
    # Extract document ID
    document_id = None
    for doc in drivers_ref:
        document_id = doc.id
        
        break  # Assuming there's only one document
    busname = None
    for doc in drivers_ref:
        busname = doc.to_dict().get('busname')
        print(busname)
    
    # Pass the document ID to the template if found
    context = {'document_id': document_id, 'busname':busname}
    
    return render(request, 'driver/payments.html', context)
def sendnot(request):
    if request.method == 'POST':
        db = firestore.client()
        email = request.session.get('email')
        print(email)
        drivers_ref = db.collection('Drivers').where('email', '==', email).limit(1)
        
        # Get the documents returned by the query
        driver_docs = drivers_ref.get()

        # Initialize busname variable
        busname = None

        # Check if any documents were found
        for doc in driver_docs:
            # Extract the 'busname' field from the document
            busname = doc.to_dict().get('busname')
            print(busname)

        if busname is not None:
            trips_ref = db.collection('Trips').where('busName', '==', busname)
            
            # List to store dates
            dates = []

            # Get the documents returned by the query
            trips_docs = trips_ref.get()

            # Iterate over the documents
            for doc in trips_docs:
                # Extract the 'dates' field from the document
                trip_data = doc.to_dict()
                if trip_data.get('busName') == busname:
                    dates.append(trip_data.get('date', ''))
            

            d=list(set(dates))
            
            context = {'busname': busname,'d':d}
    return render(request, 'driver/sendnot.html', context)

'''def send_not(request):
    if request.method == 'POST':
        message = request.POST.get('notificationMessage')
        token = request.POST.get('token')

        server_key = 'AAAAfVles3E:APA91bHb4miaOIYmNQTTDObJ5LZqLiPoCr3qeTgBf_7k80ESQpxX_f3QRFfX7sKce8OCNOL36z5tKsHJATf6pNL0psfASl1t6tV-XR-Wdpc0O9lrPycRtkc_wAUeLlUYLiJ5go8ERLVS'
        url = 'https://fcm.googleapis.com/fcm/send'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=' + server_key,
        }
        payload = {
            'to': token,
            'notification': {
                'title': 'New Notification',
                'body': message,
            },
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            return HttpResponse('Notification sent successfully!')
        else:
            return HttpResponse(f'Failed to send notification. Response: {response.text}', status=response.status_code)
    else:
creturn HttpResponse('Invalid request method', status=405)'''

   
    
    # Initialize Firestore client
   
    
    

def send_not(request):
    if request.method == 'POST':
        message_body = request.POST.get('notificationMessage')
        tokens = request.POST.get('passengerIds')
        busname = request.POST.get('busname')
        s = tokens.strip("[]").replace("'", "")
        token = s.split(",")
        # Split the tokens by comma and strip any extra whitespace
        token_list = [name.strip() for name in token]
        titles="New Notification from "+busname
        print(token_list)
        # Create the notification
        notification = messaging.Notification(
            title=titles,
            body=message_body,
        )

        # Track successes and failures
        success_count = 0
        failure_count = 0
        errors = []

        for token in token_list:
           
            # Create the message for each token
            token= token.replace('"','')
            message = messaging.Message(
                notification=notification,
                token=token,
            )
            try:
                # Send a message to the device corresponding to the provided token
                response = messaging.send(message)
                print('Successfully sent message:', response)
                success_count += 1
            except Exception as e:
                print('Error sending message:', e)
                failure_count += 1
                errors.append(str(e))

        return HttpResponse(f'Notification sent successfully to devices. Failed to send to {failure_count} devices. Errors: {errors}')
    else:
        return HttpResponse('Invalid request method', status=405)

