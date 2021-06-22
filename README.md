## API overview:

Project allows users to upload image files and depending on the plan, to receive the output data in the form of thumbnails of the uploaded file.

POST endpoint '/create/' only accept file with .png or .jpg extensions, otherwise ValueError is being raised.

User with admin privileges can log into admin panel and create custom plans with specified image height and other options.

## Installation:

In order to install please create new virtual environment and install all dependencies from requirements.txt

```
pip install -r requirements.txt
```

Please add a SECRET_KEY env variable by typing in your terminal:

```
export SECRET_KEY='your_secret_key'
```

Then go into directory with manage.py and start a django project
```
python manage.py runserver
```

## API Testing
SQLite database has been uploaded so in order to test app just follow installation part.

Logged in as one of the predefined user in order to test API at '/admin/:
- user1, password1, (Basic Plan),
- user2, password2, (Premium Plan),
- user3, password3, (Enterprise Plan),
- user4, password4, (Custom Plan and Administrator),

Once you logged, go to '/list/' endpoint. Now you can list all your images according to the plan that the account has.

You can also upload new images at '/create/'. All you have to do is choose file for 'Original size image'(Everything else happens in the background.)
