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
from api.serializers import RegisterSerializer
from rest_framework import generics
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

class RegisterView(generics.CreateAPIView):
    """
        Description:
            Contains Registration variables initialization
    """
    authentication_classes = []
    permission_classes = (AllowAny,)
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer


class CustomAuthToken(ObtainAuthToken):
    """
        Description:
            Contains post function to create a custom authentication token
    """
    authentication_classes = []
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Description:
            For a login generate Authentication Token

        Arguments:
            request - contains login data

        Returns:
            Status if token created
        """
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
    """
        Description:
            Contains post function for logging out
    """
    def post(self, request, format=None):
        """
        Description:
            Deleted token to force a login
        Arguments:
            request - contains authentication token

        Returns:
            Status of logging out
        """
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class DeckModelList(APIView):
    """
        Description:
            Contains get function for getting decks
    """
    def get(self, request, format=None):
        """
        Description:
            Returns all decks for a user

        Arguments:
            request - contains deck id

        Returns:
            All decks of user
        """
        objects  = FlashDeck.objects.filter(owner = request.user)
        serializer = FlashDeckSerializer(objects, many=True)
        return Response(serializer.data)

class ExistingFlashCardsList(APIView):
    """
        Description:
            Contains get function for fetching flashcards
    """
    def get(self, request, format=None):
        """
        Description:
            Returns all the flashcards for a deck
        Arguments:
            request - contains deck id

        Returns:
            Flashcard for deck id
        """
        deck_id = request.query_params.get('deck_id')
        flashdeck = FlashDeck.objects.get(pk = deck_id)
        objects  = Flashcard.objects.filter(owner=request.user, flash_deck = flashdeck)
        serializer = FlashCardSerializer(objects, many=True)
        return Response(serializer.data)

class GetTodaysRevisionFlashCardforDeck(APIView):
    """
        Description:
            Contains get function for active recall
    """
    def get(self, request, format=None):
        """
        Description:
            Retuns all the flash cards that are due before today sorted in time taken in previous revision
        Arguments:
            request - deck id

        Returns:
            Cards that need to be revised today
        """
        deck_id = request.query_params.get('deck_id')
        flashdeck = FlashDeck.objects.get(pk = deck_id)
        objects  = Flashcard.objects.filter(owner=request.user, flash_deck = flashdeck)
        serializer = FlashCardSerializer(objects, many=True)
        returnlist=[]
        for row in serializer.data:
            flashcard_id=list(row.values())[0]
            objects1 = FlashcardUser.objects.filter(flashcard = flashcard_id,user=request.user)
            serializer1 = FlashCardUserSerializer(objects1, many=True)
            if(list(serializer1.data[-1].values())[-1]==None or datetime.datetime.strptime(list(serializer1.data[-1].values())[-1],"%Y-%m-%dT%H:%M:%S.%fZ")<=datetime.datetime.utcnow()):
                returnlist.append(row)
        final_returnlist=[]
        list_len=len(returnlist)
        for i in range(list_len):
            min_index=0
            min_time=list(returnlist[0].values())[2]
            index=0
            min_row=returnlist[0]
            for row in returnlist:
                if(list(row.values())[2]>min_time):
                    min_index=index
                    min_time=list(row.values())[2]
                    min_row=row
                index+=1
            final_returnlist.append(min_row)
            del returnlist[min_index]
        return Response(final_returnlist)

class SaveStart(APIView):
    """
        Description:
            Contains post function for storing start time of flashcards
    """
    def post(self, request, format=None): 
        """
        Description:
            Stores a dummy date in flashcarduser model to later compare the time and know the time taken by user

        Arguments:
            request - Flash card id that started revision 

        Returns:
            Status if the start time is saved or not
        """
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
    """
        Description:
            Contains post function for storing end time of flashcards
    """
    def post(self, request, format=None):
        """
        Description:
            Stores the next_scheduled_day for flashcard after revising the card by calculating the time taken and user's selection

        Arguments:
            request - flashcard if of current flash card that finished revising 

        Returns:
            Status if the card is scheduled or not
        """
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
        elif difficulty==2:
            next_scheduled_at=now+gap_in_revision+gap7days
        else:
            next_scheduled_at=now+gap_in_revision+gap3days
        # Chaining Filters: https://stackoverflow.com/questions/8164675/chaining-multiple-filter-in-django-is-this-a-bug
        FlashcardUser.objects.filter(pk=id_of_flashcarduser).update(last_opened=datetime.datetime.now(),last_time_taken=last_time_taken,next_scheduled_at=next_scheduled_at,)
        activity_objects = ActivityMonitor.objects.filter(user=request.user)
        activity_serializer = ActivityMonitorSerializer(activity_objects, many=True)
        ActivityMonitor.objects.filter(pk=list(activity_serializer.data[-1].values())[0]).update(time_spent=curr_time_taken,cards_seen=list(activity_serializer.data[-1].values())[4]+1,)


        Flashcard.objects.filter(pk=request.data['flashcard_id']).update(next_scheduled_at=next_scheduled_at,)

        return Response(status=status.HTTP_201_CREATED)

        
class DeckManager(APIView):
    """
        Description:
            Contains post function for sadding a new deck
    """
    def post(self, request, format=None):
        """
        Description:
            Saved a new deck into the model

        Arguments:
            request -contains deck name 

        Returns:
            Status of new deck creation
        """
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

class NewFlashCardList(APIView):
    """
        Description:
            Contains post function for storing  of flashcards
    """

    def post(self, request, format=None):
        """
        Description:
            Saves new flashcard for given deck

        Arguments:
            request - contains new flash card details i.e title , question, answer

        Returns:
            Status of new flashcard creation
        """
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

class DeleteFlashCard(APIView):
    """
        Description:
            Contains post function to delete flashcards
    """
    def post(self, request, format=None):
        """
        Description:
            Deletes flashcard given flashcard_id
        Arguments:
            request - flash card id 

        Returns:
            Status if flashcard successfully deleted
        """
        Flashcard.objects.filter(pk=request.data['card_id']).delete()
        return Response(status=status.HTTP_201_CREATED)

class EditFlashCard(APIView):
    """
        Description:
            Contains post function to edit flashcards
    """
    def post(self, request, format=None):
        """
        Description:
            Updates flashcard using new information

        Arguments:
            request - contains flashcard id and user id

        Returns:
            Status of edit, if its successful
        """
        Flashcard.objects.filter(pk=request.data['card_id']).update(title=request.data['title'],question=request.data['question'],answer=request.data['answer'],)
        
        return Response(status=status.HTTP_201_CREATED)


class LoggedinUserDetail(APIView):
    """
        Description:
            Contains get function to get details of logged in user
    """
    def get(self, request, format=None):
        """
        Description:
            Gets details of logged in user details

        Arguments:
            request - user id 

        Returns:
            User details of currently loggen in user
        """
        resp = get_logged_in_user()
        serializer = UserSerializer(resp)
        return Response(serializer.data)


class UserDetail(APIView):
    """
        Description:
            Manages user details
    """
    def get_object(self, key, value, current_user):
        """
        Description:
            Get every user object for correct key value pair

        Arguments:
            request - contains  user id

        Returns:
            Returns user object
        """
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
        """
        Description:
            Gets user object based on search key and search value

        Arguments:
            request - contains user token key and value

        Returns:
            Returns data of user as response
        """
        search_key = request.query_params.get('key')
        search_value = request.query_params.get('value')
        obj = self.get_object(search_key, search_value, request.user)
        serializer = UserSerializer(obj)
        return Response(serializer.data)


class FriendDetail(APIView):
    """
        Description:
            Contains post function for fetching friends details
    """
    def post(self, request, format=None):
        """
        Description:
            Get details of friends for a user

        Arguments:
            request - friend id  

        Returns:
            Details of friend
        """
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
        Description:
            Getting Friend List
    """
    def get(self, request, format=None):
        """
        Description:
            Gets list of all the friends of the user

        Arguments:
            request - contains user details

        Returns:
            Data of user's friend
        """
        current_user = request.user
        objects  = current_user.relations.all()
        serializer = UserSerializer(objects, many=True)
        return Response(serializer.data)

class LeaderboardList(APIView):
    """
        Description:
            Functions to handle leaderboard generation
    """
    def get_start_date(self, period):
        """
        Description:
            Gets date for before a requested time for  leaderboard

        Arguments:
            request - contains time period

        Returns:
            Date before a requested time
        """
        now = datetime.datetime.now()
        if period == 'Last 1 Month':
            return now + dateutil.relativedelta.relativedelta(months=-1)
        elif period == 'Last 7 Days':
            return now + dateutil.relativedelta.relativedelta(days=-7)
        elif period == 'Last 1 day':
            return now + dateutil.relativedelta.relativedelta(days=-1)
        return now

    def get_user_ids(self, current_user):
        """
        Description:
            Fetch the list of users to display it on leaderboard

        Arguments:
            request - id and other details of current user 

        Returns:
            all ids of friends of userid passed to it
        """
        all_ids = []
        all_ids.append(current_user.id)
        friend_ids = list(current_user.relations.all().values_list('id', flat=True))
        all_ids += friend_ids
        return all_ids

    def get_order_criteria(self, criteria):
        """
        Description:
            Gets the order criteria for a user

        Arguments:
            request - contains display critera

        Returns:
            The display criteria requested
        """
        if(criteria == 'Cards Revised'):
            return "-total_cards"
        else:
            return "-total_time"

    def get(self, request, format=None):
        """
        Description:
            Gets the details of time taken by friends and the number of cards revised y them sand sorted in terms of the requested order

        Arguments:
            request - contains crtieria and period of displaying leaderboard 

        Returns:
            The leaderboard details in sorted manner
        """
        criteria = request.query_params.get('criteria')
        period = request.query_params.get('period')
        all_ids = self.get_user_ids(request.user)
        start_date = self.get_start_date(period)
        order = self.get_order_criteria(criteria)
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
        Description:
            Contains get and post functions for sharing flashcards
    """
    def post(self, request, format=None):
        """
        Description:
            Saves a copy of flashcards in a deck for a friend

        Arguments:
            request - contains  deck id and friend id

        Returns:
            Returns response if succesfully created or not
        """
        deck_id = request.data['deck_id']
        friend_user_id = request.data['friend_id']
        friend = ScUser.objects.get(username = friend_user_id)
        deck_cpy = FlashDeck.objects.get(pk = deck_id)
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

