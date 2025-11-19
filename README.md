# gamer-journey
Web app for tracking/rating video games played and creating wishlist for future playing! 

I got the idea for this project since I am huge fan of video games, but also movies. For my movie watching hobby I use
[Letterboxd](https://letterboxd.com/) to track everything I am watching, so I thought it would be cool if there was a
similar app for playing video games.

Currently, I am an aerospace engineer but, I am hoping to pivot my career to software engineering hopefully soon. I am
hopeful that continuing to work on personal projects like this will help me to develop the skills and portfolio
necessary to make the switch in careers.

## Live Web App
Please check out the live version of the gamer-journey web app at
[https://gamer-journey.onrender.com](https://gamer-journey.onrender.com). The web app is fully functional, however due
to being on the free tier the database will be refreshed on a monthly basis (i.e., if you create an account and populate
it with games, it will all be deleted eventually). Also, when accessing the web app it may take up to 1 minute to load
initially, this is another fallout of using the Render free tier. 

## Differences From Local Dev Branch
This branch of the gamer-journey project is in a ready for deployment state. I used Render for deploying the web app,
but I am sure there are other suitable options for deployment. 

In addition to adding things needed for compatibility with Render, this branch also removed a lot of the Django models
that are on the local-dev branch. When working in the local-dev branch I wanted to practice working with various
relationships within Django (many-to-many, one-to-many, and one-to-one) but some of these models were redundant to
information that I am able to query from the IGDB database and therefore unnecessarily taking space on the
gamer-journey database. 

## Deploy Web App on [Render](https://dashboard.render.com/)
- Create a `.env` file in the `src` directory that has all the required information indicated in the `.env.example`
(note that `.env` is in `.gitignore` since it will contain personal/sensitive information)
  - If using a smtp such as gmail (or maybe others) you may need to create an
  [application password](https://support.google.com/accounts/answer/185833?hl=en)
- Create a Postgres database on Render
- Initiate creating a Web Service on Render
- Add four environment variables to the Web Service
  - `DATABASE_URL`: The value for this is the `External Database URL` under the Connections sections of the Postgres
  database that you created 
  - `DEBUG`: Set the value to `False`
  - `PYTHON_VERSION`: Set the value to `3.13.2` (or whatever version of Python that you used when working on this
  project)
  - `SECRET_KEY`: Use the Render option `Generate` to get a secure secret key 
- Add a secret file to the Web Service named `.env` and copy in the contents of the `.env` file that you created in the
previous step
- Update `ALLOWED_HOSTS` in `src/gamer_journey/settings.py` to include the website URL that Render generated for the
project upon initializing
- Use `Manual Deploy` button on Render web service page to deploy the web app


## Future Work
At this time I don't have any plans to expand gamer-journey nor switch to a paid tier of Render so that web 
app can truly be live.
