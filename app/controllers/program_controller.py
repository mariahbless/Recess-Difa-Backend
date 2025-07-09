from app.extension import db
from app.models.organisation_model import Organisation
from app.models.program_model import Program
from flask import Blueprint,request,jsonify
from app.status_code import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_409_CONFLICT
# import validators

#Creating a new student

# Define the bluerints
program = Blueprint('program',__name__,url_prefix='/api/v1/program')

# Define the route
@program.route('/create_program', methods = ['POST'])
def create_program():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    duration = data.get('duration')
    outcome = data.get('outcome')
    #program_id = data.get('program_id')
    #program = Program.query.get(program_id)

    # Verification of the details
    if not name or not description or not duration or not outcome  :
        return jsonify({
            'error':'All fields are required!'
        }),HTTP_400_BAD_REQUEST
    
    
    # Registering the new student
    try:
         new_program = Program(name=name,description=description,duration=duration,outcome=outcome)

         # Adding the new data to the database
         db.session.add(new_program)
         db.session.commit()

         # The return message
         return jsonify({
              'message': new_program.name + '' 'has successfully been created as student',
              'name': new_program.name,
              'description': new_program.description,
              'duration': new_program.duration,
              'outcome' : new_program.outcome
             # 'program_id': new_student.program_id
         }),HTTP_200_OK

    except Exception as e:
         return jsonify({
              'error': str(e)
         }),HTTP_500_INTERNAL_SERVER_ERROR






#  Getting all stdents
@program.route('/get', methods = ['GET'])
def get_all_program():
     all_programs = Program.query.all()
     programs_data = []

     for program in all_programs:
          program_information = {
              'name': program.name,
              'description': program.description,
              'duration': program.duration,
              'outcome': program.outcome,
              
        
          }

          programs_data.append(program_information)

          # The return message

     return jsonify({
              'message': 'All programs have successfully been retrieved',
              'Total': len(programs_data),
              'programs': programs_data
             
         }),HTTP_200_OK





# (e) Delete a student
@program.route('/delete/<int:id>', methods = ['DELETE'])
def delete_program(id):
     try:
          program = Program.query.filter_by(id = id).first()
          if not program:
            return jsonify({
                'error': 'This program does not exist!'
            }),HTTP_404_NOT_FOUND
          
          else:
               db.session.delete(program)
               db.session.commit()
          
          # The return message
               return jsonify({
                    'message': 'The program has been successifully deleted',    
                }),HTTP_200_OK

          

     except Exception as e:
          return jsonify({
               'error': str(e)
          }),HTTP_500_INTERNAL_SERVER_ERROR



