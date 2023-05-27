#  initializing all the necessary libraries
from flask import Flask 
from datetime import timedelta,datetime
import random ,json
from hashlib import sha512
from sys import platform
import pandas as pd
import os,shutil,random
from dotenv import load_dotenv
from flask import render_template ,request,redirect,url_for,session
# initializing environment variables
load_dotenv()

# app initialization with flask and seting up secret key
app = Flask(__name__)
SECRET_key = os.environ.get("SECRET_KEY")
app.secret_key = SECRET_key
app.permanent_session_lifetime = timedelta(days=10)

# declaration of all the csv coloumns
fields = ["ID","User Name","Email_id","Phone_number","Password","Salt","First_login"]
fields_details = ["ID","age","weight","height","blood group"]
calorie_field = ["Id","Date","Calories"]
calories_burnt = ['ID','Burnt calories','Date']
feedback_field = ['ID','feedback']

# quote class with various fucntions to randomly generate quotes and return the writer and quote
class quotes:
    def random_quote(lst):
        random_generated = lst[random.randint(0,len(lst)-1)]
        return random_generated
    def writer(quote): 
        quote_str, writer = quote.split("-")
        return writer
    def quote_string(quote):
        quote_str, writer = quote.split("-")
        return quote_str
    def quote_list():
        quotes_list =[]
        with open(file_id.quote_file(),mode="r",encoding="utf8") as file:
            quotes_list = list(file.readlines())
        return quotes_list

# article class that reads the articles folder in our resources and randomly generates an article with its header and body(in the form of an array)
class articles:

    def locs_list():
        # returns the list of articels present in our articles folder
        locs = {}
        if platform == 'win32':
            working_folder = os.getcwd() + r"\resources\articles"
            articles_list = os.listdir(working_folder)
            for i in range(len(articles_list)):
                locs[i+1] = working_folder +"\\" + articles_list[i]

        else:
            working_folder = os.getcwd() + "/resources/articles"
            articles_list = os.listdir(working_folder)
            for i in range(len(articles_list)):
                locs[i+1] = working_folder + "/" + articles_list[i]
        return locs

    # pics an random article from the list of articles i.e. the address of the article
    def random_article(locs):
        a = len(locs)
        val = random.randint(1, a)
        return locs[val]

    # returns the title of the article given
    def read_heading(file):
        with open(file,mode='r',encoding='utf8') as curr_file:
            heading = curr_file.readline()
        return heading
    #  return the body of the article in form of a list
    def read_body(file):
        body_arr = []
        with open(file,mode='r',encoding="utf8") as curr_file:
            heading = curr_file.readline()
            body = curr_file.readlines()
            for i in body:
                body_arr.append(i)
        return body_arr

# class to deal with all are calories data related opperations
class calorie_functions:
    # gives us the current date
    def get_date():
        return str(datetime.today().date())
    
    # writes data to our calories data csv file
    def write_data(ID,date,calories):
        df = pd.read_csv(file_id.calorie_dataset())
        df = df[calorie_field]
        df1 =df
        df1 = df1.loc[df1['Date'] == date]
        df1= df1.loc[df1["Id"]==ID]
        
        if df1.size == 0: # check for existing data of the user on the same day
            df2 = pd.DataFrame([[ID,date,calories]],columns=calorie_field)
            df = df.append(df2)
            df = df.sort_values("Id")
            df = df[calorie_field]
            
            df.to_csv(file_id.calorie_dataset())
            del df,df1,df2
        else:
            idx = df1.index[0]
            curr_calories = df1.at[idx,"Calories"]
        
            curr_calories = int(curr_calories)
            curr_calories += calories
            df1.at[idx,"Calories"] = curr_calories
            df = df.append(df1)
            df = df.sort_values("Id")
            df = df.drop_duplicates(subset= ["Id","Date"],keep='last')
            df = df[calorie_field]
            df.to_csv(file_id.calorie_dataset())
            del df,df1,curr_calories
        

# class to return the absolute pathing of all our datasets and is system independent
class file_id:

    def feedback_form():
        cwd = os.getcwd()
        if platform == 'win32':
            working_dir = cwd + r"\resources"
            working_file = working_dir + r"\feedback_form.csv"
        elif platform == 'darwin' or platform =='linux':
            working_dir = cwd + "/resources"
            working_file = working_dir + "/feedback_form.csv"
        
        return working_file


    def User_info():
        cwd = os.getcwd()
        if platform == 'win32':
            working_dir = cwd + r"\resources"
            working_file = working_dir + r"\User_info.csv"
        elif platform == 'darwin' or platform =='linux':
            working_dir = cwd + "/resources"
            working_file = working_dir + "/User_info.csv"
        
        try:
            os.mkdir(working_dir)
        except:
            pass
        return working_file
    
    def details():
        cwd = os.getcwd()
        if platform == 'win32':
            working_dir = cwd + r"\resources"
            working_file = working_dir + r"\details.csv"
        elif platform == 'darwin' or platform =='linux':
            working_dir = cwd + "/resources"
            working_file = working_dir + "/details.csv"
        
        return working_file

    def articles(name):
        Name = name
        cwd = os.getcwd()
        if platform == 'win32':
            working_dir = cwd + r"\resources"
            working_file = working_dir + Name
        elif platform == 'darwin' or platform =='linux':
            working_dir = cwd + "/resources"
            working_file = working_dir + Name
        
        return working_file

    def data():
        cwd = os.getcwd()

        if platform == 'win32':
            working_dir = cwd + r"\resources"
            working_file = working_dir + r"\Food and Calories - Sheet1.csv"
        elif platform == 'darwin' or platform =='linux':
            working_dir = cwd + "/resources"
            working_file = working_dir + "/Food and Calories - Sheet1.csv"
        
        return working_file

    def calorie_dataset():
        cwd = os.getcwd()

        if platform == 'win32':
            working_dir = cwd + r"\resources"
            working_file = working_dir + r"\calorie_data.csv"
        elif platform == 'darwin' or platform =='linux':
            working_dir = cwd + "/resources"
            working_file = working_dir + "/calorie_data.csv"
        
        return working_file

    def exercise_dataset():
        cwd = os.getcwd()

        if platform == 'win32':
            working_dir = cwd + r"\resources"
            working_file = working_dir + r"\exercise_dataset.csv"
        elif platform == 'darwin' or platform =='linux':
            working_dir = cwd + "/resources"
            working_file = working_dir + "/exercise_dataset.csv"
        
        return working_file

    def quote_file():
        cwd = os.getcwd()

        if platform == 'win32':
            working_dir = cwd + r"\resources"
            working_file = working_dir + r"\quotes.txt"
        elif platform == 'darwin' or platform =='linux':
            working_dir = cwd + "/resources"
            working_file = working_dir + "/quotes.txt"
        
        return working_file
    
    def burnt_calories():
        cwd = os.getcwd()

        if platform == 'win32':
            working_dir = cwd + r"\resources"
            working_file = working_dir + r"\calories_burnt.csv"
        elif platform == 'darwin' or platform =='linux':
            working_dir = cwd + "/resources"
            working_file = working_dir + "/calories_burnt.csv"
        
        return working_file        



# page to tracking page
@app.route("/trackingpage")
def trackingpage():
    if "Id" in session:
        df = pd.read_csv(file_id.calorie_dataset())
        df1 = pd.read_csv(file_id.burnt_calories())
        df = df.loc[df["Id"]==session['Id']]
        df1 = df1.loc[df1['ID']==session["Id"]]
        df = df.tail(7)
        df1 = df1.tail(7)
        date =list(df['Date'])
        calories_eaten = list(df['Calories'])
        calories_eaten = make_dict(date, calories_eaten)
        date = list(df1['Date'])
        calories_burnt_1 = list(df1['Burnt calories'])
        calories_burnt_1 = make_dict(date, calories_burnt_1)
        final_arr=[]
        
        for i in calories_eaten.keys():
            lst = [i,calories_eaten[i],0]
            final_arr.append(lst)
        for i in calories_burnt_1.keys():
            if i not in date:
                lst = [i,0,calories_burnt_1[i]]
                final_arr.append(lst)
            else:
                idx =0
                for j in range(len(final_arr)):
                    if i == final_arr[j][0]:
                        idx = j
                        break
                final_arr[idx][2] = calories_burnt_1[i]
        return render_template('reported.html',data= final_arr)
    else:
        return redirect('landingpage')
    

# landing page route
@app.route("/",methods =['GET','POST'])
def landing_page():
   
    return render_template("landing_page.html")

# main page route 
@app.route("/mainpage",methods=['GET','POST'])
def mainpage():
    if 'Id' in session:
        Id = session['Id']
        # random article sending to main page
        if "article" not in session:
            if 'date' not in session:
                session['date'] = str(datetime.today().date())
            locs = articles.locs_list()
            article = articles.random_article(locs)
            head = articles.read_heading(article)
            body = articles.read_body(article)
            session['article'] = article
        else:
           
            if session['date'] == str(datetime.today().date()):
                article = session['article']
                head = articles.read_heading(article)
                body = articles.read_body(article)
            else:
                session['date'] = str(datetime.today().date())
                locs = articles.locs_list()
                article = articles.random_article(locs)
                head = articles.read_heading(article)
                body = articles.read_body(article)
                session['article'] = article
                
        # sending data for the feedback form
        less,more = bodySplitter(body)
        df = pd.read_csv(file_id.User_info())
        df1 = df.loc[df['ID']==session['Id']]
        df1 = df1.drop(columns=['Password','Salt','First_login'])
        mail_id = list(df1['Email_id'])
        Phone_number = list(df1['Phone_number'])
        Name = list(df1['User Name'])

        if request.method == 'POST': # taking in the feedback form data
            feedback = request.form['feedback']
            user_feedback(Id, feedback)
            del feedback
            return redirect('mainpage')
        return render_template('main.html',Id = Id,head = head,less = less,more=more,email_id = mail_id[0],phone_number = Phone_number[0],name=Name[0])
    else: 
        return redirect('signinpage')
#route for profile page
@app.route('/profilepage',methods=['GET','POST'])
def profilepage():
    if 'Id' in session:            
        data = retriveData()
        if request.method == 'POST':
            data['Name'] = request.form['name']
            data['BloodGroup'] = request.form['Blood']
            data['Age'] = request.form['age']
            data['Height'] = request.form['height']
            data['Weight'] = request.form['weight']
            data['BMI'] = request.form['Your BMI']

        return render_template('profile_page.html',name = data['Name'],bloodGroup = data['BloodGroup'],age = data['Age'],height = data['Height'],weight=data['Weight'],bmi = data['BMI'],idealWeight = data['IdealWeight'])
    else:
        return redirect('landingpage')
# route for exercise page
@app.route('/exercise')
def exercise():
    if 'Id' in session:
        quote_lst  = quotes.quote_list()
        quote = quotes.random_quote(quote_lst)
        writer = quotes.writer(quote)
        sentence = quotes.quote_string(quote)
        return render_template('exercise.html',writer = writer,quote = sentence)
    else:
        return redirect('landingpage')


# route for exercise videos based on body parts
@app.route('/body')
def bodyparts():
    if 'Id' in session:
        return render_template('bodypart.html')
    else:
        return redirect('landingpage')

# route for types of exercises
@app.route('/typesofexercise')
def typesofexercise():
    if 'Id' in session:
        return render_template('varietyexercise.html')
    else:
        return redirect('landingpage')
#route for yoga
@app.route('/yoga')
def yoga():
    if 'Id' in session:
        return render_template('yoga.html')
    else:
        return redirect('landingpage')

# route for diet page
@app.route('/diet')
def diet():
    if 'Id' in session:
        return render_template('diet.html')
    else:
        return redirect('landingpage')

# route for tracking calories
@app.route("/take")
def take():
    if 'Id' in session:
        df = pd.read_csv(file_id.data())
        food_data = df['Food']
        serving_data =df['Serving']
        serving_data = list(serving_data)
        food_data = list(food_data)
        df1 = pd.read_csv(file_id.exercise_dataset())
        df2 = pd.read_csv(file_id.details())

        exercise_list = list(df1["Activity, Exercise or Sport (1 hour)"])
        calories_per_kg = list(df1["Calories per kg"])
        exercise_dict = make_dict(exercise_list, calories_per_kg)
        data_dict = make_dict(food_data, serving_data)
        del df,df1,df2
        return render_template("take.html",data = data_dict,food_list = food_data,exercise_list=exercise_list,exercise_dict = exercise_dict)
    else:
        return redirect("landing_page")


# route for managing the js data from burnt calories
@app.route("/testinput",methods=["POST"])
def testinput():
    if "Id" in session:
        data1 = request.get_json() # taking in the json data
        
        burnt_calories = data1['data'] 
        print(burnt_calories)
        df1 = pd.read_csv(file_id.details())
        df1 = df1.loc[df1['ID']==session['Id']]
        weight = list(df1['weight'])
        weight = weight[0]
        burnt_calories = float((burnt_calories*weight)/60.0)
        df = pd.read_csv(file_id.burnt_calories()) # reading the csv file
        df1 = df.loc[df["ID"]==session['Id']]
        date = str(datetime.today().date())
        df1 = df1.loc[df1['Date'] == date]

        if df1.size == 0: # check for if the user has already logged data on that day
            
            data = [[session['Id'],burnt_calories,date]]
            df2 = pd.DataFrame(data,columns=calories_burnt)
            df =df.append(df2)
            df = df.sort_values('ID')
            df = df[calories_burnt]
            df.to_csv(file_id.burnt_calories())
        
        else:

            previous_calories = list(df1['Burnt calories'])
            previous_calories = previous_calories[0]
            burnt_calories +=previous_calories
            data = [[session['Id'],burnt_calories,date]]
            df1 = pd.DataFrame(data,columns=calories_burnt)
            df = df.append(df1)
            df = df.sort_values('ID')
            df = df.drop_duplicates(subset=['ID','Date'],keep='last')
            df = df[calories_burnt]
            df.to_csv(file_id.burnt_calories())

        
        return data1
    else:
        return redirect('landing_page')

        
# route to take calories eaten and append it to the dataset
@app.route("/takeinput",methods=['POST'])
def takeinput():
    if "Id" in session:
        food_dict = request.get_json()
        Calories = 0
        df = pd.read_csv(file_id.data())
        food_list =list(df["Food"])
        calorie_list = list(df["Calories"])
        
        for i in food_dict.keys() :
            a = food_list.index(i)
            val = calorie_list[a]
            num,cal = val.split(" ")
            num = int(num)
            Calories+=num*(int(food_dict[i]))
        date = calorie_functions.get_date()
        calorie_functions.write_data(session["Id"], date, Calories)
        return food_dict
    else:
        return redirect('landing_page')


# read more page route where the full article will be visible


# signup or create account page
@app.route("/signuppage",methods=['GET','POST'])
def SignUp_page():
    username = ""
    password = ""
    if request.method == 'POST':
        if "SignUp" in request.form.keys():
            username = request.form['User_name']
            Email_id = request.form['Email_id']
            Phone = request.form['Phone_number']
            password = request.form['password']
            reenter =  request.form['re_password'] 
            
            df = pd.read_csv(file_id.User_info())
            user_list = df["User Name"]
            user_list = list(user_list)
            if len(Phone) != 10:
                return render_template("signuppage.html")

            if password == reenter :
                if username not in user_list:
                    del user_list,reenter,df
                    return account_creation(username, password,Email_id,Phone)
                else:
                    return "<h1> User already exists please Sign In</h1>"
            else:
                return "<h1>Wrong Confirm Password go back to home page</h1>"
        else:
            username = request.form['User_name']
            password = request.form['password']
            
            rememberme = request.form.get('rememberme')
            password_encoded = sha512(password.encode()).hexdigest()
        
            df = pd.read_csv(file_id.User_info())
            user_list = df["User Name"]
            user_list = list(user_list)
            
            if username in user_list:
                password_list = df["Password"]
                password_list = list(password_list)
                num = user_list.index(username)
                pass_in_data = password_list[num]
                salt_list =  df["Salt"]
                salt_list = list(salt_list)
                salt = salt_list[num]
                log_list = df["First_login"]
                log_list = list(log_list)
                log = log_list[num]

                password_encoded = password_encoded + salt

                if pass_in_data == password_encoded:
                    session['Id'] = num
                    
                    session.permanent = True   
                         
                    del df,salt_list,log_list,password_list,user_list
                    return redirect('mainpage') # return main page here
                else:
                    del df,salt_list,log_list,password_list,user_list
                    return "<h1> Wrong Username or Password</h1>"
            else:
                    return "<h1> Wrong Username or Password</h1>"
    else:
        return render_template("signuppage.html")


# sign in page 
@app.route("/signinpage",methods=['GET','POST'])
def SignIn_page():
    if 'Id' in session:
        return redirect('/mainpage')
    if request.method == 'POST':
        username = request.form['User_name']
        password = request.form['password']
        
        rememberme = request.form.get('rememberme')
        password_encoded = sha512(password.encode()).hexdigest()
    
        df = pd.read_csv(file_id.User_info())
        user_list = df["User Name"]
        user_list = list(user_list)
        
        if username in user_list:
            password_list = df["Password"]
            password_list = list(password_list)
            num = user_list.index(username)
            pass_in_data = password_list[num]
            salt_list =  df["Salt"]
            salt_list = list(salt_list)
            salt = salt_list[num]
            log_list = df["First_login"]
            log_list = list(log_list)
            log = log_list[num]

            password_encoded = password_encoded + salt

            if pass_in_data == password_encoded:
                session['Id'] = num
                
                session.permanent = True            
       
                del df,salt_list,log_list,password_list,user_list
                return redirect('mainpage') # return main page here
            else:
                del df,salt_list,log_list,password_list,user_list
                return "<h1> Wrong Username or Password</h1>"
        else:
                return "<h1> Wrong Username or Password</h1>"
   
    return render_template("signinpage.html")


# exeercise and there routes

@app.route('/exercise/body/b1')
def b1():
    return render_template('abs.html')

@app.route('/exercise/body/b2')
def b2():
    return render_template('arm.html')

@app.route('/exercise/body/b3')
def b3():
    return render_template('back.html')

@app.route('/exercise/body/b4')
def b4():
    return render_template('chest.html')


@app.route('/exercise/body/b5')
def b5():
    return render_template('legs.html')


@app.route('/exercise/body/b6')
def b6():
    return render_template('shoulder.html')



@app.route('/exercise/typesofexercise/t1')
def t1():
    return render_template('aerobicexercise.html')

@app.route('/exercise/typesofexercise/t2')
def t2():
    return render_template('circuittraining.html')


@app.route('/exercise/typesofexercise/t3')
def t3():
    return render_template('flexibility.html')


@app.route('/exercise/typesofexercise/t4')
def t4():
    return render_template('highintensity.html')


@app.route('/exercise/typesofexercise/t5')
def t5():
    return render_template('lowintensity.html')


@app.route('/exercise/typesofexercise/t6')
def t6():
    return render_template('resistanceexercise.html')


@app.route('/ourteam')
def ourteam():
    return render_template('ourteam.html')
# logout action url
@app.route('/logout')
def logout():
    session.pop('Id',None)
    session.pop('article',None)
    session.pop('date',None)
    return redirect(url_for('SignIn_page'))


# function to create an account
def account_creation(username , password,Email_id,Phone):
    # here we will create a private key and public key for the user
    password_encoded = sha512(password.encode()).hexdigest()
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"
    chars=[]

    for i in range(16):
        chars.append(random.choice(ALPHABET))
    salt = "".join(chars)
    password_encoded = password_encoded + salt
    # here we are appending the data to our files
    
    df = pd.read_csv(file_id.User_info())
    df1 = df[fields]
    Id_arr = df["ID"]
    num = Id_arr[len(Id_arr)-1] + 1
    log = 0
    data = [[num,username,Email_id,Phone,password_encoded,salt,log]]
    df2 = pd.DataFrame(data,columns=fields)
    
    df1 = df1.append(df2)
    df1 = df1[fields]
    df1.to_csv(file_id.User_info())
    session['Id'] = int(num)
    return redirect("/accountdetails") #here we will redirect to our main page

#  function to record our user feedback
def user_feedback(ID,feedback):
    df = pd.read_csv(file_id.feedback_form())
    data = [[ID,feedback]]
    df1 = pd.DataFrame(data,columns=feedback_field)
    df = df.append(df1)
    df = df[feedback_field]
    df.to_csv(file_id.feedback_form())
    del df,df1

# function to make a dicitonary with key and value list
def make_dict(key_lsit,val_list):
    dict = {}
    for i in range(len(key_lsit)):
        dict[key_lsit[i]] = val_list[i]

    return dict


def bodySplitter(body):
    less = ""
    more = ""
    for i in range(3):
        less += body[i][:-2]
        less += "."
    for i in range(3,len(body)):
        more+=body[i][:-2]
        more+="."
    
    return less,more



# function to read all the data of the user and send a dict for the profile page
def retriveData():
    data = {}
    df = pd.read_csv(file_id.User_info())
    df = df[['ID','User Name']]
    df = df.loc[df['ID']==session['Id']]
    name = list(df['User Name'])[0]
    data['Name'] = name  
    df = pd.read_csv(file_id.details())
    df = df[fields_details]
    df = df.loc[df['ID'] == session['Id']]
    
    weight = list(df['weight'])[0]
    age = list(df['age'])[0]
    height = list(df['height'])[0]
    blood = list(df['blood group'])[0]
    data['Weight'] = weight
    data['Height'] = height
    data['Age'] = age
    data['BloodGroup'] = blood
    data['IdealWeight'] = 21.7*((height/100.0)**2)
    data['BMI'] = weight/((height/100.0)**2)
    return data

# running of the page
if(__name__ ==" __main__"):
    app.run()
