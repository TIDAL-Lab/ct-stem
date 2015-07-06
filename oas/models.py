from django.db import models

class TeacherManager(models.Manager):
	def getSchoolChoices(self):
		return [(t['school'], t['school']) for t in self.get_query_set().values('school').distinct()]

class Teacher(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	school = models.CharField(max_length=50)
	display_name = models.CharField(max_length=40) # this would hold: Mr. Weintrop, Ms. Trouille, etc.
	email = models.EmailField()

	objects = TeacherManager()

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name

class Section(models.Model):
  name = models.CharField(max_length=30)
  teacher = models.ForeignKey(Teacher)
  subject = models.CharField(max_length=10)
  section = models.CharField(max_length=30)
  
  def __unicode__(self):
		return self.teacher.last_name + ', ' + self.teacher.first_name + ": " + self.name + " section: " + self.section

class Student(models.Model):
	student_id = models.CharField(max_length=50)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	grade = models.IntegerField()
	sex = models.CharField(max_length=1)
	dob = models.DateField()
	school = models.CharField(max_length=50, blank=True)
	email = models.EmailField(blank=True)
	ethnicity = models.CharField(max_length=200)

	def __unicode__(self):
		return self.last_name + ' ' + self.first_name

class AssessEvent(models.Model):
	student = models.ForeignKey(Student)
	section = models.ForeignKey(Section)
	date = models.DateTimeField()					# should this be called start time? do we also want end time? or infer that from the last response?
	location = models.CharField(max_length=40)
	assessment_set = models.CharField(max_length=30) # "Purple Bugs", "HDI", "Warblers", "CPS1", etc.

	def __unicode__(self):
		return self.student.last_name + ': ' + self.assessment_set

class Response(models.Model):
	assess_event = models.ForeignKey(AssessEvent)
	item_name	= models.CharField(max_length=10) 						#"PB1a", "Warb1"  
	response = models.CharField(max_length=400)
 	submitted_at = models.DateTimeField()
 	score = models.IntegerField() #Kevin change, score field holds integer score of each question
 	

 	def __unicode__(self):
 		return self.assess_event.student.last_name + ': ' +self.item_name + ' : ' + self.response

#new table 
class Items(models.Model):
	assessment_set = models.CharField(max_length=30) # "Purple Bugs", "HDI", "Warblers", "CPS1", etc.
	item_name = models.CharField(max_length=3) # 1, 2b, 3a, etc.
	question_text = models.CharField(max_length=400) #arbitrarily set the length to 400, actual question, ie "what happens..
	question_type = models.CharField(max_length=15) #MC_Radio, MC_checkbox, number, short answer, etc.
	answer = models.CharField(max_length=400) #actual answer
	#max_points = models.IntegerField() #potentially used in the future
	#skills = models.CharField() #potentially for coding questions
	
	def __unicode__(self):
		return self.assessment_set + ' ' + self.item_name +  ' ' + self.question_text + '\n Answer: ' + self.answer 
		
