class Weather:
    def __init__(self, city, temp, desc, wind, date, country):
        self.__city = city
        self.__temp = temp
        self.__desc = desc
        self.__wind = wind
        self.__date = date
        self.__country = country

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, city):
        self.__city = city

    @property
    def temp(self):
        return self.__temp

    @temp.setter
    def temp(self, temp):
        self.__temp = temp

    @property
    def desc(self):
        return self.__desc

    @desc.setter
    def desc(self, desc):
        self.__desc = desc

    @property
    def wind(self):
        return self.__wind

    @wind.setter
    def wind(self, wind):
        self.__wind = wind

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        self.__date = date

    @property
    def country(self):
        return self.__country

    @country.setter
    def country(self, country):
        self.__country = country
