ApexRide Nepal — fix for "No module named 'flask_sqlalchemy'"
================================================================
What happened: Flask-SQLAlchemy was not installed for the Python
that ran app.py. requirements.txt already lists it, so the fix is
to install with the SAME Python that runs the app:

  python -m pip install -r requirements.txt

Easiest way on Windows: double-click RUN-ME.bat in this folder.
It runs that install, then starts the app.

Then open: http://127.0.0.1:5000
Demo: customer@apexride.com.np / apexride123
       owner@apexride.com.np / apexride123
