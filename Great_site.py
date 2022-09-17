import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import time

st.set_page_config(layout='wide')

country = pd.read_csv('https://pkgstore.datahub.io/core/gdp/gdp_csv/data/0048bc8f6228d0393d41cac4b663b90f/gdp_csv.csv')
df = sns.load_dataset("penguins")


txt_name = st.text_input('Your name:')
if txt_name:
        st.write(f'Hello, {txt_name}! How are you? 😊')
        st.write("Do you want to know a little about GDP?")
        flag = st.checkbox('Yes')
        if flag:
            @st.cache
            def convert_df(df):
                return df.to_csv().encode('utf-8')

            st.write('_Gross domestic product (GDP) is the total monetary or market value of all the finished goods and services produced within'
                     ' a country’s borders in a specific time period. As a broad measure of overall domestic production, it functions as a comprehensive'
                     ' scorecard of a given country’s economic health. GDP is a key tool to guide policymakers, investors, and '
                     'businesses in strategic decision-making._')

            if st.checkbox('see data'):
                    st.write(country)

            choice = st.selectbox(
                    'Please, choose country/group of country',
                    country['Country Name'].unique())
            st.write('*You selected:* ', choice)

            country_slider = st.slider('Year', min_value=int(country['Year'].min()), max_value=int(country['Year'].max()), value=[int(country['Year'].min()),int(country['Year'].max())])

            selected_country=country[(country['Country Name']==choice) & (country['Year'].isin([i for i in range(min(country_slider),max(country_slider)+1)]))]
            selected_country_change=selected_country.iloc[-1]['Value']/selected_country.iloc[-2]['Value']

            col_1, col_2, col_3, col_4 = st.columns(4)
            col_1.metric('Average GDP, bln US $', int(round(selected_country['Value'].mean()/1000000000, 0)))
            col_2.metric('Min GDP, bln US $', int(round(selected_country['Value'].min()/1000000000, 0)))
            col_3.metric('Max GDP, bln US $', int(round(selected_country['Value'].max()/1000000000, 0)))
            col_4.metric('Last GDP, bln US $', value=int(round(selected_country.iloc[-1]['Value']/1000000000, 0)), delta='{:.2f}%'.format((selected_country_change-1)*100))

            selected_country_Year = selected_country.copy()
            selected_country_Year['Year']=selected_country_Year['Year'].astype(str)

            #st.area_chart(selected_country_Year[['Year','Value']].set_index('Year'))
            st.subheader(f'GDP graph ({country_slider[0]}-{country_slider[1]})')
            st.area_chart(selected_country_Year, x='Year', y='Value')

            csv = convert_df(selected_country[['Year','Value']])

            *_,col=st.columns(7)

            col.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='large_df.csv',
                mime='text/csv',
            )

            from PIL import Image
            image = Image.open('ВВП.PNG')
            st.image(image, caption='GDP per Capita')

            options = st.multiselect('Please, select the countries', country['Country Name'].unique())
            if options:
                colors = ['#6161ff', '#ff2400', '#42aaff','#00a550', '#ffff00', '#120a8f', 'fc0fc0']
                fig, ax = plt.subplots()
                sns.boxplot(x=country[(country['Country Name'].isin(options))]['Value'], y=country[country['Country Name'].isin(options)]['Country Name'], palette=colors)
                st.pyplot(fig)

            choice_year = st.selectbox(
                    'Please, choose year',
                    country['Year'].unique())

            color = st.color_picker('Pick A Color', '#FF4B4B')

            data_bar_chart = country[(country['Year']==choice_year)].sort_values('Value', ascending=False).iloc[1:11]
            st.altair_chart(alt.Chart(data_bar_chart).mark_bar(fill=color).encode(x=alt.X('Country Name', sort=None),y='Value', tooltip=['Country Name', 'Value']), use_container_width=True)

            video_file = open('myvideo.mp4', 'rb')
            video_bytes = video_file.read()
            st.video(video_bytes)

            st.write("_Let's get distracted! Do you want to learn something from penguins?_")
            if st.checkbox('I want 🐧'):
                    with st.spinner('Wait for it...'):
                        fig = sns.pairplot(df, hue="species")
                        st.pyplot(fig)

            feedback = st.radio(
                f'{txt_name}, please, give feedback',
                ('Very cool, keep up the good work!', 'Okay, but something needs to be done', 'There are many changes to be made'))
            if feedback=='Very cool, keep up the good work!':
                    st.write('Thank you, we are glad!' ":smile:")
            if feedback=='Okay, but something needs to be done':
                    st.write('Thanks for noticing 😅')
            if feedback=='There are many changes to be made':
                    txt = st.text_area("Please, write down what you didn't like")
                    if txt:
                            st.write('Thank you, we will take your comments into account!')

            if st.button('Finish! 👈'):
                    st.balloons()
        else:
            if st.checkbox('No'):
                st.write("Okay, I won't take up your time 😉")
