# beyond-resume <br>
__A Machine Learning Based Approach for Hiring Qualified Individuals__<br>
This implementation profits both the employer and the applicant. Below are some the key highlights of the implmentation - 
* MongoDB based backend provides seamless and fast querying and information retrieval
* An enhanced job-descrition to cater to other possible areas of expertise which might be closely linked to the ones mentioned in the description.
* A comparative measure of applicants abilities and skills with the requirements of the position.
* A Flask based web application which has been integrated with both Python and MongoDB.

## Data Gathering, Pre-processing and Backend Development
The data was gathered for 4 types of job description - 
* Data Scientist
* Data Engineer
* Software Engineering
* Quantitative Analyst

Some key steps involved in this process include - 
* The job descriptions were filtered for keywords and their related vocabulary through web-scrapping
* The data was stored in the form of a Graph where each node is linked with its related vocabulary words e.g. Deep Learning is linked with Neural Networks

## Applicant Evaluation and Front-end Development
Using the data gathered, we perform the following measures of evaluation of an applicant - 
* Based on the applicant skills and how closely it is related to the skills identified from the job description, we provide a score to their skills through topological measures of network analysis
* The top 15 skills of the applicant which align with the job description are returned
__Skills pertaining to the Data Science Job Description__<br>
![Sample Plot](https://github.com/srish28/beyond-resume/blob/dev/templates/sample_plot.png)

## Applicant Friendly Features
* The web application lets the applicant know if there is a very low match between his expertise and the job's required skill-set.
* Based on the applicant's skills, the application is capable of suggesting other jobs which are in the system which are a better match to their skill-set

## Conclusion
Some of the key points which can be inferred from our development are - 
* The development is highly scalable with its ability to improve based on the dataset used to create the backend using NLP and Textual data mining techniques.
* The backend for this application can be made lighter with the envolvement of AI based recommendation system
