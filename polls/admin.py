from django.contrib import admin
from .models import choice,Question
class ChoiceInline(admin.TabularInline):
	model=choice
	extra=2
class QuestionAdmin (admin.ModelAdmin):
	fieldsets=[
	(None,{'fields':['quesText']}),
	('Date information',{'fields':['pub_date'],'classes':['collapse']}),
	]
	list_display=('quesText','pub_date','was_published_recently')
	list_filter=['pub_date']
	search_fileds=["quesText"]
	inlines=[ChoiceInline]
admin.site.register(Question,QuestionAdmin)
admin.site.register(choice)

# Register your models here.
