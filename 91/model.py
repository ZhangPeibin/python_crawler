#!/usr/bin/env python
# coding=utf-8


class VideoModel(object):

    def __init__(self, url, name, time, addtime, author, authorurl, views, likes, comments):
        self.videourl = url
        self.videoname = name
        self.videotime = time
        self.addtime = addtime
        self.author = author
        self.authorurl = authorurl
        self.views = views
        self.likes = likes
        self.comments = comments

    def __str__(self):
        return "%s" % self.videourl




