from django.contrib import admin

from head.candidates.models import Candidate

class CandidateAdmin(admin.ModelAdmin):
    list_display = ("name", "electoral_unit", "number", "tse_id", "party",)
    list_filter = ("electoral_unit", "party")



admin.site.register(Candidate, CandidateAdmin)