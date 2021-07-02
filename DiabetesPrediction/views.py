from django.http import JsonResponse, BadHeaderError
from django.shortcuts import render
import numpy as np
import pandas as pd
from pyglet import model
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import date

from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
from .forms import ContactForm


def home(request):
    return render(request, 'Home.html')


def predict(request):
    return render(request, 'Prediction.html')


def result(request):
    #  Data collection and analaysis
    #  PIMA Diabetes Dataset
    # 1.loading the diabetes dataset to a pandas dataframe
    diabetes_dataset = pd.read_csv(r'C:\Users\anjal\PycharmProjects\Diabetes prediction ml project\diabetes.csv')

    # seperating the data and labels
    X = diabetes_dataset.drop('Outcome', axis=1)
    Y = diabetes_dataset['Outcome']
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

    # Training the model

    classifier = svm.SVC(kernel='linear')

    # training the support vector machine classifier

    classifier.fit(X_train, Y_train)

    val1 = float(request.GET['n1'])
    val2 = float(request.GET['n2'])
    val3 = float(request.GET['n3'])
    val4 = float(request.GET['n4'])
    val5 = float(request.GET['n5'])
    val6 = float(request.GET['n6'])
    val7 = float(request.GET['n7'])
    val8 = float(request.GET['n8'])

    # storing value to pred variable
    pred = classifier.predict([[val1, val2, val3, val4, val5, val6, val7, val8]])

    result1 = ""
    if pred == [1]:
        result1 = "Positive"
    else:
        result1 = "Negative"

    return render(request, 'Prediction.html', {"result2": result1})


def heart(request):
    """
    Reading the training data set.
    """
    df = pd.read_csv(r'C:\Users\anjal\PycharmProjects\Diabetes prediction ml project\Heart_train.csv')
    data = df.values
    X = data[:, :-1]
    Y = data[:, -1:]

    """ 
    
    Reading data from the user. 
    """

    value = ''

    if request.method == 'POST':

        age = float(request.POST['age'])
        sex = float(request.POST['sex'])
        cp = float(request.POST['cp'])
        trestbps = float(request.POST['trestbps'])
        chol = float(request.POST['chol'])
        fbs = float(request.POST['fbs'])
        restecg = float(request.POST['restecg'])
        thalach = float(request.POST['thalach'])
        exang = float(request.POST['exang'])
        oldpeak = float(request.POST['oldpeak'])
        slope = float(request.POST['slope'])
        ca = float(request.POST['ca'])
        thal = float(request.POST['thal'])

        user_data = np.array(
            (age,
             sex,
             cp,
             trestbps,
             chol,
             fbs,
             restecg,
             thalach,
             exang,
             oldpeak,
             slope,
             ca,
             thal)
        ).reshape(1, 13)

        rf = RandomForestClassifier(
            n_estimators=16,
            criterion='entropy',
            max_depth=9
        )

        rf.fit(np.nan_to_num(X), Y)
        rf.score(np.nan_to_num(X), Y)
        predictions = rf.predict(user_data)

        if int(predictions[0]) == 1:
            value = 'have'
        elif int(predictions[0]) == 0:
            value = "don\'t have"

    return render(request,
                  'heart.html',
                  {
                      'context': value,
                      'title': 'Heart Disease Prediction',
                      'active': 'btn btn-success peach-gradient text-white',
                      'heart': True,
                      'background': 'bg-danger text-white'
                  })


# Create your views here.


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'This user name is already exist')
            return redirect('register')

        elif User.objects.filter(email=email).exists():
            messages.info(request, 'This email is already exist ')
            return redirect('register')

        else:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password, email=email)
            user.save();
            messages.success(request, f"New Account Created: {username}")
            return redirect('login')



    else:
        return render(request, 'register.html')


def login(request):
    global username
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'username or password not correct')
            return redirect('login')

    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('Home')


# Create your views here.


# loading model

import joblib as jb
import cgi, os

# !C:\Users\anjal\AppData\Local\Programs\Python\Python39

model = jb.load(r'C:\Users\anjal\PycharmProjects\Diabetes prediction ml project\DiabetesPrediction\trained_model (1)')


def checkdisease(request):
    global predicted_disease, confidencescore
    diseaselist = ['Fungal_infection', 'Allergy', 'GERD', 'Chronic_cholestasis', 'Drug_Reaction', 'Peptic_ulcer_diseae',
                   'AIDS', 'Diabetes ',
                   'Gastroenteritis', 'Bronchial Asthma', 'Hypertension ', 'Migraine', 'Cervical spondylosis',
                   'Paralysis(brain hemorrhage)',
                   'Jaundice', 'Malaria', 'Chickenpox', 'Dengue', 'Typhoid', 'hepatitis A', 'Hepatitis B',
                   'Hepatitis C', 'Hepatitis D',
                   'Hepatitis E', 'Alcoholic hepatitis', 'Tuberculosis', 'CommonCold', 'Pneumonia',
                   'Dimorphic hemmorhoids(piles)',
                   'Heart attack', 'Varicose_veins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia',
                   'Osteoarthristis',
                   'Arthritis', '(vertigo) Paroymsal  Positional Vertigo', 'Acne', 'Urinarytract_infection',
                   'Psoriasis', 'Impetigo']

    symptomslist = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills',
                    'joint_pain',
                    'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition',
                    'spotting_ urination',
                    'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss',
                    'restlessness', 'lethargy',
                    'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes',
                    'breathlessness', 'sweating',
                    'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea',
                    'loss_of_appetite', 'pain_behind_the_eyes',
                    'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine',
                    'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach',
                    'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation',
                    'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
                    'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
                    'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
                    'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails',
                    'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips',
                    'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints',
                    'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness',
                    'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine',
                    'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
                    'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body',
                    'belly_pain',
                    'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite',
                    'polyuria', 'family_history', 'mucoid_sputum',
                    'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion',
                    'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen',
                    'history_of_alcohol_consumption', 'fluid_overload', 'blood_in_sputum', 'prominent_veins_on_calf',
                    'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling',
                    'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister',
                    'red_sore_around_nose',
                    'yellow_crust_ooze']

    alphabaticsymptomslist = sorted(symptomslist)

    if request.method == 'GET':
        return render(request, 'checkdisease.html', {"list2": alphabaticsymptomslist})




    elif request.method == 'POST':

        ## access you data by playing around with the request.POST object

        inputno = int(request.POST["noofsym"])
        print(inputno)
        if (inputno == 0):
            return JsonResponse({'predicteddisease': "none", 'confidencescore': 0})

        else:

            psymptoms = []
            psymptoms = request.POST.getlist("symptoms[]")

            print(psymptoms)

            """      #main code start from here...
            """

            testingsymptoms = []
            # append zero in all coloumn fields...
            for x in range(0, len(symptomslist)):
                testingsymptoms.append(0)

            # update 1 where symptoms gets matched...
            for k in range(0, len(symptomslist)):

                for z in psymptoms:
                    if (z == symptomslist[k]):
                        testingsymptoms[k] = 1

            inputtest = [testingsymptoms]

            print(inputtest)

            predicted = model.predict(inputtest)
            print("predicted disease is : ")
            print(predicted)

            y_pred_2 = model.predict_proba(inputtest)
            confidencescore = y_pred_2.max() * 100
            print(" confidence score of : = {0} ".format(confidencescore))

            confidencescore = format(confidencescore, '.0f')
            predicted_disease = predicted[0]

    return JsonResponse({'predicteddisease': predicted_disease, 'confidencescore': confidencescore,
                         })

    # new logic!


def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, 'contact.html', {'form': form})


def successView(request):
    return render(request,'success.html')
