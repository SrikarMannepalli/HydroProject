import math
class PET():
    def __init__(self, press, temp, dew_temp, rel_hum, wind_speed, wind_dir, soil_moist):
        super().__init__()
        self.press = 0.1*press # to convert to kpa from hpa
        self.temp = temp
        self.dew_temp = dew_temp
        self.rel_hum = rel_hum
        self.wind_speed = wind_speed
        self.wind_dir = wind_dir
        self.soil_moist = soil_moist
        self.Rn = 0.19 #for now. Until we find a proper formula
        self.G = 0 #since daily being used
        self.g = None
        self.D = None
        self.Tav = temp
        self.u2=wind_speed
        self.es = None
        self.ea = None
        self.latent_heat_vap = None
        self.calculate()

    def calculate(self):
        self.D = (4098*0.618*math.exp((17.27*self.Tav)/(self.Tav+237.3)))/((self.Tav+237.3)**2)
        self.ea = 0.61*math.exp((17.27*self.dew_temp)/(self.dew_temp+237.3))
        # self.ea = self.es*(self.rel_hum/100)
        self.es = 100*self.ea/self.rel_hum
        self.latent_heat_vap = 2.501-2.361*0.001*self.temp
        self.g = 0.00163*self.press/self.latent_heat_vap
    

    def hargreaves(self):
        Td = self.Tmax - self.Tmin
        est = 0.0023*(self.Ra)*(17.8+0.5*self.Tmean)*(math.sqrt(Td))
        return est

    def penman(self):
        et_num = 0.408*self.D*(self.Rn-self.G) + self.g*(900/(273+self.Tav))*self.u2*(self.es-self.ea)
        et_den = self.D + self.g*(1+0.34*self.u2)
        est = et_num/et_den
        return est
    

class AET():
    def __init__(self,p,pet):
        super().__init__()
        self.P = p
        self.pet = pet
        

    def turc(self):
        est = self.P/(math.sqrt(0.9+((self.P**2)/(self.pet**2))))
        return est;

    def zhang(self):
        est = self.P*self.pet*(1-math.exp(-self.pet/self.P))*math.tanh(self.P/self.pet)
        est = math.sqrt(est)
        return est

# pet = PET(10101,24.33,13.8,49.67,2.06,136,17.96)
# print(pet.penman())