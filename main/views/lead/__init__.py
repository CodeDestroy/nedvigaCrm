from .ajax import AjaxLeadListView
from .main import LeadListView, LeadListDeletedView, LeadMoneyView, LeadCreateView, LeadUpdateView, LeadPageView, \
    LeadQuestionsCreateView, LeadQuestionsUpdateView, LeadPassportCreateView, LeadPassportUpdateView, \
    LeadTaskCreateView, LeadSourceCreateView, LeadSourceDeleteView, LeadDeleteView, LeadUnassembledView, \
    LeadShowingCreateView, LeadUploadView, ChangeLeadResponsibleView
from .modals import ModalTaskLeadCreate, ModalSourceLeadCreate, ModalLeadDelete, ModalShowingLeadCreate, \
    ModalDealLeadCreate
from .tabs import ActivityTabLeadView, SourceTabLeadView, QuestionsTabLeadView, PassportTabLeadView, TasksTabLeadView, \
    ShowsTabLeadView, WhatsappTabLeadView, CallsTabLeadView
