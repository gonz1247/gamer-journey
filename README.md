# gamer-journey
Web app for tracking/rating video games played and creating wishlist for future playing! 

I got the idea for this project since I am huge fan of video games, but also movies. For my movie watching hobby I use
[Letterboxd](https://letterboxd.com/) to track everything I am watching, so I thought it would be cool if there was a
similar app for playing video games.

Currently, I am an aerospace engineer but, I am hoping to pivot my career to software engineering hopefully soon. I am
hopeful that continuing to work on personal projects like this will help me to develop the skills and portfolio
necessary to make the switch in careers.

## Setup
- Clone repository to your local machine
- Install required dependencies using the `requirements.txt` document
  - `python -m pip install -r ./src/requirements.txt`
- Follow the [IGDB instructions](https://api-docs.igdb.com/#account-creation) for obtaining a `Client ID` and
`Client Secret` for the required API
- Create a `.env` file in the `src` directory that has all the required information indicated in the `.env.example`
(note that `.env` is in `.gitignore` since it will contain personal/sensitive information)
  - If using a smtp such as gmail (or maybe others) you may need to create an
  [application password](https://support.google.com/accounts/answer/185833?hl=en)
- Working within the `src` directory, migrate changes for the project 
  - `python manage.py migrate`
- Create a superuser if needed
  - `python manage.py createsuperuser` and input requested info
  - Note that the superuser will not automatically have an account for gamer-journey so will need to add account
  manually: `python manage.py shell` > `u = User.objects.get(pk=<superuser-id>)` > `Patron.objects.create(user=u)`
- Run the server
  - `python manage.py runserver`
- Use link provided in terminal (i.e., `http://127.0.0.1:8000/`) to access gamer-journey web app

## Future Work
The creation of this web-app was done as a learning exercise for myself so no future work is currently planned. Please
see the render-deploy branch and/or visit [https://gamer-journey.onrender.com/](https://gamer-journey.onrender.com/) to
see the final live version. 