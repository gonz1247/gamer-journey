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
[https://gamer-journey.com](https://gamer-journey.com). The web app is fully functional and deployed via Amazon Web Services (AWS).

## Differences From Local Dev Branch

This branch of the gamer-journey project is in a ready for deployment state. In addition to adding things needed for production deployment,
this branch also removed a lot of the Django models that are on the local-dev branch. When working in the local-dev branch I wanted to
practice working with various relationships within Django (many-to-many, one-to-many, and one-to-one) but some of these models were redundant to
information that I am able to query from the IGDB database and therefore unnecessarily taking space on the gamer-journey database.

## Setup For Local Development

- Clone repository to your local machine
  - Install required dependencies using the `requirements.txt` document
    - `python -m pip install -r ./src/requirements.txt`
  - Follow the [IGDB instructions](https://api-docs.igdb.com/#account-creation) for obtaining a `Client ID` and
    `Client Secret` for the required API
  - Create `terraform.tfvars` file and populate add `igdb_client_id`, `igdb_client_secret`, `admin_email`, and `admin_email_pw` (see `terraform.tfvars.example`)
    - Likely need to setup an [application password](https://support.google.com/accounts/answer/185833?hl=en) to use smtp through gmail (or other service)
    - Note that `terraform.tfvars` is in `.gitignore` since it will contain sensitive information
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

At this time I don't have any plans to expand gamer-journey.
