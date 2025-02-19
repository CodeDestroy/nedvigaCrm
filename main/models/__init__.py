from django.db.models.signals import pre_save

from .created_updated_mixin import CreatedUpdatedMixin

from .auth_log import AuthLog
from .avito_call import AvitoCall
from .bank import Bank
from .call import Call
from .comment import Comment
from .deal import Deal
from .dmp import Dmp
from .funnel import Funnel
from .lead import Lead
from .lead_source import LeadSource
from .message_template import MessageTemplate
from .mortgage import Mortgage
from .money import Money
from .notification import Notification
from .partner import Partner
from .passport import Passport
from .phone import Phone
from .showing import Showing
from .source import Source
from .stage import Stage
from .task import Task
from .user import User
from .log_entry import UserLogEntry
from .questions import Questions
from .wantresult import Wantresult
from .whatsapp_message import WhatsappMessage
from .chessboard import *

__all__ = [
    'CreatedUpdatedMixin',

    'AuthLog',
    'AvitoCall',
    'Bank',
    'Call',
    'Comment',
    'Deal',
    'Dmp',
    'Funnel',
    'Lead',
    'LeadSource',
    'MessageTemplate',
    'Mortgage',
    'Money',
    'Notification',
    'Partner',
    'Passport',
    'Phone',
    'Showing',
    'Source',
    'Stage',
    'Task',
    'User',
    'UserLogEntry',
    'Questions',
    'Wantresult',
    'WhatsappMessage',
]

from .. import signals

pre_save.connect(signals.log_update, sender=Bank)
pre_save.connect(signals.log_update, sender=Comment)
pre_save.connect(signals.log_update, sender=Deal)
pre_save.connect(signals.log_update, sender=Funnel)
pre_save.connect(signals.log_update, sender=Lead)
pre_save.connect(signals.log_update, sender=Money)
pre_save.connect(signals.log_update, sender=Mortgage)
pre_save.connect(signals.log_update, sender=Passport)
pre_save.connect(signals.log_update, sender=Questions)
pre_save.connect(signals.log_update, sender=Stage)
pre_save.connect(signals.log_update, sender=Showing)
pre_save.connect(signals.log_update, sender=Task)

