"""
Object-Relational Mapping (ORM) models for XBox voting app

Author: Nick Stevens <nickastevens@yahoo.com>
"""
from django.db import models
from django.utils import timezone


class Game(models.Model):
    ''' ORM model for XBox games either being voted on or owned '''
    MAX_TITLE_LEN = 255
    title = models.CharField(max_length=MAX_TITLE_LEN)
    owned = models.BooleanField()
    created = models.DateTimeField('created date')

    def add_vote(self, datetime=timezone.now()):
        ''' Adds a vote for this game '''
        v = Vote(game_id=self.id, created=datetime)
        v.save()

    def set_owned(self):
        ''' Sets this game as "owned" and saves the result '''
        self.owned = True
        self.save()

    @property
    def votes(self):
        return self.vote_set.count()

    def __unicode__(self):
        return self.title


class Vote(models.Model):
    ''' ORM model for votes cast for a particular XBox game '''
    game = models.ForeignKey(Game)
    created = models.DateTimeField('created date')

    def __unicode__(self):
        return self.created
