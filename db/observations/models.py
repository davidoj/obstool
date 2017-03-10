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

    def __str__(self):
        return 'Observation {} on {}'.format(self.obsnum, self.date)

class Item(models.Model):
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=2000, blank=True, default='')

    def __str__(self):
        return self.name

class ItemObservation(models.Model):
    observation = models.ForeignKey('Observation', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)

    def __str__(self):
        return 'Observation of item {} from {}'.format(self.item, self.observation)

class NumberedItemObservation(ItemObservation):
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
    notes = models.CharField(
        max_length=5000,
        verbose_name='Notes')

class InteractionObservation(models.Model):
    observation = models.ForeignKey(
        'Observation', 
        on_delete=models.CASCADE,
        related_name='interactionobservations')
    minute = models.IntegerField(
        verbose_name='Minute',
        help_text='How many minutes into the lesson is this observation?')
    intcode = models.CharField(
        max_length=2,
        default='',
        blank=True,
        choices= [
            ('','NA'),
            ('P','Prior learning'),
            ('FB','Feedback on learning'),
            ('FF','Feed-forward support'),
            ('Co','Co-construction')],
        verbose_name = 'Interaction Type')
    evidenceDIPS = models.CharField(
        max_length=2000, 
        blank=True, 
        default='',
        verbose_name='Power sharing',
        help_text='Evidence of discursive interactions and power sharing strategies')
    studentint = models.CharField(
        max_length=1,
        choices= [
            ('I','Indigenous or minoritised student'),
            ('O','Interaction with other student')], 
        blank=True, 
        default='',
        verbose_name='Group Interactions',
        help_text='Which students is the teacher interacting with?')
    teacherloc = models.CharField(max_length=1, 
        blank=True, 
        default='',
        choices=[
            ('','NA'),
            ('S','Stationary'),
            ('I','Moving around room'),
            ('O','Out of room')],
        verbose_name='Teacher Location')

    def __str__(self):
        return "Interaction minute {} for observation {}".format(self.minute, self.observation)

    class Meta:
        verbose_name = 'interactionobservation'
        verbose_name_plural = 'interactionobservations'