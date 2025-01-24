# README

### This contains the following information"
1. How to setup and run the code
2. The code itself, where and how it was used and written.
   1. More details can be found by following the git history of the project using this link:
   2. https://github.com/Aniket-Mishra/JBI100_Visualisation/commits/main/

## Getting the code
#### If Github:
Code location:
https://github.com/Aniket-Mishra/JBI100_Visualisation

- It is a private repo. I've temporarily made it public to show the history of the code.
- Can add access if needed for the future. I do not wish to keep this public as it can be used by future students.
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

Description: Initially I implemented the whole app using Python, Streamlit, and plotly. It was completely on my own, except some syntax things from my previous projects and google. I reused a lot of my old code.
Source: I have been using streamlit and plotly for over 5 years now. I am quite comfortable with my libraries of choice.

#### Pandas code - References:
The pandas code is completely my own albeit some googling for some syntax here and there. I have 4+ years of professional experience in Python, dealing with ETL pipelines, mostly using pandas and polars.
Example personal projects to prove track record (NDA on professonal code):
1. https://github.com/Aniket-Mishra/exploration_of_data
2. https://github.com/Aniket-Mishra/playing-with-data
3. https://github.com/Aniket-Mishra/Sales-Analysis-and-Reporting

#### Plotly code - References:
I have prior experience in plotly, proven by the git history of the projects provided below. I used them as reference for graphs and data manipulation/analysis and the plotly code:
1. https://github.com/Aniket-Mishra/playing-with-data
2. https://github.com/Aniket-Mishra/data_science_tasks/tree/main/

#### The app itself - References
Unfortunately Streamlit no longer supports brushiung (Through a 3rd party library). So I had to move my code and rebuild the whole thing using Dash. For that, I referred to multiple youtube playlists, and github repos, stactoverflow, and other projects. They are added to references to my report as well.
1. Multiple Dash projects: https://www.youtube.com/playlist?list=PLAOxwF8Hem-DwvdkUGqY8pe1AW0Exodli
2. Advanced callbacks along with deployment: https://www.youtube.com/playlist?list=PLYD54mj9I2JevdabetHsJ3RLCeMyBNKYV
3. Video that got me started: https://www.youtube.com/watch?v=hSPmj7mK6ng&ab_channel=CharmingData
4. Referred template: https://github.com/Coding-with-Adam/Dash-by-Plotly/tree/master/Other/Dash_Introduction

