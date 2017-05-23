from django.contrib.auth.models import User
from django.db import models
from datetime import date
from collections import Counter, OrderedDict
from .util import replace_chars


class Profile(models.Model):
    TEACHER = 1
    OBSERVER = 2
    role = models.PositiveSmallIntegerField(
        choices = ((TEACHER, 'Teacher'),(OBSERVER, 'Observer')),
        verbose_name = 'Role'
        )
    school = models.ForeignKey(
        'School',
        null=True,
        default=None,
        blank=True,
        verbose_name='School')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {} ({})".format(self.user.first_name, self.user.last_name, self.user.username)


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
        return self.name
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

    class Meta:
        verbose_name = 'observation'
        verbose_name_plural = 'observations'
        abstract = True
        ordering = ['-date']

    def __str__(self):
        if self.teacher:
            return 'Observation {} on {} (data); {school}'.format(self.obsnum, 
                self.date, 
                school=self.teacher.school if self.teacher.school else 'no school')    
        else:
            return 'Observation {} on {} (data)'.format(self.obsnum, 
                self.date)

class ReviewObservation(Observation):

    teacher = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='reviewfobservations')
    observer = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='reviewobservations_conducted')

    class Meta:
        verbose_name = 'Review observation'
        verbose_name_plural = 'Review observations'

    def __str__(self):
        try:
            return 'Observation {} on {} (data); {school}'.format(self.obsnum, 
                self.date, 
                school=self.teacher.school if self.teacher.school else 'no school')    
        except self._meta.model.teacher.RelatedObjectDoesNotExist:
            return 'Observation {} on {} (data)'.format(self.obsnum, 
                self.date)


class DataObservation(Observation):

    teacher = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='dataobservations')
    observer = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='dataobservations_conducted')
    kti = models.BooleanField(default=False, verbose_name = 'Know Thine Impact')
    fb = models.BooleanField(default=False, verbose_name = 'Feedback')
    ipt = models.BooleanField(default=False, verbose_name = 'Inspired and Passionate Teaching')
    # aitsl1 = models.BooleanField(default=False, verbose_name = 'AITSL 1: Know students & How they learn')
    # aitsl2 = models.BooleanField(default=False, verbose_name = 'AITSL 1: Know students & How they learn')
    # aitsl3 = models.BooleanField(default=False, verbose_name = 'AITSL 1: Know students & How they learn')
    # aitsl4 = models.BooleanField(default=False, verbose_name = 'AITSL 1: Know students & How they learn')
    # aitsl5 = models.BooleanField(default=False, verbose_name = 'AITSL 1: Know students & How they learn')
    # aitsl6 = models.BooleanField(default=False, verbose_name = 'AITSL 1: Know students & How they learn')
    # aitsl7 = models.BooleanField(default=False, verbose_name = 'AITSL 1: Know students & How they learn')


    class Meta:
        verbose_name = 'Data observation'
        verbose_name_plural = 'Data observations'

    def get_coding_tallies(self):
        c = Counter()
        for mbm in self.interactions.all():
            c.update(Counter(mbm.get_coding_fieldset()))
        return c

    def get_notes_comments(self):
        d = OrderedDict()
        for mbm in self.interactions.all():
            if mbm.get_notes():
                d['Notes minute {}'.format(mbm.minute)] = replace_chars(mbm.get_notes())
            if mbm.other:
                d['Comments minute {}'.format(mbm.minute)] = replace_chars(mbm.other)
        return d

    def __str__(self):
        try:
            return 'Observation {} on {} (data); {school}'.format(self.obsnum, 
                self.date, 
                school=self.teacher.school if self.teacher.school else 'no school')    
        except self._meta.model.teacher.RelatedObjectDoesNotExist:
            return 'Observation {} on {} (data)'.format(self.obsnum, 
                self.date)


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
        help_text='How much evidence of this item did you see',
        null=True,
        default=None)
    notes = models.TextField(
        verbose_name='Notes',
        blank=True,
        default='')

class BaseCodeMixin:
    def get_coding_fieldset(self):
        return {}

class IPTCodeMixin(models.Model):
    # Inspired and Passionate Teaching interactions
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


    class Meta:
        abstract = True

    def get_coding_fieldset(self):
        fieldset = super(IPTCodeMixin, self).get_coding_fieldset()
        if self.observation.ipt:
            fieldset.update({
                            'demonstrating_care':int(self.demonstrating_care),
                            'providing_feedback':int(self.providing_feedback),
                            'safe_classroom':int(self.safe_classroom),
                            'clarifying_lp':int(self.clarifying_lp),
                            'providing_challenge':int(self.providing_challenge),
                            'high_exp':int(self.high_exp),
                            'focus_learning':int(self.focus_learning),
                            'range_strategies':int(self.range_strategies)
                            })
        return fieldset

class KTICodeMixin(models.Model):
    # Know Thine Impact interactions
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
    
    class Meta:
        abstract = True

    def get_coding_fieldset(self):
        fieldset = super(KTICodeMixin, self).get_coding_fieldset()
        if self.observation.kti:
            fieldset.update({
                            'learning_evidence':int(self.learning_evidence),
                            'evaluating_effect':int(self.evaluating_effect),
                            'acting_knowledge':int(self.acting_knowledge),
                            'sharing_understanding':int(self.sharing_understanding)
                            })
        return fieldset

class FBCodeMixin(models.Model):
    # Feedback interactions
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

    class Meta:
        abstract = True

    def get_coding_fieldset(self):
        fieldset = super(FBCodeMixin, self).get_coding_fieldset()
        if self.observation.fb:
            fieldset.update({
                            'aspiration_feedback':int(self.aspiration_feedback),
                            'jit_feedback':int(self.jit_feedback),
                            'task_feedback':int(self.task_feedback),
                            'process_feedback':int(self.process_feedback),
                            'sr_feedback':int(self.sr_feedback),
                            'praise':int(self.praise),
                            'peer_feedback':int(self.peer_feedback),
                            'seeking_feedback':int(self.seeking_feedback)
                            })
        return fieldset

class AITSLCodeMixin(models.Model):
    pass

class MbMData(IPTCodeMixin,KTICodeMixin,FBCodeMixin,BaseCodeMixin):
    """ Minute-by-minute observation"""
    observation = models.ForeignKey(
        'DataObservation', 
        on_delete=models.CASCADE,
        related_name='interactions')
    minute = models.IntegerField(
        verbose_name='Minute',
        help_text='How many minutes into the lesson is this observation?')
    first10 = models.TextField(
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
    rest = models.TextField(
        default='',
        blank=True,
        verbose_name='Rest of minute')

    other = models.CharField(
        max_length=1000,
        verbose_name='Other',
        help_text='Please be specific',
        blank=True,
        default='')

    def __str__(self):
        return "Minute {} of observation {}".format(self.minute, self.observation)

    def get_notes(self):
        return self.first10 + '; ' + self.rest

    class Meta:
        verbose_name = 'Minute by minute datum'
        verbose_name_plural = 'Minute by minute data'
        ordering = ['minute']


class SIData(models.Model):
    observation = models.ForeignKey(
        'DataObservation', 
        on_delete=models.CASCADE,
        related_name='studentinterviews')
    whatlearning = models.TextField(
        verbose_name = 'What are you learning today?',
        blank=True,
        null=True,
        default='')
    howsuccess = models.TextField(
        verbose_name = 'How do you know how well you are going?',
        blank=True,
        null=True,
        default='')
    whatnext = models.TextField(
        verbose_name= 'What do you think your next steps are?',
        blank=True,
        null=True,
        default='')

    def __str__(self):
        return "Student {} of observation {}".format(self.id % 3 , self.observation)