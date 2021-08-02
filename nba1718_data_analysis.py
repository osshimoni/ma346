"""
Osher Shimoni
Professor Chow - MA 346
26 April 2021
Final Project

This project uses data from the NBA 2017-2018 season an analyzes player statistics and salaries
"""

import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'
import researchpy as rp
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

### Importing the Data

# The following code reads each csv datafile and saves them into their respective pandas dataframe.
# The nbastats data was gathered from BasketballReference and the salary data was gathered from Kaggle.
# I personally created the teams data file.
stats = pd.read_csv('nbastats.csv', encoding="ISO-8859-1", engine='python')
salary = pd.read_csv('salary.csv', encoding="ISO-8859-1", engine='python')
teams = pd.read_csv("teams.csv")
# Each data file is now saved into a pandas dataframe using an appropriate name

# I noticed that the longitude values in the teams dataset were all inverted. This code inverts
# each longitude value by multiplying it by -1.
teams["longitude"] = teams["longitude"] * (-1)
# Each longitude value in the teams dataframe is now inverted so that its mapping point will be
# properly placed on the map.

### Data Cleaning

# The following code removes the backslashes from each of the player's names in the Player column
# of the stats dataframe. It does so by looping through each record in the stats dataframe. It looks
# at the Player column for each record and sets it equal to a substring that takes the beginning
# of each player name up to the backslash. This is necessary to be able to merge this dataframe with
# the other datafarmes in this project
for i in range(len(stats.index)):
    stats["Player"][i] = stats["Player"][i][:stats["Player"][i].index("\\")]
# Each player name is now saved as the original data minus everything after the backslash which
# included the player's social media profile names. Now, this code can be used to merge the stats
# dataframe with the other dataframes being used in this project.

# This code merges the salary dataframe with the stats dataframe using the Player column. Both of these
# dataframes contain the player names of all NBA players from the 2017-2018 season. Thus, we can use this
# similar data to combine the dataframes. This joint dataframe is saved into the dataframe "df".
df = stats.merge(salary, on="Player")
# The variable "df" now contains the joint dataframe of the stats data and the player salary data.
# Each record in this dataframe now contains each player's name, stats, and their salary.

# The following code merges the teams dataframe with the df dataframe that was created above.
# The teams dataframe contains a list of all of the NBA teams, along with their conference (east, west)
# and the city's latitude and longitude. This code only merges the team and conference data. It uses the
# "Tm" (team) variable to merge the dataframes as each dataframe contains the team data.
df = df.merge(teams[["Tm", "Conference"]], on="Tm")
# The variable "df" now contains the full dataset where each record contains the player name, their stats
# their salary, and their conference.

# I noticed that the salary column had an inconvenient name. This code renames the salary column to be
# more practical when being referenced in analysis. It uses the rename function to rename the column to "Salary"
df = df.rename(columns={"season17_18": "Salary"})

# I noticed that many players had NaN values in their shooting percentages when they did not
# attempt any field goals, free throws, or three pointers. The following code uses the fillna()
# function to replace all NaN values with 0 as not taking any three pointers is as good as not making any.
df = df.fillna(0)
# The dataframe no longer has any NaN values. Instead, all NaN values now hold value 0. This
# prevents any complication in analysis when performing math on the data.

# I noticed an unnecessary, unreconizable column. The following code drops the column by setting
# df equal to df after dropping the column.
df = df.drop(columns=["Unnamed: 0"])
# The df dataframe no longer contains this column.

# The following code creates a new variable called "Age_Group". This variable classifies each player
# into their respective age group. The bins variable holds the values at which to split the groups.
# The labels variable holds the respective bin name for each bin. There are 7 age groups starting at
# 18 and going by 3-year-increments. The final bin is 36+ which holds all players aged 36 and over.
# This code uses the pd.cut() command to classify the records based on their Age value and using the bins
# and labels data created below.
bins = [18, 21, 24, 27, 30, 33, 36, df["Age"].max()]
labels = ["18-21", "21-24", "24-27", "27-30", "30-33", "33-36", "36+"]
df["Age_Group"] = pd.cut(df["Age"], bins=bins, labels=labels, right=False)
# Each record now contains Age_Group data which classifies them into their respective age group based on
# their Age.


# The following code uses the pd.to_csv() command to export the df dataframe into a csv file.
# This file can now be explored/edited externaly from PyCharm in a workbook program such as Excel
df.to_csv('full_nba_data.csv')
# the df dataframe is now saved in the environment and on the machine as "full_nba_data" as a csv file.

# The following data makes a copy of the df dataframe and saves it as df2. The df2 dataframe
# will only contain the numerical information for each record. This code also creates a "mean"
# record in this dataframe which saves the mean value for each variable in this dataframe.
# Now, this record can be used to compare individual player statistics with league mean statistics.
# Lastly, this code drops the columns that contain NaN values so as to avoid any calculation errors.
df2 = df.copy()
df2 = df2.drop(columns=["Player", "Pos", "Tm", "Conference", "Age_Group"])
df2.loc['mean'] = df2.mean()
df2 = df2.dropna(axis="columns")
# The df2 dataframe now contains all of the numerical data for each player, as well as a mean record
# which contains the average statistics for each variable.


# The following code begins the dashboard creation:
### Streamlit

def main():
    # The following code creates a title and subheader on the sidebar to describe the project.
    st.sidebar.title("NBA Player Statistics")
    st.sidebar.subheader("2017-2018 Season")
    # The streamlit dashboard now hsa a title that says "NBA Player Statistics" and a subheader
    # that describes that this data refers to the NBA data from the 2017-2018 season.

    # The following data creates a dropdown menu where the user can select how they would like to
    # interact with the data. The options include "Home", "Individual Player Statistics", "League Statistics Visualizations",
    # and "East vs West Hypothesis Testing". Each option takes them to a new page in the streamlit dashboard.
    option = st.sidebar.selectbox("Select an Option", (
        "Home", "Individual Player Statistics", "League Statistics Visualizations", "East vs West Hypothesis Testing"))
    # There is now a dropdown menu on the sidebar of the dashboard that allows th euser to navigate the
    # project dashboard.

    # The first option is the default option which is titled "Home". If the user is selecting the
    # Home option, the dashboard will display a title that displays the selected option title. It
    # also displays a subheader and a map.
    if option == "Home":
        st.title("Home")

        # Provide a link to the project reort
        st.subheader("Please Read: Link to [Project Report](https://www.scribd.com/document/518485833/Osher-Shimoni-NBA-2017-18-Data-Project-Report)")
        st.write()
        
        # The following code creates a map that displays a point where on a global map where there
        # exists an NBA team. It uses the teams data which contains longitude and latitude information
        # for each NBA city.
        st.subheader("NBA Teams Map")
        st.map(teams)
        # The map is displayed on the home page with a red point at the exact longitude and latitude
        # for each team in the NBA.

    # If the user selects the Individual Player Statistics option, they can view an individual player's
    # statistics and compare it to the league average statistics.
    if option == "Individual Player Statistics":

        st.subheader("Player Statistics vs League Averages")

        # The following code uses the st.text_input() function to gather a text input from the user.
        # The user can input a player's name and this string will get saved to the name variable to be
        # used in filtering the dataframe by this name.
        name = st.text_input("Enter a Player Name")

        # If the player name is a valid player name, it will display a title for the table using the
        # player's name. For example, it may say "Stephen Curry Individual Statistics". If invalid,
        # it will not display a title.
        if name in df["Player"]:
            st.write("**" + name + " Individual Statistics**")

        # The following code filters the df dataframe using the name variable that was gathered
        # from the user input. It will print all of the data for the record whose name in the
        # Player column matches the player name that the user inputted.
        st.write(df[df["Player"] == name].astype('object'))

        # The following code uses the mean values record that was created in the df2 dataframe
        # to print the league mean statistics to be compared with an individual player's statistics.
        # Because the mean record is the last in the df2 dataframe, it uses the tail() function
        # to display the last record in the df2 dataframe.
        st.write("**League Mean Statistics**")
        st.write(df2.tail(1))
        # The dashboard now displays a table of the average statistics across the entire league. It may
        # also display a table of an individual player's statistics if a valid name is inputted.

    # The following code performs the appropriate code related to the "League Statistics Visualizations"
    # option in the dashboard interaction options drop down menu.
    if option == "League Statistics Visualizations":

        # The following code presents a drop-down menu so that the user can select what type
        # of visualization they would like to produce. The options are histogram, boxplot, and heatmap.
        # The option they select is saved into the chart variable.
        chart = st.sidebar.selectbox("Select a Chart to View", ("Histogram", "Boxplot", "Heatmap"))

        # If the user selects histogram, a new dropdown is presented which presents the list of variables
        # that the user can select to view as a histogram from the df2 (numerical data) dataframe.
        if chart == "Histogram":
            stat = st.sidebar.selectbox("Select a Stat to Visualize", (df2.columns))
            # The statistic that the user selects is saved into the stat variable which allows us
            # to grab this statistic from the dataframe by using it in column-selection.

            # Another dropdown is presented which is a filter option. The user can choose
            # to filter the data by player position.
            filter = st.sidebar.selectbox("Filter By", ["None (League-wide)", "Position"])
            # The option they select is saved into the filter variable.

            # If the user chooses not to select a filter, the histograms will be of
            # league-wide data. To create the histograms, I use the seaborn package's sns.histplot()
            # function on the df2 dataframe using the column that the user was interested in, gathered above
            # in the stat variable.
            if filter == "None (League-wide)":
                fig, ax = plt.subplots()
                sns.histplot(df2[stat])
                ax.set_title("Histogram of '" + stat + "' Variable")
                st.write(fig)

            # If the user chooses to filter the data by position, a new dropdown menu will appear
            # which allows them to select which position they would like to view the data by, using
            # the unique() function to dipslay the unique values of the Pos (position) column in the df dataframe.
            # The position they choose is saved into the position variable.
            elif filter == "Position":
                position = st.selectbox("Select a Position", (df.Pos.unique()))
                fig, ax = plt.subplots()

                # The following code uses the histplot() function to generate a histogram of the variable
                # of interest, filtering by the position that was gathered above in the position variable.
                sns.histplot(df[df["Pos"] == position][stat])

                # The following code creates a title for the histogram using the variables gathered above to
                # give a more descriptive title.
                ax.set_title("Histogram of '" + stat + "' Variable Among Position '" + position + "'")
                st.write(fig)

        # If the user chooses to view a heatmap of the data, the following code runs. This code uses
        # the seaborn package's heatmap() function to create a correlation matrix of the data.
        if chart == "Heatmap":
            st.subheader("Correlation Matrix of Stat Variables")
            fig, ax = plt.subplots()
            sns.heatmap(df2.corr(), ax=ax, cmap="rocket")
            st.write(fig)
            # Using this heatmap, we can view how each variable is correlated with the other variables
            # in the dataset.

        # If the user chooses to select the boxplot visualization option, the following code will run.
        if chart == "Boxplot":
            # A dropdown menu will appear which asks the user to select which statistic they
            # would like to he chart by taking the column names in the df2 (numerical data) dataframe.
            # This is saved into the stat variable.
            stat = st.sidebar.selectbox("Select a Stat to Visualize", (df2.columns))

            # A second dropdown menu is presented which offers options for the user to group the boxplots
            # The options are position, team, and age group.
            filter = st.sidebar.selectbox("Group By", ["Pos", "Tm", "Age_Group"])
            fig, ax = plt.subplots()
            ax.set_title("Boxplot of '" + stat + "' Variable by '" + filter + "'")
            sns.boxplot(x=df[stat], y=df[filter])
            st.write(fig)
            # Using this boxplot feature, the user can view how the summary statistics for each variable
            # changes across different factors.

    # If the user selects the "East vs West Hypothesis Testing" option in the dashboard's interaction
    # options dropdown menu, the following code will run. It performs a statistical hypothesis test
    # to view if a variable is statistically different between the eastern and western conferences.
    if option == "East vs West Hypothesis Testing":

        # A dropdown menu is presented which allows the user to select any variable they would like
        # to test by taking the columns of the df2 dataframe. This selection is saved in the stat variable.
        stat = st.selectbox("Select a Stat to Compare Between the Eastern and Western Conferences", (df2.columns))

        # A boxplot of this variable grouped by the two conferences is generated
        fig, ax = plt.subplots()
        sns.boxplot(x=df2[stat], y=df["Conference"])
        st.write(fig)
        # The user has a visualization of the difference in means between the two conferences for
        # the variable that they selected.

        ### T-test

        # The following code saves the respective data for the stat that was selected above
        # for the eastern and western conferences. It does so by filtering the dataframe by each
        # conference and using numpy array to save the data into an array.
        east_data, west_data = (np.array(df[df["Conference"] == "East"][stat])), np.array(
            df[df["Conference"] == "West"][stat])
        # The east_data and west_data variables contain the data for the variable that the user selected above
        # filtered respectively by each conference.

        # The following code displays a subheader that gives a title for the hypothesis testing section
        st.subheader("**Hypothesis Test: Is the '" + stat + "' Variable Significantly Different "
                                                            "between the Eastern and Western Conference?**")

        # This code displays the null and alternative hypothesis using the variable that the user selected.
        st.write(
            "**Null Hypothesis:** '" + stat + "' Variable Mean is Equivalent Between the Eastern and Western Conferences.")
        st.write(
            "**Alternative Hypothesis:** '" + stat + "' Variable Mean is Significantly Different Between the Eastern and Western Conferences.")
        st.write("**Alpha Level of Significance:** 0.05")

        # The following code uses the researchpy package to perform a t-test to test
        # whether the means for the selected stat are significantly different between the eastern and
        # western conferences. It saves the summary and results of the test into the summary and results
        # variables.
        summary, results = rp.ttest(group1=df[stat][df['Conference'] == 'East'], group1_name="East",
                                    group2=df[stat][df['Conference'] == 'West'], group2_name="West")

        # The following code displays the relevant information from the results and summary tables such
        # as the t-statistic and p-value, and the means for each group,
        st.table(results[0:4])
        st.table(summary.iloc[0:2, [0, 2, 1]])

        # The following code creates a conclusion for the test. It saves the alpha level of significance
        # of 0.05 into the ALPHA variable to be used in comparison with the p-value. It also saves
        # the p-value into the p_value variable by grabbing the proper cell from the results table.
        ALPHA = 0.05
        p_value = results.iloc[3, 1]

        # Bolded conclusion header
        st.subheader("**Conclusion**")

        # If the p-value is less than alpha, we reject the null hypothesis. The code tells the user
        # that we reject the null hypothesis and that the mean of the statistic that was selected by the user
        # is significantly difference between the East and West conferences.
        if p_value < ALPHA:
            st.write("**Reject the null hypothesis**")
            st.write(
                "The '" + stat + "' variable is signifncantly different between the Eastern and Western conferences.")

        # If the p-value is not lower than the alpha level of significance, we fail to reject the null
        # hypothesis. The code tells the user that we fail to reject the null hypothesis and that
        # the mean of the selected statistic is not significantly different between the East and West
        # conferences.
        else:
            st.write("**Fail to reject the null hypothesis**")
            st.write(
                "The '" + stat + "' variable is not signifncantly different between the Eastern and Western conferences.")


main()
