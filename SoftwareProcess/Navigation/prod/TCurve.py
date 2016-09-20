import math
class TCurve(object):

# outward facing methods
    def __init__(self, n=None):
        functionName = "TCurve.__init__: "
        if(n == None):
            raise ValueError(functionName + "invalid n")
        if(not(isinstance(n, int))):
            raise ValueError(functionName + "invalid n")
        if((n < 2) or (n >= 30)):
            raise ValueError(functionName + "invalid n")
        self.n = n

    
    def p(self, t=None, tails=1):
        functionName = "TCurve.p: "
        if(t == None):
            raise ValueError(functionName + "missing t")
        if(not(isinstance(t, float))):
            raise ValueError(functionName + "invalid t")
        if(t < 0.0):
            raise ValueError(functionName + "invalid t")
        
        if(not(isinstance(tails, int))):
            raise ValueError(functionName + "invalid tails")
        if((tails != 1) & (tails != 2)):
            raise ValueError(functionName + "invalid tails")
        
        constant = self. calculateConstant(self.n)
        integration = self.integrate(t, self.n, self.f)
        if(tails == 1):
            result = constant * integration + 0.5
        else:
            result = constant * integration * 2
            
        if(result > 1.0):
            raise ValueError(functionName + "result > 1.0")
        
        return result
        
# internal methods
    def gamma(self, x):
        if(x == 1):
            return 1
        if(x == 0.5):
            return math.sqrt(math.pi)
        return (x - 1) * self.gamma(x - 1)
    
    def calculateConstant(self, n):
        n = float(n)
        numerator = self.gamma((n + 1.0) / 2.0)
        denominator = self.gamma(n / 2.0) * math.sqrt(n * math.pi)
        result = numerator / denominator
        return result
    
    def f(self, u, n):
        n = float(n)
        base = (1 + (u ** 2) / n)
        exponent = -(n + 1.0) / 2
        result = base ** exponent
        return result
    
    def integrate(self, t, n, f):
        if (t == 0.0):
            return 0.0
        epsilon = 0.001
        simpsonOld = 0
        simpsonNew = epsilon
        s = 4 # Number of regions to begin with
        lowBound = 0
        highBound = t
        while((abs(simpsonOld - simpsonNew) / simpsonNew) > epsilon):
            simpsonOld = simpsonNew
            w = (highBound - lowBound) / s
            # Takes care of the first and last element with coefficient 1
            simpsonSum = (f(lowBound, n) + f(highBound, n))
            # 1, 3, 5, ... n - 1
            for i in range(1, s, 2):
                # Takes care of the odd elements with coefficient 4
                simpsonSum += 4 * f(lowBound + i * w, n)
            # 2, 4, 6, ... n - 2
            for i in range(2, s-1, 2):
                # Takes care of the even elements with coefficient 2
                simpsonSum += 2 * f(lowBound + i * w, n)
            simpsonNew = (w/3) * simpsonSum;
            s = s * 2
            
        return simpsonNew
    
    def fTest(self, u, n):
        return u
        
        
    
        
            
        
