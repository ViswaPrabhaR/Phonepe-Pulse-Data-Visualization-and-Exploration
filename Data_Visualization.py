# Libraries
import pandas as pd
import numpy as np
import json
import requests

# SQL libraries
import pymysql

# Dash board libraries
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go



#--------------------------------- MYSQL to Python Connect and Table Read--------------------------------------------#

conn = pymysql.connect(host='localhost', user='root', password='admin123', db='phonepe_pulse')
cursor = conn.cursor()

 # --------------------------------------------- STREAMLIT DASHBOARD -------------------------------------------------------------- #
    
# Page Configuration
st.set_page_config(page_title="Phonepe Pulse Data Visualization",page_icon="📱",layout="wide")

# --------------------------------------------  CSS Style   ---------------------------------------------------------------------------------- #
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #FFFFFF;
    border-color:#391C59;color:#391C59;
}
div.stButton > button:hover {
    background-color: #391C59;
    color:#ffffff;
}
div.stButton > button:active {
    position:relative; top:3px;
    background-color: #391C59;
    color:#ffffff;
}
.stSelectbox [data-baseweb="select"] > div {
    background-color: white;
     color:#391C59; border-color: #2d408d;        
 }</style>""", unsafe_allow_html=True) 

#------------------ Fuction for Dataframe ---------------------------- #
def transaction_count(x):
    cursor.execute(x)
    total_sum_list=cursor.fetchall()
    for total in total_sum_list:  # iterates through each tuple
        for s in total:  # iterates through each tuple items
            total_sum=s
        return total_sum
def total_data(q):
    cursor.execute(q)
    my_tuple_list = cursor.fetchall()
    return my_tuple_list
def my_widget(key):
    new_title = '<p style="font-family:cambria; font-weight:bold; color:#6b3395; font-size: 30px;">₹ Phonepe Pulse Data Visualization and Exploration</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    return

# Title
clicked = my_widget("first")
my_expander = st.expander("Filters and Search", expanded=False)
with my_expander:
        title,trans=st.columns([7,4])
        with title:
            option,analysis=st.columns([2,2])
    # Radio Button
            with option:
                select = st.radio("**Choose Your Option**",["India", "States"],horizontal=True)
            with analysis:
                radio = st.radio("**Choose Your Option**",["Transaction","User"],horizontal=True)
# ---------------------------------- India Transaction Details ------------------------------- #
if select=="India":
    if radio=="Transaction":
        with trans:
            year_t,quarter_t=st.columns([2,2])
            with year_t:
                 in_tr_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='in_tr_yr')
            with quarter_t:
                 in_tr_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='in_tr_qtr')

            in_tr_tr_typ = st.selectbox('**Select Transaction type**',
                                            ('Recharge & bill payments', 'Peer-to-peer payments',
                                             'Merchant payments', 'Financial Services', 'Others'), key='in_tr_tr_typ')

        geomap_t,transdata=st.columns([7,4])
        with geomap_t:
            # Transaction Wise Analysis
            st.subheader(f"Phonepe - Transaction Details for Quarter{in_tr_qtr} in Year - {in_tr_yr}, Mode - {in_tr_tr_typ}")
            cursor.execute(
                f"SELECT State, Transaction_count, Transaction_amount FROM aggregated_transaction WHERE Year = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
            in_tr_anly_tab_qry_rslt = cursor.fetchall()
            df_in_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(in_tr_anly_tab_qry_rslt),
                                                      columns=['State', 'Transaction_count', 'Transaction_amount'])
            df_in_tr_anly_tab_qry_rslt1 = df_in_tr_anly_tab_qry_rslt.set_index(
            pd.Index(range(1, len(df_in_tr_anly_tab_qry_rslt) + 1)))
                
                # -------------------------- CSV File for State ---------------------------------- #
                
                #Drop a State column from df_in_tr_tab_qry_rslt
            df_in_tr_anly_tab_qry_rslt.drop(columns=['State'], inplace=True)
                    # Read Indian States Json File
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data1 = json.loads(response.content)
            # Extract state names and sort them in alphabetical order
            state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
            state_names_tra.sort()
            # Create a DataFrame with the state names column
            df_state_names_tra = pd.DataFrame({'State': state_names_tra})
            # Combine the Gio State name with df_in_tr_tab_qry_rslt 
            df_state_names_tra[['Transaction_count','Transaction_amount']]= df_in_tr_anly_tab_qry_rslt  
            # convert dataframe to csv file
            df_state_names_tra.to_csv('State_trans.csv', index=False)
            # Read csv
            df = pd.read_csv('State_trans.csv')                 
                 # -------------------------- India Map Plot ---------------------------------- # 
            
            fig = go.Figure(data=go.Choropleth(
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locationmode='geojson-id',
    locations=df['State'],
    z=df['Transaction_amount'],
    colorscale='YlGn',  
    colorbar=dict(
        title={'text': "Transaction Amount"},
        thickness=15,
        len=.65,
        bgcolor='rgba(255,255,255,0.6)',   
      )
))
            hovertemp = '<i>State:</i> %{location} <br>'
            hovertemp += '<i>Transaction Amount:</i> %{z:,.2f} <extra></extra>'
            fig.update_traces(hovertemplate=hovertemp)
            fig.update_geos(visible=False, lonaxis={'range': [68, 98]}, lataxis={'range': [6, 38]})
            fig.update_layout(margin={'r': 0, 't': 30, 'l': 0, 'b': 0},height=550,width=550)
            st.plotly_chart(fig,use_container_width=True)
    # -------------------------------- Transaction Details with Transaction Type --------------- #
        with transdata:
            with st.container(border=True):  
                st.write(f'<p style="font-family:cambria; font-size: 14px; font-weight:bold;"> All PhonePe Transaction (UPI + Cards + Vallets)</p>', unsafe_allow_html=True)
                transaction_count_query = f"SELECT sum(transaction_count) FROM aggregated_transaction WHERE YEAR={in_tr_yr} AND QUARTER={in_tr_qtr};"
                transaction_sum = transaction_count(transaction_count_query)
                st.write(f"{ '{:,}'.format(transaction_sum)}") 
                
                # Total Payment value for particular year and quarter
                val3, val4 = st.columns([1, 1])
                with val3:
                    st.write(f'<p style="font-family:cambria; font-size: 16px;font-weight:bold;"> Total Payment value </p>', unsafe_allow_html=True)
                    transaction_amount_query =f"SELECT sum(transaction_amount) FROM aggregated_transaction WHERE YEAR={in_tr_yr} AND QUARTER={in_tr_qtr};"
                    transaction_amount = transaction_count(transaction_amount_query)
                    st.write(f"₹ {'{:,}'.format(round(transaction_amount / 10000000))}", "Cr")
                        
                # Average Transaction Value for paticular year and quater
                with val4:
                    st.write(f'<p style="font-family:cambria; font-size: 16px;font-weight:bold;"> Average Transaction </p>', unsafe_allow_html=True)
                    average_trans = (transaction_amount*10000000) // round(transaction_sum)
                    average_trans = '{:,}'.format(round(average_trans/10000000))
                    st.write(f"₹ {average_trans}")
                st.markdown("------------------------")

                # Categories wise Transaction Count  for particular year and quarter
                st.write(f'<p style="font-family:cambria; font-size: 16px;font-weight:bold;"> Categories wise Transaction Count </p>', unsafe_allow_html=True)
                merchant_pay = f"SELECT sum(transaction_count) FROM aggregated_transaction WHERE TRANSACTION_TYPE= 'Merchant payments' AND YEAR={in_tr_yr} AND QUARTER={in_tr_qtr};"
                merchant_pay = '{:,}'.format(transaction_count(merchant_pay))
                st.write(f" Merchant Payments --- {merchant_pay}")
                    
                peer2peer_pay = f"SELECT sum(transaction_count) FROM aggregated_transaction WHERE TRANSACTION_TYPE= 'Peer-to-peer payments' AND YEAR={in_tr_yr} AND QUARTER={in_tr_qtr};"
                peer2peer_pay = '{:,}'.format(transaction_count(peer2peer_pay))
                st.write(f" Peer-to-peer Payments --- {peer2peer_pay}")
        
                rechargebill_pay = f"SELECT sum(transaction_count) FROM aggregated_transaction WHERE TRANSACTION_TYPE= 'Recharge & bill payments' AND YEAR={in_tr_yr} AND QUARTER={in_tr_qtr};"
                rechargebill_pay = '{:,}'.format(transaction_count(rechargebill_pay))
                st.write(f" Recharge & Bill Payments --- { rechargebill_pay}")
        
                financial_service = f"SELECT sum(transaction_count) FROM aggregated_transaction WHERE TRANSACTION_TYPE= 'Financial Services' AND YEAR={in_tr_yr} AND QUARTER={in_tr_qtr};"
                financial_service = '{:,}'.format(transaction_count(financial_service))
                st.write(f" Financial Services --- {financial_service}")
        
                others = f"SELECT sum(transaction_count) FROM aggregated_transaction WHERE TRANSACTION_TYPE= 'Others' AND YEAR={in_tr_yr} AND QUARTER={in_tr_qtr};"
                others = '{:,}'.format(transaction_count(others))
                st.write(f" Others --- {others}")
        # ---------------------- Over all Transaction Details ------------------------ #
        growth,payment=st.columns([6,6])
        with growth:
            with st.container (border=True):
        # -------------------------------- Bar Chart Total Phonepe Transaction ------------------------------- #
                st.subheader(f"India's Total PhonePe Transaction Growth Between Year 2018 to 2023")
                t_Trans = f"select year, sum(transaction_amount) , sum(Transaction_count) from aggregated_transaction group by year ;"
                t_df = pd.DataFrame(total_data(t_Trans), columns=[ "Year", "Transaction_amount",'Transaction_count'])
                t_df.index = t_df.index + 1
    
                fig = px.bar(t_df, x='Year', y='Transaction_amount', text_auto='.2s',
                             hover_data=['Year','Transaction_amount' ,'Transaction_count'], color='Transaction_amount',  labels={'Transactions_Count':'Transaction_count'},width=800, height=400, color_continuous_scale="thermal")
                st.plotly_chart(fig, use_container_width=True)
                    
         # -------------------------------- Bar Chart Payment type wise Transaction ------------------------------- #
        with payment:
            with st.container(border=True):
                st.subheader(f"India's Payment Types Growth Between Year 2018 to 2023")
                pt_user = f"select year, transaction_type,sum(transaction_amount),sum(transaction_count) from aggregated_transaction group by year, transaction_type;"
                u_df = pd.DataFrame(total_data(pt_user), columns=["Year", "Transaction_type", "Transaction_amount", "Transaction_count"])
                u_df.index = u_df.index + 1
                fig = px.bar(u_df,  x='Transaction_count', y='Year', orientation='h',
                                 hover_data=['Year', 'Transaction_amount'], color='Transaction_type', text="Transaction_type",
                                 width=800, height=500, color_continuous_scale="thermal")
                fig.update_layout(barmode='stack', yaxis={'categoryorder':'category descending'})
                st.plotly_chart(fig, use_container_width=True)
            
#-------------------------------------------------------- User Transaction Details ----------------------------------------------- #
    elif radio=="User":
        with trans:
            year_u,quarter_u=st.columns([2, 2])
            with year_u:
                in_us_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='in_us_yr')
            with quarter_u:
                in_us_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='in_us_qtr')

        geomap_user, userdata = st.columns([7, 4])
        with geomap_user:
            cursor.execute(
                f"select state, sum(Registered_User), sum(app_opens) from map_user WHERE Year = '{in_us_yr}' AND Quarter = '{in_us_qtr}'  GROUP BY State;")
            in_us_tab_qry_rslt = cursor.fetchall()
            df_in_us_tab_qry_rslt = pd.DataFrame(np.array(in_us_tab_qry_rslt), columns=["State", "Registered_User", "App_Opens"])
            df_in_us_tab_qry_rslt1 = df_in_us_tab_qry_rslt.set_index(pd.Index(range(1, len(df_in_us_tab_qry_rslt) + 1)))

            df_in_us_tab_qry_rslt.drop(columns=['State'], inplace=True)
            # Clone the gio data
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data2 = json.loads(response.content)
            # Extract state names and sort them in alphabetical order
            state_names_use = [feature['properties']['ST_NM'] for feature in data2['features']]
            state_names_use.sort()
            # Create a DataFrame with the state names column
            df_state_names_use = pd.DataFrame({'State': state_names_use})
            # Combine the Gio State name with df_in_tr_tab_qry_rslt
            df_state_names_use[['Registered_User','App_Opens']] = df_in_us_tab_qry_rslt
            # convert dataframe to csv file
            df_state_names_use.to_csv('Map_user.csv', index=False)
            # Read csv
            df_use = pd.read_csv('Map_user.csv')
            # Geo plot
            st.subheader(f"Phonepe APP User Details for Quarter{in_us_qtr} in {in_us_yr}")

            # -------------------------- India Map Plot ---------------------------------- #

            fig = go.Figure(data=go.Choropleth(
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locationmode='geojson-id',
                locations=df_use['State'],
                z=df_use['Registered_User'],
                colorscale='Aggrnyl',
                colorbar=dict(
                    title={'text': "Registered_User"},
                    thickness=15,
                    len=.65,
                    bgcolor='rgba(255,255,255,0.6)',
                )
            ))
            hovertemp = '<i>State:</i> %{location} <br>'
            hovertemp += '<i>Registered_User:</i> %{z:,} <extra></extra>'
            fig.update_traces(hovertemplate=hovertemp)
            fig.update_geos(visible=False, lonaxis={'range': [68, 98]}, lataxis={'range': [6, 38]})
            fig.update_layout(margin={'r': 0, 't': 30, 'l': 0, 'b': 0}, height=550, width=550)
            st.plotly_chart(fig, use_container_width=True)

    #--------------------- User count Details Over all --------------------------------- #
        with userdata:
            with st.container(border=True):
                count_u,count_a=st.columns([2,2])
                with count_u:
                    st.markdown(
                        f'__<p style="font-family:cambria; color:#6b3395; font-size: 14px;"> Register User Q{in_us_qtr} {in_us_yr}</p>__',
                        unsafe_allow_html=True)
                    as_c = f"SELECT sum(Registered_User) FROM map_user WHERE YEAR <={in_us_yr} AND QUARTER <={in_us_qtr};"
                    as_count_till = transaction_count(as_c)
                    if as_count_till == None:
                        st.write("Data Not Available")
                    else:
                        st.write(f"{'{:,}'.format(as_count_till)}")

                with count_a:
                    st.markdown(
                        f'__<p style="font-family:Cambria; color:#6b3395; font-size: 14px;">App Opens in Q{in_us_qtr} {in_us_yr}</p>__',
                        unsafe_allow_html=True)
                    as_app = f"SELECT sum(app_opens) FROM map_user WHERE YEAR ={in_us_yr} AND QUARTER ={in_us_qtr} ;"
                    as_app_till = transaction_count(as_app)
                    st.write(f"{'{:,}'.format(as_app_till)}")

            with st.container(border=True):
                # --------------------------------- Phone Brand ------------------------------------------- #
                st.markdown(
                    f'__<p style="font-family:Cambria; color:#6b3395; font-size: 16px;">Phone Brand Wise APP Users in Q{in_us_qtr} {in_us_yr}</p>__',
                    unsafe_allow_html=True)
                cursor.execute(
                    f"SELECT brands, SUM(User_Count) FROM aggregated_user WHERE Year = '{in_us_yr}' AND Quarter = '{in_us_qtr}'  GROUP BY brands;")
                in_us_brand_qry_rslt = cursor.fetchall()
                df_in_us_brand_qry_rslt = pd.DataFrame(np.array(in_us_brand_qry_rslt), columns=['Brands', 'User Count'])
                df_in_us_brand_qry_rslt1 = df_in_us_brand_qry_rslt.set_index(
                    pd.Index(range(1, len(df_in_us_brand_qry_rslt) + 1)))
                st.table(df_in_us_brand_qry_rslt1)

            # -------------------------------- Over All  Phonepe Users ------------------------------- #
        growth_u,payment_u=st.columns([6,6])
        with growth_u:
            # -------------------------------- Bar Chart Total Phonepe Transaction ------------------------------- #
            st.subheader(f"India's Total PhonePe Users Growth Between Year 2018 to 2023")
            u_count = f"select year, sum(Registered_User)  from map_user group by year ;"
            u_df = pd.DataFrame(total_data(u_count), columns=["Year", "Registered_User"])
            fig = px.line(u_df, x='Registered_User', y='Year', color='Year', markers=True)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        with payment_u:
            # -------------------------------- Bar Chart Payment type wise Transaction ------------------------------- #
            st.subheader(f"Phone Brand Wise Users Between Year 2018 to 2023")
            ut_user = f"select year, brands, sum(user_count) from aggregated_user group by brands, Year;"
            ur_df = pd.DataFrame(total_data(ut_user), columns=["Year", "Brands", "User_Count"])
            ur_df_fig = px.bar(ur_df, x='Brands', y='User_Count',
                                   hover_data=['Year', 'Brands', 'User_Count'], color='Year',
                                   width=700, height=500,text='Year' )
            ur_df_fig.update_layout(barmode='stack')
            st.plotly_chart(ur_df_fig, use_containe_width=True)
#--------------------------------- State wise Transaction -----------------------------------------#
elif select == "States":
    with trans:
        year_st,quarter_st=st.columns([2,2])
        with year_st:
            st_tr_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='st_tr_yr')
        with quarter_st:
            st_tr_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='st_tr_qtr')
        st_tr_st = st.selectbox('**Select State**', (
                    'andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar',
                    'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                    'haryana', 'himachal-pradesh',
                    'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                    'maharashtra', 'manipur',
                    'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                    'tamil-nadu', 'telangana',
                    'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'), key='st_tr_st')
    #----------------- State wise Transaction -------------------------------#
    if radio == "Transaction":
        statechart_st, district_st = st.columns([7,4])
        with statechart_st:
            st.write(
                f' <p style="font-family:cambria; font-size: 20x; font-weight:Bold; color:#391C59;"><br> Over all State Transaction Analysis </p>',
                unsafe_allow_html=True)
            # Transaction State  Analysis table query
            cursor.execute(
                f"SELECT State, sum(Transaction_Amount) FROM aggregated_transaction WHERE Year = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}' group by state;")
            st_tr_anly_tab_qry_rslt = cursor.fetchall()
            df_st_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(st_tr_anly_tab_qry_rslt),
                                                      columns=['State', 'Transaction_Amount'])
            df_st_tr_anly_tab_qry_rslt1 = df_st_tr_anly_tab_qry_rslt.set_index(
                pd.Index(range(1, len(df_st_tr_anly_tab_qry_rslt) + 1)))
            figch = px.line(df_st_tr_anly_tab_qry_rslt1, x='State', y='Transaction_Amount', width=850, height=525)
            st.plotly_chart(figch, config=dict({'displayModeBar': False}, **{'displaylogo': False}),
                            use_container_width=True, layout=dict({'width': '100%'}, **{'height': '100%'}))
            #----------------- District wise ----------------------------#
        with district_st:
            st.write(
                f' <p style="font-family:cambria; font-size: 20x; font-weight:Bold; color:#391C59;"><br> {st_tr_st} State Transaction in {st_tr_yr}, Quarter {st_tr_qtr}  </p>',
                unsafe_allow_html=True)
            cursor.execute(
                f"SELECT State,District, sum(Transaction_Amount),sum(Transaction_Count) FROM map_transaction WHERE State = '{st_tr_st}' AND Year = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}' group by state, district;")
            st_dist_qry_rslt = cursor.fetchall()
            df_st_dist_qry_rslt = pd.DataFrame(np.array(st_dist_qry_rslt),
                                                      columns=['State','District', 'Transaction_Amount','Transaction_Count'])
            df_st_dist_qry_rslt1 = df_st_dist_qry_rslt.set_index(
                pd.Index(range(1, len(df_st_dist_qry_rslt) + 1)))
            #st.table(df_st_dist_qry_rslt1)
            fig_st = px.sunburst(df_st_dist_qry_rslt1, path=['State', 'District', 'Transaction_Count'],
                                 values='Transaction_Amount', color='Transaction_Count')
            st.plotly_chart(fig_st, use_container_width=True)

        data_st,top10=st.columns([6,6])
        with data_st:
            # ------  /  State wise Total Transaction calculation Table  /  ---- #
            st.subheader(f" State Wise Transaction Details for Quarter Q{st_tr_qtr}  in  Year {st_tr_yr}")
            cursor.execute(
                f"SELECT State, sum(Transaction_count), sum(Transaction_amount) FROM map_transaction WHERE  Year = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}' GROUP BY state ;")
            st_tr_anly_tab_qry_rslt = cursor.fetchall()
            state_dataset = pd.DataFrame(np.array(st_tr_anly_tab_qry_rslt),
                                             columns=['State', 'Transaction_count', 'Transaction_amount'])
            def split_frame(input_df, rows):
                df = [input_df.loc[i: i + rows - 1, :] for i in range(1, len(input_df), rows)]
                return df
            top_menu = st.columns(3)
            with top_menu[0]:
                sort = st.radio("Sort Data", options=["Yes", "No"], horizontal=1, index=1)
            if sort == "Yes":
                with top_menu[1]:
                    sort_field = st.selectbox("Sort By", options=state_dataset.columns)
                with top_menu[2]:
                    sort_direction = st.radio(
                            "Direction", options=["⬆️", "⬇️"], horizontal=True
                        )
                state_dataset = state_dataset.sort_values(
                        by=sort_field, ascending=sort_direction == "⬆️", ignore_index=True
                    )
            pagination = st.container()

            bottom_menu = st.columns((4, 1, 1))
            with bottom_menu[2]:
                batch_size = st.selectbox("Page Size", options=[10,20,30])
            with bottom_menu[1]:
                total_pages = (
                        int(len(state_dataset) / batch_size) if int(len(state_dataset) / batch_size) > 0 else 1
                    )
                current_page = st.number_input(
                        "Page", min_value=1, max_value=total_pages, step=1
                    )
            with bottom_menu[0]:
                st.markdown(f"Page **{current_page}** of **{total_pages}** ")

            pages = split_frame(state_dataset, batch_size)
            pagination.table(data=pages[current_page - 1])
    #--------------------------Top 10 Transaction -----------------------------------------#
        with top10:
            st.subheader(f"Top 10 Transaction of  Q{st_tr_qtr}  in  Year {st_tr_yr}")
            state_10, district_10 = st.columns([1, 1])
            with state_10:
                state = st.button("STATES")
            with district_10:
                district = st.button("DISTRICTS")
            if state:
               st.markdown(
                    '<p style="font-family:sans-serif; color:#6b3395; font-size: 15px;">Top 10 States</p>',
                    unsafe_allow_html=True)
               cursor.execute(f"SELECT state, transaction_count FROM map_transaction WHERE YEAR={st_tr_yr} AND QUARTER={st_tr_qtr} ORDER BY transaction_count DESC LIMIT 10;")
               st_top_tab_qry_rslt = cursor.fetchall()
               df_st_top_tab_qry_rslt = pd.DataFrame(np.array(st_top_tab_qry_rslt),
                                                          columns=['State', 'Transaction_Count'])

               fig = px.pie(df_st_top_tab_qry_rslt, values='Transaction_Count', names='State', hole=.4,
                             title=' ', color_discrete_sequence=px.colors.sequential.RdBu)
               fig.update_layout(
                   annotations=[dict(text='state', x=0.50, y=0.5, font_size=20, showarrow=False),
                               ])
               st.plotly_chart(fig, theme=None, use_container_width=True)

            elif district:
               st.markdown(
                    '<p style="font-family:sans-serif; color:#6b3395; font-size: 15px;">Top 10 Districts</p>',
                    unsafe_allow_html=True)
               cursor.execute(f"SELECT state, district,transaction_count FROM map_transaction WHERE YEAR={st_tr_yr} AND QUARTER={st_tr_qtr} ORDER BY transaction_count DESC LIMIT 10;")
               st_top_tab_qry_rslt = cursor.fetchall()
               df_st_top_tab_qry_rslt = pd.DataFrame(np.array(st_top_tab_qry_rslt),
                                                          columns=['State','District' ,'Transaction_Count'])

               fig_st = px.sunburst(df_st_top_tab_qry_rslt, path=['State', 'District', 'Transaction_Count'],
                                    values='Transaction_Count', color='District')
               st.plotly_chart(fig_st, theme=None, use_container_width=True)

    elif radio == "User":
        statechart_us, district_us = st.columns([7, 4])
        with statechart_us:
            st.write(
                f' <p style="font-family:cambria; font-size: 20x; font-weight:Bold; color:#391C59;"><br> Over all State Registered Users </p>',
                unsafe_allow_html=True)
            cursor.execute(
            f"SELECT State, sum(Registered_User) FROM map_user WHERE Year = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}' group by state;")
            st_user_tab_qry_rslt = cursor.fetchall()
            df_st_user_tab_qry_rslt = pd.DataFrame(np.array(st_user_tab_qry_rslt),
                                                  columns=['State', 'Registered_User'])
            df_st_user_tab_qry_rslt1 = df_st_user_tab_qry_rslt.set_index(
                     pd.Index(range(1, len(df_st_user_tab_qry_rslt) + 1)))
            figuser = px.line(df_st_user_tab_qry_rslt1, x='State', y='Registered_User', width=850, height=525)
            st.plotly_chart(figuser, config=dict({'displayModeBar': False}, **{'displaylogo': False}),
                        use_container_width=True, layout=dict({'width': '100%'}, **{'height': '100%'}))
        with district_us:
            st.write(
                f' <p style="font-family:cambria; font-size: 20x; font-weight:Bold; color:#391C59;"><br> {st_tr_st} State User Details in {st_tr_yr}, Quarter {st_tr_qtr}  </p>',
                unsafe_allow_html=True)
            cursor.execute(
                f"SELECT State,District, sum(Registered_User),sum(App_Opens) FROM map_user WHERE State = '{st_tr_st}' AND Year = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}' group by state, district;")
            st_dist_us_qry_rslt = cursor.fetchall()
            df_st_dist_us_qry_rslt = pd.DataFrame(np.array(st_dist_us_qry_rslt),
                                                      columns=['State','District', 'Registered_User','App_Opens'])
            df_st_dist_us_qry_rslt1 = df_st_dist_us_qry_rslt.set_index(
                pd.Index(range(1, len(df_st_dist_us_qry_rslt) + 1)))
            #st.table(df_st_dist_qry_rslt1)
            fig_st = px.sunburst(df_st_dist_us_qry_rslt1, path=['State', 'District'],
                                 values='Registered_User', color='Registered_User')
            st.plotly_chart(fig_st, use_container_width=True)

        data_ut, top10 = st.columns([6, 6])
        with data_ut:
            # ------  /  State wise Total Transaction calculation Table  /  ---- #
            st.subheader(f" Over All State Wise User Details 2018 - 2023")
            cursor.execute(
                f"SELECT State, sum(Registered_User), sum(App_Opens) FROM map_user GROUP BY state ;")
            st_ur_map_tab_qry_rslt = cursor.fetchall()
            state_user_dataset = pd.DataFrame(np.array(st_ur_map_tab_qry_rslt),
                                         columns=['State', 'Registered_User', 'App_Opens'])
            # -------------------------- Sorting the Datas --------------------------------------- #
            def split_frame(input_df, rows):
                df = [input_df.loc[i: i + rows - 1, :] for i in range(1, len(input_df), rows)]
                return df
            top_menu = st.columns(3)
            with top_menu[0]:
                sort = st.radio("Sort Data", options=["Yes", "No"], horizontal=1, index=1)
            if sort == "Yes":
                with top_menu[1]:
                    sort_field = st.selectbox("Sort By", options=state_user_dataset.columns)
                with top_menu[2]:
                    sort_direction = st.radio(
                        "Direction", options=["⬆️", "⬇️"], horizontal=True
                    )
                state_user_dataset = state_user_dataset.sort_values(
                    by=sort_field, ascending=sort_direction == "⬆️", ignore_index=True
                )
            #------------------------- Pagination ------------------------------------ #
            pagination = st.container()

            bottom_menu = st.columns((4, 1, 1))
            with bottom_menu[2]:
                batch_size_us = st.selectbox("Page Size", options=[10, 20, 30])
            with bottom_menu[1]:
                total_pages = (
                    int(len(state_user_dataset ) / batch_size_us) if int(len(state_user_dataset ) / batch_size_us) > 0 else 1
                )
                current_page = st.number_input(
                    "Page", min_value=1, max_value=total_pages, step=1
                )
            with bottom_menu[0]:
                st.markdown(f"Page **{current_page}** of **{total_pages}** ")

            pages = split_frame(state_user_dataset , batch_size_us)
            pagination.table(data=pages[current_page - 1])
    # ---------------------------------- Top 10 User Details ----------------------------------#
        with top10:
            st.subheader(f"Top 10 User Details of  Q{st_tr_qtr}  in  Year {st_tr_yr}")
            state_10, district_10 = st.columns([1, 1])
            with state_10:
                state = st.button("STATES",)
            with district_10:
                district = st.button("DISTRICTS")
            # --------------------------- Top 10 State User Details --------------------------- #
            if state:
                st.markdown(
                    '<p style="font-family:Cambria; color:#6b3395; font-size: 20px;">Top 10 States</p>',
                    unsafe_allow_html=True)
                cursor.execute(
                    f"SELECT state, sum(Registered_User) as Registered_Users FROM map_user WHERE YEAR={st_tr_yr} AND QUARTER={st_tr_qtr} GROUP BY STATE ORDER BY Registered_Users DESC LIMIT 10;")
                st_top_tab_qry_rslt = cursor.fetchall()
                df_st_top_tab_qry_rslt = pd.DataFrame(np.array(st_top_tab_qry_rslt),
                                                      columns=['State', 'Registered_Users'])
                fig = px.pie(df_st_top_tab_qry_rslt, values='Registered_Users', names='State', hole=.4,
                             title=' ', color_discrete_sequence=px.colors.sequential.RdBu)
                fig.update_layout(
                    annotations=[dict(text='state', x=0.50, y=0.5, font_size=20, showarrow=False),
                                 ])
                st.plotly_chart(fig, theme=None, use_container_width=True)
            #--------------------------- Top 10 District User Details --------------------------- #
            elif district:
                st.markdown(
                    '<p style="font-family:Cambria; color:#6b3395; font-size: 20px;">Top 10 District</p>',
                    unsafe_allow_html=True)
                cursor.execute(
                    f"SELECT state, District, sum(Registered_User) as Registered_Users FROM map_user WHERE YEAR={st_tr_yr} AND QUARTER={st_tr_qtr} GROUP BY District,State ORDER BY Registered_Users DESC LIMIT 10;")
                st_user_tab_qry_rslt = cursor.fetchall()
                df_st_user_tab_qry_rslt = pd.DataFrame(np.array(st_user_tab_qry_rslt),
                                                      columns=['State','District', 'Registered_Users'])
                fig_st = px.sunburst(df_st_user_tab_qry_rslt, path=['State', 'District'],
                                     values='Registered_Users', maxdepth=2,color='District',color_continuous_scale='RdBu',)
                st.plotly_chart(fig_st, theme=None, use_container_width=True)


