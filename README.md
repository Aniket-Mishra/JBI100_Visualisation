# README

### This contains information on how to setup and run the code
### IT also contains information on the code itself, where and how it was used and written.

## Getting the code
#### If Github:
Code location:
https://github.com/Aniket-Mishra/JBI100_Visualisation

- It is a private repo. Can add access if needed.
- Cloning: (ssh)
	- git clone git@github.com:Aniket-Mishra/JBI100_Visualisation.git

I use Mac, so most of my commands will work on Linux/Mac.
For windows, they'll be slightly different. I've added links to docs.

#### If local: Just download the zip, unzip in your location.

### How to run the code:

1. Go to the directory of the code.
2. Make sure you have python installed.
	- https://www.python.org/downloads/
	- Mac with UV (Super fast and easy):
		- uv python install 3.11
3. Go to your virtual environment
	- https://docs.python.org/3/library/venv.html#creating-virtual-environments
	- Using UV:
		- uv venv --python 3.11 /Users/paniket/Environments/tue_uvenv_311
4. Activate virtual environment
	- https://docs.python.org/3/tutorial/venv.html
	- command:
		- source ~/Environments/tue_uvenv_311/bin/activate
5. Install the libraries required
	- Windows:
		- pip install pandas dash dash_bootstrap_components plotly
	- Linux/Mac:
		- pip3 install pandas dash dash_bootstrap_components plotly
	- Using UV:
		- uv pip install pandas dash dash_bootstrap_components plotly
6. Run the dash app
	- Linux/Mac
		- python3 app.py
	- Windows
		- python app.py
7. Ideally you'll get:
	Dash is running on http://127.0.0.1:8080/

	 * Serving Flask app 'app'
	 * Debug mode: off
	WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
	 * Running on http://127.0.0.1:8080
	Press CTRL+C to quit
8. If you get the above, 
	- just copy the URL to the browser.
	- Or just ctrl/cmd+click on the link.
	It'll open the app

## About the code:
