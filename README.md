# SQLAlchemy-Challenge
### Brief description of the project:

> Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area. you’ll use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib to do the following:

## Analyze and Explore the Climate Data

- Used the SQLAlchemy create_engine() function to connect to the SQLite database
- Used the SQLAlchemy automap_base() function to reflect tables into classes, and then saved references to the classes
- Linked Python to the database by creating a SQLAlchemy session
- Performed a precipitation and a station analysis

## Precipitation Analysis

- Found the most recent date in the dataset
- Retrieved the previous 12 months of precipitation data by querying the previous 12 months of data
- Selected only the "date" and "prcp" values
- Loaded the query results into a Pandas DataFrame and set the column names
- Sorted the DataFrame values by "date"
- Ploted the results by using the DataFrame plot method
- Used Pandas to print the summary statistics for the precipitation data

## Station Analysis

- Designed a query to calculate the total number of stations in the dataset.
- Designed a query to find the most-active stations
    - Listed the stations and observation counts in descending order
- Designed a query that calculated the lowest, highest, and average temperatures that filters on the most-active station id found
- Designed a query to get the previous 12 months of temperature observation (TOBS) data
    - Filtered by the station that has the greatest number of observations
    - Queried the previous 12 months of TOBS data for that station
    - Plotted the results as a histogram
## Design a simple Climate App using Flask API

- Created a homepage route that lists all available routes
- Created a precipitation route that converts the query results from the precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value, and is returned in JSON format
- Created a stations route that returns a JSON list of stations from the dataset
- Created a tobs route that queries the dates and temperature observations of the most-active station for the previous year of data, and is returned in JSON format
- Created a user-input route that takes a specified start date, calculates TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date, and is returned in JSON format
- Created a user-input route that takes a specified start date and end date, calculates TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive, and is returned in JSON format