import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
import plotly.figure_factory as ff
import preprocessor, helper

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = df.astype({'Year': 'str'})
df = preprocessor.preprocess(df, region_df)

st.sidebar.title("Olympics Data Analysis")
st.sidebar.image("https://qph.cf2.quoracdn.net/main-qimg-be47d9970e36f45335eb7ec604f8efb1")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)

# st.dataframe(pf)



if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_tolist(df)
    selected_year = st.sidebar.selectbox("select Year", years)
    selected_country = st.sidebar.selectbox("select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Medal Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + selected_year + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country+"'s Overall Performance in Olympics")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country+"'s Performance in "+ selected_year + " Olympics")

    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Host Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.header("Events")
        st.title(events)
    with col5:
        st.header("Countries")
        st.title(nations)
    with col6:
        st.header("Athletes")
        st.title(athletes)

        st.header(" ")
    st.title("Participation of Nations over time")
    nations_over_time = helper.data_over_time(df, 'region')
    nations_over_time.rename(columns={'region': 'No. of countries'}, inplace=True)
    fig = px.line(nations_over_time, x='Edition', y='No. of countries')
    st.plotly_chart(fig)

    st.header(" ")
    st.title("Number of Events over time")
    events_over_time = helper.data_over_time(df, 'Event')
    fig2 = px.line(events_over_time, x = 'Edition', y = 'Event')
    st.plotly_chart(fig2)

    st.header(" ")
    st.title("Number of Athletes over time ")
    athletes_over_time = helper.data_over_time(df, 'Name')
    athletes_over_time.rename(columns={'Name': 'No. of Athletes'}, inplace=True)
    fig3 = px.line(athletes_over_time, x = 'Edition', y = 'No. of Athletes')
    st.plotly_chart(fig3)

    st.title("No. of Events over time(For Each Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    # ax = plt.figure(figsize=(20,20))
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athlete")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.mostSuccesful(df, selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig4 = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country+ " Medal Tally over the years")
    st.plotly_chart(fig4)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 Athletes of "+ selected_country)
    top10_df = helper.mostSuccesfulAthlete(df, selected_country)
    st.table(top10_df)

if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset={'Name', 'region'})
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False )
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x=[]
    name = []
    famous_sports=['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics','Swimming', 'Badminton', 'Sailing', 'Gymnastics','Art Competitions', 'Handball', 'Weightlifting', 'Wrestling','Water Polo', 'Hockey', 'Rowing', 'Fencing','Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing','Tennis', 'Golf', 'Softball', 'Archery','Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball','Rhythmic Gymnastics', 'Rugby Sevens','Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    famous_sports.sort(reverse=True)
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False )
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    st.title("Height vs Weight")

    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_vs_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x = athlete_df['Weight'], y = athlete_df['Height'], hue = temp_df['Medal'], style = temp_df['Sex'], s=50)
    st.pyplot(fig)

    st.title("Men vs Women Participation over the years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)