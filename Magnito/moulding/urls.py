from django.urls import path
from . import views
from . import views_auth

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Mould Changes
    path('mould-changes/', views.mould_change_list, name='mould_change_list'),
    path('mould-changes/create/', views.mould_change_create, name='mould_change_create'),
    path('mould-changes/<int:pk>/status/<str:status>/', views.mould_change_update_status, name='mould_change_update_status'),
    
    # Troubleshooting
    path('troubleshooting/', views.troubleshooting_list, name='troubleshooting_list'),
    path('troubleshooting/<int:pk>/', views.troubleshooting_detail, name='troubleshooting_detail'),
    path('troubleshooting/log/create/', views.troubleshooting_log_create, name='troubleshooting_log_create'),
    
    # Hourly Checklist
    path('checklists/', views.checklist_list, name='checklist_list'),
    path('checklists/create/', views.checklist_create, name='checklist_create'),
    
    # Master Samples
    path('master-samples/', views.master_sample_list, name='master_sample_list'),
    path('master-samples/create/', views.master_sample_create, name='master_sample_create'),
    
    # Product Comparison
    path('comparisons/', views.comparison_list, name='comparison_list'),
    path('comparisons/create/', views.product_comparison_create, name='product_comparison_create'),
    path('comparisons/<int:pk>/', views.comparison_detail, name='comparison_detail'),
    
    # Defect Types
    path('defect-types/', views.defect_types_list, name='defect_types_list'),
    path('defect-types/<int:pk>/', views.defect_type_detail, name='defect_type_detail'),
    
    # Mould Runs
    path('mould-runs/', views.mould_run_list, name='mould_run_list'),
    path('mould-runs/create/', views.mould_run_create, name='mould_run_create'),
    path('mould-runs/<int:pk>/stop/', views.mould_run_stop, name='mould_run_stop'),
    
    # Production Orders
    path('production-orders/', views.production_order_list, name='production_order_list'),
    path('production-orders/create/', views.production_order_create, name='production_order_create'),
    path('production-orders/<int:pk>/', views.production_order_detail, name='production_order_detail'),
    path('production-orders/<int:pk>/status/<str:status>/', views.production_order_update_status, name='production_order_update_status'),
    
    # Issue Management
    path('issues/', views.issue_list, name='issue_list'),
    path('issues/create/', views.issue_create, name='issue_create'),
    path('issues/<int:pk>/', views.issue_detail, name='issue_detail'),
    path('issues/<int:pk>/status/<str:status>/', views.issue_update_status, name='issue_update_status'),
    path('issues/<int:pk>/resolve/', views.issue_resolve, name='issue_resolve'),
    
    # Maintenance Job Cards
    path('job-cards/', views.job_card_list, name='job_card_list'),
    path('job-cards/create/', views.job_card_create, name='job_card_create'),
    path('job-cards/<int:pk>/status/<str:status>/', views.job_card_update_status, name='job_card_update_status'),
    
    # Housekeeping
    path('housekeeping/', views.housekeeping_list, name='housekeeping_list'),
    path('housekeeping/create/', views.housekeeping_create, name='housekeeping_create'),
    path('housekeeping/<int:pk>/', views.housekeeping_detail, name='housekeeping_detail'),
    path('housekeeping/<int:pk>/complete/', views.housekeeping_complete, name='housekeeping_complete'),
    
    # Troubleshooting Chart
    path('troubleshooting/chart/', views.troubleshooting_chart, name='troubleshooting_chart'),
    
    # Authentication URLs
    path('auth/', views_auth.login_home, name='login_home'),
    path('auth/company/register/', views_auth.company_register, name='company_register'),
    path('auth/company/login/', views_auth.company_login, name='company_login'),
    path('auth/company/dashboard/', views_auth.company_dashboard, name='company_dashboard'),
    path('auth/employee/register/', views_auth.manager_supervisor_register, name='manager_supervisor_register'),
    path('auth/user/login/', views_auth.user_login, name='user_login'),
    path('auth/logout/', views_auth.logout_view, name='logout'),
]
