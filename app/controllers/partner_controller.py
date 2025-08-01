from app.extension import db
from app.models.organisation_model import Organisation
from app.models.partner_model import Partner
from flask import Blueprint,request,jsonify,current_app
from app.status_code import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_409_CONFLICT
#from sqlalchemy import func
from flask_mail import Message
from app import mail


#Creating a new donor

# Define the bluerints
partner = Blueprint('partner',__name__,url_prefix='/api/v1/partner')

# Define the route
@partner.route('/create_partner', methods=['POST'])
def create_apartner():
    data = request.json
    firstname = data.get('firstname')
    lastname = data.get('lastname')            
    email = data.get('email')
    contact = data.get('contact')
    message = data.get('message')

    if not firstname or not lastname or not email or not contact or not message:
        return jsonify({'error': 'All fields are required!'}), 400

    try:
        new_partner = Partner(firstname=firstname, lastname=lastname, email=email, contact=contact, message=message)
        db.session.add(new_partner)
        db.session.commit()

        # Send thank-you email
        try:
            msg = Message(
                subject="Thank you so much for contacting DIFA-UG!",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[email]
            )
            msg.body = f"Dear {firstname},\n\n I am glad that you contacted DIFA-UG \n\nWe would like to know if you want to PARTNER with us or VOLUNTEER\n\n We look forward to seeing your reply with one of the above options\n\nThank you!\n\n Regards DIFA-Ug"
            mail.send(msg)
        except Exception as mail_err:
            print(f"Email sending failed: {mail_err}")

        return jsonify({
            'message': f'{firstname} , you have succesfull contacted DIFA-Ug',
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'contact': contact,
            'message': message
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500