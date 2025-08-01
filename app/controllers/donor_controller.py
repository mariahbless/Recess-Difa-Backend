from app.extension import db
from app.models.organisation_model import Organisation
from app.models.donor_model import Donor
from flask import Blueprint,request,jsonify,current_app
from app.status_code import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_409_CONFLICT
from sqlalchemy import func
from flask_mail import Message
from app import mail


#Creating a new donor

# Define the bluerints
donor = Blueprint('donor',__name__,url_prefix='/api/v1/donor')

# Define the route
@donor.route('/create_donor', methods=['POST'])
def create_donor():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')            
    email = data.get('email')
    contact = data.get('contact')
    amount = data.get('amount')

    if not first_name or not last_name or not email or not contact or not amount:
        return jsonify({'error': 'All fields are required!'}), 400

    try:
        new_donor = Donor(first_name=first_name, last_name=last_name, email=email, contact=contact, amount=amount)
        db.session.add(new_donor)
        db.session.commit()

        # Send thank-you email
        try:
            msg = Message(
                subject="Thank you so much for donating to DIFA-UG!",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[email]
            )
            msg.body = f"Dear {first_name},\n\n I am honured to inform you that, \n\nDIFA-Ug has received your donation and we are very grateful.\n\n We look forward to continue interacting with you\n\nThank you!"
            mail.send(msg)
        except Exception as mail_err:
            print(f"Email sending failed: {mail_err}")

        return jsonify({
            'message': f'{first_name} has successfully been registered as a donor',
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'contact': contact,
            'amount': amount
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# @donor.route('/create_donor', methods = ['POST'])
# def create_student():
#     data = request.json
#     first_name = data.get('first_name')
#     last_name = data.get('last_name')            
#     email = data.get('email')
#     contact = data.get('contact')
#     amount = data.get('amount')


    
    

#     # Verification of the details
#     if not first_name or not last_name or not email or not contact or not amount  :
#         return jsonify({
#             'error':'All fields are required!'
#         }),HTTP_400_BAD_REQUEST
    
    
#     # Registering the new student
#     try:
#          new_donor = Donor(first_name=first_name,last_name=last_name, email=email,contact=contact,amount=amount)

#          # Adding the new data to the database
#          db.session.add(new_donor)
#          db.session.commit()

#          # The return message
#          return jsonify({
#               'message': new_donor.first_name + 'has successfully been created as student',
#               'first_name': new_donor.first_name,
#               'last_name': new_donor.last_name,
#               'email': new_donor.email,
#               'contact': new_donor.contact,
#               'amount': new_donor.amount
#              # 'organisation_id': new_donor.organisation_id
#          }),HTTP_200_OK

#     except Exception as e:
#          return jsonify({
#               'error': str(e)
#          }),HTTP_500_INTERNAL_SERVER_ERROR



#  Getting all donors
@donor.route('/get', methods = ['GET'])
def get_all_donors():
     all_donors = Donor.query.all()
     donor_data = []

     for donor in all_donors:
          donor_information = {
              'id': donor.id, 
              'first_name': donor.first_name,
              'last_name':donor.last_name,
              'email': donor.email,
              'contact': donor.contact,
              'amount': donor.amount
        
          }

          donor_data.append(donor_information)

          # The return message

     return jsonify({
              'message': 'All Donors have successfully been retrieved',
              'Total': len(donor_data),
              'donors': donor_data
             
         }),HTTP_200_OK

#Updating the donor details
@donor.route('/update/<int:id>', methods=['PUT'])
def update_donor(id):
    try:
        data = request.json

        # Retrieve donor by ID
        don = Donor.query.get(id)
        if not don:
            return jsonify({'error': 'Donor not found'}), 404

        # Define allowed fields for update
        allowed_fields = ['first_name', 'last_name', 'email', 'contact', 'amount']

        # Update only provided and allowed fields
        for key, value in data.items():
            if key in allowed_fields:
                setattr(don, key, value)

        db.session.commit()

        return jsonify({
            'message': 'Donor updated successfully',
            'donor': {
                'id': don.id,
                'first_name': don.first_name,
                'last_name': don.last_name,
                'email': don.email,
                'contact': don.contact,
                'amount': don.amount
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


#Deleting donor
@donor.route('/delete/<int:id>', methods=['DELETE'])
def delete_donor(id):
    try:
        donor_obj = Donor.query.filter_by(id=id).first()
        if not donor_obj:
            return jsonify({
                'error': 'This donor does not exist!'
            }), HTTP_404_NOT_FOUND

        db.session.delete(donor_obj)
        db.session.commit()

        return jsonify({
            'message': 'The donor has been successfully deleted',
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
    


#Getting all donation per month
@donor.route('/stats/donations_per_month', methods=['GET'])
def donations_per_month():
    results = db.session.query(
        func.date_format(Donor.created_at, '%Y-%m'),
        func.sum(Donor.amount)
    ).group_by(func.date_format(Donor.created_at, '%Y-%m')).all()

    data = [{'month': r[0], 'total_amount': float(r[1])} for r in results]

    return jsonify({
        'message': 'Donations grouped per month',
        'data': data
    }), 200


