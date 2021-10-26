from typing import get_type_hints
from django.conf import settings
from django.db.models.expressions import RawSQL
from api.models import FlashDeck, Flashcard, ActivityMonitor, ScUser, FlashDeckUser, FlashcardUser
from api.serializers import ActivityMonitorSerializer, FlashCardSerializer, FlashCardUserSerializer, FlashDeckSerializer, UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from api.lib import get_logged_in_user
import datetime
import dateutil.relativedelta
from django.db.models import Sum

# from django.contrib.auth.models import User
from api.serializers import RegisterSerializer
from rest_framework import generics

from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny

from django.contrib.auth import get_user_model




class RegisterView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = (AllowAny,)
    queryset = get_user_model().objects.all()
    # permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class CustomAuthToken(ObtainAuthToken):
    authentication_classes = []
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        update_last_login(None, user)
        now = datetime.datetime.now()
        activity_monitor = ActivityMonitor(date = now, user = user)
        activity_monitor.save()
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'first_name': user.first_name,
            'last': user.last_name,
        })

class Logout(APIView):
    def post(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)



class DeckModelList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        objects  = FlashDeck.objects.filter(owner = request.user)
        serializer = FlashDeckSerializer(objects, many=True)
        return Response(serializer.data)


    # def post(self, request, format=None):
    #      print(request.data)
    #     #  serializer = TestModelSerializer(data=request.data)
    #     #  if serializer.is_valid():
    #     #      serializer.save()
    #     #      return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     #  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExistingFlashCardsList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        deck_id = request.query_params.get('deck_id')
        flashdeck = FlashDeck.objects.get(pk = deck_id)
        objects  = Flashcard.objects.filter(owner=request.user, flash_deck = flashdeck)
        serializer = FlashCardSerializer(objects, many=True)
        return Response(serializer.data)

class GetTodaysRevisionFlashCardforDeck(APIView):
    
    def get(self, request, format=None):
        deck_id = request.query_params.get('deck_id')
        flashdeck = FlashDeck.objects.get(pk = deck_id)
        objects  = Flashcard.objects.filter(owner=request.user, flash_deck = flashdeck)
        serializer = FlashCardSerializer(objects, many=True)
        returnlist=[]
        for row in serializer.data:
            flashcard_id=list(row.values())[0]
            # print(flashcard_id)
            objects1 = FlashcardUser.objects.filter(flashcard = flashcard_id,user=request.user)
            serializer1 = FlashCardUserSerializer(objects1, many=True)
            # print(serializer1.data)
            # if(list(serializer1.data[-1].values())[-1]!=None):
            #     print(datetime.datetime.strptime(list(serializer1.data[-1].values())[-1],"%Y-%m-%dT%H:%M:%S.%fZ"))
            # print(datetime.datetime.now())
            if(list(serializer1.data[-1].values())[-1]==None or datetime.datetime.strptime(list(serializer1.data[-1].values())[-1],"%Y-%m-%dT%H:%M:%S.%fZ")<=datetime.datetime.utcnow()):
                returnlist.append(row)
        print(returnlist)
        return Response(returnlist)

class SaveStart(APIView):
    def post(self, request, format=None): 
        objects1 = FlashcardUser.objects.filter(flashcard = request.data['flashcard_id'],user=request.user)
        serializer1 = FlashCardUserSerializer(objects1, many=True)    
        last_time_taken=list(serializer1.data[-1].values())[2] 
        if last_time_taken==None:
            last_time_taken=0
        last_opened=list(serializer1.data[-1].values())[1] 
        flashcard_user = FlashcardUser(flashcard_id = request.data['flashcard_id'], user = request.user,next_scheduled_at=datetime.datetime.now(),last_time_taken=last_time_taken,last_opened=last_opened,)
        flashcard_user.save()
        return Response(status=status.HTTP_201_CREATED)

class SaveFinish(APIView):
    def post(self, request, format=None):
        objects1 = FlashcardUser.objects.filter(flashcard = request.data['flashcard_id'],user=request.user)
        serializer1 = FlashCardUserSerializer(objects1, many=True)
        id_of_flashcarduser=list(serializer1.data[-1].values())[0]
        start_time=datetime.datetime.strptime(list(serializer1.data[-1].values())[-1],"%Y-%m-%dT%H:%M:%S.%fZ")
        end_time=datetime.datetime.now()
        difficulty=request.data['difficulty']
        alpha=0.5
        curr_time_taken=(end_time-start_time).seconds
        if(curr_time_taken>300):
            curr_time_taken=300
        last_time_taken=alpha*list(serializer1.data[-1].values())[2]+(1-alpha)*curr_time_taken
        now=datetime.datetime.utcnow()
        last_opened=list(serializer1.data[-1].values())[1]
        if last_opened==None:
            afterAminute=(now+dateutil.relativedelta.relativedelta(minutes=1))
            gap_in_revision=afterAminute-now
        else:
            gap_in_revision=now-datetime.datetime.strptime(last_opened,"%Y-%m-%dT%H:%M:%S.%fZ")
        
        penalty=(300-curr_time_taken)/300
        gap3days=dateutil.relativedelta.relativedelta(days=(3+int(penalty*7)))
        gap7days=dateutil.relativedelta.relativedelta(days=(7+int(penalty*14)))
        gap14days=dateutil.relativedelta.relativedelta(days=(14+int(penalty*30)))
        if(difficulty==1):
            next_scheduled_at=now+gap_in_revision+gap14days
            print(next_scheduled_at)
        elif difficulty==2:
            next_scheduled_at=now+gap_in_revision+gap7days
        else:
            next_scheduled_at=now+gap_in_revision+gap3days
        FlashcardUser.objects.filter(pk=id_of_flashcarduser).update(last_opened=datetime.datetime.now(),last_time_taken=last_time_taken,next_scheduled_at=next_scheduled_at,)
        # flashcard_user = FlashcardUser(flashcard_id = request.data['flashcard_id'], user = request.user,last_opened=datetime.datetime.now(),last_time_taken=last_time_taken,next_scheduled_at=next_scheduled_at,)
        # flashcard_user.save()
        activity_objects = ActivityMonitor.objects.filter(user=request.user)
        activity_serializer = ActivityMonitorSerializer(activity_objects, many=True)
        ActivityMonitor.objects.filter(pk=list(activity_serializer.data[-1].values())[0]).update(time_spent=curr_time_taken,cards_seen=list(activity_serializer.data[-1].values())[4]+1,)


        Flashcard.objects.filter(pk=request.data['flashcard_id']).update(next_scheduled_at=next_scheduled_at,)

        return Response(status=status.HTTP_201_CREATED)

        
class DeckManager(APIView):
    """
    List all snippets, or create a new snippet.
    """
    # def get(self, request, format=None):
    #     objects  = FlashDeck.objects.all()
    #     serializer = FlashDeckSerializer(objects, many=True)
    #     return Response(serializer.data)


    def post(self, request, format=None):
        custom_deck_ids=request.data['deck_ids']
        deck_title = request.data['title']
        deck = FlashDeck(title = deck_title, owner = request.user)
        deck.save()
        deck_user = FlashDeckUser(flashdeck = deck , user = request.user)
        deck_user.save()
        if(request.data['custom_required']==1 and len(custom_deck_ids)!=0):
            for deck_id in custom_deck_ids:
                flashdeck = FlashDeck.objects.get(pk = deck_id)
                objects  = Flashcard.objects.filter(owner=request.user, flash_deck = flashdeck)
                serializer = FlashCardSerializer(objects, many=True)
                for flashcard in serializer.data:
                    fcard=Flashcard(title=list(flashcard.values())[1],flash_deck_id=deck.id,owner=request.user,question=list(flashcard.values())[2],answer=list(flashcard.values())[3],)
                    fcard.save()
                    flashcard_user = FlashcardUser(flashcard = fcard, user = request.user)
                    flashcard_user.save()
        return Response(status=status.HTTP_201_CREATED)
        # if serializer.is_valid():
        #     serializer.save()
            
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewFlashCardList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    # def get(self, request, format=None):
    #     objects  = FlashDeck.objects.all()
    #     serializer = FlashDeckSerializer(objects, many=True)
    #     return Response(serializer.data)


    def post(self, request, format=None):
        print(request.data)
        card_title = request.data['title']
        card_question = request.data['question']
        card_answer = request.data['answer']
        deck_id = request.data['deck_id']
        
        now = datetime.datetime.now()
        flashdeck = FlashDeck.objects.get(pk = deck_id)
        flashcard = Flashcard(title = card_title, question = card_question, answer = card_answer, flash_deck = flashdeck, owner = request.user)
        flashcard.save()

        flashcard_user = FlashcardUser(flashcard = flashcard, user = request.user)
        flashcard_user.save()
        return Response(status=status.HTTP_201_CREATED)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteFlashCard(APIView):
    """
    List all snippets, or create a new snippet.
    """
    # def get(self, request, format=None):
    #     objects  = FlashDeck.objects.all()
    #     serializer = FlashDeckSerializer(objects, many=True)
    #     return Response(serializer.data)


    def post(self, request, format=None):
        Flashcard.objects.filter(pk=request.data['card_id']).delete()
        return Response(status=status.HTTP_201_CREATED)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditFlashCard(APIView):
    """
    List all snippets, or create a new snippet.
    """
    # def get(self, request, format=None):
    #     objects  = FlashDeck.objects.all()
    #     serializer = FlashDeckSerializer(objects, many=True)
    #     return Response(serializer.data)

    def post(self, request, format=None):
        print(request.data)
        Flashcard.objects.filter(pk=request.data['card_id']).update(title=request.data['title'],question=request.data['question'],answer=request.data['answer'],)
        
        return Response(status=status.HTTP_201_CREATED)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoggedinUserDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get(self, request, format=None):
        resp = get_logged_in_user()
        serializer = UserSerializer(resp)
        return Response(serializer.data)


class UserDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, key, value, current_user):
        #Getting user object which has correct value for that key
        kwargs = {
            '{0}'.format(key) : '{0}'.format(value)
        }
        try:
            current_user_id = current_user.id
            queryset = ScUser.objects.all().exclude(id = current_user_id)
            result =  queryset.filter(**kwargs)
            if(len(result) == 0):
                raise Http404
            return result[0]
        except ScUser.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        search_key = request.query_params.get('key')
        search_value = request.query_params.get('value')
        obj = self.get_object(search_key, search_value, request.user)
        serializer = UserSerializer(obj)
        return Response(serializer.data)


class FriendDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def post(self, request, format=None):
        print("\n\n\n\n\n")
        print(request.data)
        friend_user_id = request.data['friend_id']
        if not friend_user_id:
            raise Http404
        current_user = request.user
        new_user = ScUser.objects.get(id = friend_user_id)
        friend_ids = list(current_user.relations.all().values_list('id', flat=True))
        if new_user.id not in friend_ids:
            current_user.relations.add(new_user)
            current_user.save()
            serializer = UserSerializer(current_user)
            return Response(serializer.data)
        else:
            raise Http404

class FriendList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        current_user = request.user
        objects  = current_user.relations.all()
        serializer = UserSerializer(objects, many=True)
        return Response(serializer.data)

class LeaderboardList(APIView):

    def get_start_date(self, period):
        now = datetime.datetime.now()
        if period == 'Last 1 Month':
            return now + dateutil.relativedelta.relativedelta(months=-1)
        elif period == 'Last 7 Days':
            return now + dateutil.relativedelta.relativedelta(days=-7)
        elif period == 'Last 1 day':
            return now + dateutil.relativedelta.relativedelta(days=-1)
        return now

    def get_user_ids(self, current_user):
        all_ids = []
        all_ids.append(current_user.id)
        friend_ids = list(current_user.relations.all().values_list('id', flat=True))
        all_ids += friend_ids
        return all_ids

    def get_order_criteria(self, criteria):
        if(criteria == 'Cards Revised'):
            return "-total_cards"
        else:
            return "-total_time"

    def get(self, request, format=None):
        
        criteria = request.query_params.get('criteria')
        period = request.query_params.get('period')


        print("\n\n\n\\n\n\n")
        print(criteria, period)
        all_ids = self.get_user_ids(request.user)
        start_date = self.get_start_date(period)
        order = self.get_order_criteria(criteria)

        print("start_date: ", start_date)
        print("ids: ", all_ids)
        print("order: ", order)
        query_set = ActivityMonitor.objects.filter(user_id__in = all_ids, date__date__gt = start_date).values('user_id').annotate(total_time = Sum('time_spent'), total_cards = Sum('cards_seen')).order_by(order)
        result_set = []
        for result in query_set:
            data = {}
            user = ScUser.objects.get(pk = result['user_id'])
            data['username'] = user.username
            data['total_time'] = result['total_time'] 
            data['total_cards'] = result['total_cards'] 
            result_set.append(data)
        return Response(result_set)

class shareFlashdeck(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def post(self, request, format=None):
        deck_id = request.data['deck_id']
        friend_user_id = request.data['friend_id']

        friend = ScUser.objects.get(username = friend_user_id)
        deck_cpy = FlashDeck.objects.get(pk = deck_id)
        
        #copy deck to new object
        deck_cpy.id = None
        deck_cpy.owner = friend
        deck_cpy.save()

        old_deck = FlashDeck.objects.get(pk = deck_id)

        for card in old_deck.flashcard_set.all():
            flashcard = Flashcard(title = card.title, question = card.question, answer = card.answer, flash_deck = deck_cpy, owner = friend)
            flashcard.save()

            flashcard_user = FlashcardUser(flashcard = flashcard, user = friend)
            flashcard_user.save()
        return Response(status=status.HTTP_201_CREATED)

