from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import urllib.request
from .models import PDFFile
from nltk.corpus import stopwords as sw
from nltk.tokenize import word_tokenize, sent_tokenize
import PyPDF2

# Create your views here.
def home(request):
    return render(request, 'rps/home.html')

def handleSignup(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for errors
        if len(username) > 50:
            messages.error(request, "Username must be under 50 characters")
            return render(request, 'rps/home.html')
        if pass1 != pass2:
            messages.error(request, "Passwords do not match!")
            return render(request, 'rps/home.html')
        if not username.isalnum():
            messages.error(request, "Your username should not contain special characters")
            return render(request, 'rps/home.html')
        # Create User
        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        messages.success(request, "Your RPS account has been successfully created")
        return render(request, 'rps/home.html')
    else:
        messages.error(request, "Invalid Response")
        return render(request, 'rps/home.html')

def handleLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In!")
        else:
            messages.error(request, "Invalid Credentials, Please try again")
        return render(request, 'rps/home.html')

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out!")
    return render(request, 'rps/home.html')


def handleSearch(request):
    if request.method == "POST":
        heading = request.POST['heading']
        values = dict()
        if PDFFile.objects.filter(filename=heading).exists():
            values['heading'] = heading
            values['file'] = PDFFile.objects.filter(filename=heading)
            return render(request, 'rps/show.html', context=values)
        else:
            messages.error(request, "No such summary available")
            return render(request, 'rps/home.html')


def extractPDF(request):
    if request.method == "POST":
        url = request.POST['link']
        print("URL: ", url)
        if url == '':
            messages.error(request, "Invalid URL")
            return render(request, 'rps/home.html')
        try:
            resp = urllib.request.urlopen(url)
            file = open('./rps/store/1.pdf', 'wb')
            file.write(resp.read())
            file.close()
        except Exception as e:
            print("Exception based url")
            print(e)
            messages.error(request, "Invalid URL")
            return render(request, 'rps/home.html')
        # Summarizing the Data
        values=dict()
        pdf = PyPDF2.PdfFileReader('./rps/store/1.pdf', strict=False)
        heading = pdf.getDocumentInfo()['/Title']
        pdfPages = pdf.getNumPages()
        content = ''
        for i in range(pdfPages):
            content += pdf.getPage(i).extractText()
        content = content.encode('utf-8', 'ignore').decode('utf-8')
        summarized_text = summarizer(content)
        if not PDFFile.objects.filter(filename=heading).exists():
            obj = PDFFile(filename=heading, summary=summarized_text)
            obj.save()
            print("hello")
        values['heading']=heading
        values['file']=PDFFile.objects.filter(filename=heading)
        return render(request, 'rps/show.html', context=values)


def summarizer(text):
    frequency_table = dict()
    sentence_frequency = dict()
    sum_values = 0
    summary = ""
    sentences = sent_tokenize(text)
    stopwords = sw.words('english')
    words = word_tokenize(text)

    for word in words:
        if word.lower() in stopwords:
            continue
        if word.lower() not in frequency_table:
            frequency_table[word.lower()] = 1
        else:
            frequency_table[word.lower()] += 1

    for sentence in sentences:
        for word, freqency in frequency_table.items():
            if word in sentence.lower():
                if sentence not in sentence_frequency:
                    sentence_frequency[sentence] = freqency
                else:
                    sentence_frequency[sentence] += freqency

    for sentence in sentence_frequency:
        sum_values += sentence_frequency[sentence]

    mean = sum_values // len(sentence_frequency)
    for sentence in sentences:
        if (sentence in sentence_frequency) and (sentence_frequency[sentence] > mean*1.2):
            summary += ' ' + sentence
    return summary

def download(request):
    if request.method == "POST":
        fs = FileSystemStorage()
        filename = 'rps/store/summary.pdf'
        if fs.exists(filename):
            with fs.open(filename) as pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="store/summary.pdf"'
                return response
        else:
            return HttpResponseNotFound('The requested pdf was not found in our server.')
