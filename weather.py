class Weather:
    def __init__(self):
        self.currentWeather = "default"
        self.previousWeather = self.currentWeather
        self.previousWeatherEffect = 0.0
        #weather types = "default", "sunny", "rainy", "thunder" for now**
    def getWeather(self):
        #here would be the call to the api to get the current weather
        pass
    def getWeatherEffect(self):
        def weatherEffectChange(weatherVal):
            weatherEffect = weatherVal - self.previousWeatherEffect
            self.previousWeatherEffect = weatherVal
            return weatherEffect
        if self.currentWeather == "default":
            return weatherEffectChange(0.0)
        elif self.currentWeather == "sunny":
            return weatherEffectChange(1.0)
        elif self.currentWeather == "rainy":
            return weatherEffectChange(-1.0)
        elif self.currentWeather == "thunder":
            return weatherEffectChange(-2.0)