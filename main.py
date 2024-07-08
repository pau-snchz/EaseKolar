from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from sqlalchemy import text
import pymysql

# App configuration
app = Flask(__name__)
app.secret_key = "secretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Mariella123@localhost/easekolar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database initialization
db = SQLAlchemy(app)

# Login manager setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Admin credentials
ADMIN_EMAIL = "admin"
ADMIN_PASSWORD_HASH = generate_password_hash("admin")

# Database models
class Applicant(db.Model):
    __tablename__ = 'applicants'
    Applicant_ID = db.Column(db.String(20), primary_key=True)
    Applicant_Name = db.Column(db.String(100), nullable=False)
    GradeLvlApplied = db.Column(db.Integer, nullable=False)
    Citizenship = db.Column(db.String(20), nullable=False)
    Sex = db.Column(db.String(2), nullable=False)
    Birthdate = db.Column(db.Date, nullable=False)
    Birthplace = db.Column(db.String(50), nullable=False)
    PermanentAddress = db.Column(db.String(120), nullable=False)
    MailingAddress = db.Column(db.String(120))
    StudentLandlineNo = db.Column(db.String(8))
    StudentPhoneNo = db.Column(db.String(12), nullable=False)
    StudentEmail = db.Column(db.String(50), nullable=False)
    EmergencyContactName = db.Column(db.String(40), nullable=False)
    EmergencyContactPhoneNo = db.Column(db.String(15), nullable=False)
    School_ID = db.Column(db.String(12), db.ForeignKey('schools.School_ID'), nullable=False)
    __table_args__ = (
        db.UniqueConstraint('Applicant_Name', 'Birthdate', 'StudentEmail', name='unique_applicant'),
    )

    @staticmethod
    def generate_id():
        last_record = Applicant.query.order_by(Applicant.Applicant_ID.desc()).first()
        if last_record:
            last_id = int(last_record.Applicant_ID[3:])  # Skip the 'APP' prefix
            new_id = f"APP{last_id + 1:06d}"
        else:
            new_id = "APP000001"
        return new_id

class School(db.Model):
    __tablename__ = 'schools'
    School_ID = db.Column(db.String(20), primary_key=True)
    SchoolName = db.Column(db.String(50), nullable=False)
    SchoolType = db.Column(db.String(2), nullable=False)
    SchoolAddress = db.Column(db.String(120), nullable=False)
    SchoolEmail = db.Column(db.String(30), nullable=False)
    SchoolPhoneNo = db.Column(db.String(15), nullable=False)
    __table_args__ = (
        db.UniqueConstraint('SchoolName', 'SchoolEmail', name='unique_school'),
    )
    @staticmethod
    def generate_id():
        last_record = School.query.order_by(School.School_ID.desc()).first()
        if last_record:
            last_id = int(last_record.School_ID[3:])  # Skip the 'SCH' prefix
            new_id = f"SCH{last_id + 1:06d}"
        else:
            new_id = "SCH000001"
        return new_id


class Parent(db.Model):
    __tablename__ = 'parents'
    Applicant_ID = db.Column(db.String(20), db.ForeignKey('applicants.Applicant_ID'), nullable=False)
    Parent_ID = db.Column(db.String(20), primary_key=True)
    ParentType = db.Column(db.String(2), nullable=False)
    PrName = db.Column(db.String(50), nullable=False)
    PrContactNo = db.Column(db.String(12), nullable=False)
    PrEmail = db.Column(db.String(30), nullable=False)
    PrNatureOfWork = db.Column(db.String(2))
    PrOccupation = db.Column(db.String(50))
    PrCompanyName = db.Column(db.String(50))
    PrCompanyAddress = db.Column(db.String(120))
    PrGrossAnnualIncome = db.Column(db.Numeric(10, 2))
    PrHighestEducAttainment = db.Column(db.String(30))
    PrSchoolGradFrom = db.Column(db.String(50))
    PrYearGraduated = db.Column(db.String(10))

    __table_args__ = (
        db.UniqueConstraint('Applicant_ID', 'ParentType', 'PrName', 'PrEmail', name='unique_parent'),
    )

    @staticmethod
    def generate_id():
        last_record = Parent.query.order_by(Parent.Parent_ID.desc()).first()
        if last_record:
            last_id = int(last_record.Parent_ID[3:])  # Assuming 'PAR000001' format
            new_id = f"PAR{last_id + 1:06d}"
        else:
            new_id = "PAR000001"
        return new_id

class SiblingNLS(db.Model):
    __tablename__ = 'siblings_nls'
    Applicant_ID = db.Column(db.String(20), db.ForeignKey('applicants.Applicant_ID'), nullable=False)
    SiblingNLS_ID = db.Column(db.String(20), primary_key=True)
    SbName_NLS = db.Column(db.String(40), nullable=False)
    SbAge_NLS = db.Column(db.Integer, nullable=False)
    SbCivilStatus_NLS = db.Column(db.String(1), nullable=False)
    SbHighestEducAttainment = db.Column(db.String(30), nullable=False)
    SbNatureOfWork = db.Column(db.String(2), nullable=False)
    SbCompany = db.Column(db.String(50), nullable=False)
    SbGrossAnnualIncome = db.Column(db.Numeric(10, 2), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('Applicant_ID', 'SbName_NLS', 'SbAge_NLS', name='unique_sibling_nls'),
    )

    @staticmethod
    def generate_id():
        last_record = SiblingNLS.query.order_by(SiblingNLS.SiblingNLS_ID.desc()).first()
        if last_record:
            last_id = int(last_record.SiblingNLS_ID[3:])  # Skip the 'NLS' prefix
            new_id = f"NLS{last_id + 1:06d}"
        else:
            new_id = "NLS000001"
        return new_id
    
class SiblingSS(db.Model):
    __tablename__ = 'siblings_ss'
    Applicant_ID = db.Column(db.String(20), db.ForeignKey('applicants.Applicant_ID'), nullable=False)
    SiblingSS_ID = db.Column(db.String(20), primary_key=True)
    SbName_SS = db.Column(db.String(40), nullable=False)
    SbAge_SS = db.Column(db.Integer, nullable=False)
    SbCivilStatus_SS = db.Column(db.String(1), nullable=False)
    SbYearLevel = db.Column(db.String(30), nullable=False)
    SbSchoolName = db.Column(db.String(50), nullable=False)
    SbAnnualTuition = db.Column(db.Numeric(8, 2), nullable=True)
    SbTuitionPaidBy = db.Column(db.String(30), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('Applicant_ID', 'SbName_SS', 'SbAge_SS', name='unique_sibling_ss'),
    )

    @staticmethod
    def generate_id():
        last_record = SiblingSS.query.order_by(SiblingSS.SiblingSS_ID.desc()).first()
        if last_record:
            last_id = int(last_record.SiblingSS_ID[2:])  # Skip the 'SS' prefix
            new_id = f"SS{last_id + 1:06d}"
        else:
            new_id = "SS000001"
        return new_id


class Admin(UserMixin):
    id = "admin"

@login_manager.user_loader
def load_user(user_id):
    if user_id == "admin":
        return Admin()
    return Applicant.query.get(user_id)


# Define SQL queries as SQLAlchemy text objects or strings
SQL_QUERIES = {
    'easy1': "SELECT * FROM easekolar.applicants WHERE GradeLvlApplied IN (7,8,9,10) ORDER BY GradeLvlApplied;",
    'easy2': "SELECT * FROM easekolar.applicants WHERE GradeLvlApplied IN (11,12) ORDER BY GradeLvlApplied DESC;",
    'easy3': "SELECT Applicant_ID FROM easekolar.parents WHERE PrNatureOfWork = 'NA';",
    'moderate1': "SELECT GradeLvlApplied, COUNT(*) as 'Number of Applicants' FROM easekolar.applicants GROUP BY GradeLvlApplied ORDER BY GradeLvlApplied;",
    'moderate2': "SELECT School_ID, COUNT(*) as 'Number of Applicants' FROM easekolar.applicants GROUP BY School_ID;",
    'moderate3': "SELECT Applicant_ID, COUNT(*) as 'Number of Siblings Still Studying' FROM easekolar.siblings_ss GROUP BY Applicant_ID;",
    'moderate4': "SELECT Applicant_ID, SUM(PrGrossAnnualIncome) as 'Parents Total Annual Income' FROM easekolar.parents GROUP BY Applicant_ID HAVING SUM(PrGrossAnnualIncome) < 900000;",
    'difficult1': "SELECT A.Applicant_ID, A.Applicant_Name, S.SchoolName FROM easekolar.applicants A, easekolar.schools S WHERE A.School_ID = S.School_ID AND (S.SchoolName LIKE '%Science%' OR S.SchoolType = 'Pb');",
    'difficult2': "SELECT A.Applicant_ID, A.Applicant_Name, COUNT(Sibling.Applicant_ID) AS 'Number of Siblings' FROM easekolar.applicants A LEFT JOIN (SELECT Applicant_ID FROM easekolar.siblings_nls UNION ALL SELECT Applicant_ID FROM easekolar.siblings_ss) Sibling ON A.Applicant_ID = Sibling.Applicant_ID GROUP BY A.Applicant_ID, A.Applicant_Name;",
    'difficult3': "SELECT A.Applicant_ID, A.Applicant_Name, S.SchoolName, SUM(P.PrGrossAnnualIncome) as 'Parents Total Annual Income' FROM easekolar.applicants A, easekolar.schools S, easekolar.parents P WHERE A.Applicant_ID = P.Applicant_ID AND A.School_ID = S.School_ID AND (S.SchoolType = 'Pb' OR S.SchoolName LIKE '%Science%') GROUP BY Applicant_ID HAVING SUM(P.PrGrossAnnualIncome) <= 900000 ORDER BY SUM(P.PrGrossAnnualIncome);",
}

# Routes
@app.route('/dbconnect')
def dbconnect():
    try:
        db.session.query(Applicant).first()
        return 'Database connected successfully!'
    except Exception as e:
        return f'Database connection failed. Error: {str(e)}'


@app.route('/static/home.html')
@app.route('/home.html')
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/admin', methods=['GET', 'POST'])
@app.route('/static/admin-page/admin.html', methods=['GET', 'POST'])
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        admin_id = request.form.get('admin-ID')
        admin_pass = request.form.get('admin-pass')
        if admin_id == ADMIN_EMAIL and check_password_hash(ADMIN_PASSWORD_HASH, admin_pass):
            login_user(Admin())
            return redirect(url_for('show_database'))
        flash('Invalid credentials')
    return render_template('/admin.html')


# Route to display database tables
@app.route('/database')
def show_database():
    applicants = Applicant.query.all()  
    parents = Parent.query.all()        
    schools = School.query.all()        
    siblings_nls = SiblingNLS.query.all()  
    siblings_ss = SiblingSS.query.all()  

    return render_template('database.html', applicants=applicants, parents=parents,
                           schools=schools, siblings_nls=siblings_nls, siblings_ss=siblings_ss)

@app.route('/update_record/<table>/<record_id>', methods=['POST'])
def update_record(table, record_id):
    # Assuming you have SQLAlchemy models defined, adjust the code accordingly
    if table == 'applicants':
        record = Applicant.query.get(record_id)
    elif table == 'parents':
        record = Parent.query.get(record_id)
    elif table == 'schools':
        record = School.query.get(record_id)
    # Add similar conditions for other tables (siblings_nls, siblings_ss) if needed

    if not record:
        return jsonify({'success': False, 'error': f'Record with ID {record_id} not found.'}), 404

    try:
        # Update record fields based on the data received in the POST request
        data = request.json
        for key, value in data.items():
            setattr(record, key, value)
        
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.session.close()


@app.route('/delete_record/<table>/<record_id>', methods=['DELETE'])
def delete_record(table, record_id):
    try:
        if table == 'applicants':
            record_to_delete = Applicant.query.get(record_id)
        elif table == 'parents':
            record_to_delete = Parent.query.get(record_id)
        elif table == 'siblings_nls':
            record_to_delete = SiblingNLS.query.get(record_id)
        elif table == 'siblings_ss':
            record_to_delete = SiblingSS.query.get(record_id)
        elif table == 'schools':
            record_to_delete = School.query.get(record_id)
        else:
            return jsonify({'success': False, 'error': 'Invalid table name'})

        db.session.delete(record_to_delete)
        db.session.commit()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Route to execute SQL queries
@app.route('/execute-query', methods=['POST'])
def execute_query():
    try:
        data = request.json
        query_key = data.get('query_name')  # Ensure correct variable name

        # Ensure the query key exists in SQL_QUERIES
        if query_key in SQL_QUERIES:
            query = SQL_QUERIES[query_key]

            # Connect to MySQL database
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Mariella123',
                database='easekolar',
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = conn.cursor()

            # Execute the SQL query
            cursor.execute(query)
            results = cursor.fetchall()

            cursor.close()
            conn.close()

            return jsonify({'success': True, 'data': results})  # Return JSON response

        else:
            return jsonify({'success': False, 'error': f'Query {query_key} not found'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/AppForm', methods=['GET', 'POST'])
def AppForm():
    if request.method == 'POST':
        try:
            # Check if school already exists
            existing_school = School.query.filter_by(
                SchoolName=request.form['school-grad-from'],
                SchoolEmail=request.form['school-email']
            ).first()

            if existing_school:
                school = existing_school
            else:
                school_data = {
                    'School_ID': School.generate_id(),
                    'SchoolName': request.form['school-grad-from'],
                    'SchoolType': request.form['school-type'],
                    'SchoolAddress': request.form['school-address'],
                    'SchoolEmail': request.form['school-email'],
                    'SchoolPhoneNo': request.form['school-contact-num']
                }
                school = School(**school_data)
                db.session.add(school)
                db.session.flush()

            # Check if applicant already exists
            existing_applicant = Applicant.query.filter_by(
                Applicant_Name=request.form['applicant-name'],
                Birthdate=datetime.datetime.strptime(request.form['birthdate'], '%Y-%m-%d').date(),
                StudentEmail=request.form['email-address']
            ).first()

            if existing_applicant:
                flash('An application with this name, birthdate, and email already exists.')
                return render_template('apply-form.html')

            # Process applicant data
            applicant_data = {
                'Applicant_ID': Applicant.generate_id(),
                'Applicant_Name': request.form['applicant-name'],
                'GradeLvlApplied': request.form['grade-lvl'],
                'Citizenship': request.form['citizenship'],
                'Sex': request.form['sex'],
                'Birthdate': datetime.datetime.strptime(request.form['birthdate'], '%Y-%m-%d').date(),
                'Birthplace': request.form['birthplace'],
                'PermanentAddress': request.form['permanent-address'],
                'MailingAddress': request.form.get('mailing-address', ''),
                'StudentLandlineNo': request.form.get('landline-num', ''),
                'StudentPhoneNo': request.form['phone-num'],
                'StudentEmail': request.form['email-address'],
                'EmergencyContactName': request.form['emergency-contact-name'],
                'EmergencyContactPhoneNo': request.form['emergency-contact-num'],
                'School_ID': school.School_ID
            }
            new_applicant = Applicant(**applicant_data)
            db.session.add(new_applicant)
            db.session.flush()

            # Process parent data
            if not process_parent_data(new_applicant.Applicant_ID):
                db.session.rollback()
                flash('A parent with the same information already exists.')
                return render_template('apply-form.html')

            # Process sibling data
            if not process_sibling_data(new_applicant.Applicant_ID):
                db.session.rollback()
                flash('A sibling with the same information already exists.')
                return render_template('apply-form.html')

            db.session.commit()
            flash('Application submitted successfully')
            return render_template('home.html')

        except Exception as e:
            db.session.rollback()
            print(f"Detailed error: {e}")
            return jsonify({'success': False, 'message': f'Error submitting application: {str(e)}'})

    return render_template('apply-form.html')

def process_parent_data(applicant_id):
    parent_count = len(request.form.getlist('parentguardian-name[]'))
    for i in range(parent_count):
        parent_data = {
            'Parent_ID': Parent.generate_id(),  # 'PAR000001
            'Applicant_ID': applicant_id,
            'ParentType': request.form.getlist(f'parent-type-{i}')[0],
            'PrName': request.form.getlist('parentguardian-name[]')[i],
            'PrContactNo': request.form.getlist('pg-phone-num[]')[i],
            'PrEmail': request.form.getlist('pg-email-address[]')[i],
            'PrOccupation': request.form.getlist('occupation[]')[i],
            'PrCompanyName': request.form.getlist('company-name[]')[i],
            'PrCompanyAddress': request.form.getlist('company-address[]')[i],
            'PrNatureOfWork': request.form.getlist(f'nature-of-work-{i}')[0],
            'PrGrossAnnualIncome': float(request.form.getlist('gross-annual-income[]')[i] or 0),
            'PrHighestEducAttainment': request.form.getlist('highest-educational-attainment[]')[i],
            'PrSchoolGradFrom': request.form.getlist('school-graduated-from[]')[i],
            'PrYearGraduated': request.form.getlist('pg-year-graduated[]')[i]
        }
        existing_parent = Parent.query.filter_by(
            Applicant_ID=applicant_id,
            ParentType=parent_data['ParentType'],
            PrName=parent_data['PrName'],
            PrEmail=parent_data['PrEmail']
        ).first()
        if existing_parent:
            # Update existing parent info if needed
            for key, value in parent_data.items():
                setattr(existing_parent, key, value)
        else:
            new_parent = Parent(**parent_data)
            db.session.add(new_parent)
    return True

def process_sibling_data(applicant_id):
    # Process siblings no longer studying (NLS)
    for key in request.form:
        if key.startswith('sibling-nls-name['):
            index = key[len('sibling-nls-name['):-1]
            sibling_nls_data = {
                'SiblingNLS_ID': SiblingNLS.generate_id(),  # 'NLS000001
                'Applicant_ID': applicant_id,
                'SbName_NLS': request.form.get(f'sibling-nls-name[{index}]'),
                'SbAge_NLS': int(request.form.get(f'sibling-nls-age[{index}]') or 0),
                'SbCivilStatus_NLS': request.form.get(f'sibling-nls-civilstatus-{index}'),
                'SbHighestEducAttainment': request.form.get(f'sibling-nls-highesteducationalattainment[{index}]'),
                'SbCompany': request.form.get(f'sibling-nls-companyname[{index}]'),
                'SbNatureOfWork': request.form.get(f'sibling-nls-natureofwork-{index}'),
                'SbGrossAnnualIncome': float(request.form.get(f'sibling-nls-grossannualincome[{index}]') or 0)
            }
            existing_sibling_nls = SiblingNLS.query.filter_by(
                Applicant_ID=applicant_id,
                SbName_NLS=sibling_nls_data['SbName_NLS'],
                SbAge_NLS=sibling_nls_data['SbAge_NLS']
            ).first()
            if existing_sibling_nls:
                # Update existing sibling info if needed
                for key, value in sibling_nls_data.items():
                    setattr(existing_sibling_nls, key, value)
            else:
                sibling_nls = SiblingNLS(**sibling_nls_data)
                db.session.add(sibling_nls)

    # Process siblings still studying (SS)
    for key in request.form:
        if key.startswith('sibling-ss-name['):
            index = key[len('sibling-ss-name['):-1]
            sibling_ss_data = {
                'SiblingSS_ID': SiblingSS.generate_id(),  # 'SS000001
                'Applicant_ID': applicant_id,
                'SbName_SS': request.form.get(f'sibling-ss-name[{index}]'),
                'SbAge_SS': int(request.form.get(f'sibling-ss-age[{index}]') or 0),
                'SbCivilStatus_SS': request.form.get(f'sibling-ss-civilstatus-{index}'),
                'SbYearLevel': request.form.get(f'sibling-ss-yearlvl[{index}]'),
                'SbSchoolName': request.form.get(f'sibling-ss-schoolname[{index}]'),
                'SbAnnualTuition': float(request.form.get(f'sibling-ss-annualtuition[{index}]') or 0),
                'SbTuitionPaidBy': request.form.get(f'sibling-ss-tuitionpaidby[{index}]')
            }
            existing_sibling_ss = SiblingSS.query.filter_by(
                Applicant_ID=applicant_id,
                SbName_SS=sibling_ss_data['SbName_SS'],
                SbAge_SS=sibling_ss_data['SbAge_SS']
            ).first()
            if existing_sibling_ss:
                # Update existing sibling info if needed
                for key, value in sibling_ss_data.items():
                    setattr(existing_sibling_ss, key, value)
            else:
                sibling_ss = SiblingSS(**sibling_ss_data)
                db.session.add(sibling_ss)

    return True
if __name__ == '__main__':
     app.run(debug=True)