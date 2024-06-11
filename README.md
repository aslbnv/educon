# About
Goal of the project is to develop a LMS for employee education.

Main functionality:

 - Creation of education courses
 - Filling courses with content
 - Distribution of courses by users
 - Opportunity to take a course
 - Tracking user education progress

 There are two roles in the system - employee and administrator.

# Requirements
- Python = **3.8.0**

# Setup
Clone this repo and cd in it
```
git clone git@github.com:temsolv/educon.git
```

Create virtual environment and activate it
```
python -m venv venv_name
```

Install necessary packages
```
pip install -r requirements.txt
```

Run background tasks and local server
```
make run
make tasks
```
