from numpy import NaN


class sensorType(object):

    def __init__(self, name=""):
        self.name = name

class pressureSensor(object):
    '''
    classdocs
    '''

    def __init__(self, name="", intercept=NaN, dudh=NaN, dudt=NaN, sigma = NaN):
        self.name = name
        self.intercept = intercept
        self.dudh = dudh
        self.dudt = dudt
        self.sigma = sigma

class temperatureSensor(object):
    '''
    classdocs
    '''

    def __init__(self, name="", sigma = NaN):
        self.name = name
        self.sigma = sigma 


class temperatureShaft(object):
    '''
    classdocs
    '''

    def __init__(self, name="", t_sensor_name=NaN, sensors_depth=NaN):
        self.name = name
        self.t_sensor_name = t_sensor_name
        self.sensors_depth = sensors_depth