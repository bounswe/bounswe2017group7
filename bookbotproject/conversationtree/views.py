# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import MultipleObjectsReturned
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from conversationtree.models import Node
from conversationtree.models import Comment
from conversationtree.models import Rate
from conversationtree.models import Book
from serializers import NodeSerializer
from conversationtree.models import TelegramUser
from serializers import TelegramUserSerializer
from witapi import *
import numpy
import math
#import recommend

# Create your views here.
@csrf_exempt
def node_list(request):
    """
    List all nodes, or create a new node.
    """
    if request.method == 'GET':
        nodes = Node.objects.all()
        serializer = NodeSerializer(nodes, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NodeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def nodes_detail(request, pk):
    """
    Retrieve, update or delete a node.
    """
    try:
        node = Node.objects.get(intent=pk)
    except Node.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = NodeSerializer(node)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = NodeSerializer(node, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        node.delete()
        return HttpResponse(status=204)

@csrf_exempt
def get_user_info(request, pk):
    """
    Gets user info if it exists, otherwise creates new one 
    """
    try:
        user = TelegramUser.objects.get(userid=pk)
    except TelegramUser.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TelegramUserSerializer(user)
        return JsonResponse(serializer.data)

@csrf_exempt
def get_current_node(request, _userid):
    """
    Gets current node of user
    """
    try:
        curr_node_intent = TelegramUser.objects.get(userid=_userid).currentnode.intent
    except TelegramUser.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        intent=  "{\"intent\""+":\""+ curr_node_intent+"\"}"
        #{"name":"john","age":22,"class":"mca"}
        bytes = intent.encode('utf-8')
        print intent
        return HttpResponse(bytes, content_type='application/json')



@csrf_exempt
def add_new_user(request, _name, _userid, _chatid):
    """
    Gets user info if it exists, otherwise creates new one 
    """
    try:
        node = Node.objects.get(intent="root")
    except Node.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':
        newUser = TelegramUser.objects.create(name=_name, userid=_userid, chatid = _chatid, currentnode = node)
        return HttpResponse(status=200)



@csrf_exempt
def add_comment (  request, _title, _userid, _comment ):
        try:
            commentbook = Book.objects.get(title=_title)
            print(_title)
        except:
            Book.objects.create(title=_title)
            commentbook = Book.objects.get(title=_title)
        _user = TelegramUser.objects.get(userid=_userid)
        newComment = Comment.objects.create( user=_user,comment=_comment, book=commentbook)
        return HttpResponse(status=200)

@csrf_exempt
def add_rating (  request, _title, _userid, _rating ):
    _title_conv = _title.replace('_', ' ')
    try:
        ratebook = Book.objects.get(title=_title_conv)
        _count = ratebook.count
        _avg_rating = ratebook.avg_rating
        new_rating = (((_avg_rating*_count)+int(_rating))/(_count+1))
        Book.objects.filter(title=_title_conv).update(avg_rating=new_rating)
        Book.objects.filter(title=_title_conv).update(count=_count+1)
    except:
        Book.objects.create(title=_title_conv, avg_rating=_rating,count=1)
        ratebook = Book.objects.get(title=_title_conv)
    
    _user = TelegramUser.objects.get(userid=_userid)
    newRating = Rate.objects.create( user_id=_user.userid,value=int(_rating), book_title = _title_conv)

    return HttpResponse(status=200)
#def get_recommendation():

@csrf_exempt
def get_comments(request,book):
    """
    Returns comments of a given book 
    """ 

    try:
        b = Book.objects.get(title=book)
    except Book.DoesNotExist:
        comment_json="{\"comments\""+":\"None\"}"
        return HttpResponse(comment_json, content_type='application/json')

    try:
        comments = Comment.objects.get(book=b)
    except Comment.DoesNotExist:
        comment_json="{\"comments\""+":\"None\"}"
        return HttpResponse(comment_json, content_type='application/json')
    except MultipleObjectsReturned:
        comments = Comment.objects.filter(book=b).filter(isFlagged=False)


    if request.method == 'GET':
        print(comments)
        comment_json="{\"comments\""+":["
        for c in comments:
            comment_json += "{\"comment\":\"" + str(c.comment) + "\"},"

        comment_json = comment_json[:-1] + "]}"
        return HttpResponse(comment_json, content_type='application/json')

@csrf_exempt
def get_average_rating(request,book):
    """
    Returns average rating of a given book 
    """ 

    try:
        b = Book.objects.get(title=book)
    except Book.DoesNotExist:
        rate_json = "{\"rating\""+":\"None\"}"
        return HttpResponse(rate_json, content_type='application/json')


    if request.method == 'GET':
        rate_json = "{\"rating\""+":\""+ str(b.avg_rating)+"\"}"
        return HttpResponse(rate_json, content_type='application/json')


#recommendation part starts
class Table(dict):
    
    def __init__(self):
        self.value_indices = {}
    
    def set(self, i, j, v):
        self[(i, j)] = v
        if i in self.value_indices:
            self.value_indices[i].add(j)
        else:
            self.value_indices[i] = set([j])
        
    def read(self, i, j):
        return self.get((i, j), None)
    
    def hasValues(self, i):
        idx = self.value_indices.get(i, None)
        return idx

def importer(T):
    for i in range (len(Rate.objects.all())):
        tempRate = Rate.objects.all()[i]
        userid = tempRate.user_id
        booktitle = tempRate.book_title
        rating = tempRate.value
        T.set(userid, booktitle, rating)

def averagecalc(T):
    it = sorted(T.items())
    sums= {}
    counts= {}
    for i in it:
        user=i[0][0]
        rating=i[1]
        if user in sums:
            sums[user]= sums[user]+rating
            counts[user]= counts[user]+1
        else:
            sums[user]= rating
            counts[user]=1

    sumlist=sorted(sums.items())
    averages={}
    for user in sumlist:
        averages[user[0]]=sums[user[0]]/counts[user[0]]
    return averages

def predict(_userid, averages, T):
    userId = _userid
    v1=T.hasValues(userId)
    similarusers={}

    for j in sorted(averages.items()):
        simId = j[0]
        v2 = T.hasValues(simId)
        if userId != j[0] :

            myuser=[]
            simuser=[]
            similarity=0
            overlap = v1.intersection(v2)
            for i in overlap:
                myuser.append(T.read(userId, i) - averages[userId])
                simuser.append(T.read(simId,i)- averages[simId])

            myuserdot=numpy.array(myuser)
            simuserdot=numpy.array(simuser)
            dividend= numpy.dot(myuserdot.T, simuserdot)
            divider= math.sqrt(numpy.dot(myuserdot.T, myuserdot))*math.sqrt(numpy.dot(simuserdot.T, simuserdot))
            if divider!=0:
                similarity= dividend/divider

            if math.fabs(similarity)>0.5:
                similarusers[simId]=similarity
                if len(similarusers)>3:
                    break
    prediction = averages[userId]
    simeff=0
    simsum=0
    fivestars=[]
    fourstars=[]

    myuserbooks = []
    myuser =Rate.objects.filter(user_id=_userid)
    for i in range (len(myuser)):
        myuserbooks.append(myuser[i].book_title)

    for simus in similarusers.keys():

        rates=Rate.objects.filter(user_id=simus)



        #print rates[0].user_id
        for i in range(len(rates)):
            #print rates[i].book_title
            if(rates[i].value==5 and rates[i].book_title not in myuserbooks):
                fivestars.append(rates[i].book_title)
            elif(rates[i].value==4 and rates[i].book_title not in myuserbooks):
                fourstars.append(rates[i].book_title)
    
    print fivestars
    print fourstars
    if len(fivestars)>2:
        return fivestars
    else: 
        return fivestars + fourstars
#recommendation part ends

def get_response(request, _message, _chatid):
    """ waits until a response from wit ai, it may take so much time !!!!"""

    if request.method == 'GET':
        intent_ret = None
        intent_count = 0
        while intent_ret == None and intent_count<6:
            intent_count = intent_count + 1
            intent_ret = get_Intent(_message)


        curr_user = TelegramUser.objects.get(chatid=_chatid)
        curr_node = curr_user.currentnode

        db_intents = ['comment_on_book','book_name_comment','rate_book','book_name_rating','get_by_author','get_by_genre','get_by_title','get_comments','get_average_rating']
        if intent_ret is None and str(curr_node.intent) not in db_intents:
            return JsonResponse('I couldn\'t understand can you express it more simple?', safe=False)
        elif intent_ret == 'end_dialog':
            curr_user.currentnode=Node.objects.all()[0]
            curr_user.save()
            return JsonResponse('Goodbye bookworm!', safe=False)
        elif curr_node.intent == 'comment_on_book':
            curr_user.currentnode=curr_node.get_children()[0]
            curr_user.save()
            return JsonResponse(curr_user.currentnode.message, safe=False)
        elif curr_node.intent == 'get_comments':
            curr_user.currentnode=curr_node.get_children()[0]
            curr_user.save()
            return JsonResponse(curr_user.currentnode.message, safe=False)
        elif curr_node.intent == 'get_average_rating':
            curr_user.currentnode=curr_node.get_children()[0]
            curr_user.save()
            return JsonResponse(curr_user.currentnode.message, safe=False)
        elif curr_node.intent == 'avg':
            curr_user.currentnode=Node.objects.all()[0]
            curr_user.save()
            return JsonResponse(curr_user.currentnode.message, safe=False)
        elif curr_node.intent == 'comment':
            curr_user.currentnode=Node.objects.all()[0]
            curr_user.save()
            return JsonResponse(curr_user.currentnode.message, safe=False)
        elif curr_node.intent == 'book_name_comment':
            curr_user.currentnode=Node.objects.all()[0]
            curr_user.save()
            return JsonResponse('Your comment is saved!', safe=False)
        elif curr_node.intent == 'rate_book':
            curr_user.currentnode=curr_node.get_children()[0]
            curr_user.save()
            return JsonResponse(curr_user.currentnode.message, safe=False)
        elif curr_node.intent == 'book_name_rating':
            curr_user.currentnode=Node.objects.all()[0]
            curr_user.save()
            return JsonResponse('Your rating is saved!', safe=False)    
        elif curr_node.intent == 'search_by_author':
            curr_user.currentnode=curr_node.get_children()[0]
            curr_user.save()
            return JsonResponse(curr_user.currentnode.message, safe=False)  
        elif curr_node.intent == 'search_by_genre':
            curr_user.currentnode=curr_node.get_children()[0]
            curr_user.save()
            return JsonResponse(curr_user.currentnode.message, safe=False)
        elif curr_node.intent == 'search_by_title':
            curr_user.currentnode=curr_node.get_children()[0]
            curr_user.save()
            return JsonResponse(curr_user.currentnode.message, safe=False)

        elif curr_node.intent == 'get_by_author':
            curr_user.currentnode=Node.objects.all()[0]
            curr_user.save()
            return JsonResponse("Showing more books from this author", safe=False)

        elif curr_node.intent == 'get_by_genre':
            curr_user.currentnode=Node.objects.all()[0]
            curr_user.save()
            return JsonResponse("Showing more books from this genre", safe=False)

        elif curr_node.intent == 'get_by_title':
            curr_user.currentnode=Node.objects.all()[0]
            curr_user.save()
            return JsonResponse("Showing more books from this title", safe=False)

        elif curr_node.intent == 'recommendation':
            print('recommendation giris')
            T = Table()
            importer(T)
            averages=averagecalc(T)
            booklist = predict(curr_user.userid, averages, T)
            print(type(booklist))
            booklist = [book.encode('utf-8') for book in booklist]
            s = ""
            for book in booklist:
                s += book + ", "
            curr_user.currentnode=Node.objects.all()[0]
            
            curr_user.save()
            return JsonResponse(s[:-2], safe=False)
        else:   
            for i in range(len(curr_node.get_children())):
                if intent_ret == curr_node.get_children()[i].intent:
                    curr_user.currentnode=curr_node.get_children()[i]
                    curr_user.save()
                    return JsonResponse(curr_user.currentnode.message, safe=False)
            print('general_jose')
            return JsonResponse(curr_user.currentnode.message, safe=False)

        
