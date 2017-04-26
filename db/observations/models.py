from django.db import models
from datetime import date


class Person(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)

class Teacher(Person):
    school = models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        verbose_name="Teacher's School")
    identifier = models.IntegerField(
        verbose_name='Teacher Identifier',
        choices = [
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5')
        ])

class Observer(Person):
    pass

class School(models.Model):
    name = models.CharField(
        max_length=50, 
        unique=True,
        verbose_name='Name')
    region = models.CharField(
        max_length=50,
        choices=[
            ('alice', 'Alice Springs'),
            ('barkly', 'Barkly')],
        verbose_name='Region')
    remoteness = models.CharField(
        max_length=50,
        choices=[
            ('urban', 'Urban'),
            ('remote','Remote'),
            ('vremote', 'Very Remote')],
        verbose_name='Remoteness')

    def __str__(self):
        return self.name

class Obsform(models.Model):
    name = models.CharField(
        max_length=50)
    def __str__(self):
        return self.name + "observation template"
    class Meta:
        verbose_name='Observation template'
        verbose_name_plural='Observation templates'

class Observation(models.Model):
    date = models.DateField(
        default=date.today,
        verbose_name='Observation Date',
        help_text='Enter observation date')
    obsnum = models.CharField(
        max_length=1,
        choices = [
            ('A','Observation A (first of two)'),
            ('B','Observation B (second of two)')],
        verbose_name='Observation Index',
        help_text='Is this the first or second observation?')
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    observer = models.ForeignKey('Observer', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'observation'
        verbose_name_plural = 'observations'
        abstract = True

    def __str__(self):
        return 'Observation {} on {}'.format(self.obsnum, self.date)

class ReviewObservation(Observation):
    class Meta:
        verbose_name = 'Review observation'
        verbose_name_plural = 'Review observations'

    def __str__(self):
        return 'Observation {} on {} (review)'.format(self.obsnum, self.date)    


class FeedbackObservation(Observation):

    class Meta:
        verbose_name = 'Feedback observation'
        verbose_name_plural = 'Feedback observations'

    def __str__(self):
        return 'Observation {} on {} (feedback focus)'.format(self.obsnum, self.date)    

class Item(models.Model):
    form = models.ForeignKey(
        'Obsform',
        on_delete=models.CASCADE,
        related_name='items')
    name = models.CharField(
        max_length=100,
        help_text='short name')
    description = models.CharField(
        max_length=5000,
        help_text='extended description',
        blank=True,
        default='')

    class Meta:
        verbose_name = 'observation item'
        verbose_name_plural = 'observation items'
        unique_together=('name','description')

    def __str__(self):
        return self.name


class Result(models.Model):
    observation = models.ForeignKey('ReviewObservation', on_delete=models.CASCADE, related_name='results')
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='results')

    def __str__(self):
        return 'Observation of item {} from {}'.format(self.item, self.observation)

    class Meta:
        abstract=True

class NumberedResult(Result):
    score = models.IntegerField(
        choices = [
            (1,'1 (No evidence)'),
            (2,'2 (Little evidence)'),
            (3,'3 (Some evidence)'),
            (4,'4 (Lots of evidence)'),
            (5,'5 (Great deal of evidence)')
        ],
        verbose_name='Score',
        help_text='How much evidence of this item did you see')
    notes = models.TextField(
        verbose_name='Notes',
        blank=True,
        default='')


class MbMInteraction(models.Model):
    """ Minute-by-minute observation"""
    minute = models.IntegerField(
        verbose_name='Minute',
        help_text='How many minutes into the lesson is this observation?')
    first10 = models.CharField(
        max_length=5000,
        default='',
        blank=True,
        verbose_name='First 10 seconds')

    location = models.CharField(
        max_length=2,
        choices=(
            ('D',"Desk"),
            ('S',"Stationary"),
            ('M','Moving around room'),
            ('O','Out of room')),
        verbose_name='Location',
        blank=True,
        default='')

    def __str__(self):
        return "Minute {} of observation {}".format(self.minute, self.observation)

    class Meta:
        verbose_name = 'Minute by minute observation'
        verbose_name_plural = 'Minute by minute observations'

class KtIInteraction(MbMInteraction):
    learning_evidence = models.BooleanField(
        default=False,
        verbose_name='Gathering Evidence',
        help_text='Gathering evidence of student progress or learning')
    evaluating_effect = models.BooleanField(
        default=False,
        verbose_name='Evaluating effect',
        help_text='Evaluating the effect he/she is having on students learning')
    acting_knowledge = models.BooleanField(
        default=False,
        verbose_name='Acting on knowledge',
        help_text='Acting on his/her knowledge of student learning')
    sharing_understanding = models.BooleanField(
        default=False,
        verbose_name='Students sharing understanding',
        help_text='The student(s) are sharing their understanding of learning')
    other = models.CharField(
        max_length=1000,
        verbose_name='Other',
        help_text='Please be specific',
        blank=True,
        default='')
    class Meta:
        verbose_name='Know thine Impact observation'
        verbose_name_plural='Know thine Impact observations'

class IPTInteraction(MbMInteraction):
    demonstrating_care = models.BooleanField(
        default=False,
        verbose_name='Relational trust',
        help_text='Demonstrating to student(s) that he/she cares about their learning')
    providing_feedback = models.BooleanField(
        default=False,
        verbose_name='Providing feedback',
        help_text='Providing feedback to students')
    dialogue = models.BooleanField(
        default=False,
        verbose_name='Engaged in dialogue',
        help_text='Engaged in dialogue with students')
    safe_classroom = models.BooleanField(
        default=False,
        verbose_name='Safe classroom',
        help_text='Ensuring it is safe to make mistakes')
    clarifying_lp = models.BooleanField(
        default=False,
        verbose_name='Clarifying learning progressions',
        help_text='Making learning progressions clear to students')
    providing_challenge = models.BooleanField(
        default=False,
        verbose_name='Providing challenge')
    high_exp = models.BooleanField(
        default=False,
        verbose_name='High expectations',
        help_text='Setting and demonstrating high expectations')
    focus_learning = models.BooleanField(
        default=False,
        verbose_name='Focussing on learning',
        help_text='Managing classroom so learning is focus, not behaviour')
    range_strategies = models.BooleanField(
        default=False,
        verbose_name='Wide range of strategies',
        help_text='Using a wide range of instructional strategies')
    other = models.CharField(
        max_length=1000,
        verbose_name='Other',
        help_text='Please be specific',
        blank=True,
        default='')
    class Meta:
        verbose_name='Inspired and Passionate Teaching observation'
        verbose_name_plural='Inspired and Passionate observations'

class FBInteraction(MbMInteraction):
    observation = models.ForeignKey(
        'FeedbackObservation', 
        on_delete=models.CASCADE,
        related_name='interactions')
    aspiration_feedback = models.BooleanField(
        default=False,
        verbose_name='Aspirational feedback',
        help_text='Delivering feedback that is aspirational')
    jit_feedback = models.BooleanField(
        default=False,
        verbose_name='Just in time',
        help_text='Delivering feedback just in time')
    whw_feedback = models.BooleanField(
        default=False,
        verbose_name='Where, how, where next',
        help_text='Feedback answers "Where am I going", "How am I going", "Where next"')
    task_feedback = models.BooleanField(
        default=False,
        verbose_name='Task feedback',
        help_text='Task feedback to students learning something new')
    process_feedback = models.BooleanField(
        default=False,
        verbose_name='Process feedback',
        help_text='Process feedback to students who are becoming more proficient')
    sr_feedback = models.BooleanField(
        default=False,
        verbose_name='Self-regulation feedback',
        help_text='Self-regulation feedback to students with high proficiency')
    praise = models.BooleanField(
        default=False,
        verbose_name='Praise')
    peer_feedback = models.BooleanField(
        default=False,
        verbose_name='Peer feedback',
        help_text='Working with students to ensure peer feedback is accurate')
    seeking_feedback = models.BooleanField(
        default=False,
        verbose_name='Seeking feedback',
        help_text='Seeking feedback from students')
    other = models.CharField(
        max_length=1000,
        verbose_name='Other',
        help_text='Please be specific',
        blank=True,
        default='')
    class Meta:
        verbose_name='Effective Feedback Teaching observation'
        verbose_name_plural='Effective Feedback observations'

# class MbMItemObservation(models.Model):
#     mbmobservation = models.ForeignKey('MbMObservation', on_delete=models.CASCADE)
#     item = models.ForeignKey('VLItem', on_delete=models.CASCADE)

#     def __str__(self):
#         return 'Observation of item {} from {}'.format(self.item, self.observation)
            # intcode = models.CharField(
    #     max_length=2,
    #     default='',
    #     blank=True,
    #     choices= [
    #         ('','NA'),
    #         ('P','Prior learning'),
    #         ('FB','Feedback on learning'),
    #         ('FF','Feed-forward support'),
    #         ('Co','Co-construction')],
    #     verbose_name = 'Interaction Type')
    # evidenceDIPS = models.CharField(
    #     max_length=2000, 
    #     blank=True, 
    #     default='',
    #     verbose_name='Power sharing',
    #     help_text='Evidence of discursive interactions and power sharing strategies')
    # studentint = models.CharField(
    #     max_length=1,
    #     choices= [
    #         ('I','Indigenous or minoritised student'),
    #         ('O','Interaction with other student')], 
    #     blank=True, 
    #     default='',
    #     verbose_name='Group Interactions',
    #     help_text='Which students is the teacher interacting with?')
    # teacherloc = models.CharField(max_length=1, 
    #     blank=True, 
    #     default='',
    #     choices=[
    #         ('','NA'),
    #         ('S','Stationary'),
    #         ('I','Moving around room'),
    #         ('O','Out of room')],
    #     verbose_name='Teacher Location')