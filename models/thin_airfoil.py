import numpy as np
import matplotlib.pyplot as plt

def naca_4_digit_airfoil(x,m,p):


    mask = x <= p 
    
    z = np.zeros_like(x)

    
    z[mask] = ((m/p**2) * (2 * p * (x[mask]) - (x[mask])**2))
    
    z[~mask] = (m/(1-p)**2) * (1 - 2*p + 2*p*(x[~mask]) - (x[~mask])**2)

    return z



def naca_4_digit_airfoil_slope(x,m,p):

    mask = x <= p 
    
    dzdx = np.zeros_like(x)

    
    dzdx[mask] = (m/p**2) * (2 * p - 2 * x[mask])
    
    dzdx[~mask] = (m/(1-p)**2) * (2*p - 2*x[~mask])

    return dzdx

def alpha_L_0(theta, m, p):
    x = 0.5 * (1 - np.cos(theta))
    result = (-1/np.pi) * np.trapz(naca_4_digit_airfoil_slope(x, m, p) * (np.cos(theta) - 1), theta)
    return result



## NACA 2412

m = 0.02
p = 0.4
theta = np.linspace(0, np.pi, 100)

alpha_L_0 = alpha_L_0(theta,m,p)
print(f'Alpha_L_0: {alpha_L_0:.4f} radians | {np.degrees(alpha_L_0):.4f} degrees')

z = naca_4_digit_airfoil(x, m, p)


plt.plot(x, z)
plt.title('NACA 2412 Airfoil')
plt.xlabel('x/c')
plt.ylabel('z/c')
plt.grid()
plt.axis('equal')
plt.show()