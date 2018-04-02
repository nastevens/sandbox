"""
Views to handle incoming connections to xboxvoting app

Author: Nick Stevens <nickastevens@yahoo.com>
"""
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.conf import settings


from xboxvoting.models import Game

TEMPLATE_DIR = 'xboxvoting/templates/'
SATURDAY = 5
SUNDAY = 6


class LastAction():
    '''
    Object for storing datetime and action type between calls to the app.
    '''
    def __init__(self, datetime, action_type):
        self.datetime = datetime
        self.type = action_type


def index(request):
    '''
    Render the main page of the voting app using index.html template
    '''
    voting_list = Game.objects.filter(owned__exact=False)
    owned_list = Game.objects.filter(owned__exact=True)
    error_message = _decode_error(request.GET.get('e', None))
    success_message = _decode_success(request.GET.get('s', None))
    return render_to_response(TEMPLATE_DIR + 'index.html', {
        'voting_list': voting_list,
        'owned_list': owned_list,
        'error_message': error_message,
        'success_message': success_message,
        'DEBUG': settings.DEBUG},
        context_instance=RequestContext(request))


def vote(request, game_id):
    '''
    Record a vote for a game unless the client has already voted, already
    added a game, or it is a weekend
    '''
    g = get_object_or_404(Game, pk=game_id)

    today = timezone.now().date()
    (action_date, action_type) = _get_last_action(request.session)

    # Redirect with error message if user already voted/added
    if(action_date == today):
        if(action_type == 'vote'):
            return _index_with_error('voted_twice')
        if(action_type == 'add'):
            return _index_with_error('add_then_vote')

    # Redirect with error on weekends
    if(today.weekday() == SATURDAY or today.weekday() == SUNDAY):
        return _index_with_error('weekend')

    # Add the vote and set session cookie for user
    g.add_vote(timezone.now())
    request.session['last_action'] = LastAction(timezone.now(), 'vote')
    return _index_with_success('voted')


def add(request):
    '''
    Add a new game to the list
    '''
    today = timezone.now().date()
    (action_date, action_type) = _get_last_action(request.session)

    # Redirect with error if user already voted/added
    if(action_date == today):
        if(action_type == 'add'):
            return _index_with_error('added_twice')
        if(action_type == 'vote'):
            return _index_with_error('vote_then_add')

    # Redirect with error on weekends
    if(today.weekday() == SATURDAY or today.weekday() == SUNDAY):
        return _index_with_error('weekend')

    # Retrieve title suggestion and make sure it is not empty, too long,
    # or a duplicate
    new_title = request.POST.get('new_title', None)
    if(new_title is None or len(new_title) == 0):
        return _index_with_error('empty_title')
    if(len(new_title) > Game.MAX_TITLE_LEN):
        return _index_with_error('title_too_long')
    if(Game.objects.filter(title__iexact=new_title).exists()):
        return _index_with_error('dup_game')

    # All error checking has passed, so create game and set session cookie
    g = Game(title=new_title, owned=False, created=timezone.now())
    g.save()
    g.add_vote(timezone.now())
    request.session['last_action'] = LastAction(timezone.now(), 'add')
    return _index_with_success('added')


def own(request, game_id):
    '''
    Mark an existing game as "owned"
    '''
    g = get_object_or_404(Game, pk=game_id)
    if(g.owned):
        # if already owned just go back to index
        return HttpResponseRedirect(reverse('xboxvoting.views.index'))
    else:
        g.set_owned()
        return _index_with_success('owned')


def manage(request):
    '''
    Manage the list of owned games
    '''
    voting_list = Game.objects.filter(owned__exact=False)
    return render_to_response(TEMPLATE_DIR + 'manage.html',
        {'voting_list': voting_list},
        context_instance=RequestContext(request))


def clear_cookie(request):
    '''
    Debug action to clear the client cookie so another vote can be logged.
    Action is not valid if DEBUG is not enabled.
    '''
    if settings.DEBUG:
        request.session['last_action'] = None
    return HttpResponseRedirect(reverse('xboxvoting.views.index'))


def _get_last_action(session):
    # Get session cookie with last datetime this user performed an action
    last_action = session.get('last_action', None)
    try:
        # Not sure if session vars are valid/present, so wrap in 'try'
        action_date = last_action.datetime.date()
        action_type = last_action.type
    except AttributeError:
        action_date = None
        action_type = None

    return (action_date, action_type)


def _decode_error(error_token):
    '''
    Decode an error token into a user-friendly error message or return None
    if token is not understood.
    '''
    return {'voted_twice': "You've already voted once today!",
            'add_then_vote': "You cannot vote after adding a new game!",
            'vote_then_add': "You cannot add a game after voting!",
            'added_twice': "You've already added a game today!",
            'weekend': "No voting or adding games allowed on the weekends!",
            'dup_game': "That game already exists!",
            'empty_title': "You've entered an empty title!",
            'title_too_long': "Title must be less than 255 characters."
           }.get(error_token, None)


def _decode_success(success_token):
    return {'voted': "Your vote was successfully counted!",
            'added': "Your game was successfully added!",
            'owned': "Congratulations on your new game purchase!"
           }.get(success_token, None)


def _index_with_error(error_token):
    return HttpResponseRedirect(reverse('xboxvoting.views.index') +
                             '?e=' + error_token)


def _index_with_success(success_token):
    return HttpResponseRedirect(reverse('xboxvoting.views.index') +
                             '?s=' + success_token)
