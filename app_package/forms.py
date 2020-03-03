from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,IntegerField,RadioField
from wtforms.validators import DataRequired,EqualTo,ValidationError
from app_package.models import User


class LoginForm(FlaskForm):
    username=StringField("Username:", validators=[DataRequired()])
    password=PasswordField("Password:", validators=[DataRequired()])
    remember_me=BooleanField("Remember me")
    submit=SubmitField("Sign in")
    
    
class RegistrationForm(FlaskForm):
    username=StringField("Username:", validators=[DataRequired()])
    password=PasswordField("Password:", validators=[DataRequired()])
    password2=PasswordField("Repeat Password:", validators=[DataRequired(),EqualTo("password")])
    submit=SubmitField("Register")
    
    
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username exists,choose another one")
            
         
         
class AddCustomerForm(FlaskForm):    
    cname=StringField("Username:", validators=[DataRequired()])
    caccno=IntegerField("AccountNo:", validators=[DataRequired()])
    caadhar=IntegerField("AadharNumber:",validators=[DataRequired()])
    cmobile=IntegerField("Mobile:", validators=[DataRequired()])
    ctype=RadioField('Type', choices = [('ordinary','ordinary'),('priority','priority')])
    cbalance=IntegerField("Balance:", validators=[DataRequired()])
    submit=SubmitField("Add customer")
    
    
class DepositForm(FlaskForm): 
    caccno=IntegerField("AccountNumber:")
    amt=IntegerField("Amount Deposit:", validators=[DataRequired()])
    submit=SubmitField("Deposit")
    
    
class DeleteCustomerForm(FlaskForm):
    caccno=IntegerField("AccountNumber:", validators=[DataRequired()])
    submit=SubmitField("Delete Customer")
    
class DisplayForm(FlaskForm): 
    caccno=IntegerField("AccountNo:", validators=[DataRequired()])
    submit=SubmitField("Display Customer")
    
    
class WithDrawForm(FlaskForm): 
    caccno=IntegerField("AccountNumber:")
    amt=IntegerField("Amount Withdraw:", validators=[DataRequired()])
    submit=SubmitField("withdraw")
    
    
    
    
    
    
    
    
    


