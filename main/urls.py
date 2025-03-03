from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetCompleteView, PasswordResetDoneView, PasswordResetConfirmView
from django.urls import path, include, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView

from . import views
from .forms import CustomAuthenticationForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm
from .forms.site import *

app_name = 'main'

urlpatterns = [
    path('', views.LeadUnassembledView(), name='lead-unassembled'),
    path('notify/<int:notify_id>/delete/', views.NotifyDeleteView.as_view(), name='notify-delete'),
    path('statistic/', include([
        path('<int:funnel_id>/responsible/', views.ResponsibleStatsView(), name='responsible-stats'),
        path('deals/', views.DealStatsView(), name='deals-stats'),
        path('empty/sources/', views.SourceStatsEmptyView(), name='sources-stats-empty'),
        path('<int:funnel_id>/sources/', include([
            path('', views.SourceStatsView(), name='sources-stats'),
            path('<int:stage_id>/ajax/', views.AjaxSourceStageView(), name='sources-stats-ajax'),
        ])),
        path('debtor/<str:frm>/', views.DebtorStatsView(), name='debtor-stats')
    ])),
    path('exclusive/', include([
        path('list/', views.ExclusiveListView(), name='exclusive-list'),
        path('create/', include([
            path('commerce-lease/', views.ExclusiveFormView(
                extra_context={'title': 'Создание эксклюзива'}, form_class=CommerceLease), name='exclusive-create-cl'),
            path('commerce-sale/', views.ExclusiveFormView(
                extra_context={'title': 'Создание эксклюзива'}, form_class=CommerceSale), name='exclusive-create-cs'),
            path('flat-sale-new/', views.ExclusiveFormView(
                extra_context={'title': 'Создание эксклюзива'}, form_class=FlatSaleNew), name='exclusive-create-fsn'),
            path('flat-sale-old/', views.ExclusiveFormView(
                extra_context={'title': 'Создание эксклюзива'}, form_class=FlatSaleOld), name='exclusive-create-fso'),
            path('flat-lease/', views.ExclusiveFormView(
                extra_context={'title': 'Создание эксклюзива'}, form_class=FlatLease), name='exclusive-create-fl'),
            path('garage-lease/', views.ExclusiveFormView(
                extra_context={'title': 'Создание эксклюзива'}, form_class=GarageLease), name='exclusive-create-gl'),
            path('garage-sale/', views.ExclusiveFormView(
                extra_context={'title': 'Создание эксклюзива'}, form_class=GarageSale), name='exclusive-create-gs'),
            path('house-lease/', views.ExclusiveFormView(
                extra_context={'title': 'Создание эксклюзива'}, form_class=HouseLease), name='exclusive-create-hl'),
            path('house-lease-day/', views.ExclusiveFormView(
                extra_context={'title': 'Создание эксклюзива'}, form_class=HouseLeaseDay), name='exclusive-create-hld'),
            path('house-sale/', views.ExclusiveFormView(
                extra_context={'title': 'Создание эксклюзива'}, form_class=HouseSale), name='exclusive-create-hs'),
            path('land-lease/', views.ExclusiveFormView(
                extra_context={'title': 'Создание эксклюзива'}, form_class=LandLease), name='exclusive-create-ll'),
            path('land-sale/', views.ExclusiveFormView(
                extra_context={'title': 'Создание эксклюзива'}, form_class=LandSale), name='exclusive-create-ls'),
            path('room-lease/', views.ExclusiveFormView(
                extra_context={'title': 'Создание эксклюзива'}, form_class=RoomLease), name='exclusive-create-rl'),
            path('room-sale/', views.ExclusiveFormView(
                extra_context={'title': 'Создание эксклюзива'}, form_class=RoomSale), name='exclusive-create-rs'),
        ])),
        path('<int:exclusive_id>/', include([
            path('', views.ExclusivePageView(), name='exclusive-page'),
            path('update/', views.ExclusiveFormView(extra_context={'title': 'Обновление эксклюзива'}),
                 name='exclusive-update'),
            path('publish/', views.ExclusivePublish(), name='exclusive-publish'),
            path('delete/', views.ExclusiveDeleteView(), name='exclusive-delete'),
            path('delete/modal/', views.ModalExclusiveDelete(), name='modal-exclusive-delete')
        ]))
    ])),
    path('reports/', include([
        path('lead/', views.LeadReportView(), name='lead-report')
    ])),
    path('api/', include([
        path('calls/', csrf_exempt(views.CallView.as_view()), name='api-calls'),
        path('tilda/', csrf_exempt(views.TildaView.as_view()), name='api-tilda'),
        path('wantresult/<int:num>/', csrf_exempt(views.WantresultView.as_view()), name='api-wantresult'),
        path('dmp/', csrf_exempt(views.DmpView.as_view()), name='api-dmp'),
        path('whatsapp/webhook', csrf_exempt(views.WhatsappApiView.as_view()), name='api-whatsapp'),
        path('landing/', csrf_exempt(views.LandingView.as_view()), name='api-landing'),
        path('site/', csrf_exempt(views.SiteView.as_view()), name='api-site'),
        path('forums/', csrf_exempt(views.ForumsView.as_view()), name='api-forums')
    ])),
    path('calls/', include([
        path('missed/', views.CallMissedListView(), name='call-missed'),
        path('all/', views.CallListView(), name='call-all'),
        path('make/<int:phone>/', views.MakeCallView.as_view(), name='call-make'),
        path('<int:call_id>/processed/', views.CallProcessedView(), name='call-processed')
    ])),
    path('partner/', include([
        path('ajax/search/', views.AjaxPartnerListView(), name='ajax-search-partner'),
        path('list/', views.PartnerListView(), name='partner-list'),
        path('create/', views.PartnerCreateView(), name='partner-create'),
        path('create/modal/', views.ModalPartnerCreate(), name='modal-partner-create'),
        path('<int:partner_id>/', include([
            path('update/', views.PartnerUpdateView(), name='partner-update'),
            path('delete/', views.PartnerDeleteView(), name='partner-delete'),
            path('modals/', include([
                path('update/', views.ModalPartnerUpdate(), name='modal-partner-update'),
                path('delete/', views.ModalPartnerDelete(), name='modal-partner-delete')
            ]))
        ]))
    ])),
    path('deal/', include([
        path('create/', views.DealCreateView(), name='deal-create'),
        path('list/', views.DealListView(), name='deal-list'),
        path('<int:deal_id>/', include([
            path('', views.DealPageView(), name='deal-page'),
            path('update/', views.DealUpdateView(), name='deal-update'),
            path('delete/', views.DealDeleteView(), name='deal-delete'),
            path('task/create/', views.DealTaskCreateView(), name='deal-task-create'),
            path('showing/create/', views.DealShowingCreateView(), name='deal-showing-create'),
            path('modals/', include([
                path('delete/', views.ModalDealDelete(), name='modal-deal-delete'),
                path('task/create/', views.ModalTaskDealCreate(), name='modal-deal-task-create'),
                path('showing/create/', views.ModalShowingDealCreate(), name='modal-deal-showing-create'),
            ])),
            path('money/', include([
                path('create/', views.DealMoneyCreateView(), name='deal-money-create'),
                path('<int:money_id>/update/', views.DealMoneyUpdateView(), name='deal-money-update'),
            ])),
            path('mortgage/', include([
                path('create/', views.DealMortgageCreateView(), name='deal-mortgage-create'),
                path('<int:mortgage_id>/update/', views.DealMortgageUpdateView(), name='deal-mortgage-update'),
            ])),
        ]))
    ])),
    path('funnel/', include([
        path('create/', views.FunnelCreateView(), name='funnel-create'),
        path('modals/create/', views.ModalFunnelCreate(), name='modal-funnel-create'),
        path('<int:funnel_id>/', include([
            path('<int:user_id>/', views.FunnelPageView(), name='funnel-page'),
            path('update/', views.FunnelUpdateView(), name='funnel-update'),
            path('delete/', views.FunnelDeleteView(), name='funnel-delete'),
            path('modals/', include([
                path('update/', views.ModalFunnelUpdate(), name='modal-funnel-update'),
                path('delete/', views.ModalFunnelDelete(), name='modal-funnel-delete'),
            ])),
            path('no-stage/ajax/', views.LeadNoStageListAjax(), name='ajax-no-stage-list'),
            path('stage/', include([
                path('create/', views.StageCreateView(), name='stage-create'),
                path('modals/create/', views.ModalStageCreate(), name='modal-stage-create'),
                path('<int:stage_id>/', include([
                    path('leads/change_stage/', views.ChangeStageAjax(), name='ajax-change-stage'),
                    path('<int:user_id>/leads/ajax/', views.LeadStageListAjax(), name='ajax-stage-list'),
                    path('update/', views.StageUpdateView(), name='stage-update'),
                    path('delete/', views.StageDeleteView(), name='stage-delete'),
                    path('modals/', include([
                        path('update/', views.ModalStageUpdate(), name='modal-stage-update'),
                        path('delete/', views.ModalStageDelete(), name='modal-stage-delete'),
                    ]))
                ]))
            ]))
        ]))
    ])),
    path('comment/', include([
        path('<int:comment_id>/', include([
            path('update/', views.CommentUpdateView(), name='comment-update'),
            path('delete/', views.CommentDeleteView(), name='comment-delete')
        ])),
        path('<str:type>/<int:item_id>/create', views.CommentCreateView(), name='comment-create')
    ])),
    path('showing/', include([
        path('create/', views.ShowingCreateView(), name='showing-create'),
        path('<str:date_str>/', include([
            path('closed/', views.ClosedShowingListView(), name='showing-list-closed'),
            path('other/', views.OtherShowingListView(), name='showing-list-other'),
            path('outdated/', views.OutdatedShowingListView(), name='showing-list-outdated'),
            path('today/', views.TodayShowingListView(), name='showing-list-today'),
            path('tomorrow/', views.TomorrowShowingListView(), name='showing-list-tomorrow'),
        ])),
        path('<int:showing_id>/', include([
            path('', views.ShowingPageView(), name='showing-page'),
            path('update/', views.ShowingUpdateView(), name='showing-update'),
            path('close/', views.ShowingCloseView(), name='showing-close'),
            path('modal/close/', views.ModalShowingClose(), name='modal-showing-close')
        ])),
    ])),
    path('task/', include([
        path('create/', views.TaskCreateView(), name='task-create'),
        path('<str:date_str>/', include([
            path('outdated/', views.OutdatedTaskListView(), name='task-list-outdated'),
            path('today/', views.TodayTaskListView(), name='task-list-today'),
            path('tomorrow/', views.TomorrowTaskListView(), name='task-list-tomorrow'),
            path('other/', views.OtherTaskListView(), name='task-list-other'),
            path('closed/', views.ClosedTaskListView(), name='task-list-closed'),
        ])),
        path('<int:task_id>/', include([
            path('', views.TaskPageView(), name='task-page'),
            path('update/', views.TaskUpdateView(), name='task-update'),
            path('close/', views.TaskCloseView(), name='task-close'),
            path('modal/close/', views.ModalTaskClose(), name='modal-task-close')
        ])),
    ])),
    path('lead/', include([
        path('', views.LeadListView(), name='lead-list'),
        path('ajax/search/', views.AjaxLeadListView(), name='ajax-search-lead'),
        path('deleted/', views.LeadListDeletedView(), name='lead-list-deleted'),
        path('create/', views.LeadCreateView(), name='lead-create'),
        path('unassembled/', RedirectView.as_view(pattern_name='main:lead-unassembled', permanent=True)),
        path('money/', views.LeadMoneyView(), name='lead-money'),
        path('upload/', views.LeadUploadView(), name='lead-upload'),
        path('change-responsible-massive/', views.ChangeLeadResponsibleView(), name='lead-responsible-change-massive'),
        path('<int:lead_id>/', include([
            path('', views.LeadPageView(), name='lead-page'),
            path('update/', views.LeadUpdateView(), name='lead-update'),
            path('delete/', views.LeadDeleteView(), name='lead-delete'),
            path('questions/', include([
                path('create/', views.LeadQuestionsCreateView(), name='lead-questions-create'),
                path('<int:questions_id>/update/', views.LeadQuestionsUpdateView(), name='lead-questions-update'),
            ])),
            path('passport/', include([
                path('create/', views.LeadPassportCreateView(), name='lead-passport-create'),
                path('<int:passport_id>/update/', views.LeadPassportUpdateView(), name='lead-passport-update'),
            ])),
            path('task/create/', views.LeadTaskCreateView(), name='lead-task-create'),
            path('showing/create/', views.LeadShowingCreateView(), name='lead-showing-create'),
            path('modals/', include([
                path('delete/', views.ModalLeadDelete(), name='modal-lead-delete'),
                path('task/create/', views.ModalTaskLeadCreate(), name='modal-lead-task-create'),
                path('showing/create/', views.ModalShowingLeadCreate(), name='modal-lead-showing-create'),
                path('source/create/', views.ModalSourceLeadCreate(), name='modal-lead-source-create'),
                path('deal/create/', views.ModalDealLeadCreate(), name='modal-lead-deal-create'),
            ])),
            path('source/', include([
                path('create/', views.LeadSourceCreateView(), name='lead-source-create'),
                path('<int:ls_id>/delete/', views.LeadSourceDeleteView(), name='lead-source-delete'),
            ])),
            path('tabs/', include([
                path('activity/', views.ActivityTabLeadView(), name='lead-tab-activity'),
                path('source/', views.SourceTabLeadView(), name='lead-tab-source'),
                path('questions/', views.QuestionsTabLeadView(), name='lead-tab-questions'),
                path('passport/', views.PassportTabLeadView(), name='lead-tab-passport'),
                path('tasks/', views.TasksTabLeadView(), name='lead-tab-tasks'),
                path('shows/', views.ShowsTabLeadView(), name='lead-tab-shows'),
                path('whatsapp/', views.WhatsappTabLeadView(), name='lead-tab-whatsapp'),
                path('calls/', views.CallsTabLeadView(), name='lead-tab-calls')
            ]))
        ]))
    ])),
    path('source/', include([
        path('', views.SourceListView(), name='source-list'),
        path('create/', views.SourceCreateView(), name='source-create'),
        path('modals/create/', views.ModalSourceCreate(), name='modal-source-create'),
        path('<int:source_id>/', include([
            path('update/', views.SourceUpdateView(), name='source-update'),
            path('delete/', views.SourceDeleteView(), name='source-delete'),
            path('modals/', include([
                path('update/', views.ModalSourceUpdate(), name='modal-source-update'),
                path('delete/', views.ModalSourceDelete(), name='modal-source-delete'),
            ]))
        ]))
    ])),
    path('user/', include([
        path('', views.UserListView(), name='user-list'),
        path('create/', views.UserCreateView(), name='user-create'),
        path('modals/create/', views.ModalUserCreate(), name='modal-user-create'),
        path('<int:user_id>/', include([
            path('update/', views.UserUpdateView(), name='user-update'),
            path('modals/update/', views.ModalUserUpdate(), name='modal-user-update'),
        ])),
    ])),
    path('whatsapp/', include([
        path('', views.WhatsappView(), name='whatsapp-list'),
        path('<int:lead_id>/send/', views.WhatsappSendMessage(), name='whatsapp-send'),
        path('<int:lead_id>/send/template/<int:template_id>/', views.WhatsappSendTemplate(),
             name='whatsapp-send-template'),
        path('<int:lead_id>/get/ajax/', views.WhatsappLeadView(), name='whatsapp-get-ajax'),
    ])),
    path('management/', include([
        path('tasks/', views.ManagementTaskView(), name='management-tasks'),
        path('change-task-user/', views.ManagementChangeUserTask(), name='management-change-task-user'),
        path('showings/', views.ManagementShowingView(), name='management-showings'),
        path('notifications/', views.ManagementNotificationView(), name='management-notifications'),
        path('change-showing-user/', views.ManagementChangeUserShowing(), name='management-change-showing-user'),
        path('messages/', include([
            path('', views.MessageTemplateList(), name='management-message-list'),
            path('create/', views.MessageTemplateCreate(), name='management-message-create'),
            path('<int:message_id>/', include([
                path('update/', views.MessageTemplateUpdate(), name='management-message-update'),
                path('delete/', views.MessageTemplateDelete(), name='management-message-delete')
            ]))
        ]))
    ])),
    path('mortgage/', include([
        path('list/', views.MortgageListView(), name='mortgage-list'),
        path('<str:status>/', views.MortgageStatusListAjax(), name='mortgage-status-ajax')
    ])),
    path('legal/', include([
        path('list/', views.LegalListView(), name='legal-list'),
        path('<str:status>/', views.LegalStatusListAjax(), name='legal-status-ajax')
    ])),
    # Фиды
    path('feeds/', include([
        path('avito/', views.AvitoFeed.as_view(), name='feed-avito'),
        path('domclick/', views.DomClickFeed.as_view(), name='feed-domclick')
    ])),
    # Ссылки авторизации
    path('fired/', views.FiredView.as_view(), name='fired'),
    path('account/', include([
        path('login/', LoginView.as_view(template_name='custom_registration/login.html',
                                         form_class=CustomAuthenticationForm,
                                         redirect_authenticated_user=True), name='login'),
        path('logout/', LogoutView.as_view(template_name='custom_registration/logged_out.html'),
             {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
        path('password/', include([
            path('change/', PasswordChangeView.as_view(success_url=reverse_lazy('main:password_change_done'),
                                                       form_class=CustomPasswordChangeForm,
                                                       template_name='custom_registration/password_change_form.html'),
                 name='password_change'),
            path('change/done/', PasswordChangeDoneView.as_view(
                template_name='custom_registration/password_change_done.html'), name='password_change_done'),
            path('reset/', PasswordResetView.as_view(
                form_class=CustomPasswordResetForm,
                email_template_name='custom_registration/password_reset_email.txt',
                html_email_template_name='custom_registration/password_reset_email.html',
                subject_template_name='custom_registration/password_reset_subject.txt',
                success_url=reverse_lazy('main:password_reset_done'),
                template_name='custom_registration/password_reset_form.html'), name='password_reset'),
            path('reset/done/', PasswordResetDoneView.as_view(
                template_name='custom_registration/password_reset_done.html'), name='password_reset_done'),
            path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
                form_class=CustomSetPasswordForm,
                template_name='custom_registration/password_reset_confirm.html',
                success_url=reverse_lazy("main:password_reset_complete")), name="password_reset_confirm"),
            path('reset/complete/', PasswordResetCompleteView.as_view(
                template_name='custom_registration/password_reset_complete.html'), name='password_reset_complete'),
        ])),
    ])),
    path('chess/', include([
        path('', views.ResidentialComplexListView.as_view(), name='residential_complex_list'),
        path('complex/<int:complex_id>/', views.ResidentialComplexDetailView.as_view(), name='residential_complex_detail'),
        path('building/', include([
            path('create/', views.BuildingCreateView.as_view(), name='building_create'),
            #path('<int:building_id>/', views.BuildingDetailView.as_view(), name='building_detail'),
            path('<int:building_id>/', include([
                path('', views.BuildingDetailView.as_view(), name='building_detail'),
                path('apartment/', include([
                    path('create/', views.ApartmentCreateView.as_view(), name='apartment_create'),
                    path('<int:apartment_id>/update/', views.ApartmentUpdateView.as_view(), name='apartment_update'),
                ]))
            ])),
            path('<int:building_id>/update/', views.BuildingUpdateView.as_view(), name='building_update'),
        ])),
        
    
    ])),
]
