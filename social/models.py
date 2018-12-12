from django.db import models

# Create your models here.
from lib.http import render_json


class Swipre(models.Model):
    '''滑动记录'''
    FLAGS = (
        ('superlike','上滑'),
        ('like','右滑'),
        ('dislike','左滑'),
    )
    uid = models.IntegerField(verbose_name='滑动者的UID')
    sid = models.IntegerField(verbose_name='被滑动者的UID')
    flag = models.CharField(max_length=10,choices=FLAGS)
    dtime = models.DateTimeField(auto_now=True)

    @classmethod
    def like(cls, uid, sid):
        obj = cls.objects.create(uid=uid, sid=sid, flage='like')
        return obj

    @classmethod
    def superlike(cls, uid, sid):
        obj = cls.objects.create(uid=uid, sid=sid, flage='superlike')
        return obj

    @classmethod
    def dislike(cls, uid, sid):
        obj = cls.objects.create(uid=uid, sid=sid, flage='dislike')
        return obj

    @classmethod
    def is_liked(cls, uid, sid):
        return cls.objects.filter(uid=uid, sid=sid, flag__in=['superlike', 'like']).exists()


class Friend(models.Model):
    '''好友关系'''
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    @classmethod
    def make_friends(cls, uid1, uid2):
        uid1, uid2 = sorted([uid1, uid2])
        cls.objects.get_or_create(uid1=uid1, uid2=uid2)
