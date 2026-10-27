# FoundDesk

FoundDesk is a simple campus lost-and-found app.

Users can:

- Create an account
- Log in
- Report lost or found items
- Add a category, location, and description
- See who posted an item
- Delete only their own posts
- View possible matches between lost and found items

## Run the project

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

Then run:

```bash
python main.py
```

Set `FOUNDDESK_SECRET_KEY` to your own random value before sharing the app with others.

## Run the tests

```bash
python -m pip install pytest
python -m pytest
```

## Built with

- Python
- Flask
- SQLite
- HTML and CSS

Made for students who want an easier way to find lost items.

## AI Assistance

AI was used as a coding assistant during development. It helped explain the use of Flask, SQLite, and HTML concepts. It is also used to generate ideas for new features. All AI recommendations were reviewed and tested before being added to the project.