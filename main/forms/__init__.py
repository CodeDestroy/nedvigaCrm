from .authentication import CustomAuthenticationForm
from .password_change import CustomPasswordChangeForm
from .password_reset import CustomPasswordResetForm
from .set_password_form import CustomSetPasswordForm

from .base_form import BaseModelForm, BaseForm
from .comment import CommentForm
from .funnel import FunnelForm
from .lead_source import LeadSourceForm
from .message_template import MessageTemplateForm
from .money import MoneyForm
from .mortgage import MortgageForm
from .partner import PartnerForm
from .passport import PassportForm
from .showing import ShowingForm
from .source import SourceForm
from .stage import StageForm
from .task import TaskForm
from .questions import QuestionsForm
from .user import UserForm, UserUpdateForm
from .chess import *
from .apartment_photo import ApartmentPhotoForm

__all__ = [
    'ApartmentForm',
    'ApartmentPhotoForm',
    'CustomAuthenticationForm',
    'CustomPasswordChangeForm',
    'CustomPasswordResetForm',
    'CustomSetPasswordForm',

    'BaseModelForm',
    'BaseForm',
    'CommentForm',
    'FunnelForm',
    'LeadSourceForm',
    'MessageTemplateForm',
    'MoneyForm',
    'MortgageForm',
    'PartnerForm',
    'PassportForm',
    'ShowingForm',
    'SourceForm',
    'StageForm',
    'TaskForm',
    'QuestionsForm',
    'UserForm',
    'UserUpdateForm'
]
