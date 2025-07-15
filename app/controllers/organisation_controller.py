from app.extension import db,bcrypt,jwt
from app.models.organisation_model import Organisation
from flask import Blueprint,request,jsonify
from app.status_code import HTTP_200_OK,HTTP_404_NOT_FOUND,HTTP_201_CREATED,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_409_CONFLICT
import validators
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt_identity




organisation = Blueprint('organisation', __name__, url_prefix='/api/v1/organisation')

@organisation.route('/create_user', methods=['POST'])
def register_user(): # registering the user
    data = request.json # variable of object storing data
    name = data.get('name') #accessing variables from the table
    location = data.get('location')
    contact = data.get('contact')
    email = data.get('email').lower()
    password = data.get('password')
    message = data.get('message')  
    


#Request response cycle 

    if not name or not location or not contact or not email or not password or not message: 
        return jsonify({"error": "All fields are required" }),HTTP_400_BAD_REQUEST

    
    if len(password) < 8: #Password should not be less than 8
        return jsonify({'error': "Password is too short"}),HTTP_400_BAD_REQUEST
    
    if not validators.email(email): 
        return jsonify({"error":"Email is invalid"}),HTTP_400_BAD_REQUEST
    
    
    if  Organisation.query.filter_by(email=email).first() is not None: #Ensuring email and contact constraints 
          return jsonify({"error":"Email address in use"}),HTTP_409_CONFLICT 
    
    if Organisation.query.filter_by(contact=contact).first() is not None:
          return jsonify({"error":"Phone number already in use"}),HTTP_409_CONFLICT
    
    try:
        # Hashing password to encrypt password,to avoid unauthorised access
         hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')


        #Creating the user
         new_user = Organisation(name=name,location=location,password=hashed_password,email=email,contact=contact,message=message)
         db.session.add(new_user)
         db.session.commit()

         # Author name
         username = new_user.name


         return jsonify({
              'message': username + 'has been successfully created',
              'user':{
                   'id':new_user.id,
                   'name':new_user.name,
                   'location':new_user.location,
                   'contact':new_user.contact,
                   'email' : new_user.email,
                   'message':new_user.message,
                   'created': new_user.created_at,

                   
                 }
         }),HTTP_201_CREATED
    
    except Exception as e:
         db.session.rollback()
         return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    

   #user login
@organisation.post('/login')
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    
    try:
       if not password or not email:
        return jsonify({'Message': "Email and Password are required."}), HTTP_400_BAD_REQUEST
    
    
       user = Organisation.query.filter_by(email=email.lower()).first()
       if user:
            
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            #refresh_token = create_refresh_token(identity=str(user.id))
            if hashed_password:
                   access_token = create_access_token(identity=str(user.id))
                   refresh_token = create_refresh_token(identity= str(user.id)) 
                   return jsonify({
                'user':{
                    'id': user.id,
                    'username': user.name,
                    'email': user.email,
                    'access_token': access_token,
                    'refresh_token': refresh_token 
                   },
                     'message': "You have successfully logged into your account."
                  }), HTTP_200_OK
            
            else: 
                return jsonify({'Message': "Invalid password."}), HTTP_401_UNAUTHORIZED
           

       else:
         return jsonify({'Message': "Invalid email address."}), HTTP_401_UNAUTHORIZED

    except Exception as e:
        return jsonify({
            'error': str(e)
            }), HTTP_500_INTERNAL_SERVER_ERROR
    

 
#Updating the organisation details
@organisation.route('/edit/<int:id>', methods=["PUT"])
def update_organisation(id):
    try:
        data = request.json

        org = Organisation.query.get(id)
        if not org:
            return jsonify({'error': 'Organisation not found'}), 404

        # Securely update only allowed fields
        allowed_fields = ['name', 'location', 'contact', 'email', 'password', 'message']

        for key, value in data.items():
            if key in allowed_fields:
                if key == 'email':
                    value = value.lower()
                    # Validate email format if changed
                    if value != org.email and not validators.email(value):
                        return jsonify({'error': 'Invalid email format'}), 400

                    # Check if email already exists in another record
                    existing_email = Organisation.query.filter_by(email=value).first()
                    if existing_email and existing_email.id != org.id:
                        return jsonify({'error': 'Email already in use'}), 400

                if key == 'password':
                    if len(value) < 8:
                        return jsonify({'error': 'Password too short'}), 400
                    value = bcrypt.generate_password_hash(value).decode('utf-8')

                setattr(org, key, value)

        db.session.commit()

        return jsonify({'message': 'Organisation updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Delete an organisation details

@organisation.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    try:
        organisation = Organisation.query.get(id)

        if not organisation:
            return jsonify({
                'error': 'This user does not exist!'
            }), HTTP_404_NOT_FOUND

        db.session.delete(organisation)
        db.session.commit()

        return jsonify({
            'message': 'The user has been successfully deleted',
        }), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR

















 










    




