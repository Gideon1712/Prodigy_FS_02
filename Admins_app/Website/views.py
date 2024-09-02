from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for, Flask
from flask_login import login_required, current_user
from .models import Note, User, UserProfile, db
import json
from datetime import datetime, timedelta

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("index.html", user=current_user)

countyData = {
    "United States": ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"],
    "Canada": ["Alberta", "British Columbia", "Manitoba", "New Brunswick", "Newfoundland and Labrador", "Nova Scotia", "Ontario", "Prince Edward Island", "Quebec", "Saskatchewan"],
    "Australia": ["New South Wales", "Queensland", "South Australia", "Tasmania", "Victoria", "Western Australia"],
    "India": ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"],
    "United Kingdom": ["Bedfordshire", "Berkshire", "Bristol", "Buckinghamshire", "Cambridgeshire", "Cheshire", "Cornwall", "Cumbria", "Derbyshire", "Devon", "Dorset", "Durham", "East Riding of Yorkshire", "East Sussex", "Essex", "Gloucestershire", "Greater London", "Greater Manchester", "Hampshire", "Herefordshire", "Hertfordshire", "Isle of Wight", "Kent", "Lancashire", "Leicestershire", "Lincolnshire", "Merseyside", "Norfolk", "North Yorkshire", "Northamptonshire", "Northumberland", "Nottinghamshire", "Oxfordshire", "Rutland", "Shropshire", "Somerset", "South Yorkshire", "Staffordshire", "Suffolk", "Surrey", "Tyne and Wear", "Warwickshire", "West Midlands", "West Sussex", "West Yorkshire", "Wiltshire", "Worcestershire"]
}

cityData = {
    "Bedfordshire": ["Bedford", "Luton", "Dunstable", "Leighton Buzzard"],
    "Berkshire": ["Reading", "Slough", "Windsor", "Maidenhead", "Bracknell"],
    "Bristol": ["Bristol"],
    "Buckinghamshire": ["Milton Keynes", "Aylesbury", "High Wycombe", "Amersham"],
    "Cambridgeshire": ["Cambridge", "Peterborough", "Ely", "Huntingdon"],
    "Cheshire": ["Chester", "Warrington", "Crewe", "Macclesfield"],
    "Cornwall": ["Truro", "Falmouth", "Penzance", "Newquay"],
    "Cumbria": ["Carlisle", "Kendal", "Barrow-in-Furness", "Whitehaven"],
    "Derbyshire": ["Derby", "Chesterfield", "Buxton", "Matlock"],
    "Devon": ["Exeter", "Plymouth", "Torquay", "Barnstaple"],
    "Dorset": ["Dorchester", "Bournemouth", "Poole", "Weymouth"],
    "Durham": ["Durham", "Darlington", "Stockton-on-Tees", "Hartlepool"],
    "East Riding of Yorkshire": ["Hull", "Beverley", "Bridlington", "Goole"],
    "East Sussex": ["Brighton", "Hastings", "Eastbourne", "Lewes"],
    "Essex": ["Chelmsford", "Colchester", "Southend-on-Sea", "Basildon"],
    "Gloucestershire": ["Gloucester", "Cheltenham", "Stroud", "Cirencester"],
    "Greater London": ["London"],
    "Greater Manchester": ["Manchester", "Salford", "Stockport", "Bolton", "Oldham"],
    "Hampshire": ["Winchester", "Southampton", "Portsmouth", "Basingstoke"],
    "Herefordshire": ["Hereford", "Leominster", "Ross-on-Wye", "Ledbury"],
    "Hertfordshire": ["Hertford", "St Albans", "Watford", "Stevenage"],
    "Isle of Wight": ["Newport", "Ryde", "Cowes", "Sandown"],
    "Kent": ["Maidstone", "Canterbury", "Dover", "Tonbridge", "Tunbridge Wells"],
    "Lancashire": ["Lancaster", "Preston", "Blackpool", "Burnley"],
    "Leicestershire": ["Leicester", "Loughborough", "Hinckley", "Melton Mowbray"],
    "Lincolnshire": ["Lincoln", "Grimsby", "Scunthorpe", "Boston"],
    "Merseyside": ["Liverpool", "Birkenhead", "St Helens", "Southport"],
    "Norfolk": ["Norwich", "King's Lynn", "Great Yarmouth", "Thetford"],
    "North Yorkshire": ["York", "Harrogate", "Scarborough", "Northallerton"],
    "Northamptonshire": ["Northampton", "Kettering", "Corby", "Wellingborough"],
    "Northumberland": ["Morpeth", "Berwick-upon-Tweed", "Hexham", "Alnwick"],
    "Nottinghamshire": ["Nottingham", "Mansfield", "Worksop", "Newark-on-Trent"],
    "Oxfordshire": ["Oxford", "Banbury", "Bicester", "Witney"],
    "Rutland": ["Oakham", "Uppingham"],
    "Shropshire": ["Shrewsbury", "Telford", "Ludlow", "Oswestry"],
    "Somerset": ["Taunton", "Bath", "Weston-super-Mare", "Yeovil"],
    "South Yorkshire": ["Sheffield", "Barnsley", "Doncaster", "Rotherham"],
    "Staffordshire": ["Stafford", "Stoke-on-Trent", "Lichfield", "Burton upon Trent"],
    "Suffolk": ["Ipswich", "Bury St Edmunds", "Lowestoft", "Sudbury"],
    "Surrey": ["Guildford", "Woking", "Epsom", "Farnham"],
    "Tyne and Wear": ["Newcastle upon Tyne", "Sunderland", "Gateshead", "South Shields"],
    "Warwickshire": ["Warwick", "Coventry", "Stratford-upon-Avon", "Nuneaton"],
    "West Midlands": ["Birmingham", "Wolverhampton", "Solihull", "Dudley"],
    "West Sussex": ["Chichester", "Crawley", "Worthing", "Horsham"],
    "West Yorkshire": ["Leeds", "Bradford", "Wakefield", "Huddersfield"],
    "Wiltshire": ["Salisbury", "Swindon", "Chippenham", "Trowbridge"],
    "Worcestershire": ["Worcester", "Redditch", "Kidderminster", "Malvern"]
}


@views.route('/create_profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        user_id = request.form.get('userId')  # Get user ID from form
        if not profile:
            profile = UserProfile(user_id=user_id)  # Use provided user ID
            db.session.add(profile)
        profile.user_id = user_id  # Update user ID
        profile.job_type = request.form.get('jobType')  # Get Job Type from form
        profile.salary = request.form.get('salary')  # Get Salary from form
        profile.title = request.form.get('title')
        profile.first_name = request.form.get('firstName')
        profile.surname = request.form.get('surname')
        dob_str = request.form.get('dob')
        if dob_str:
            profile.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        profile.address1 = request.form.get('address1')
        profile.address2 = request.form.get('address2')
        profile.postcode = request.form.get('postcode')
        profile.county = request.form.get('county')
        profile.country = request.form.get('country')
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('views.create_profile_confirmation'))

    return render_template('create_profile.html', profile=profile, countyData=countyData)

@views.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    # Handle updating an existing profile
    user_id = request.form.get('userId')
    profile = UserProfile.query.filter_by(user_id=user_id).first()

    if profile:
        # Update the profile fields
        profile.job_type = request.form.get('jobType')
        profile.salary = request.form.get('salary')
        profile.title = request.form.get('title')
        profile.first_name = request.form.get('firstName')
        profile.surname = request.form.get('surname')
        dob_str = request.form.get('dob')
        if dob_str:
            profile.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        profile.address1 = request.form.get('address1')
        profile.address2 = request.form.get('address2')
        profile.postcode = request.form.get('postcode')
        profile.county = request.form.get('county')
        profile.country = request.form.get('country')

        # Commit the changes to the database
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('views.create_profile_confirmation'))
    else:
        flash('Profile not found.', 'danger')
        return redirect(url_for('views.create_profile'))

@views.route('/create_profile_confirmation')
@login_required
def create_profile_confirmation():
    profile = UserProfile.query.filter_by(user_id=current_user.id).first()  # Fetch profile to display user ID
    return render_template('create_profile_confirmation.html', profile=profile)

@views.route('/read', methods=['GET'])
@login_required
def read_employee():
    employee_id = request.args.get('employeeId')
    employee = None
    searched = False

    if employee_id:
        searched = True
        employee = UserProfile.query.filter_by(user_id=employee_id).first()

    return render_template('read.html', employee=employee, searched=searched)


@views.route('/delete', methods=['GET', 'POST'])
@login_required
def delete_profile():
    if request.method == 'POST':
        employee_id = request.form.get('employeeId')
        
        # Fetch the employee profile by ID
        profile = UserProfile.query.filter_by(user_id=employee_id).first()

        if profile:
            # Optionally, delete related records first (if not using cascading deletes)
            # Example: Delete notes associated with the user
            notes = Note.query.filter_by(user_id=employee_id).all()
            for note in notes:
                db.session.delete(note)

            # Now, delete the profile itself
            db.session.delete(profile)
            db.session.commit()
            flash('Employee profile and related information deleted successfully!', 'success')
        else:
            flash('Employee profile not found.', 'danger')

        return redirect(url_for('views.create_profile_confirmation'))

    # Render delete.html for GET requests
    return render_template('delete.html')


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
