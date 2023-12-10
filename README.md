# Phonepe-Pulse-Data-Visualization-and-Exploration
Data visualization involves presenting data in a visually engaging manner through charts, graphs, and other visual elements. Its purpose is to enhance comprehension and analysis by presenting information in an aesthetically pleasing and easily understandable format. By utilizing these visualizations, users can swiftly comprehend trends, patterns, and valuable insights from their transaction history.

# Problem Statement:
The Phonepe pulse Github repository contains a large amount of data related to various metrics and statistics.The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.

# Approach:

**Data Extraction:**
To begin, we will clone the Github repository for Phonepe pulse using scripting. This will allow us to fetch the necessary data and store it in a suitable format, such as CSV or JSON.

**Data Transformation:**
Next, we will utilize a scripting language like Python, along with libraries like Pandas, to manipulate and preprocess the data. This step involves tasks such as cleaning the data, handling any missing values, and transforming the data into a format that is suitable for analysis and visualization.

**Database Insertion:**
Using the "mysql-connector-python" library in Python, we will establish a connection with a MySQL database. Through SQL commands, we will insert the transformed data into the database.

**Dashboard Creation:**
To create an interactive and visually appealing dashboard, we will employ the Streamlit and Plotly libraries in Python. Plotly's built-in geo map functions will enable us to display the data on a map, while Streamlit will allow us to develop a user-friendly interface. The dashboard will offer multiple dropdown options for users to select different facts and figures they wish to view.

**Data Retrieval:**
To update the dashboard dynamically, we will once again use the "mysql-connector-python" library to connect to the MySQL database. By fetching the data into a Pandas dataframe, we can utilize the information within to keep the dashboard up to date.

**Deployment:**
In this final step, we will ensure that the solution is secure, efficient, and user-friendly. Thorough testing will be conducted to guarantee its functionality. Once complete, the dashboard will be deployed publicly, making it accessible to users.

# Technologies:
**• Github Cloning**

**• Python**

**• Pandas**

**• MySQL**

**• Streamlit**

**• Plotly**

# Dashboard:
It includes details about the Visualisation of Data on the Homepage include GEO MAP Visualisation

**ANALYSIS:**

It offers data based on States, all of India, and the top categories.

It analysis under these based on User and Transaction data for every category.

Information is given according to the **year and Quarter**

**INSIGHTS:** 

From the analysis, a set of fundamental insights were presented in an approachable way.



