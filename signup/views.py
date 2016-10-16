import PyPDF2 as PyPDF2
import numpy as np
from math import log
from django.http import HttpResponse
from django.urls import reverse
from passlib.handlers.sha2_crypt import sha256_crypt
from .models import User
from .forms import NameForm,LoginForm, UploadFileForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
import os
import json
try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'

x=User()
num_token={}
d2hash={}
d={}
doc_dict={}

def get_docx_text(path):
    """
    Take the path of a docx file as argument, return the text in unicode.
    """
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)

    paragraphs = []
    for paragraph in tree.getiterator(PARA):
        texts = [node.text
                 for node in paragraph.getiterator(TEXT)
                 if node.text]
        if texts:
            paragraphs.append(''.join(texts))

    return '\n\n'.join(paragraphs)


def convertpdf(name):
    pdfobj=open("UploadedDocuments/"+str(name),'rb')
    pdfreader=PyPDF2.PdfFileReader(pdfobj)
    print(pdfreader.numPages)
    desturl = "r"+str(name)+""
    fob = open("UploadedDocuments/" + desturl, "w", encoding="utf-8")
    for page in pdfreader.pages:
        s = page.extractText()
        lines=s.split("\\n")
        for line in lines:
            fob.write((line + "\n"))

    fob.close()
    pdfobj.close()


def handle_uploaded_file(f,name,content):
    global d2hash
    fo = open("UploadedDocuments/"+str(name), "wb+")
    for chunk in f.chunks():
        fo.write(chunk)
    fo.close()
    if content.endswith("pdf"):
        convertpdf(name)
    if content.endswith("document"):
        text = get_docx_text('UploadedDocuments/'+str(name))
        text = os.linesep.join([s for s in text.splitlines() if s])
        s=str(name)
        fo = open('UploadedDocuments/'+s[:s.rfind('.')]+".txt", "w",encoding="utf-8")
        fo.write(text)
        fo.close()
    filename="UploadedDocuments/"+str(name)
    maked2hash(filename)
    print("d2hash made successfully ")
    d2hash={}


def maked2hash(filename):
    global num_token
    global d
    global d2hash
    d1hash=np.load("preprocess/results/d1hash.npy").item()
    docs_len = np.load("preprocess/results/docslenhash.npy").item()
    c = 1
    fo = open(filename, "r", encoding="utf-8")
    str2 = fo.read()
    fo.close()
    lis = str2.strip().split()
    for i in lis:
        x = d1hash.get(i)

        n = len(x)
        d[i] = n
        num_token[c] = i
        list2 = x.keys()
        for j in list2:
            if j in d2hash:
                temp = d2hash.get(j)
                temp[c] = d1hash.get(i).get(j)
                d2hash[j] = temp

            else:
                d2hash[j] = {}
                d2hash[j][c] = d1hash.get(i).get(j)
        c += 1
    values2 = [{"doc id": k, "word count reference": v} for k, v in d2hash.items()]
    fo = open("preprocess/results/d2hash.json", "w")
    fo.write(json.dumps(values2, indent=4))
    fo.close()
    global doc_dict
    path = 'preprocess/Files'
    N=len([f for f in os.listdir(path)
                 if os.path.isfile(os.path.join(path, f))])
    for i in d2hash.keys():
        var = 0
        for j in d2hash[i]:
            n = d[num_token[j]]
            t = log(N / n)
            m = (log(d2hash[i][j] + 1) * t)
            var += m
            var=float(var)
        cosine = var / log(docs_len.get(i))
        # cosine = var / doc_count
        doc_dict[i] = cosine

    print(doc_dict)
    ll = list(doc_dict.values())
    ll.sort()
    print(ll)
    va = [{"doc id": k, "plag rate": v} for k, v in doc_dict.items()]

    fo = open("preprocess/results/final.json", "w")
    fo.write(json.dumps(va, indent=4))
    fo.close()


def index(request):
    # if this is a POST request we need to process the form data
    # print(x.email)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        signupform = NameForm(request.POST)
        loginform = LoginForm(request.POST)
        uploadform=UploadFileForm(request.POST, request.FILES)
        # check whether it's valid:
        if signupform.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            listusername = []
            listemail=[]
            for i in User.objects:
                listusername.append(i.username)
                listemail.append(i.email)
            if signupform.cleaned_data['your_username'] not in listusername:
                if signupform.cleaned_data['your_email'] not in listemail:
                    hash = sha256_crypt.encrypt(signupform.cleaned_data['your_password'])
                    user = User(name=signupform.cleaned_data['your_name'],
                                username=signupform.cleaned_data['your_username'],
                                email=signupform.cleaned_data['your_email'], password=hash)
                    user.save()
                    # return render(request, 'signup/success.html',{'name':signupform.cleaned_data['your_name']})
                    return HttpResponseRedirect(reverse('signup:success'))
                else:
                    return HttpResponse(
                        '<script> alert(\'EMAIL ALREADY REGISTERED..!!\'); window.location=""; </script>')
            else:
                return HttpResponse("<script> alert('USERNAME TAKEN ALREADY..please select a new one!!'); window.location=\"\"; </script>")


        if loginform.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            listusername=[]
            listemail=[]
            listpass=[]
            listname=[]
            for user in User.objects:
                listusername.append(user.username)
                listemail.append(user.email)
                listpass.append(user.password)
                listname.append(user.name)
            if loginform.cleaned_data['nameoremail'] in listusername:
                if sha256_crypt.verify(loginform.cleaned_data['passlogin'],listpass[listusername.index(loginform.cleaned_data['nameoremail'])]):

                    n=listname[listusername.index(loginform.cleaned_data['nameoremail'])]
                    request.session['name']=n
                    #return render(request, 'signup/loginsuccess.html',{'name': user.name})
                    return HttpResponseRedirect(reverse('signup:loginsuccess'))
                else:
                    '''
                    error="wrong password"
                    return render(request, 'signup/index.html', {'formsignup': signupform,'formlogin':loginform,'error':error})
                    '''
                    return HttpResponse("<script> alert('PASSWORD INCORRECT..!!'); window.location=\"\"; </script>")
            elif loginform.cleaned_data['nameoremail'] in listemail:
                if sha256_crypt.verify(loginform.cleaned_data['passlogin'],listpass[listemail.index(loginform.cleaned_data['nameoremail'])]):

                    n=listname[listemail.index(loginform.cleaned_data['nameoremail'])]
                    request.session['name']=n
                    #return render(request, 'signup/loginsuccess.html',{'name': user.name})
                    return HttpResponseRedirect(reverse('signup:loginsuccess'))
                else:
                    '''
                    error="wrong password"
                    return render(request, 'signup/index.html', {'formsignup': signupform,'formlogin':loginform,'error':error})
                    '''
                    return HttpResponse("<script> alert('PASSWORD INCORRECT..!!'); window.location=\"\"; </script>")

            else:
                '''
                error="Invalid username or email"
                return render(request, 'signup/index.html', {'formsignup': signupform,'formlogin':loginform,'error':error})
                '''
                return HttpResponse("<script> alert('invalid username or email..!!'); window.location=\"\"; </script>")

        if uploadform.is_valid():
            file = request.FILES['file']
            print(file.name)
            print(file.content_type)
            handle_uploaded_file(file,file.name,file.content_type)
            return HttpResponse('form has beeen submitted successfully')
    # if a GET (or any other method) we'll create a blank form
    else:
        signupform = NameForm()
        loginform=LoginForm()

    return render(request, 'signup/index.html', {'formsignup': signupform,'formlogin':loginform})


def success(request):
    return render(request,'signup/success.html',{})


def loginsuccess(request):
    print("this is session variable"+request.session['name'])
    form = UploadFileForm()
    return render(request,'signup/loginsuccess.html',{"name":request.session['name'],'form': form})

