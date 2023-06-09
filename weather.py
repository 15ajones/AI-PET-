import python_weather

import asyncio
import os

async def getweather():
  # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
  async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
    # fetch a weather forecast from a city
    weather = await client.get('London')
    
    # returns the current day's forecast temperature (int)
    print(weather.current.temperature)
    
    # get the weather forecast for a few days
    for forecast in weather.forecasts:
      print(forecast)
      
      # hourly forecasts
      for hourly in forecast.hourly:
        print(f' --> {hourly!r}')

if __name__ == '__main__':
  # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
  # for more details
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
  asyncio.run(getweather())

# class Weather:
#     def __init__(self):
#         self.currentWeather = "default"
#         self.previousWeather = self.currentWeather
#         self.previousWeatherEffect = 0.0
#         #weather types = "default", "sunny", "rainy", "thunder" for now**
#     def getWeather(self):
#         #here would be the call to the api to get the current weather
#         pass
#     def getWeatherEffect(self):
#         def weatherEffectChange(weatherVal):
#             weatherEffect = weatherVal - self.previousWeatherEffect
#             self.previousWeatherEffect = weatherVal
#             return weatherEffect
#         if self.currentWeather == "default":
#             return weatherEffectChange(0.0)
#         elif self.currentWeather == "sunny":
#             return weatherEffectChange(1.0)
#         elif self.currentWeather == "rainy":
#             return weatherEffectChange(-1.0)
#         elif self.currentWeather == "thunder":
#             return weatherEffectChange(-2.0)