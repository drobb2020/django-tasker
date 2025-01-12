# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Task, Review, Profile


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'is_completed',
        'date_created',
        'date_due',
    )
    list_filter = ('author', 'is_completed', 'date_created', 'date_updated', 'date_due')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'reviewer_name',
        'review_title',
        'task',
        'review_notes',
    )
    list_filter = ('task',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'email',
        'phone',
    )
    list_filter = ('user',)
