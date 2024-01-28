from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import firebase_admin
from firebase_admin import credentials , firestore
from datetime import datetime
import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render, redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode


oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    user = request.session.get("user").get("userinfo").get("name")
    adref = db.collection('ADMIN').document(user).get()
    
    if adref.exists:
        return redirect(request.build_absolute_uri(reverse("helperPage")))
    return redirect(request.build_absolute_uri(reverse("userPage")))


def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )


def logout(request):
    request.session.clear()
    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("homePage")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )


cred = credentials.Certificate(r'auth.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
ref = db.collection('chatHistory')


def homePage(request):
    return render(request, 'index.html'  )

def helperPage(request):
    user = request.session.get("user").get("userinfo").get("name")
    adref = db.collection('ADMIN').document(user).get()
    if not adref.exists:
        return redirect(request.build_absolute_uri(reverse("userPage")))
    
    return render(request, 'helper.html', context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },)

def userPage(request):
    user = request.session.get("user").get("userinfo").get("name")
    adref = db.collection('ADMIN').document(user).get()
    if adref.exists:
        return redirect(request.build_absolute_uri(reverse("helperPage")))
    return render(request, 'user.html', context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },)

def get_users(request):
    users_ref = db.collection('chatHistory')
    docs = users_ref.stream()
    users = [doc.id for doc in docs]
    return JsonResponse({'users': users})

def get_chat_history_for_user(request):
    if request.method == 'GET':
        user = request.GET.get('user', '')
        user_doc = ref.document(user).get()

        if user_doc.exists:
            user_data = user_doc.to_dict()
            messages = user_data.get('Message', [])
            replies = user_data.get('replies', [])

            # Combine messages and replies, sort by timestamp
            chat_history = sorted(
                [{'type': 'message', 'content': message, 'timestamp': timestamp}
                 for message, timestamp in zip(messages, user_data.get('Timestamp', []))] +
                [{'type': 'reply', 'content': reply, 'timestamp': timestamp}
                 for reply, timestamp in zip(replies, user_data.get('replies_timestamp', []))],
                key=lambda x: x['timestamp']
            )

            return JsonResponse({'chat_history': chat_history}, status=202)
        else:
            return JsonResponse({}, status=203)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_chat_history(request):
    user = request.session.get("user").get("userinfo").get("name")

    print(user)
    user_doc = ref.document(user).get()

    if user_doc.exists:
        user_data = user_doc.to_dict()
        messages = user_data.get('Message', [])
        replies = user_data.get('replies', [])

        # Combine messages and replies, sort by timestamp
        chat_history = sorted(
            [{'type': 'message', 'content': message, 'timestamp': timestamp}
             for message, timestamp in zip(messages, user_data.get('Timestamp', []))] +
            [{'type': 'reply', 'content': reply, 'timestamp': timestamp}
             for reply, timestamp in zip(replies, user_data.get('replies_timestamp', []))],
            key=lambda x: x['timestamp']
        )
        print('sending chat history')
        return JsonResponse({'chat_history': chat_history}, status=202)
    else:
        print("No chat history found!")
        return JsonResponse({}, status=203)


def index(request):
    return render(request, 'index.html')


def send_reply(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user = request.session.get("user").get("userinfo").get("name")

        print(user)
        message = data.get('message', '')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Check if a document for the user already exists
        user_doc = ref.document(user).get()

        if user_doc.exists:
            # If the user document exists, update it by appending the new message
            user_data = user_doc.to_dict()
            user_data['replies'].append(message)
            user_data['replies_timestamp'].append(timestamp)
            ref.document(user).update(user_data)
        # else:
        #     user_data = {'User': user, 'Message': [message], 'Timestamp': [timestamp], 'replies': [], 'replies_timestamp': []}
        #     ref.document(user).set(user_data)

        return JsonResponse({'message': 'Success'},status=202)
    else:
        # Handle invalid request method (e.g., GET)
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user = request.session.get("user").get("userinfo").get("name")

        print(user)
        message = data.get('message', '')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Check if a document for the user already exists
        user_doc = ref.document(user).get()

        if user_doc.exists:
            # If the user document exists, update it by appending the new message
            user_data = user_doc.to_dict()
            user_data['Message'].append(message)
            user_data['Timestamp'].append(timestamp)
            ref.document(user).update(user_data)
        else:
            user_data = {'User': user, 'Message': [message], 'Timestamp': [timestamp], 'replies': [], 'replies_timestamp': []}
            ref.document(user).set(user_data)

        return JsonResponse({'message': 'Success'},status=202)
    else:
        # Handle invalid request method (e.g., GET)
        return JsonResponse({'error': 'Invalid request method'}, status=400)