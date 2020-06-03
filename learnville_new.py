from flask import Flask, render_template, redirect, url_for, request, session
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'learnzilla'

mysql = MySQL(app)
app.secret_key = 'S66D0HrapD9c8rGpBoGR'

@app.route("/")
def home():
    return render_template('js.html')

@app.route("/register", methods = ["GET","POST"])
def register():
    return render_template('register.html') 

@app.route('/login', methods = ["GET","POST"])
def login():
    if request.method == 'POST':
        userdetails=request.form
        name = userdetails['username']
        password = userdetails['password']
        cur = mysql.connection.cursor()
        result = cur.execute("select username,password from student")
        all_users = cur.fetchall()
        if (name,password) in all_users:
            session['username'] = name
            session['type'] = 'student'
            return redirect(url_for('dashboard'))
        else:        
            result = cur.execute("select username,password from teacher")
            all_users = cur.fetchall()
            if (name,password) in all_users:
                session['username'] = name
                session['type'] = 'teacher'
                return redirect(url_for('dashboard'))
            else:    
                return 'Incorrect Username or Password'
    else:
        return redirect(url_for('register'))           

@app.route('/choice', methods = ["GET","POST"])
def choice():
    if request.method == 'POST':
        signupdetails=request.form
        fullname = signupdetails["fullname"]
        email = signupdetails["emailid"]
        return render_template('profile.html', fullname=fullname,email=email)
    else:    
        return redirect(url_for('register'))

@app.route('/signup/<atype>/<fullname>/<email>', methods = ["GET","POST"])
def signup(atype, fullname, email):
    if request.method == 'POST':
        finaldetails=request.form
        username = finaldetails["username"]
        password = finaldetails["pass"]
        conpass = finaldetails["conpass"]
        institution = finaldetails["institution"]
        date = finaldetails["date"]
        bio = finaldetails["bio"]
        cur = mysql.connection.cursor()
        result = cur.execute("select username from teacher union select username from student")
        usernames = cur.fetchall()
        ok = True
        for u in usernames:
            if u[0] == username:
                ok = False
                break
        if ok:        
            if password == conpass:
                cur = mysql.connection.cursor()
                cur.execute("insert into %s values('%s','%s','%s','%s','%s','%s','%s')" %(atype, username,fullname,email,password,institution,date,bio))
                mysql.connection.commit()
                cur.close()
                return redirect(url_for('register'))     
            else:
                return "The passwords do not match"    
        else:
            return "Username has been taken"        
    else:
        return render_template('SignUp2.html')    

@app.route("/dashboard")           
def dashboard():
    if "username" in session:
        if session['type'] == 'teacher':            
            cur = mysql.connection.cursor()
            result = cur.execute("select * from course where taught_by='%s'" %(session['username']))    
            all_courses = cur.fetchall()
            return render_template('home.html', all_courses = all_courses,stype='teacher')  
        elif session['type'] == 'student':
            cur = mysql.connection.cursor()
            result = cur.execute("select c.* from used_courses u,course c where u.courseid=c.courseid and u.username='%s'" %(session['username']))   
            all_courses = cur.fetchall() 
            return render_template('home.html', all_courses = all_courses,stype='student')                   
    else:
        return redirect(url_for('register')) 

@app.route("/addcourse", methods=['GET','POST'])
def addcourse():
    if "username" in session:
        if request.method=='POST':
            cur = mysql.connection.cursor()
            result = cur.execute("select max(courseid) from course")
            fetch = cur.fetchall()
            if fetch==((None,),):
                new_course_id='00000'
            else:
                new_course_id = str(int(fetch[0][0])+1).rjust(5,'0')
            newcdetails = request.form
            cname=newcdetails['cname']
            subt=newcdetails['subt']
            cur = mysql.connection.cursor()
            cur.execute("insert into course values('%s','%s','%s',null,'%s',null)" %(new_course_id,cname,subt,session['username']))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('course',course_id=new_course_id))
        else:
            return render_template('addcourse.html')
    else:
        return redirect(url_for('register'))                 

@app.route("/allcourses")
def allcourses():
    if "username" in session:            
        cur = mysql.connection.cursor()
        result = cur.execute("select * from course")   
        all_courses = cur.fetchall() 
        cur = mysql.connection.cursor()
        result = cur.execute("select courseid from used_courses where username='%s'" %(session['username']))   
        selected_courses = cur.fetchall() 
        return render_template('allcourses.html', all_courses = all_courses,stype=session['type'], selected_courses=selected_courses)                   
    else:
        return redirect(url_for('register')) 

@app.route("/pincourse/<course_id>")        
def pincourse(course_id):
    if "username" in session:
        cur = mysql.connection.cursor()
        cur.execute("insert into used_courses values('%s','%s',null)" %(session["username"],course_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('allcourses'))
    else:
        return redirect(url_for('register'))    

@app.route("/unpincourse/<course_id>/<where_from>")
def unpincourse(course_id,where_from):
    if "username" in session:
        cur = mysql.connection.cursor()
        cur.execute("delete from used_courses where username='%s' and courseid='%s';" %(session["username"],course_id))
        mysql.connection.commit()
        cur.close()
        if where_from=='dash':
            return redirect(url_for('dashboard'))
        else:   
            return redirect(url_for('allcourses')) 
    else:
        return redirect(url_for('register'))                

@app.route("/profile")
def profile():
    if "username" in session:
        cur = mysql.connection.cursor()
        result = cur.execute("select * from %s where username = '%s'" %(session['type'],session['username']))
        user_profile = cur.fetchall()
        return render_template('profile_details.html', user_profile=user_profile, type = session['type'])
    else:
        return redirect(url_for('register'))   

@app.route('/choose')
def choose():
    return render_template('profile.html')        

@app.route("/course/<course_id>")
def course(course_id):
    if "username" in session:
        cur = mysql.connection.cursor()
        result = cur.execute("select problemid,problem_name from problems where course='%s'" %(course_id))
        all_problems = cur.fetchall()
        result = cur.execute("select name from course where courseid='%s'" %(course_id))
        course_name = cur.fetchall()[0][0]
        return render_template('course.html', all_problems=all_problems, course_id=course_id, course_name=course_name,stype=session['type'])      
    else:
        return redirect(url_for('register'))    

@app.route("/course/<course_id>/<problem_id>", methods = ["GET","POST"])
def problem(course_id,problem_id):
    solved = False
    if "username" in session:
        if session['type']=='student':
            cur = mysql.connection.cursor()
            result = cur.execute("select s.problemid from solved_problems s, problems p where s.problemid=p.problemid and username='%s' and course='%s'" %(session['username'],course_id))
            solvedproblems=cur.fetchall()
            if (problem_id,) in solvedproblems:
                solved = True 
        if request.method=='POST' and session['type']=='student':
            cur = mysql.connection.cursor()
            result = cur.execute("select solution from problems where problemid='%s'" %(problem_id))
            solution = cur.fetchall()[0][0]
            submission = request.form
            answer = submission['answer']
            if solution==answer:
                cur = mysql.connection.cursor()
                cur.execute("insert into solved_problems values('%s','%s')" %(session['username'],problem_id))
                mysql.connection.commit()
                cur.close()
                return redirect(url_for('problem',course_id=course_id,problem_id=problem_id))
            else:
                return 'Wrong Answer'    
        else:    
            cur = mysql.connection.cursor()
            result = cur.execute("select problemid,problem_name from problems where course='%s'" %(course_id))
            all_problems = cur.fetchall()
            result = cur.execute("select * from problems where problemid='%s'" %(problem_id))
            current_problem = cur.fetchall()
            if current_problem[0][0]!=(all_problems[len(all_problems) - 1][0]):
                next_Problem=all_problems[all_problems.index((current_problem[0][0],current_problem[0][4]))+1][0]
            else:
                next_Problem=0    
            return render_template('Ws.html',all_problems=all_problems,current_problem=current_problem,atype=session['type'], solved=solved, next_Problem=next_Problem)        
    else:
        return redirect(url_for('register')) 

@app.route("/deleteproblem/<course_id>/<problem_id>")
def deleteproblem(course_id,problem_id):
    cur = mysql.connection.cursor()
    cur.execute("delete from solved_problems where problemid='%s'" %(problem_id))
    mysql.connection.commit()
    cur.execute("delete from problems where problemid='%s'" %(problem_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('course',course_id=course_id)) 

@app.route("/addproblem/<course_id>", methods = ["GET","POST"])
def addproblem(course_id):
    if "username" in session:
        if request.method=='POST':
            new_problem=request.form
            cur = mysql.connection.cursor()
            result = cur.execute("select max(problemid) from problems")
            fetch = cur.fetchall()
            if fetch==((None,),):
                new_id='00000'
            else:
                new_id = str(int(fetch[0][0])+1).rjust(5,'0')
            name = new_problem["name"]
            problem_statement = new_problem["subject"]
            qtype = new_problem["qtype"]
            solution = new_problem["Answer"] 
            cur = mysql.connection.cursor() 
            if qtype=='problem':     
                cur.execute("insert into problems values('%s','null','%s','%s','%s','%s','%s')" %(new_id,problem_statement,course_id,name,solution,qtype))
            else:
                cur.execute("insert into problems values('%s','null','%s','%s','%s','None','%s')" %(new_id,problem_statement,course_id,name,qtype))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('problem',course_id=course_id,problem_id=new_id))
        else:    
            return render_template('wst.html')
    else:
        return redirect(url_for('register'))    

@app.route("/about")
def about():
    if "username" in session:
        return render_template('about.html', stype=session['type']) 
    else:
        return render_template('about.html', stype='None')                

if __name__=='__main__':
    app.run(debug=True)