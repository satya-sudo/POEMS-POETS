# Capstone

# POEMS&POETS
This website was created for completing CS50W Harvard course. The website's primary goal is to provide to people an audience with their poetry . Users can post their poems. They can read other user's
poems, add comments on their work. and finally maintain their own poetry library . Some of the features this website has are:

- User sessions
- Profile page
- Posting poems 
- Creating their library 
- Comment on poems
- Edit their old poems

### important features

- the website has total of five models
    -User (django abstract user)
    - User_profile which extents user model using OnetoOne relation
    - the Poem model 
    - Comment model
    - Library model 
- the website uses javascript on the front end to provide a nice user experience 
- The website uses some bootstrap elements like container, rows and column for a mobile responsive experience 
- The icons are from fontawesome.com


### All the pages of the website
- the landing page of the website :
    - on the landing page the user is greeted with a nice quotation
    - all the published  poem from all the users on website are displayed in a card style format
    - ie the latest 12 poems per page
- The user(logged in or not ) can view any of the poem from the landing page
- But to maintain a library or to comment on the poem the user have to sign up or log in
- Sign up page is pretty simple and requires only a unique username,an email and a password
- After signing up the user have their own profile page where the user can change their name, add a about me and add a profile image 
- All poems by the user will show up here  itself (published or unpublish) 
- User can edit his/her poem form the profile page itself
- User can create their poems from '/create' page
- /create page is a two part form 
    - 1st part has a text area where user can write their poem which is saved as draft(markdown is supported here)
    - 2nd part  - user can add a title to their poem 
                - add a short description
                - add a cover image
                - user can choose to publish their poem right away or save it as a draft
                - all the fields in part2 are not mandatory and have a default value
- /library a logged in user can add/remove poems to his/her library   



### Smaller features the website has:

- All the textfields gets converted to html using markdown2
- Has a dark and light mode , which gets toggled via the default theme of the OS (mac,windows,linux)
- Has ajax elements which uses fetch which allows certain edits like adding comments , changing profile details without a window refresh
- The website is completely mobile responsive


### This project uses:

- Python (3.8.3)
- Django (3.1.2)
- JavaScript
- CSS
- HTML
- bootstrap
- FontAwesome
- markdown2
- PIL or Pillow

### Requirements:
-asgiref==3.2.10
-Django==3.1.2
-markdown2==2.3.10
-Pillow==8.0.1
-pytz==2020.1
-sqlparse==0.4.1

### getting started 
- pip install -r requirements.txt
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver

### The website is reloaded with some demo users and post for convenience 


## the website is the end product of all the knowledge I gained from the course cs50 web programming using python and javascript

## WATCH THE DEMONSTRATION HERE - https://youtu.be/KSwxWD5BLxc