# Importing Libraries
import pandas as pd
import pymongo
import streamlit as st
import seaborn as sns
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import os

# Setting up page configuration
icon = Image.open("airbnb_logo.png")
st.set_page_config(page_title="Airbnb Data Visualization | By Ponishadevi",
                   page_icon=icon,
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={'About': """# This dashboard app is created by *Ponishadevi*!
                                        Data has been gathered from mongodb atlas"""})

# Creating option menu in the sidebar
with st.sidebar:
    selected = option_menu("Menu", ["Home", "Overview", "Explore"],
                           icons=["house", "graph-up-arrow", "bar-chart-line"],
                           menu_icon="menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px",
                                               "--hover-color": "#FF5A5F"},
                                   "nav-link-selected": {"background-color": "#FF5A5F"}}
                           )

# CREATING CONNECTION WITH MONGODB ATLAS AND RETRIEVING THE DATA
client = pymongo.MongoClient("mongodb+srv://ponishadevi:1234@cluster0.cmfx4pr.mongodb.net/?retryWrites=true&w=majority")
mydb = client["sample_airbnb"]
col = mydb["listingsAndReviews"]

# READING THE CLEANED DATAFRAME
df = pd.read_csv('Airbnb_data.csv')

# HOME PAGE
# HOME PAGE
if selected == "Home":
    

    # Title and Banner with Rainbow Color
    st.title(':rainbow[Explore Airbnb Insights] 🏡')

    # Minimize the size of the image
    st.image("airbnb_banner.jpg", width=300)
    st.balloons()
    # Project Overview
    st.markdown("## :blue_book: Airbnb Data Analysis Project Overview")
    st.write("Welcome to the Airbnb Data Analysis project! Delve into the extensive world of Airbnb data and uncover valuable insights through thorough analysis and visualization.")

    # Project Objectives
    st.markdown("## :dart: Project Objectives")
    st.write("1. **Analyze Pricing:** Explore pricing variations in Airbnb listings.")
    st.write("2. **Visualize Availability:** Create visualizations for availability patterns and occupancy rates.")
    st.write("3. **Location-based Insights:** Investigate trends and insights based on locations.")
    st.write("4. **Interactive Visualizations:** Develop interactive maps and dynamic visualizations for a comprehensive exploration.")

    # Technologies Used
    st.markdown("## :computer: Technologies Used")
    st.write("Python, Streamlit, MongoDB, Tableau or Power BI")

    # Get Started
    st.markdown("## :rocket: Get Started")
    st.write("Navigate through the project sections using the sidebar. Explore pricing trends, availability patterns, and location-based insights. Have a data-driven journey!")

    # Collaboration and Learning
    st.markdown("## :handshake: Collaboration and Learning")
    st.write("This project is an opportunity to enhance skills in Python scripting, data preprocessing, visualization, exploratory data analysis (EDA), Streamlit, MongoDB, and PowerBI or Tableau.")

    # Note
    st.markdown("Note: Make sure to check the sidebar for various sections and analyses.")


# OVERVIEW PAGE
# OVERVIEW PAGE
if selected == "Overview":
    # Sidebar for user input
    st.markdown("## DATA OVERVIEW")
    countries = df['Country'].unique()
    property_types = df['Property_type'].unique()
    room_types = df['Room_type'].unique()

    # Sidebar for user input
    selected_countries = st.sidebar.multiselect('Select Countries', countries, countries)
    selected_property_types = st.sidebar.multiselect('Select Property Types', property_types, property_types)
    selected_room_types = st.sidebar.multiselect('Select Room Types', room_types, room_types)

    # RAW DATA TAB
    with st.expander("Raw Data"):
        # RAW DATA
        if st.button("Click to view Raw data"):
            raw_data = col.find_one()
            st.write(raw_data)

    # Filter data based on user selection
    price = st.slider('Select Price', df.Price.min(), df.Price.max(), (df.Price.min(), df.Price.max()), key='price_slider')
    filtered_df = df[(df['Country'].isin(selected_countries)) &
                    (df['Property_type'].isin(selected_property_types)) &
                    (df['Room_type'].isin(selected_room_types)) &
                    (df['Price'] >= price[0]) & (df['Price'] <= price[1])]

    # Display the filtered data
    # st.write("Filtered Data:")
    # st.write(filtered_df)
    filtered_df['Price_Percentage'] = (filtered_df['Price'] / filtered_df['Price'].max()) * 100
    # Map Visualization
    fig = px.scatter_geo(filtered_df,
                         lat='Latitude',
                         lon='Longitude',
                         color='Price_Percentage',
                         hover_data=['Country', 'Property_type', 'Room_type','Price_Percentage'],
                         title=f'Geo Visualization for {", ".join(selected_countries)} - {", ".join(selected_property_types)} - {", ".join(selected_room_types)}',
                         color_continuous_scale='Viridis')

    # Example: Change color based on different conditions
    threshold_price = 4
    condition_color = 'gray'  # Default color if no condition is met
    if filtered_df['Price_Percentage'].max() > threshold_price:  # Change the condition as needed
        condition_color = 'red'

    # Calculate the price percentage
    

    fig.update_traces(marker=dict(color=filtered_df['Price_Percentage'], cmin=0, cmax=100))

    # Display the price as a percentage of the maximum price
    fig.update_layout(coloraxis_colorbar=dict(title='Price (%)'))

   # Update hover template to display actual price and percentage
    #fig.update_traces(hovertemplate='%{hovertext}<br>Price: $%{customdata[0]:.2f}, %{customdata[1]:.2f}% of max price',
                  #customdata=filtered_df[['Price', 'Price_Percentage']])

    # Increase dot size
    fig.update_traces(marker=dict(size=20))  # Adjust the size value as needed

    fig.update_geos(projection_type="natural earth")
    st.plotly_chart(fig, use_container_width=True)


    # DATAFRAME FORMAT TAB
    with st.expander("DataFrame"):
        # DATAFRAME FORMAT
        if st.button("Click to view Dataframe"):
            st.write(df)

        # GETTING USER INPUTS
        price = st.slider('Select Price', df.Price.min(), df.Price.max(), (df.Price.min(), df.Price.max()))

        # CONVERTING THE USER INPUT INTO QUERY
        query = f'Price >= {price[0]} & Price <= {price[1]}'

        # CREATING COLUMNS
        col1, col2 = st.columns(2, gap='medium')

        with col1:
            # TOP 10 PROPERTY TYPES BAR CHART
            df1 = df.query(query).groupby(["Property_type"]).size().reset_index(name="Listings").sort_values(
                by='Listings', ascending=False)[:10]
            fig = px.bar(df1,
                         title='Top 10 Property Types',
                         x='Listings',
                         y='Property_type',
                         orientation='h',
                         color='Property_type',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)

            # TOP 10 HOSTS BAR CHART
            df2 = df.query(query).groupby(["Host_name"]).size().reset_index(name="Listings").sort_values(
                by='Listings', ascending=False)[:10]
            fig = px.bar(df2,
                         title='Top 10 Hosts with Highest number of Listings',
                         x='Listings',
                         y='Host_name',
                         orientation='h',
                         color='Host_name',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
            df1 = df.query(query).groupby(["Room_type"]).size().reset_index(name="counts")
            fig = px.pie(df1,
                         title='Total Listings in each Room_types',
                         names='Room_type',
                         values='counts',
                         color_discrete_sequence=px.colors.sequential.Rainbow
                         )
            fig.update_traces(textposition='outside', textinfo='value+label')
            st.plotly_chart(fig, use_container_width=True)

            # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
            country_df = df.query(query).groupby(['Country'], as_index=False)['Name'].count().rename(
                columns={'Name': 'Total_Listings'})
            fig = px.choropleth(country_df,
                                title='Total Listings in each Country',
                                locations='Country',
                                locationmode='country names',
                                color='Total_Listings',
                                color_continuous_scale=px.colors.sequential.Plasma
                                )
            st.plotly_chart(fig, use_container_width=True)

# Explore Data Page
if selected == "Explore":
    st.markdown("## Explore more about the Airbnb data")

    # File Upload
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

        # Check if file is uploaded
    if uploaded_file is not None:
        # Read data from uploaded file
        df = pd.read_csv(uploaded_file)

        # Get user inputs
        country = st.sidebar.selectbox('Select Country', df["Country"].unique())
        prop = st.sidebar.multiselect('Select a Property_type', sorted(df.Property_type.unique()), sorted(df.Property_type.unique()))
        room = st.sidebar.multiselect('Select Room_type', sorted(df.Room_type.unique()), sorted(df.Room_type.unique()))
        price = st.slider('Select Price', df.Price.min(), df.Price.max(), (df.Price.min(), df.Price.max()))

        # CONVERTING THE USER INPUT INTO QUERY
        # Use "isin" for a list of room types
        query = f'Country == "{country}" & Room_type.isin(@room) & Property_type.isin(@prop) & Price >= {price[0]} & Price <= {price[1]}'

        # Filter data based on user inputs
        filtered_df = df.query(query)

        st.write("Filtered Data:")
        st.write(filtered_df)
        # HEADING 1
        st.markdown("## Price Analysis")


        # CREATING COLUMNS
        col1, col2 = st.columns(2, gap='medium')

        with col1:
            # AVG PRICE BY ROOM TYPE BARCHART
            pr_df = df.query(query).groupby('Room_type', as_index=False)['Price'].mean().sort_values(by='Price')
            # Assuming 'Room_type' column has three unique values: 'Entire home/apt', 'Private room', 'Shared room'
            dark_colors = px.colors.qualitative.Dark24  # Dark color palette

            # Create a custom color map for each room type
            custom_colors_map = {
                'Entire home/apt': dark_colors[0],
                'Private room': dark_colors[1],
                'Shared room': dark_colors[2]
            }

            fig = px.bar(data_frame=pr_df,
                        x='Room_type',
                        y='Price',
                        color='Room_type',  # Use 'Room_type' for color mapping
                        title='Avg Price in each Room type',
                        color_discrete_map=custom_colors_map
                        )
            st.plotly_chart(fig, use_container_width=True)
            # HEADING 2
            st.markdown("## Availability Analysis")

            # AVAILABILITY BY ROOM TYPE BOX PLOT
            fig = px.box(data_frame=df.query(query),
                         x='Room_type',
                         y='Availability_365',
                         color='Room_type',
                         title='Availability by Room_type'
                         )
            st.plotly_chart(fig, use_container_width=True)


            fig = px.scatter(data_frame=df.query(query),
                         x='Country',y='Price',
                        color='Country',
                        size='Price',
                        opacity=1,
                        size_max=35,
                        title='Avg Listing Price in each Countries')
            st.plotly_chart(fig, use_container_width=True)


           

            # Scatter plot - Average Price vs Number of Reviews by Room Type
            scatter_df = df.query(query).groupby('Room_type', as_index=False).agg({'Price': 'mean', 'No_of_reviews': 'sum'})
            fig_scatter = px.scatter(scatter_df, 
                                    x='Price', 
                                    y='No_of_reviews', 
                                    color='Room_type',
                                    size='No_of_reviews',
                                    title='Average Price vs Number of Reviews by Room Type',
                                    labels={'Price': 'Average Price', 'No_of_reviews': 'Number of Reviews'}
                                    )
            st.plotly_chart(fig_scatter, use_container_width=True)



             




        with col2:
            # AVG PRICE IN COUNTRIES SCATTERGEO
            country_df = df.query(query).groupby('Country', as_index=False)['Price'].mean()
            fig = px.choropleth(filtered_df,
                            locations='Country',
                            locationmode='country names',
                            color='Price',
                            hover_data=['Price'],
                            title=f'Avg Price in {country}',
                            color_continuous_scale='agsunset'
                            )
            fig.update_geos(projection_type="natural earth")
            col2.plotly_chart(fig, use_container_width=True)
            # BLANK SPACE
            st.markdown("#   ")
            st.markdown("#   ")

            # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
            country_df = df.query(query).groupby('Country', as_index=False)['Availability_365'].mean()
            country_df.Availability_365 = country_df.Availability_365.astype(int)
            fig = px.choropleth(filtered_df,
                            locations='Country',
                            locationmode='country names',
                            color='Availability_365',
                            hover_data=['Availability_365'],
                            title=f'Avg Availability in {country}',
                            color_continuous_scale='agsunset'
                            )
            fig.update_geos(projection_type="natural earth")
            st.plotly_chart(fig, use_container_width=True)

            
             # Assuming 'Property_type' is the additional column you want to include

            # Room Type and Property Type Distribution Nested Pie Chart with Dark Colors
            nested_pie_data = filtered_df.groupby(['Room_type', 'Property_type']).size().reset_index(name='count')

            dark_colors = px.colors.qualitative.Dark24  # Replace with any dark color palette you prefer

            fig = px.sunburst(nested_pie_data, 
                            path=['Room_type', 'Property_type'], 
                            values='count',
                            title='Room Type and Property Type Distribution',
                            color_discrete_sequence=dark_colors
                            )
            st.plotly_chart(fig, use_container_width=True)


            # Calculate average review score and add it to the DataFrame
            filtered_df['Average Review Score'] = filtered_df['Review_scores'].mean()

            # Check if 'Average Review Score' is in the DataFrame columns
            if 'Average Review Score' in filtered_df.columns:
                # Add another categorical variable, e.g., 'Room_type', to the histogram
                fig = px.histogram(filtered_df, x='Average Review Score', color='Room_type',
                                title='Review Score Distribution by Room Type',
                                labels={'Average Review Score': 'Review Score'},
                                marginal='box'  # Add box plots to show quartiles
                                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("The column 'Average Review Score' does not exist in the DataFrame.")
            
            
    else:
        # Display a message if no file is uploaded
        st.warning("Please upload a CSV file.")
       
