from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField,SelectField



class AddForm(FlaskForm):

    name = StringField('Name :')
    pno=IntegerField('Phone Number: ')
    #movie=QuerySelectField(query_factory=,allow_blank=False)
    movie=SelectField('Movie Name: ',choices=[('s2','Sadak 2'),('db','Dil Bechara'),('c2','Coolie')])

    # timing=QuerySelectField(Choice.Query,allow_blank=False)
    timing=SelectField('Timing: ',choices=[])
    submit = SubmitField('Confirm Booking')

class DelForm(FlaskForm):

    name = IntegerField('Name :')
    pno=IntegerField('Phone Number :')
    movie=SelectField('Movie Name: ',choices=[('s2','Sadak 2'),('db','Dil Bechara'),('c2','Coolie')])

    # timing=QuerySelectField(Choice.Query,allow_blank=False)
    
    submit = SubmitField('Confirm Cancellation')
