from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import *
from .models.site import *


class TaskCommentAdmin(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'name', 'date_to')
    list_filter = ('date_to', 'user', 'is_done')


@admin.register(Showing)
class ShowingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'description', 'date_to')
    list_filter = ('deal', 'user', 'is_done')


@admin.register(LeadSource)
class LeadSourceAdmin(admin.ModelAdmin):
    list_display = ('lead', 'source', 'utm', 'created_at', 'updated_at')
    list_filter = ('lead__warm', 'source', 'created_at',)
    search_fields = ('created_at',)


admin.site.register(Bank)
admin.site.register(Stage)
admin.site.register(Phone)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority', 'user', 'type', 'item_id', 'read')
    list_filter = ('user', 'type', 'created_by', 'created_at')


@admin.register(Wantresult)
class WantresultAdmin(admin.ModelAdmin):
    list_display = ('vid', 'num', 'site', 'page', 'ref', 'time', 'browser', 'device', 'platform', 'country', 'region',
                    'city', 'ip', 'comment', 'phones')
    list_filter = ('num', 'time')


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'stage', 'responsible', 'reserved', 'created_at')
    list_filter = ('stage', 'responsible', 'reserved', 'frm', 'created_at')


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_filter = ['responsible', 'created_at', 'updated_at', 'warm', 'partner']
    list_display = ('pk', 'surname', 'name', 'patronymic', 'phone', 'responsible', 'created_at')
    search_fields = ['phone', 'created_at',]


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ('pk', 'phone', 'direction', 'ext', 'status', 'event', 'record', 'user', 'processed', 'created_at')
    list_filter = ['direction', 'processed', 'user', 'status', 'event', 'created_at']
    search_fields = ['phone']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('type', 'item_id', 'user', 'text')
    list_filter = ('type',)
    search_fields = ('item_id', 'text')


@admin.register(WhatsappMessage)
class WhatsappMessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'body', 'lead')
    search_fields = ['lead__phone',]


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'birth', 'sip', 'funnel', 'fired', 'return_to_list', 'debetor', 'in_stat',
                           'broker', 'can_be_responsible', 'telegram_id', 'telegram_username')}),
    )

    list_filter = ['sip', 'fired', 'debetor', 'in_stat', 'funnel']
    search_fields = ['phone',]


admin.site.register(User, MyUserAdmin)

class ObjectFieldInline(admin.StackedInline):
    model = ObjectField
    extra = 1


class ObjectPhotoInline(admin.StackedInline):
    model = ObjectPhoto
    extra = 1


@admin.register(BuyObject)
class BuyObjectAdmin(admin.ModelAdmin):
    inlines = [ObjectFieldInline, ObjectPhotoInline]


@admin.register(ObjectField)
class BuyObjectAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = ('name', 'value')


admin.site.register(ObjectStat)
admin.site.register(ObjectPhoto)