# A Web-Based Decision Support System for Spatial Problem Solving
This is a Flask project that demonstrates a simple web application built using the Flask framework. The project includes a client/server component, with the server-side implementation covered in this project.

The purpose of this project is to develop a web-based spatial decision support system aimed at assisting doctors and policymakers in assessing the risk level of Ambient Gamma Dose Rate (AGDR) in Germany. The application, developed as a master's thesis project titled 'Designing and Evaluating a Web Spatial Decision Support System for Spatial Problem Solving,' provides a comprehensive tool for analyzing and visualizing gamma ambient dose rate data. This system is evaluated using the specific requirements set forth by the Bundesamt für Strahlenschutz (BfS).

One approach to assessing the potential risk posed by elevated AGDR levels is to demonstrate that the increase in AGDR is caused by external factors and remains within a safe range. According to a report from the BfS, AGDR can experience a temporary increase of up to twice its normal level under natural circumstances when radioactive decay products of radon are washed out of the atmosphere by precipitation and subsequently deposited on the ground.

The objective of this project is to provide valuable insights to medical professionals and policymakers regarding AGDR risk levels. This is achieved by utilizing advanced data mining techniques to establish a definitive relationship between AGDR and precipitation.

AGDR data has been collected from BfS measurement stations, while precipitation data has been obtained from weather radar technology provided by the Bundesamt für Strahlenschutz in collaboration with Germany's National Meteorological Service. Both datasets are time series. We have assessed the relationship between AGDR and precipitation, as well as the impact of precipitation occurring two hours prior (considering the time series nature of the data and the possibility of a 2-hour delay on AGDR) and seasonal effects. The findings demonstrate promising correlations. Based on these data mining discoveries, we have developed an interactive and user-friendly platform that serves as a predictive and simulation model. This platform empowers doctors and policymakers to make well-informed decisions by examining these results.


# The data mining phase has been done in a project with the following address:
 - [GeoODL](https://github.com/zremami/GeoODL.git)

# The client side can be found via this address:
 - [GeoODL_Frontend](https://github.com/zremami/GeoODL_Frontend.git)


## Libraries Used

- There is a list of commonly used libraries with links to their official documentation:

1. SQLAlchemy: A SQL toolkit and Object-Relational Mapping (ORM) library for Python.
   - Documentation: [SQLAlchemy](https://www.sqlalchemy.org/)
   
2. Pandas: A powerful data manipulation and analysis library.
   - Documentation: [Pandas](https://pandas.pydata.org/)

3. Flask: A micro web framework for building web applications in Python.
   - Documentation: [Flask](https://flask.palletsprojects.com/)

4. NumPy: A fundamental package for scientific computing with Python.
   - Documentation: [NumPy](https://numpy.org/)

5. Statistics: A built-in Python library for statistical computations.
   - Documentation: [Statistics](https://docs.python.org/3/library/statistics.html)

6. JSON: A built-in Python library for working with JSON data.
   - Documentation: [JSON](https://docs.python.org/3/library/json.html)

For more details and usage instructions, please refer to the respective library documentation linked above.

## Installation
Follow the steps below to get the project up and running on your local machine:

1. Clone the repository:
   - git clone [https://github.com/zremami/GeoODL_Backend.git]
   
3. Navigate to the project directory:
   - cd your-repo
   
4. Create a virtual environment and activate it:
   - python -m venv venv
   - source venv/bin/activate

5. Set up the database:
   - Create a new database in  PostgreSQL
   - Update the database connection details

6. Run the application.
   - flask run


## Contributing
We welcome contributions to enhance the functionality and features of this project. If you would like to contribute, please follow the guidelines below:

- Fork the repository and clone it to your local machine.
- Create a new branch for your feature or bug fix: `git checkout -b my-feature`.
- Make your changes and test them thoroughly.
- Commit your changes: `git commit -m "Add my feature"`.
- Push your changes to the branch: `git push origin my-feature`.
- Submit a pull request to the `main` branch of this repository.

Please ensure that your pull request adheres to our [code of conduct](CONTRIBUTING.md) and includes a detailed description of the changes you made.

We appreciate your contributions, whether it's through bug reports, feature suggestions, or code contributions. Together, we can improve the Decision Support System and make it even more useful for users.

Thank you to the following contributors who have helped make this project better:

- Zahra Emami ([@zremami](https://github.com/zremami))

If you would like to be included in the list of contributors, please submit your pull request, and your name will be added.


## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).


Feel free to customize and modify the template according to your project's specific details and requirements.

