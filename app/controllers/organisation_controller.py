from app.extension import db
from app.models.organisation_model import Organisation
from flask import Blueprint,request,jsonify
from app.status_code import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND,HTTP_500_INTERNAL_SERVER_ERROR



 #Define the Blue Print
organisation = Blueprint('organisation',__name__,url_prefix='/api/v1/organisation')

# Define the route
@organisation.route('/create_organisation', methods = ['POST'])

# Function to create organisation
def create_organisation():
    data = request.json
    name= data.get('name')
    location = data.get('location')
    email = data.get('email')
    contact = data.get('contact')
 


    # verifying the details
    if  not name or not location or not email or not contact:
        return jsonify({
            'error': 'All fields are required!'
        }),HTTP_400_BAD_REQUEST
    
    # Creating the  new organisation
    new_organisation = Organisation(name=name,location=location,email=email,contact=contact)

    # Adding the new organisation to the database
    db.session.add(new_organisation)
    db.session.commit()

    # The return message
    return jsonify({
        'message': name  +''  'has successufully been created as anew program',
        'name': new_organisation.name,
        'location': new_organisation.location,
        'email': new_organisation.email,
        'contact': new_organisation.contact 

    }),HTTP_200_OK





# Define the route
@organisation.route('/edit/<int:organisation_id>', methods = ['PUT'])
def update_organisation(organisation_id):
    organisation = Organisation.query.filter_by(organisation_id = organisation_id).first()

    try:
        # Checking whether the organisation exists
        if not organisation:
            return jsonify({
                'error': 'This organisation does not exist!'
            }),HTTP_404_NOT_FOUND
        
        else:
           
            name = request.get_json().get('name', organisation.name)
            year = request.get_json().get('year', organisation.year)
            duration = request.get_json().get('duration', organisation.duration)
           

            # Updating the data
           
            organisation.name = name
            organisation.year= year
            organisation.duration = duration
            

            # Commiting the updated data
            db.session.commit()

            # The return message
            return jsonify({
                'message': 'The program data has successfully been updated',
                'name': organisation.name,
                'year': organisation.year,
                'duration':organisation.duration
               
            })

    except Exception as e:
        return jsonify({
            'error': str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR



    




