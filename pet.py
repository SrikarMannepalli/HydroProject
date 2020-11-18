import math
class PET():
    def __init__(self):
        super().__init__()
        pass

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
    def __init__(self):
        super().__init__()
        self.P = 10
        self.pet = 100
        pass

    def turc(self):
        est = self.P/(math.sqrt(0.9+((self.P**2)/(self.pet**2))))
        return est;

    def zhang(self):
        est = self.P*self.pet*(1-math.exp(-self.pet/self.P))*math.tanh(self.P/self.pet)
        est = math.sqrt(est)
        return est
