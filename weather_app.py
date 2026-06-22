import streamlit as st
import requests
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import base64
from datetime import datetime
st.sidebar.title("AI Weather App")

st.sidebar.info("""
Search any city and get
real-time weather updates.
""")

API_KEY = "24548b99095d384bca607c17d3676319"

import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6IExfUuwrQ5QJO0qCjZJESooi3GKGWE5-JyZ1xUuFWU_Q")

model = genai.GenerativeModel("gemini-2.5-flash")

st.title("🌦 AI Weather App")
st.markdown("### Real-Time Weather Forecast with AI Insights")

city = st.text_input("Enter City Name")

if st.button("Get Weather"):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        condition = data["weather"][0]["main"]

        bg_images = {
         
         "Clear": "https://images.unsplash.com/photo-1601297183305-6df142704ea2",
         "Clouds": "https://images.unsplash.com/photo-1534088568595-a066f410bcda",
         "Rain": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0",
         "Thunderstorm": "https://images.unsplash.com/photo-1605727216801-e27ce1d0cc28",
         "Snow": "https://images.unsplash.com/photo-1517299321609-52687d1bc55a"
        }

        bg_url = bg_images.get(condition, bg_images["Clouds"])

        st.markdown(
        f"""
         <style>
        .stApp {{
          background-image:
              linear-gradient(rgba(0,0,0,0.35), rgba(0,0,0,0.35)),
              url('{bg_url}');
              background-size: cover;
              background-position: center;
              background-attachment: fixed;
        }}
        </style>
         """,
         unsafe_allow_html=True
    )
        st.markdown("""
        <style>
        h1, h2, h3, h4, h5, h6,
        p, label, div {
             color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.success(f"Weather in {city}")
        st.write("☁ Condition:", data["weather"][0]["description"].title())
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]

        aqi_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"

        aqi_data = requests.get(aqi_url).json()

        aqi = aqi_data["list"][0]["main"]["aqi"]

        aqi_labels = {
          1: "😊 Good",
          2: "🙂 Fair",
          3: "😐 Moderate",
          4: "😷 Poor",
          5: "☠️ Very Poor"
        }

        st.subheader("🌍 Air Quality Index")
        st.write(aqi_labels.get(aqi, "Unknown"))

        icon = data["weather"][0]["icon"]
        icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"
        st.image(icon_url)

        col1, col2, col3, col4 = st.columns(4)
        with col4:
            st.metric("🥵 Feels Like", f"{data['main']['feels_like']} °C")

        with col1:
            st.metric("🌡 Temperature", f"{data['main']['temp']} °C")

        with col2:
            st.metric("💧 Humidity", f"{data['main']['humidity']} %")

        with col3:
            st.metric("💨 Wind Speed", f"{data['wind']['speed']} m/s")

        prompt = f"""

        Temperature: {data['main']['temp']}°C
        Humidity: {data['main']['humidity']}%
        Wind Speed: {data['wind']['speed']} m/s
        Weather: {data['weather'][0]['description']}

        Give a short weather summary and advice in 2-3 lines.
        """

        try:
            ai_response = model.generate_content(prompt)
            st.subheader("🤖 AI Weather Insights")
            st.write(ai_response.text)

        except Exception:
            st.warning("AI temporarily unavailable (quota exceeded). Weather app will still work.")

    
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.fromtimestamp(data["sys"]["sunset"])

        st.subheader("🌅 Sun Information")

        col1, col2 = st.columns(2)

        with col1:
         st.info(f"🌄 Sunrise: {sunrise.strftime('%I:%M %p')}")

        with col2:
         st.info(f"🌇 Sunset: {sunset.strftime('%I:%M %p')}")

        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        st.subheader("📅 Weather Forecast")

        for item in forecast_data["list"][:8]:
           st.write(
             f"{item['dt_txt']} | 🌡 {item['main']['temp']}°C | ☁ {item['weather'][0]['description']}"
            )
        temps = []
        times = []

        for item in forecast_data["list"][:10]:
           temps.append(item["main"]["temp"])
           times.append(item["dt_txt"])

           df = pd.DataFrame({
               "Time": times,
               "Temperature": temps
            })

        st.subheader("📈 Temperature Trend")

        fig = px.line(
                  df,
                 x="Time",
                 y="Temperature",
                 markers=True
                )

        st.plotly_chart(fig, use_container_width=True)

    else:
     st.error("City not found")
st.markdown("---")
st.caption("Built with ❤️ using Python, Streamlit, OpenWeather API and Gemini AI")