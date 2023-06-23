# About the project
This is a Flask project that demonstrates a simple web application built using the Flask framework. This is a client/server components that the server-side is done in this project

This project involves the development of a web-based spatial decision support system designed to assist doctors and policymakers in assessing the risk level of Ambient Gamma Dose Rate (AGDR) in Germany. The purpose of this application, developed as a master's thesis project titled "Designing and Evaluating a Web Spatial Decision Support System for Spatial Problem Solving," provides a comprehensive tool for analyzing and visualizing gamma ambient dose rate data. The system is evaluated using this application, which has been specifically commissioned by the Bundesamt für Strahlenschutz (BfS).

In order to assess the potential risk posed by elevated AGDR levels, one approach is to demonstrate that the increase in AGDR is caused by external factors and remains within a safe range. According to a report from BfS, under natural circumstances, AGDR can experience a temporary increase of up to twice its normal level when radioactive decay products of radon are washed out of the atmosphere by precipitation and subsequently deposited on the ground.

The objective of this project is to provide medical professionals and policymakers with valuable insights regarding AGDR risk levels. This is accomplished by employing advanced data mining techniques to establish a definitive relationship between AGDR and precipitation.

AGDR data was collected by BfS measurement stations. Collaboratively with Germany's National Meteorological Service, precipitation data has been obtained from weather radar technology provided by BfS. Both datasets are time series. We have assessed the relationship between AGDP and precipitation, as well as precipitation occurring two hours prior (considering the time series nature of the data and the possibility of a 2-hour delay on AGDR) and seasonal effects. The findings demonstrate promising correlations. Utilizing these data mining discoveries, an interactive and user-friendly platform has been developed as a predictive and simulation model. This platform empowers doctors and policymakers to make well-informed decisions by examining these results.


The data mining phase has been done in a project with the following adress:
---------------

the client side can be found via this adress:
---------------

## Installation

1. Clone the repository:

git clone https://github.com/your-username/flask-project.git

2. Change into the project directory:

cd flask-project

3. Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate

4.Set up the database:

Create a new database in  PostgreSQL
Update the database connection details

5.Run the application:

flask run

##License

This project is licensed under the MIT License.