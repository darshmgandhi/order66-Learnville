# Learnville
Learnville is a project made for NIIT University's hackathon HackNU 2.0.

What is Learnville
------
There are many platforms available as of now for students to learn new skills and improve theirs access to different course materials related to their respective areas of education. The amount of content available for students is numerous however, there are hardly any platforms that supplements students need for practicing a concept. Practicing a concept is a very important part of the learning process. And thus, LearnVille aims to provide students with the questions to practice a concept of a particular course curated by the teachers with interactive tools to develop a solution to a problem.
##### Students can ‘build’ their answers
We believe that learning would be most efficient if students could “build” their own answers from scratch just like they would on a pen-and-paper test.
##### Automated correction process
It is necessary to automate the correction process so that students can get instant feedback on their solution.
##### Best of both worlds
A perfect mix of both theory and practical knowledge is essential for proper understanding.

How to run it
------
To run a local instance of this website, you need these prerequisites:
* python3
* MySQL

Apart from these, you have to install these python modules:
* flask
* flask_mysqldb

The powershell code to install these is given below. This would also work on bash.
```
pip3 install flask
pip3 install flask-mysqldb
```

Open MySQL and copy-paste all the MySQL commands from [sqlcommands.txt](./sqlcommands.txt)

Open [learnville_new.py](./learnville_new.py). Change the value of `app.config['MYSQL_USER']` to your MySQL username and the value of `app.config['MYSQL_PASSWORD']` to your MySQL password.

Finally run the python code, either using an ide or opening Terminal or Powershell(depending on your os).
In the powershell, change your current directory to the one containing the codebase using `cd` command and type - 
```
python 'learnville_new.py'
```
Copy the link [http://127.0.0.1:5000/](http://127.0.0.1:5000/) and paste it on your browser's address bar.
The website will run on that url.
