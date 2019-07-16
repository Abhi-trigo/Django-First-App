import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse
class QuestionModelTests(TestCase):
	def test_was_published(self):
		""" was_published_recently() returns false 
		for question whose pub_date
		is in future
		"""
		time =timezone.now()+datetime.timedelta(days=30)
		future_question=Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(),False)
		
def test_was_published_with_old_question(self):
	'''this function returns false for question whose pub_date 
	is older than 1 day.'''
	time=timezone.now()-datetime.timedelta(days=1,seconds=1)
	old_question=Question(pub_date=time)
	self.assertIs(old_question.was_published_recently(),False)
def test_was_published_with_recent_question(self):
	""" was_published_recently() retruns true for question 
	whose pub_date is within the last day.
	"""
	time=timezone.now() - datetime.timedelta(hours=23, minutes=59,seconds=59)
	recent_question=Question(pub_date=time)
	self.assertIs(recent_question.was_published_recently(),True)
	 
def create_question(quesText,days):
	""" Create question with the given 'question txt' and published the
	given number of days offset to now (negative for question published
	in the past, positive for question that have yet to be published).
	"""
	time=timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(quesText=quesText,pub_date=time)

class QuestionIndexViewTests(TestCase):
	
	def test_no_question(self):
		""" if no question exist, an appropriate message is displayed"""
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response,"No polls are availabel.")
		self.assertQuerysetEqual(response.context['latest_question_list'],[])
	
	def test_past_question(self):
		""" Question with a pub_date in the past are displayed on the 
		index page.
		"""
		create_question(quesText="Past question.",days=-30)
		response =self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])
	
	def test_future_question(self):
		""" Question with a pub_date in the future aren't displayed on the index page"""
		create_question(quesText="Future question.",days=30)
		response=self.client.get(reverse("polls:index"))
		self.assertContains(response,"No polls are availabel.")
		self.assertQuerysetEqual(response.context['latest_question_list'],[])
	
	def test_future_past_question(self):
		""" Even if both past and future question exist, only past question are displayed."""
		create_question(quesText="Past question.",days=-30)
		create_question(quesText="Future question.",days=30)
		response=self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])

	
	def test_two_past_question(self):
		"""
		The question index page may display multiple question.
		"""
		create_question(quesText="Past question 1.",days=-30)
		create_question(quesText="Past question 2.",days=-5)
		response=self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question 2.>','<Question: Past question 1.>'])

class QuestionDetailViewTests(TestCase):
	def test_future_question(self):
		''' The detail view of a question with a pub_date in the future
		return a 404 not found '''
		future_question=create_question(quesText='Future question.',days=5)
		url=reverse('polls:detail',args=(future_question.id,))
		response=self.client.get(url)
		self.assertEqual(response.status_code,404)

	def test_past_question(self):
		''' The detail view of a question with a pub_date in the past 
		displays the question's text.'''
		past_question=create_question(quesText='Past question.',days=-5)
		url=reverse('polls:detail',args=(past_question.id,))
		response=self.client.get(url)
		self.assertContains(response,past_question.quesText) 

		
		







# Create your tests here.
