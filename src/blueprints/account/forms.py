from utils.flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import PasswordField, StringField, IntegerField, SelectField, \
    TextAreaField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired, Email, EqualTo, Optional
from wtforms_alchemy import model_form_factory
from models import User

BaseModelForm = model_form_factory(FlaskForm)

images = UploadSet('images', IMAGES)


class LoginForm(FlaskForm):
    """A Class to handle login form rendering"""

    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')


class RegisterForm(FlaskForm):
    """docstring for RegisterForm:"""
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    phone_number = IntegerField('Phone Number', validators=[InputRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is taken.')

    def validate_phone_number(self, field):
        if User.query.filter_by(phone_number=field.data).first():
            raise ValidationError('Phone Number already registered.')




class InviteUserForm(FlaskForm):
    first_name = StringField(
        'First name', validators=[InputRequired(),
                                  Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(),
                                 Length(1, 64)])
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    area_code = IntegerField('Area Code', validators=[DataRequired()])
    mobile_phone = StringField('Number')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address, user exists.')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[Email()])


class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    new_password = PasswordField('New password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])


class OTPForm(FlaskForm):
    # verify_id = HiddenField('ID')
    token = StringField('Enter your verification code:')


class ChangeEmailForm(FlaskForm):
    email = EmailField(
        'New email', validators=[DataRequired(),
                                 Length(1, 64),
                                 Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class ChangeProfileForm(BaseModelForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    summary_text = TextAreaField('Summary Text or Description')
    photo = FileField('Profile Image', validators=[
        Optional(), FileAllowed(images, 'Images only!')])
    area_code = StringField('Phone area code only',
                            validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('Enter your state', validators=[DataRequired()])

    profession = SelectField(u'Profession', choices=[('Recruiter', 'Recruiter'),
                                                     ('Ambulatory Nurse',
                                                      'Ambulatory Nurse'),
                                                     ('Anesthesiologist',
                                                      'Anesthesiologist'),
                                                     ('Audiologist',
                                                      'Audiologist'),
                                                     ('Behavioral Health Charge Nurse',
                                                      'Behavioral Health Charge Nurse'),
                                                     ('Bereavement Counselor',
                                                      'Bereavement Counselor'),
                                                     ('Biologist', 'Biologist'),
                                                     ('Cardiac Catheterization Lab Nurse',
                                                      'Cardiac Catheterization Lab Nurse'),
                                                     ('Cardiovascular Operating Room Nurse',
                                                      'Cardiovascular Operating Room Nurse'),
                                                     ('Cardiovascular Technologist',
                                                      'Cardiovascular Technologist'),
                                                     ('Charge Nurse',
                                                      'Charge Nurse'),
                                                     ('Chiropractor',
                                                      'Chiropractor'),
                                                     ('Counselor', 'Counselor'),
                                                     ('Dentist', 'Dentist'),
                                                     ('Dermatology Nurse',
                                                      'Dermatology Nurse'),
                                                     ('Dialysis Nurse',
                                                      'Dialysis Nurse'),
                                                     ('Doctor', 'Doctor'),
                                                     ('Emergency Room Nurse',
                                                      'Emergency Room Nurse'),
                                                     ('Endoscopy Nurse',
                                                      'Endoscopy Nurse'),
                                                     ('Family Nurse Practitioner',
                                                      'Family Nurse Practitioner'),
                                                     ('Flight Nurse',
                                                      'Flight Nurse'),
                                                     ('Genetic Counselor',
                                                      'Genetic Counselor'),
                                                     ('Home Health Nurse',
                                                      'Home Health Nurse'),
                                                     ('Hospice Counselor',
                                                      'Hospice Counselor'),
                                                     ('Hospice Nurse',
                                                      'Hospice Nurse'),
                                                     ('House Supervisor Nurse',
                                                      'House Supervisor Nurse'),
                                                     ('Intensive Care Nurse',
                                                      'Intensive Care Nurse'),
                                                     ('Interventional Radiology Nurse',
                                                      'Interventional Radiology Nurse'),
                                                     ('Labor and Delivery Nurse',
                                                      'Labor and Delivery Nurse'),
                                                     ('Lead Registered Nurse',
                                                      'Lead Registered Nurse'),
                                                     ('Legal Nurse Consultant',
                                                      'Legal Nurse Consultant'),
                                                     ('Licensed Practical Nurse',
                                                      'Licensed Practical Nurse'),
                                                     ('Licensed Vocational Nurse',
                                                      'Licensed Vocational Nurse'),
                                                     ('Medical Surgery Nurse',
                                                      'Medical Surgery Nurse'),
                                                     ('Microbiologist',
                                                      'Microbiologist'),
                                                     ('Neonatal Intensive Care Nurse',
                                                      'Neonatal Intensive Care Nurse'),
                                                     ('Nurse', 'Nurse'),
                                                     ('Nurse Anesthetist',
                                                      'Nurse Anesthetist'),
                                                     ('Nurse Midwife',
                                                      'Nurse Midwife'),
                                                     ('Nurse Practitioner',
                                                      'Nurse Practitioner'),
                                                     ('Nursing Assistant',
                                                      'Nursing Assistant'),
                                                     ('Occupational Health Nurse',
                                                      'Occupational Health Nurse'),
                                                     ('Occupational Health and Safety Specialist',
                                                      'Occupational Health and Safety Specialist'),
                                                     ('Occupational Therapist',
                                                      'Occupational Therapist'),
                                                     ('Office Nurse',
                                                      'Office Nurse'),
                                                     ('Oncology Nurse',
                                                      'Oncology Nurse'),
                                                     ('Operating Room Nurse',
                                                      'Operating Room Nurse'),
                                                     ('Optician', 'Optician'),
                                                     ('Optometrist', 'Optometrist'), (
                                                         'Orthotist', 'Orthotist'),
                                                     ('Outreach RN', 'Outreach RN'), (
                                                         'Paramedic', 'Paramedic'),
                                                     ('Pediatric Endocrinology Nurse',
                                                      'Pediatric Endocrinology Nurse'),
                                                     ('Pediatric Intensive Care Nurse',
                                                      'Pediatric Intensive Care Nurse'),
                                                     ('Pediatric Nurse',
                                                      'Pediatric Nurse'),
                                                     ('Pediatric Nurse Practitioner',
                                                      'Pediatric Nurse Practitioner'),
                                                     ('Perioperative Nurse',
                                                      'Perioperative Nurse'),
                                                     ('Pharmacist', 'Pharmacist'),
                                                     ('Prosthetist',
                                                      'Prosthetist'),
                                                     ('Physician', 'Physician'),
                                                     ('Podiatrist', 'Podiatrist'),
                                                     ('Post Anesthesia Nurse',
                                                      'Post Anesthesia Nurse'),
                                                     ('Postpartum Nurse',
                                                      'Postpartum Nurse'),
                                                     ('Progressive Care Nurse',
                                                      'Progressive Care Nurse'),
                                                     ('Psychiatric Nurse',
                                                      'Psychiatric Nurse'),
                                                     ('Psychiatric Nurse Practitioner',
                                                      'Psychiatric Nurse Practitioner'),
                                                     ('Public Health Nurse',
                                                      'Public Health Nurse'),
                                                     ('Registered Nurse (RN)',
                                                      'Registered Nurse (RN)'),
                                                     ('Registered Nurse (RN) Case Manager',
                                                      'Registered Nurse (RN) Case Manager'),
                                                     ('Registered Nurse(RN)Data Coordinator',
                                                      'Registered Nurse(RN)Data Coordinator'),
                                                     ('Registered Nurse (RN)First Assistant',
                                                      'Registered Nurse (RN)First Assistant'),
                                                     ('Registered Nurse (RN)Geriatric Care',
                                                      'Registered Nurse (RN)Geriatric Care'),
                                                     ('Registered Nurse (RN) Medical Inpatient Services',
                                                      'Registered Nurse (RN) Medical Inpatient Services'),
                                                     ('Registered Nurse (RN) Patient Call Center',
                                                      'Registered Nurse (RN) Patient Call Center'),
                                                     ('Registered Nurse (RN) Student Health Services',
                                                      'Registered Nurse (RN) Student Health Services'),
                                                     ('Registered Nurse (RN)Telephone Triage',
                                                      'Registered Nurse (RN)Telephone Triage'),
                                                     ('Registered Nurse (RN)Urgent Care',
                                                      'Registered Nurse (RN)Urgent Care'),
                                                     ('Registered Nurse (RN) Women Services',
                                                      'Registered Nurse (RN) Women Services'),
                                                     ('Restorative Nurse',
                                                      'Restorative Nurse'),
                                                     ('Registered Medical Assistant',
                                                      'Registered Medical Assistant'),
                                                     ('Respiration (Inhalation) Therapist',
                                                      'Respiration (Inhalation) Therapist'),
                                                     ('School Nurse',
                                                      'School Nurse'),
                                                     ('Speech-Language Pathologist',
                                                      'Speech-Language Pathologist'),
                                                     ('Surgeon', 'Surgeon'),
                                                     ('Telemetry Nurse',
                                                      'Telemetry Nurse'),
                                                     ('Therapist', 'Therapist'),
                                                     ('Veterinarian',
                                                      'Veterinarian'),
                                                     ('Veterinary Assistant',
                                                      'Veterinary Assistant'),
                                                     ('Veterinary Technologist',
                                                      'Veterinary Technologist'),
                                                     ('Wellness Nurse',
                                                      'Wellness Nurse'),
                                                     ('Athletic Trainer',
                                                      'Athletic Trainer'),
                                                     ('Certified Medical Assistant',
                                                      'Certified Medical Assistant'),
                                                     ('Certified Nurse Assistant',
                                                      'Certified Nurse Assistant'),
                                                     ('Certified Nursing Assistant',
                                                      'Certified Nursing Assistant'),
                                                     ('Clinical Liaison',
                                                      'Clinical Liaison'),
                                                     ('Clinical Nurse Manager',
                                                      'Clinical Nurse Manager'),
                                                     ('Clinical Research Associate',
                                                      'Clinical Research Associate'),
                                                     ('Clinical Research Coordinator',
                                                      'Clinical Research Coordinator'),
                                                     ('Clinical Reviewer',
                                                      'Clinical Reviewer'),
                                                     ('Clinical Specialist',
                                                      'Clinical Specialist'),
                                                     ('Dental Assistant',
                                                      'Dental Assistant'),
                                                     ('Dental Hygienist',
                                                      'Dental Hygienist'),
                                                     ('Dietitian', 'Dietitian'),
                                                     ('Exercise Physiologist',
                                                      'Exercise Physiologist'),
                                                     ('Health Educator',
                                                      'Health Educator'),
                                                     ('Home Health Aide',
                                                      'Home Health Aide'),
                                                     ('Hospice Aide',
                                                      'Hospice Aide'),
                                                     ('Massage Therapist',
                                                      'Massage Therapist'),
                                                     ('Nurse Aide', 'Nurse Aide'),
                                                     ('Nurse Clinical Educator',
                                                      'Nurse Clinical Educator'),
                                                     ('Nurse Consultant',
                                                      'Nurse Consultant'),
                                                     ('Nurse Informatics Analyst',
                                                      'Nurse Informatics Analyst'),
                                                     ('Nurse Manager',
                                                      'Nurse Manager'),
                                                     ('Nurse Paralegal',
                                                      'Nurse Paralegal'),
                                                     ('Nutritionist',
                                                      'Nutritionist'),
                                                     ('Occupational Therapy Assistant',
                                                      'Occupational Therapy Assistant'),
                                                     ('Orderly Attendant',
                                                      'Orderly Attendant'),
                                                     ('Pharmacy Clerk',
                                                      'Pharmacy Clerk'),
                                                     ('Physical Therapist Assistant',
                                                      'Physical Therapist Assistant'),
                                                     ('Physician Aide',
                                                      'Physician Aide'),
                                                     ('Physician Assistant',
                                                      'Physician Assistant'),
                                                     ('Psychiatric Aide',
                                                      'Psychiatric Aide'),
                                                     ('Radiation Therapist',
                                                      'Radiation Therapist'),
                                                     ('Recreational Therapist',
                                                      'Recreational Therapist'),
                                                     ('Regional Kidney Smart Educator',
                                                      'Regional Kidney Smart Educator'),
                                                     ('OTHER SPECIFY', 'OTHER SPECIFY')])
    custom_profession = StringField(
        'Custom Profession', validators=[Optional()])
    gender = SelectField(u'Gender', choices=[
        ('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender')])
    zip = StringField('Zip Code', validators=[DataRequired(), Length(1, 7)])
    country = SelectField(u'Select Country', choices=[
        ('Afganistan', 'Afghanistan'),
        ('Albania', 'Albania'),
        ('Algeria', 'Algeria'),
        ('American Samoa', 'American Samoa'),
        ('Andorra', 'Andorra'),
        ('Angola', 'Angola'),
        ('Anguilla', 'Anguilla'),
        ('Antigua & Barbuda', 'Antigua & Barbuda'),
        ('Argentina', 'Argentina'),
        ('Armenia', 'Armenia'),
        ('Aruba', 'Aruba'),
        ('Australia', 'Australia'),
        ('Austria', 'Austria'),
        ('Azerbaijan', 'Azerbaijan'),
        ('Bahamas', 'Bahamas'),
        ('Bahrain', 'Bahrain'),
        ('Bangladesh', 'Bangladesh'),
        ('Barbados', 'Barbados'),
        ('Belarus', 'Belarus'),
        ('Belgium', 'Belgium'),
        ('Belize', 'Belize'),
        ('Benin', 'Benin'),
        ('Bermuda', 'Bermuda'),
        ('Bhutan', 'Bhutan'),
        ('Bolivia', 'Bolivia'),
        ('Bonaire', 'Bonaire'),
        ('Bosnia & Herzegovina', 'Bosnia & Herzegovina'),
        ('Botswana', 'Botswana'),
        ('Brazil', 'Brazil'),
        ('British Indian Ocean Ter', 'British Indian Ocean Ter'),
        ('Brunei', 'Brunei'),
        ('Bulgaria', 'Bulgaria'),
        ('Burkina Faso', 'Burkina Faso'),
        ('Burundi', 'Burundi'),
        ('Cambodia', 'Cambodia'),
        ('Cameroon', 'Cameroon'),
        ('Canada', 'Canada'),
        ('Canary Islands', 'Canary Islands'),
        ('Cape Verde', 'Cape Verde'),
        ('Cayman Islands', 'Cayman Islands'),
        ('Central African Republic', 'Central African Republic'),
        ('Chad', 'Chad'),
        ('Channel Islands', 'Channel Islands'),
        ('Chile', 'Chile'),
        ('China', 'China'),
        ('Christmas Island', 'Christmas Island'),
        ('Cocos Island', 'Cocos Island'),
        ('Colombia', 'Colombia'),
        ('Comoros', 'Comoros'),
        ('Congo', 'Congo'),
        ('Cook Islands', 'Cook Islands'),
        ('Costa Rica', 'Costa Rica'),
        ('Cote DIvoire', 'Cote DIvoire'),
        ('Croatia', 'Croatia'),
        ('Cuba', 'Cuba'),
        ('Curaco', 'Curacao'),
        ('Cyprus', 'Cyprus'),
        ('Czech Republic', 'Czech Republic'),
        ('Denmark', 'Denmark'),
        ('Djibouti', 'Djibouti'),
        ('Dominica', 'Dominica'),
        ('Dominican Republic', 'Dominican Republic'),
        ('East Timor', 'East Timor'),
        ('Ecuador', 'Ecuador'),
        ('Egypt', 'Egypt'),
        ('El Salvador', 'El Salvador'),
        ('Equatorial Guinea', 'Equatorial Guinea'),
        ('Eritrea', 'Eritrea'),
        ('Estonia', 'Estonia'),
        ('Ethiopia', 'Ethiopia'),
        ('Falkland Islands', 'Falkland Islands'),
        ('Faroe Islands', 'Faroe Islands'),
        ('Fiji', 'Fiji'),
        ('Finland', 'Finland'),
        ('France', 'France'),
        ('French Guiana', 'French Guiana'),
        ('French Polynesia', 'French Polynesia'),
        ('French Southern Ter', 'French Southern Ter'),
        ('Gabon', 'Gabon'),
        ('Gambia', 'Gambia'),
        ('Georgia', 'Georgia'),
        ('Germany', 'Germany'),
        ('Ghana', 'Ghana'),
        ('Gibraltar', 'Gibraltar'),
        ('Great Britain', 'Great Britain'),
        ('Greece', 'Greece'),
        ('Greenland', 'Greenland'),
        ('Grenada', 'Grenada'),
        ('Guadeloupe', 'Guadeloupe'),
        ('Guam', 'Guam'),
        ('Guatemala', 'Guatemala'),
        ('Guinea', 'Guinea'),
        ('Guyana', 'Guyana'),
        ('Haiti', 'Haiti'),
        ('Hawaii', 'Hawaii'),
        ('Honduras', 'Honduras'),
        ('Hong Kong', 'Hong Kong'),
        ('Hungary', 'Hungary'),
        ('Iceland', 'Iceland'),
        ('Indonesia', 'Indonesia'),
        ('India', 'India'),
        ('Iran', 'Iran'),
        ('Iraq', 'Iraq'),
        ('Ireland', 'Ireland'),
        ('Isle of Man', 'Isle of Man'),
        ('Israel', 'Israel'),
        ('Italy', 'Italy'),
        ('Jamaica', 'Jamaica'),
        ('Japan', 'Japan'),
        ('Jordan', 'Jordan'),
        ('Kazakhstan', 'Kazakhstan'),
        ('Kenya', 'Kenya'),
        ('Kiribati', 'Kiribati'),
        ('Korea North', 'Korea North'),
        ('Korea Sout', 'Korea South'),
        ('Kuwait', 'Kuwait'),
        ('Kyrgyzstan', 'Kyrgyzstan'),
        ('Laos', 'Laos'),
        ('Latvia', 'Latvia'),
        ('Lebanon', 'Lebanon'),
        ('Lesotho', 'Lesotho'),
        ('Liberia', 'Liberia'),
        ('Libya', 'Libya'),
        ('Liechtenstein', 'Liechtenstein'),
        ('Lithuania', 'Lithuania'),
        ('Luxembourg', 'Luxembourg'),
        ('Macau', 'Macau'),
        ('Macedonia', 'Macedonia'),
        ('Madagascar', 'Madagascar'),
        ('Malaysia', 'Malaysia'),
        ('Malawi', 'Malawi'),
        ('Maldives', 'Maldives'),
        ('Mali', 'Mali'),
        ('Malta', 'Malta'),
        ('Marshall Islands', 'Marshall Islands'),
        ('Martinique', 'Martinique'),
        ('Mauritania', 'Mauritania'),
        ('Mauritius', 'Mauritius'),
        ('Mayotte', 'Mayotte'),
        ('Mexico', 'Mexico'),
        ('Midway Islands', 'Midway Islands'),
        ('Moldova', 'Moldova'),
        ('Monaco', 'Monaco'),
        ('Mongolia', 'Mongolia'),
        ('Montserrat', 'Montserrat'),
        ('Morocco', 'Morocco'),
        ('Mozambique', 'Mozambique'),
        ('Myanmar', 'Myanmar'),
        ('Nambia', 'Nambia'),
        ('Nauru', 'Nauru'),
        ('Nepal', 'Nepal'),
        ('Netherland Antilles', 'Netherland Antilles'),
        ('Netherlands', 'Netherlands (Holland, Europe)'),
        ('Nevis', 'Nevis'),
        ('New Caledonia', 'New Caledonia'),
        ('New Zealand', 'New Zealand'),
        ('Nicaragua', 'Nicaragua'),
        ('Niger', 'Niger'),
        ('Nigeria', 'Nigeria'),
        ('Niue', 'Niue'),
        ('Norfolk Island', 'Norfolk Island'),
        ('Norway', 'Norway'),
        ('Oman', 'Oman'),
        ('Pakistan', 'Pakistan'),
        ('Palau Island', 'Palau Island'),
        ('Palestine', 'Palestine'),
        ('Panama', 'Panama'),
        ('Papua New Guinea', 'Papua New Guinea'),
        ('Paraguay', 'Paraguay'),
        ('Peru', 'Peru'),
        ('Phillipines', 'Philippines'),
        ('Pitcairn Island', 'Pitcairn Island'),
        ('Poland', 'Poland'),
        ('Portugal', 'Portugal'),
        ('Puerto Rico', 'Puerto Rico'),
        ('Qatar', 'Qatar'),
        ('Republic of Montenegro', 'Republic of Montenegro'),
        ('Republic of Serbia', 'Republic of Serbia'),
        ('Reunion', 'Reunion'),
        ('Romania', 'Romania'),
        ('Russia', 'Russia'),
        ('Rwanda', 'Rwanda'),
        ('St Barthelemy', 'St Barthelemy'),
        ('St Eustatius', 'St Eustatius'),
        ('St Helena', 'St Helena'),
        ('St Kitts-Nevis', 'St Kitts-Nevis'),
        ('St Lucia', 'St Lucia'),
        ('St Maarten', 'St Maarten'),
        ('St Pierre & Miquelon', 'St Pierre & Miquelon'),
        ('St Vincent & Grenadines', 'St Vincent & Grenadines'),
        ('Saipan', 'Saipan'),
        ('Samoa', 'Samoa'),
        ('Samoa American', 'Samoa American'),
        ('San Marino', 'San Marino'),
        ('Sao Tome & Principe', 'Sao Tome & Principe'),
        ('Saudi Arabia', 'Saudi Arabia'),
        ('Senegal', 'Senegal'),
        ('Seychelles', 'Seychelles'),
        ('Sierra Leone', 'Sierra Leone'),
        ('Singapore', 'Singapore'),
        ('Slovakia', 'Slovakia'),
        ('Slovenia', 'Slovenia'),
        ('Solomon Islands', 'Solomon Islands'),
        ('Somalia', 'Somalia'),
        ('South Africa', 'South Africa'),
        ('Spain', 'Spain'),
        ('Sri Lanka', 'Sri Lanka'),
        ('Sudan', 'Sudan'),
        ('Suriname', 'Suriname'),
        ('Swaziland', 'Swaziland'),
        ('Sweden', 'Sweden'),
        ('Switzerland', 'Switzerland'),
        ('Syria', 'Syria'),
        ('Tahiti', 'Tahiti'),
        ('Taiwan', 'Taiwan'),
        ('Tajikistan', 'Tajikistan'),
        ('Tanzania', 'Tanzania'),
        ('Thailand', 'Thailand'),
        ('Togo', 'Togo'),
        ('Tokelau', 'Tokelau'),
        ('Tonga', 'Tonga'),
        ('Trinidad & Tobago', 'Trinidad & Tobago'),
        ('Tunisia', 'Tunisia'),
        ('Turkey', 'Turkey'),
        ('Turkmenistan', 'Turkmenistan'),
        ('Turks & Caicos Is', 'Turks & Caicos Is'),
        ('Tuvalu', 'Tuvalu'),
        ('Uganda', 'Uganda'),
        ('United Kingdom', 'United Kingdom'),
        ('Ukraine', 'Ukraine'),
        ('United Arab Erimates', 'United Arab Emirates'),
        ('United States of America', 'United States of America'),
        ('Uraguay', 'Uruguay'),
        ('Uzbekistan', 'Uzbekistan'),
        ('Vanuatu', 'Vanuatu'),
        ('Vatican City State', 'Vatican City State'),
        ('Venezuela', 'Venezuela'),
        ('Vietnam', 'Vietnam'),
        ('Virgin Islands (Brit)', 'Virgin Islands (Brit)'),
        ('Virgin Islands (USA)', 'Virgin Islands (USA)'),
        ('Wake Island', 'Wake Island'),
        ('Wallis & Futana Is', 'Wallis & Futana Is'),
        ('Yemen', 'Yemen'),
        ('Zaire', 'Zaire'),
        ('Zambia', 'Zambia'),
        ('Zimbabwe', 'Zimbabwe')])
    submit = SubmitField('Submit')


class ContactForm(FlaskForm):
    text = TextAreaField('Message', validators=[DataRequired()])


class CreatePasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('password2', 'Passwords must match.')
        ])
    password2 = PasswordField(
        'Confirm new password', validators=[InputRequired()])
    submit = SubmitField('Set password')


# COPY HERE
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[InputRequired()])
    new_password = PasswordField(
        'New password',
        validators=[
            InputRequired(),
            EqualTo('new_password2', 'Passwords must match.')
        ])
    new_password2 = PasswordField(
        'Confirm new password', validators=[InputRequired()])
    submit = SubmitField('Update password')
