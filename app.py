from flask import Flask, render_template, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
import password_hasher as ph
import re
import json
from isbnlib import meta
from isbnlib.registry import bibformatters
from urllib.request import urlopen

app = Flask(__name__)
app.secret_key = "secret_key"
hasher = ph.PasswordHasher()
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://sql10618972:fBNE8Pwvag@sql10.freesqldatabase.com/sql10618972"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class LoggedUsers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    pswd_hash = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
    user_hash = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    avatar = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    author = db.Column(db.String(5000))
    category = db.Column(db.String(5000))
    language = db.Column(db.String(1000))
    publisher = db.Column(db.String(5000))
    library_name = db.Column(db.String(50))
    library_email = db.Column(db.String(50))
    library_phone = db.Column(db.String(20))
    library_address = db.Column(db.String(150))
    library_url = db.Column(db.String(300))


class ResourcesLibrary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(30))
    title = db.Column(db.String(100))
    edition = db.Column(db.String(10))
    author = db.Column(db.String(100))
    category = db.Column(db.String(100))
    publisher = db.Column(db.String(200))
    language = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    book_cover = db.Column(db.String(300))


class MembersLibrary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(150))
    username = db.Column(db.String(50))
    avatar = db.Column(db.Integer)
    user_id = db.Column(db.Integer)


class BorrowRequests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    isbn = db.Column(db.String(30))
    member = db.Column(db.String(20))
    from_date = db.Column(db.String(20))
    to_date = db.Column(db.String(20))
    quantity = db.Column(db.Integer)
    status = db.Column(db.String(10))
    member_name = db.Column(db.String(100))
    item = db.Column(db.String(100))
    days = db.Column(db.Integer)
    renew_date = db.Column(db.String(10))


class AidedFuncs():
    def __init__(self):
        self.countries = ['''<option value="Afghanistan">Afghanistan</option>''', '''<option value="Åland Islands">Åland Islands</option>''', '''<option value="Albania">Albania</option>''', '''<option value="Algeria">Algeria</option>''', '''<option value="American Samoa">American Samoa</option>''', '''<option value="Andorra">Andorra</option>''', '''<option value="Angola">Angola</option>''', '''<option value="Anguilla">Anguilla</option>''', '''<option value="Antarctica">Antarctica</option>''', '''<option value="Antigua and Barbuda">Antigua and Barbuda</option>''', '''<option value="Argentina">Argentina</option>''', '''<option value="Armenia">Armenia</option>''', '''<option value="Aruba">Aruba</option>''', '''<option value="Australia">Australia</option>''', '''<option value="Austria">Austria</option>''', '''<option value="Azerbaijan">Azerbaijan</option>''', '''<option value="Bahamas">Bahamas</option>''', '''<option value="Bahrain">Bahrain</option>''', '''<option value="Bangladesh">Bangladesh</option>''', '''<option value="Barbados">Barbados</option>''', '''<option value="Belarus">Belarus</option>''', '''<option value="Belgium">Belgium</option>''', '''<option value="Belize">Belize</option>''', '''<option value="Benin">Benin</option>''', '''<option value="Bermuda">Bermuda</option>''', '''<option value="Bhutan">Bhutan</option>''', '''<option value="Bolivia">Bolivia</option>''', '''<option value="Bosnia and Herzegovina">Bosnia and Herzegovina</option>''', '''<option value="Botswana">Botswana</option>''', '''<option value="Bouvet Island">Bouvet Island</option>''', '''<option value="Brazil">Brazil</option>''', '''<option value="British Indian Ocean Territory">British Indian Ocean Territory</option>''', '''<option value="Brunei Darussalam">Brunei Darussalam</option>''', '''<option value="Bulgaria">Bulgaria</option>''', '''<option value="Burkina Faso">Burkina Faso</option>''', '''<option value="Burundi">Burundi</option>''', '''<option value="Cambodia">Cambodia</option>''', '''<option value="Cameroon">Cameroon</option>''', '''<option value="Canada">Canada</option>''', '''<option value="Cape Verde">Cape Verde</option>''', '''<option value="Cayman Islands">Cayman Islands</option>''', '''<option value="Central African Republic">Central African Republic</option>''', '''<option value="Chad">Chad</option>''', '''<option value="Chile">Chile</option>''', '''<option value="China">China</option>''', '''<option value="Christmas Island">Christmas Island</option>''', '''<option value="Cocos (Keeling) Islands">Cocos (Keeling) Islands</option>''', '''<option value="Colombia">Colombia</option>''', '''<option value="Comoros">Comoros</option>''', '''<option value="Congo">Congo</option>''', '''<option value="Congo, The Democratic Republic of The">Congo, The Democratic Republic of The</option>''', '''<option value="Cook Islands">Cook Islands</option>''', '''<option value="Costa Rica">Costa Rica</option>''', '''<option value="Cote D'ivoire">Cote D'ivoire</option>''', '''<option value="Croatia">Croatia</option>''', '''<option value="Cuba">Cuba</option>''', '''<option value="Cyprus">Cyprus</option>''', '''<option value="Czech Republic">Czech Republic</option>''', '''<option value="Denmark">Denmark</option>''', '''<option value="Djibouti">Djibouti</option>''', '''<option value="Dominica">Dominica</option>''', '''<option value="Dominican Republic">Dominican Republic</option>''', '''<option value="Ecuador">Ecuador</option>''', '''<option value="Egypt">Egypt</option>''', '''<option value="El Salvador">El Salvador</option>''', '''<option value="Equatorial Guinea">Equatorial Guinea</option>''', '''<option value="Eritrea">Eritrea</option>''', '''<option value="Estonia">Estonia</option>''', '''<option value="Ethiopia">Ethiopia</option>''', '''<option value="Falkland Islands (Malvinas)">Falkland Islands (Malvinas)</option>''', '''<option value="Faroe Islands">Faroe Islands</option>''', '''<option value="Fiji">Fiji</option>''', '''<option value="Finland">Finland</option>''', '''<option value="France">France</option>''', '''<option value="French Guiana">French Guiana</option>''', '''<option value="French Polynesia">French Polynesia</option>''', '''<option value="French Southern Territories">French Southern Territories</option>''', '''<option value="Gabon">Gabon</option>''', '''<option value="Gambia">Gambia</option>''', '''<option value="Georgia">Georgia</option>''', '''<option value="Germany">Germany</option>''', '''<option value="Ghana">Ghana</option>''', '''<option value="Gibraltar">Gibraltar</option>''', '''<option value="Greece">Greece</option>''', '''<option value="Greenland">Greenland</option>''', '''<option value="Grenada">Grenada</option>''', '''<option value="Guadeloupe">Guadeloupe</option>''', '''<option value="Guam">Guam</option>''', '''<option value="Guatemala">Guatemala</option>''', '''<option value="Guernsey">Guernsey</option>''', '''<option value="Guinea">Guinea</option>''', '''<option value="Guinea-bissau">Guinea-bissau</option>''', '''<option value="Guyana">Guyana</option>''', '''<option value="Haiti">Haiti</option>''', '''<option value="Heard Island and Mcdonald Islands">Heard Island and Mcdonald Islands</option>''', '''<option value="Holy See (Vatican City State)">Holy See (Vatican City State)</option>''', '''<option value="Honduras">Honduras</option>''', '''<option value="Hong Kong">Hong Kong</option>''', '''<option value="Hungary">Hungary</option>''', '''<option value="Iceland">Iceland</option>''', '''<option value="India">India</option>''', '''<option value="Indonesia">Indonesia</option>''', '''<option value="Iran, Islamic Republic of">Iran, Islamic Republic of</option>''', '''<option value="Iraq">Iraq</option>''', '''<option value="Ireland">Ireland</option>''', '''<option value="Isle of Man">Isle of Man</option>''', '''<option value="Israel">Israel</option>''', '''<option value="Italy">Italy</option>''', '''<option value="Jamaica">Jamaica</option>''', '''<option value="Japan">Japan</option>''', '''<option value="Jersey">Jersey</option>''', '''<option value="Jordan">Jordan</option>''', '''<option value="Kazakhstan">Kazakhstan</option>''', '''<option value="Kenya">Kenya</option>''', '''<option value="Kiribati">Kiribati</option>''', '''<option value="Korea, Democratic People's Republic of">Korea, Democratic People's Republic of</option>''', '''<option value="Korea, Republic of">Korea, Republic of</option>''', '''<option value="Kuwait">Kuwait</option>''', '''<option value="Kyrgyzstan">Kyrgyzstan</option>''', '''<option value="Lao People's Democratic Republic">Lao People's Democratic Republic</option>''', '''<option value="Latvia">Latvia</option>''', '''<option value="Lebanon">Lebanon</option>''', '''<option value="Lesotho">Lesotho</option>''', '''<option value="Liberia">Liberia</option>''', '''<option value="Libyan Arab Jamahiriya">Libyan Arab Jamahiriya</option>''', '''<option value="Liechtenstein">Liechtenstein</option>''', '''<option value="Lithuania">Lithuania</option>''', '''<option value="Luxembourg">Luxembourg</option>''', '''<option value="Macao">Macao</option>''', '''<option value="Macedonia, The Former Yugoslav Republic of">Macedonia, The Former Yugoslav Republic of
        </option>''', '''<option value="Madagascar">Madagascar</option>''', '''<option value="Malawi">Malawi</option>''', '''<option value="Malaysia">Malaysia</option>''', '''<option value="Maldives">Maldives</option>''', '''<option value="Mali">Mali</option>''', '''<option value="Malta">Malta</option>''', '''<option value="Marshall Islands">Marshall Islands</option>''', '''<option value="Martinique">Martinique</option>''', '''<option value="Mauritania">Mauritania</option>''', '''<option value="Mauritius">Mauritius</option>''', '''<option value="Mayotte">Mayotte</option>''', '''<option value="Mexico">Mexico</option>''', '''<option value="Micronesia, Federated States of">Micronesia, Federated States of</option>''', '''<option value="Moldova, Republic of">Moldova, Republic of</option>''', '''<option value="Monaco">Monaco</option>''', '''<option value="Mongolia">Mongolia</option>''', '''<option value="Montenegro">Montenegro</option>''', '''<option value="Montserrat">Montserrat</option>''', '''<option value="Morocco">Morocco</option>''', '''<option value="Mozambique">Mozambique</option>''', '''<option value="Myanmar">Myanmar</option>''', '''<option value="Namibia">Namibia</option>''', '''<option value="Nauru">Nauru</option>''', '''<option value="Nepal">Nepal</option>''', '''<option value="Netherlands">Netherlands</option>''', '''<option value="Netherlands Antilles">Netherlands Antilles</option>''', '''<option value="New Caledonia">New Caledonia</option>''', '''<option value="New Zealand">New Zealand</option>''', '''<option value="Nicaragua">Nicaragua</option>''', '''<option value="Niger">Niger</option>''', '''<option value="Nigeria">Nigeria</option>''', '''<option value="Niue">Niue</option>''', '''<option value="Norfolk Island">Norfolk Island</option>''', '''<option value="Northern Mariana Islands">Northern Mariana Islands</option>''', '''<option value="Norway">Norway</option>''', '''<option value="Oman">Oman</option>''', '''<option value="Pakistan">Pakistan</option>''', '''<option value="Palau">Palau</option>''', '''<option value="Palestinian Territory, Occupied">Palestinian Territory, Occupied</option>''', '''<option value="Panama">Panama</option>''', '''<option value="Papua New Guinea">Papua New Guinea</option>''', '''<option value="Paraguay">Paraguay</option>''', '''<option value="Peru">Peru</option>''', '''<option value="Philippines">Philippines</option>''', '''<option value="Pitcairn">Pitcairn</option>''', '''<option value="Poland">Poland</option>''', '''<option value="Portugal">Portugal</option>''', '''<option value="Puerto Rico">Puerto Rico</option>''', '''<option value="Qatar">Qatar</option>''', '''<option value="Reunion">Reunion</option>''', '''<option value="Romania">Romania</option>''', '''<option value="Russian Federation">Russian Federation</option>''', '''<option value="Rwanda">Rwanda</option>''', '''<option value="Saint Helena">Saint Helena</option>''', '''<option value="Saint Kitts and Nevis">Saint Kitts and Nevis</option>''', '''<option value="Saint Lucia">Saint Lucia</option>''', '''<option value="Saint Pierre and Miquelon">Saint Pierre and Miquelon</option>''', '''<option value="Saint Vincent and The Grenadines">Saint Vincent and The Grenadines</option>''', '''<option value="Samoa">Samoa</option>''', '''<option value="San Marino">San Marino</option>''', '''<option value="Sao Tome and Principe">Sao Tome and Principe</option>''', '''<option value="Saudi Arabia">Saudi Arabia</option>''', '''<option value="Senegal">Senegal</option>''', '''<option value="Serbia">Serbia</option>''', '''<option value="Seychelles">Seychelles</option>''', '''<option value="Sierra Leone">Sierra Leone</option>''', '''<option value="Singapore">Singapore</option>''', '''<option value="Slovakia">Slovakia</option>''', '''<option value="Slovenia">Slovenia</option>''', '''<option value="Solomon Islands">Solomon Islands</option>''', '''<option value="Somalia">Somalia</option>''', '''<option value="South Africa">South Africa</option>''', '''<option value="South Georgia and The South Sandwich Islands">South Georgia and The South Sandwich Islands
        </option>''', '''<option value="Spain">Spain</option>''', '''<option value="Sri Lanka">Sri Lanka</option>''', '''<option value="Sudan">Sudan</option>''', '''<option value="Suriname">Suriname</option>''', '''<option value="Svalbard and Jan Mayen">Svalbard and Jan Mayen</option>''', '''<option value="Swaziland">Swaziland</option>''', '''<option value="Sweden">Sweden</option>''', '''<option value="Switzerland">Switzerland</option>''', '''<option value="Syrian Arab Republic">Syrian Arab Republic</option>''', '''<option value="Taiwan">Taiwan</option>''', '''<option value="Tajikistan">Tajikistan</option>''', '''<option value="Tanzania, United Republic of">Tanzania, United Republic of</option>''', '''<option value="Thailand">Thailand</option>''', '''<option value="Timor-leste">Timor-leste</option>''', '''<option value="Togo">Togo</option>''', '''<option value="Tokelau">Tokelau</option>''', '''<option value="Tonga">Tonga</option>''', '''<option value="Trinidad and Tobago">Trinidad and Tobago</option>''', '''<option value="Tunisia">Tunisia</option>''', '''<option value="Turkey">Turkey</option>''', '''<option value="Turkmenistan">Turkmenistan</option>''', '''<option value="Turks and Caicos Islands">Turks and Caicos Islands</option>''', '''<option value="Tuvalu">Tuvalu</option>''', '''<option value="Uganda">Uganda</option>''', '''<option value="Ukraine">Ukraine</option>''', '''<option value="United Arab Emirates">United Arab Emirates</option>''', '''<option value="United Kingdom">United Kingdom</option>''', '''<option value="United States">United States</option>''', '''<option value="United States Minor Outlying Islands">United States Minor Outlying Islands</option>''', '''<option value="Uruguay">Uruguay</option>''', '''<option value="Uzbekistan">Uzbekistan</option>''', '''<option value="Vanuatu">Vanuatu</option>''', '''<option value="Venezuela">Venezuela</option>''', '''<option value="Viet Nam">Viet Nam</option>''', '''<option value="Virgin Islands, British">Virgin Islands, British</option>''', '''<option value="Virgin Islands, U.S.">Virgin Islands, U.S.</option>''', '''<option value="Wallis and Futuna">Wallis and Futuna</option>''', '''<option value="Western Sahara">Western Sahara</option>''', '''<option value="Yemen">Yemen</option>''', '''<option value="Zambia">Zambia</option>''', '''<option value="Zimbabwe">Zimbabwe</option>>''']

    def get_user(self):
        db.session.commit()
        userhash = request.cookies.get('logged_user')
        elem = LoggedUsers.query.filter_by(user_hash=userhash).first()
        user = {'id': elem.id, 'name': elem.name, 'email': elem.email, 'username': elem.username,
                'avatar': elem.avatar, 'phone': elem.phone, 'user_hash': elem.user_hash}
        library = {'author': elem.author.split(';'), 'category': elem.category.split(
            ';'), 'language': elem.language.split(';'), 'publisher': elem.publisher.split(';')}
        for i in library.keys():
            if "" in library[i]:
                library[i].remove("")
        library_offline = {'library_name': elem.library_name, 'library_email': elem.library_email,
                           'library_phone': elem.library_phone, 'library_address': elem.library_address.split(';'), 'library_url': elem.library_url}

        return [user, library, library_offline]

    def get_resources(self):
        db.session.commit()
        my_id = self.get_user()[0]['id']
        main_data = ResourcesLibrary.query.filter_by(user_id=my_id)
        data = []
        for i in range(len(list(main_data))):
            resource = main_data[i]
            data.append({'isbn': resource.isbn, 'title': resource.title, 'edition': resource.edition, 'author': resource.author, 'category': resource.category,
                        'publisher': resource.publisher, 'language': resource.language, 'quantity': resource.quantity, 'book_cover': resource.book_cover, 'id': resource.id})

        return data

    def get_members(self):
        db.session.commit()
        my_id = self.get_user()[0]['id']
        main_data = MembersLibrary.query.filter_by(user_id=my_id)
        data = []
        for i in range(len(list(main_data))):
            member = main_data[i]
            data.append({'name': member.name, 'phone': member.phone, 'email': member.email,
                        'address': member.address, 'username': member.username, 'avatar': member.avatar, 'id': member.id})

        return data

    def get_borrows(self):
        db.session.commit()
        my_id = self.get_user()[0]['id']
        main_data = BorrowRequests.query.filter_by(user_id=my_id)
        data = []
        for i in range(len(list(main_data))):
            borrowed = main_data[i]
            data.append({'isbn': borrowed.isbn, 'member': borrowed.member, 'from_date': borrowed.from_date, 'to_date': borrowed.to_date, 'quantity': borrowed.quantity, 'id': borrowed.id,
                        'user_id': borrowed.user_id, 'status': borrowed.status, 'member_name': borrowed.member_name, 'item': borrowed.item, 'days': borrowed.days, 'renew': borrowed.renew_date})

        return data


aids = AidedFuncs()


@app.route('/', methods=['GET', 'POST'])
def home():
    type = request.cookies.get('type')
    log_status = request.cookies.get('logged_info')
    if log_status == '1':
        return redirect("/dashboard")
    db.session.commit()

    error = 0
    message = ""
    if request.method == 'POST':
        if type == 'sign':
            email_sign = request.form['email-signup'].strip()
            name_sign = request.form['name-signup'].strip()
            username_sign = request.form['username-signup'].strip()
            password_sign = request.form['password-signup'].strip()
            confirm_pass_sign = request.form['confirm-pass-signup'].strip()

            uniques = LoggedUsers.query.all()
            unique_usernames = [
                uniques[i].username for i in range(len(uniques))]
            unique_emails = [uniques[i].email for i in range(len(uniques))]

            if len(username_sign) < 5:
                message = "Username too short"
                error = 1
            elif len(password_sign) < 8:
                message = "Password too short"
                error = 1
            elif username_sign in unique_usernames:
                message = "Already registered user"
                error = 1
            elif email_sign in unique_emails:
                message = "Already registered email"
                error = 1
            elif password_sign != confirm_pass_sign:
                message = "Password mismatch"
                error = 1
            else:
                for i in range(len(username_sign)):
                    char = username_sign[i]
                    if not (char.isalpha() or char.isdigit() or char == '_'):
                        print(
                            "Username should contain letters, digits and underscores only")
                        break
                    elif i+1 == len(username_sign):
                        data = LoggedUsers(username=username_sign, email=email_sign, pswd_hash=hasher.get_hash(password_sign), user_hash=hasher.get_hash(
                            username_sign), name=name_sign, avatar=0, phone="", author="", category="", language="", publisher="", library_name="", library_email="", library_phone="", library_address="", library_url="")
                        db.session.add(data)
                        db.session.commit()
                        return render_template('success_signup.html')

        elif type == 'log':
            username_email_log = request.form['username_email-login'].strip()
            password_log = request.form['password-login'].strip()

            uniques = LoggedUsers.query.all()
            pswd_hashes = [uniques[i].pswd_hash for i in range(len(uniques))]
            user_hashes = [uniques[i].user_hash for i in range(len(uniques))]
            proceed = False

            if '@' in username_email_log:
                email_log = username_email_log
                unique_emails = [uniques[i].email for i in range(len(uniques))]
                if email_log in unique_emails:
                    index = unique_emails.index(email_log)
                    proceed = True
            else:
                username_log = username_email_log
                unique_usernames = [
                    uniques[i].username for i in range(len(uniques))]
                if username_log in unique_usernames:
                    index = unique_usernames.index(username_log)
                    proceed = True
                else:
                    message = "Unregistered User"
                    error = 1

            if proceed:
                error = 0
                hash = pswd_hashes[index]
                user_hash = user_hashes[index]
                code = int(re.findall('\$(\d+)\$', hash)[0])
                if hash == hasher.get_hash(password_log, code):
                    return redirect(f'/set_cookie/{index}&{user_hash}')
                else:
                    message = "Wrong Password"
                    error = 1

    return render_template('home.html', message=message, error=error)


@app.route('/feed/<feed>')
def show_feed(feed):
    return render_template(f"{feed}.html")


@app.route('/dashboard')
def dashboard():
    return redirect('/dashboard/account')


@app.route('/set_cookie/<int:index>&<user_hash>')
def set_cookie(index, user_hash):
    resp = make_response(redirect('/dashboard/account'))
    resp.set_cookie('logged_user', user_hash,
                    expires=datetime.utcnow()+timedelta(weeks=200))
    resp.set_cookie('logged_id', str(index),
                    expires=datetime.utcnow()+timedelta(weeks=200))
    resp.set_cookie('logged_info', '1',
                    expires=datetime.utcnow()+timedelta(weeks=200))
    resp.set_cookie('type', '', expires='Thu, 01 Jan 1970 00:00:00 UTC')
    return resp


@app.route('/account/settings', methods=['GET', 'POST'])
def settings():
    user, library, library_offline = aids.get_user()
    if user == None:
        return render_template('cookie_mismatch.html')

    uniques = LoggedUsers.query.all()
    unique_usernames = [uniques[i].username for i in range(len(uniques))]
    unique_emails = [uniques[i].email for i in range(len(uniques))]

    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        avatar = request.form['avatar']

        if username in unique_usernames and username != user['username']:
            print('Username not available')
        elif email in unique_emails and email != user['email']:
            print('Email already registered')
        elif len(username) < 5:
            print("Username too short")
        else:
            for i in range(len(username)):
                char = username[i]
                if not (char.isalpha() or char.isdigit() or char == '_'):
                    print(
                        "Username should contain letters, digits and underscores only")
                    break
                elif i+1 == len(username):
                    resp = make_response(redirect('/dashboard'))
                    data = LoggedUsers.query.filter_by(id=user['id']).first()
                    data.name = name
                    if data.username != username:
                        data.username = username
                        data.user_hash = hasher.get_hash(username)
                    data.email = email
                    data.avatar = avatar
                    data.phone = phone
                    db.session.add(data)
                    db.session.commit()
                    resp.set_cookie('logged_user', data.user_hash, expires=datetime.utcnow(
                    )+timedelta(weeks=200), path="/")
                    return resp

    return render_template('settings.html', user=user)


@app.route('/account/logout')
def logout():
    return render_template('logout.html')


@app.route('/dashboard/<task>', methods=['GET', 'POST'])
def do_task(task):
    logged = request.cookies.get('logged_info')
    if logged != '1':
        return redirect('/')
    else:
        user, library, library_offline = aids.get_user()
        resources = aids.get_resources()
        members = aids.get_members()
        borrowed = aids.get_borrows()
        if user == None:
            return render_template('cookie_mismatch.html')

    if task == "add-resource":
        if request.method == 'POST':
            isbn = request.form['isbn']
            title = request.cookies.get('title')
            resp = make_response(redirect('/dashboard/add-resource'))
            resp.set_cookie(
                'title', '', expires='Thu, 01 Jan 1970 00:00:00 UTC')
            edition = request.form['edition']
            author = request.form['hidden-author-tag']
            category = request.form['hidden-category-tag']
            publisher = request.form['hidden-publisher-tag']
            language = request.form['hidden-language-tag']
            all_author = request.form['hid-author-options']
            all_category = request.form['hid-category-options']
            all_language = request.form['hid-language-options']
            all_publisher = request.form['hid-publisher-options']
            quantity = request.form['quantity']
            book_cover = request.form['book-cover-url']

            data = LoggedUsers.query.filter_by(id=user['id']).first()
            data.author = all_author
            data.category = all_category
            data.language = all_language
            data.publisher = all_publisher
            db.session.add(data)
            main_data = ResourcesLibrary(isbn=isbn, title=title, edition=edition, author=author, category=category,
                                         publisher=publisher, language=language, quantity=quantity, user_id=user['id'], book_cover=book_cover)
            db.session.add(main_data)
            db.session.commit()
            return resp

    elif task == "all-resource":
        if request.method == 'POST':
            deleted = request.form['deleted'].split(';')
            deleted.remove('')
            deleted = list(map(int, deleted))
            for i in range(len(resources)):
                data = ResourcesLibrary.query.filter_by(
                    user_id=user['id'], isbn=request.form[f'{i}-isbn']).first()
                if i in deleted:
                    db.session.delete(data)
                else:
                    data.author = request.form[f'{i}-author'].replace(
                        ', ', ';')+';'
                    data.publisher = request.form[f'{i}-publisher'].replace(
                        ', ', ';')+';'
                    data.category = request.form[f'{i}-category'].replace(
                        ', ', ';')+';'
                    data.language = request.form[f'{i}-language'].replace(
                        ', ', ';')+';'
                    data.edition = request.form[f'{i}-edition']
                    data.quantity = request.form[f'{i}-quantity']
                    db.session.add(data)

            db.session.commit()
            return redirect('/dashboard/all-resource')

    elif task == "library":
        if request.method == 'POST':
            name = request.form['name-lib'].replace(';', '')
            email = request.form['email-lib'].replace(';', '')
            phone = request.form['phone-lib'].replace(';', '')
            address_1 = request.form['address-1'].replace(';', '').strip()
            address_2 = request.form['address-2'].replace(';', '').strip()
            address_city = request.form['address-city'].replace(
                ';', '').strip()
            address_state = request.form['address-state'].replace(
                ';', '').strip()
            address_postal = str(
                request.form['address-postal']).replace(';', '').strip()
            address_country = request.form['address-country'].replace(';', '')
            web = request.form['web-lib'].replace(';', '')

            data = LoggedUsers.query.filter_by(id=user['id']).first()
            data.library_name = name
            data.library_email = email
            data.library_phone = phone
            adrs = ';'.join([address_1, address_2, address_city,
                            address_state, address_postal, address_country])
            if adrs == ";;;;;":
                adrs = ""
            data.library_address = adrs
            data.library_url = web
            db.session.add(data)
            db.session.commit()
            return redirect('/dashboard/library')

    elif task == "minor-settings":
        if request.method == 'POST':
            author = request.form['hid-author']
            publisher = request.form['hid-publisher']
            category = request.form['hid-category']
            language = request.form['hid-language']

            data = LoggedUsers.query.filter_by(id=user['id']).first()
            data.author = author
            data.publisher = publisher
            data.category = category
            data.language = language
            db.session.add(data)
            db.session.commit()
            return redirect('/dashboard/minor-settings')

    elif task == "add-member":
        if request.method == 'POST':
            name = request.form['name-member']
            username = request.form['username-member']
            email = request.form['email-member']
            phone = request.form['phone-member']
            address = ""
            for i in range(1, 7):
                x = request.form[f'address-{i}']
                if x.strip() != "":
                    address += x+', '
            address = address[:-2]
            avatar = request.form['avatar']

            data = MembersLibrary(name=name, phone=phone, email=email, address=address,
                                  username=username, avatar=avatar, user_id=user['id'])
            db.session.add(data)
            db.session.commit()
            return redirect('/dashboard/all-member')

    elif task == "all-member":
        if request.method == "POST":
            deleted = request.form['deleted'].split(';')[:-1]

            for i in range(len(members)):
                data = MembersLibrary.query.filter_by(
                    username=members[i]["username"], user_id=user['id']).first()
                if members[i]["username"] in deleted:
                    db.session.delete(data)

                try:
                    edited = json.loads(request.form['edited'][:-2]+"}")
                except:
                    pass
                else:
                    if members[i]["username"] in edited:
                        mem = members[i]["username"]
                        data.name = edited[mem][0]
                        data.email = edited[mem][1]
                        data.phone = edited[mem][2]
                        data.address = edited[mem][3]
                        data.avatar = edited[mem][4]
                        db.session.add(data)

            db.session.commit()
            return redirect("/dashboard/add-member")

    elif task == "borrow-request":
        if request.method == "POST":
            member = request.form['member-borrow']
            member_name = MembersLibrary.query.filter_by(
                username=member).first().name
            item = ResourcesLibrary.query.filter_by(isbn=isbn).first().title
            isbn = (request.form['real-isbn'])
            from_date = request.form['from-borrow']
            to_date = request.form['to-borrow']
            quantity = 1
            days = request.form['days-borrow']

            if len(borrowed):
                for i in range(len(borrowed)):
                    if isbn == borrowed[i]['isbn'] and member == borrowed[i]['member']:
                        data = BorrowRequests.query.filter_by(
                            user_id=user['id'], member=member, isbn=isbn).first()
                        data.quantity += 1
                        data.from_date = from_date
                        data.to_date = to_date
                        break
                    elif i == len(borrowed)-1:
                        data = BorrowRequests(
                            user_id=user['id'], isbn=isbn, from_date=from_date, to_date=to_date, member=member, quantity=quantity, status="pending", member_name=member_name, item=item, days=days)
            else:
                data = BorrowRequests(
                    user_id=user['id'], isbn=isbn, from_date=from_date, to_date=to_date, member=member, quantity=quantity, status="pending", member_name=member_name, item=item, days=days)

            db.session.add(data)
            db.session.commit()
            return redirect("/dashboard/borrow-request")

    return render_template(task+'.html', user=user, library=library, library_offline=library_offline, resources=resources, members=members, borrowed=borrowed, option_countries=aids.countries)


def isbn_decoder():
    SERVICE = "openl"
    isbn = request.cookies.get('isbn')
    bibtex = bibformatters["bibtex"]
    try:
        urlopen('https://www.google.com')
    except:
        return ""
    else:
        try:
            if not any(char.isalpha() for char in isbn):
                res = bibtex(meta(isbn, SERVICE))
                title = re.findall(
                    "title = {(.*)}", res)[0].replace(' and ', ", ")
                author = ', '.join(
                    set(re.findall("author = {(.*)}", res)[0].replace(' and ', ", ").split(', ')))
                year = re.findall(
                    "year = {(.*)}", res)[0].replace(' and ', ", ")
                publisher = re.findall(
                    "publisher = {(.*)}", res)[0].replace(' and ', ", ")
                isbn = re.findall("isbn = {(.*)}", res)[0]

                return [title, author, year, publisher, isbn]
            else:
                return ""
        except:
            return ""


@app.route('/run-decoder')
def sender():
    result = isbn_decoder()
    return result


@app.errorhandler(500)
def err500(e):
    return render_template('500.html', url=request.url)


@app.errorhandler(404)
def err400(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True, port=9932)


# A very important thing - error messages should be shown (right now only prints are made) yup
