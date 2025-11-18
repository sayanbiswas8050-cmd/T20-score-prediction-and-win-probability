import streamlit as st
import pickle
import pandas as pd

pipe_1 = pickle.load(open("pipe.pkl","rb"))

teams =['West Indies',
        'Sri Lanka',
        'England',
        'Bangladesh',
        'India',
        'New Zealand',
        'Pakistan',
        'Nepal',
        'South Africa', 
        'Australia'
       ]
stadiums =['Sydney Cricket Ground', 'Dubai International Cricket Stadium',
       'Shere Bangla National Stadium',
       'Vidarbha Cricket Association Stadium', 'Melbourne Cricket Ground',
       'Central Broward Regional Park Stadium Turf Ground',
       'New Wanderers Stadium', 'Newlands', 'R.Premadasa Stadium',
       'Darren Sammy National Cricket Stadium', 'Narendra Modi Stadium',
       'Seddon Park', 'Kensington Oval', 'M Chinnaswamy Stadium',
       'Eden Park', 'Gaddafi Stadium', 'County Ground',
       'Wankhede Stadium', 'Trent Bridge', 'Kennington Oval',
       'Pallekele International Cricket Stadium', 'Adelaide Oval',
       'Providence Stadium', 'Zayed Cricket Stadium',
       'R Premadasa Stadium', 'Hagley Oval', 'Kingsmead', 'Warner Park',
       'Westpac Stadium', 'Sheikh Zayed Stadium',
       'National Cricket Stadium', 'Bay Oval', 'The Wanderers Stadium',
       'SuperSport Park', "Queen's Park Oval", 'Sophia Gardens',
       'National Stadium', 'Saurashtra Cricket Association Stadium',
       'Beausejour Stadium', 'Sabina Park', 'The Rose Bowl',
       'Punjab Cricket Association IS Bindra Stadium', 'Eden Gardens',
       'Old Trafford', 'Sharjah Cricket Stadium',
       'Brisbane Cricket Ground',
       'Mahinda Rajapaksa International Cricket Stadium', 'Edgbaston',
      'Zahur Ahmed Chowdhury Stadium', "Lord's"]

st.image("t20-cricket-banner-header-design-260nw-2031786302.webp")

with st.sidebar:
    User_menu = st.streamlit.radio(
        "Select an option",
        ("1st Innings","2nd Innings"))
if User_menu == "1st Innings":
    st.title("T20 score prediction")
    # col1, col2 =st.columns(2)

    # with col1:
    batting_team = st.sidebar.selectbox("Select the Batting Team",sorted(teams))
    # with col2:
    bowling_team = st.sidebar.selectbox("Select the Bowling Team",sorted(teams))

    stadium = st.selectbox("select Stadium Name",stadiums)


    col3,col4,col5 = st.columns(3)

    with col3:
        current_score = st.number_input("Current_score")
    with col4:
        over =st.number_input("Current Over")
        ball =st.number_input("Over's Ball")

    with col5:
        wicket = st.number_input("Current_wicket")


    if st.button("Predicted Score"):
        ball_left =120 -((over*6)+ball)
        if ball_left !=0:
            balls_left = ball_left 

        wicket_left = 10 - wicket
        crr = current_score/over

        user_input_df =pd.DataFrame(
            {'BattingTeam':[batting_team],"BowlingTeam":[bowling_team],'stadium':[stadium],'current_score':[current_score],
            'ball_left':[balls_left],'wicket_left':[wicket_left],"CRR":[crr]})
        st.dataframe(user_input_df)
        result = pipe_1.predict(user_input_df)
        st.text("Score : " + str(int(result[0]))) 

if User_menu == "2nd Innings":
    st.title("T20 Win prediction")
    pipe_2= pickle.load(open("pipe_2.pkl","rb"))

    # col1,col2 =st.columns(2)

    # with col1:
    batting_team = st.sidebar.selectbox("Select the batting team",sorted(teams))

    # with col2:
    bowling_team = st.sidebar.selectbox("select the bowling team",sorted(teams))


    selected_stadium = st.selectbox("Select the stadium",sorted(stadiums))


    target = st.number_input("Target")

    col3,col4,col5 = st.columns(3)
    with col3:
        current_score = st.number_input("Score")
    with col4:
        over =st.number_input("Current Over")
        ball =st.number_input("Over's Ball")

    with col5:
        wicket = st.number_input("Number of Wickets")


    if st.button("Win Probability"):
       need_run = target - current_score
       ball_left =120 -((over*6)+ball)
       if ball_left !=0:
            balls_left = ball_left 
       wickets = 10 - wicket
       CRR = current_score/over
       RRR = (need_run*6)/balls_left

       user_input_df = pd.DataFrame({'BattingTeam':[batting_team],'BowlingTeam':[bowling_team],
                                  'stadium':[selected_stadium],'balls_left':[balls_left],'need_run':[need_run],
                                  'wicket_left':[wickets],'target':[target],'CRR':[CRR],'RRR':[RRR]})
       st.table(user_input_df)
       result = pipe_2.predict_proba(user_input_df)
       lose = result[0][0]*100
       win = result[0][1]*100
       st.text(batting_team + " win probability : " + str(round(win,2))+ '%')
       st.text(bowling_team + " win probability : " + str(round(lose,2))+ '%')


