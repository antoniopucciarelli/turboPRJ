import numpy as np 

def bladeStudy(rIn, rOut, omega, rMean, VaMean, VtMeanIn, VtMeanOut, Leu, Tt0, T0, Pt0, P0, eta=1, printout=False, gamma=1.4, R=287.06):
    '''
    This function computes the behaviour of the blade at a radius r with respect to the guideline properties described by the meanline.
        The model used is the FREE VORTEX model with these assumptions: 
            -- inlet enthalpy distribution -> constant along r 
            -- inlet axial speed distribusiton -> constant along r
            -- the mean radius for the inlet and the outlet of the blade is the same 

        inputs:
            rIn         -- blade section inlet radial position
            rOut        -- blade secton outlet radial position 
            omega       -- rotation speed 
            rMean       -- stage mean radius 
            VaMean      -- axial flow speed at mean radius 
            VtMeanIn    -- tangential speed at mean radius inlet 
            VtMeanOut   -- tangential speed at mean radius outlet 
            Leu         -- euler work of the section 
            Tt0         -- inlet total temperature 
            T0          -- inlet static temperature 
            Pt0         -- inlet total pressure 
            P0          -- inlet static pressure 
            eta         -- stage efficiency
            printout    -- boolean value for the printing of the computed quantities 
            gamma       -- specific heat ratio
            R           -- gas constant
    '''

    # cP computation
    cP = gamma / (gamma - 1) * R

    # rotor inlet 
    # Va0 computation 
    Va0 = VaMean

    # rotation speed 
    U0 = omega * rIn

    # phi computation 
    phi = Va0 / U0

    # psi computation 
    psi = Leu / U0**2 

    # lam computation 
    lam = psi * 2 
    
    # Vt0 computation
    Vt0 = VtMeanIn * rMean / rIn 

    # V0 magnitude computation 
    V0 = np.sqrt(Va0**2 + Vt0**2)

    # Wa0 computation 
    Wa0 = Va0 

    # Wt0 computation 
    Wt0 = Vt0 - U0 

    # W0 magnitude computation 
    W0 = np.sqrt(Wa0**2 + Wt0**2)

    # alpha0 angle computation
    alpha0 = np.rad2deg(np.arctan(Vt0/Va0)) 

    # beta0 angle computation 
    beta0 = np.rad2deg(np.arctan(Wt0/Wa0))

    # temperature computation 
    T0 = Tt0 - V0**2 / (2 * cP)

    # speed of sound computation
    a0 = np.sqrt(gamma * R * T0)

    # mach number computation -- absolute
    M0 = V0 / a0

    # mach number computation -- relative 
    Mr0 = W0 / a0 

    # pressure computation
    P0 = Pt0 * (T0/Tt0)**(gamma/(gamma-1))

    # density computation 
    rho0 = P0 / (R * T0)

    # total density computation
    rhot0 = Pt0 / (R * Tt0)
    
    # rotor outlet computation
    # Va1 computation 
    Va1 = VaMean

    # rotation speed 
    U1 = omega * rOut
    
    # Vt1 computation
    Vt1 = VtMeanOut * rMean / rOut 

    # V1 magnitude computation 
    V1 = np.sqrt(Va1**2 + Vt1**2)

    # Wa1 computation
    Wa1 = Va1 

    # Wt1 computation
    Wt1 = Vt1 - U1

    # W1 computation
    W1 = np.sqrt(Wa1**2 + Wt1**2)

    # alpha1 angle computation
    alpha1 = np.rad2deg(np.arctan(Vt1/Va1)) 

    # beta1 angle computation
    beta1 = np.rad2deg(np.arctan(Wt1/Wa1))

    # total temperature computation
    Tt1 = Leu / cP + Tt0

    # ideal temperature computation if the process is completely 
    # isentropic without losses but the work produced is related 
    # to a process that takes into account losses in the stage  
    T1 = Tt1 - V1**2 / (2 * cP)

    # T1 isoentropic computation 
    #   this correction activates only is eta != 1
    T1 = T0 + eta * (T1 - T0)

    # mach number computation 
    a1 = np.sqrt(gamma * R * T1)

    # mach number computation -- absolute
    M1 = V1 / a1

    # mach number computation -- relative 
    Mr1 = W1 / a1 

    # pressure computation
    P1 = P0 * (T1/T0)**(gamma/(gamma-1))

    # total pressure computation
    Pt1 = P1 * (Tt1/T1)**(gamma/(gamma-1))

    # density computation 
    rho1 = P1 / (R * T1)

    # total density computation
    rhot1 = Pt1 / (R * Tt1)

    # reaction degree computation 
    rD = cP * (T1 - T0) / Leu 

    if printout:
        printLength = 54
        nAdim = int((printLength - len(' ADIMENSIONAL PARAMETERS '))/2)
        print('*' * nAdim + ' ADIMENSIONAL PARAMETERS  ' + '*' * nAdim)
        print('-- rD     = {0:>8.2f}        -- psi    = {1:>8.2f}'.format(rD, psi))
        print('-- lambda = {0:>8.2f}        -- phi    = {1:>8.2f}'.format(lam, phi))
        nWork = int((printLength - len(' WORK '))/2)
        print('*' * nWork + ' WORK ' + '*' * nWork)
        print('-- Leu    = {0:>8.2f} J/kg'.format(Leu))
        nRotation = int((printLength - len(' ROTATION '))/2)
        print('*' * nRotation + ' ROTATION ' + '*' * nRotation)
        print('-- U0  = {0:>8.2f} m/s    -- U1  = {1:>8.2f} rad/s'.format(U0, U1))
        print('*' * printLength)
        nDefinitions = int((printLength - len(' DEFINITIONS '))/2)
        print('\n' + '*' * nDefinitions + ' DEFINITIONS  ' + '*' * nDefinitions)
        print('-- 0 => rotor inlet         -- 1 => rotor outlet')
        nTotTemp = int((printLength - len(' TOTAL TEMPERATURE '))/2)
        print('*' * nTotTemp + ' TOTAL TEMPERATURE  ' + '*' * nTotTemp)
        print('-- Tt0    = {0:>8.2f} K      -- Tt1    = {1:>8.2f} K'.format(Tt0, Tt1))
        nAbsKin = int((printLength - len('KINETICS -- ABSOLUTE '))/2)
        print('*' * nAbsKin + ' KINETICS -- ABSOLUTE ' + '*' * nAbsKin)
        print('-- 0                        -- 1')
        print('-- alpha0 = {0:>8.2f} deg    -- alpha1 = {1:>8.2f} deg'.format(alpha0, alpha1))
        print('-- Va0    = {0:>8.2f} m/s    -- Va1    = {1:>8.2f} m/s'.format(Va0, Va1))
        print('-- Vt0    = {0:>8.2f} m/s    -- Vt1    = {1:>8.2f} m/s'.format(Vt0, Vt1))
        print('-- V0     = {0:>8.2f} m/s    -- V1     = {1:>8.2f} m/s'.format(V0, V1))
        nRelKin = int((printLength - len('KINETICS -- RELATIVE '))/2)
        print('*' * nRelKin + ' KINETICS -- RELATIVE ' + '*' * nRelKin)
        print('-- 0                        -- 1                        -- 2')
        print('-- U0     = {0:>8.2f} m/s    -- U1     = {1:>8.2f} m/s'.format(U0, U1))
        print('-- beta0  = {0:>8.2f} deg    -- beta1  = {1:>8.2f} deg'.format(beta0, beta1))
        print('-- Wa0    = {0:>8.2f} m/s    -- Wa1    = {1:>8.2f} m/s'.format(Wa0, Wa1))
        print('-- Wt0    = {0:>8.2f} m/s    -- Wt1    = {1:>8.2f} m/s'.format(Wt0, Wt1))
        print('-- W0     = {0:>8.2f} m/s    -- W1     = {1:>8.2f} m/s'.format(W0, W1))
        nThermo = int((printLength - len(' THERMODYNAMICS '))/2)
        print('*' * nThermo + ' THERMODYNAMICS ' + '*' * nThermo)
        print('-- 0                        -- 1 ')
        print('-- T0     = {0:>8.2f} K      -- T1     = {1:>8.2f} K    '.format(T0, T1))
        print('-- Tt0    = {0:>8.2f} K      -- Tt1    = {1:>8.2f} K    '.format(Tt0, Tt1))
        print('-- a0     = {0:>8.2f} m/s    -- a1     = {1:>8.2f} m/s  '.format(a0, a1))
        print('-- M0     = {0:>8.2f}        -- M1     = {1:>8.2f}      '.format(M0, M1))
        print('-- Mr0    = {0:>8.2f}        -- Mr1    = {1:>8.2f}      '.format(Mr0, Mr1))
        print('-- P0     = {0:>8.2f} bar    -- P1     = {1:>8.2f} bar  '.format(P0/1e+5, P1/1e+5))
        print('-- Pt0    = {0:>8.2f} bar    -- Pt1    = {1:>8.2f} bar  '.format(Pt0/1e+5, Pt1/1e+5))
        print('-- rho0   = {0:>8.2f} kg/m3  -- rho1   = {1:>8.2f} kg/m3'.format(rho0, rho1))
        print('-- rhot0  = {0:>8.2f} kg/m3  -- rhot1  = {1:>8.2f} kg/m3'.format(rhot0, rhot1))
        nBlade = int((printLength - len(' BLADE DIMENSIONS '))/2)
        print('*' * nBlade + ' BLADE DIMENSIONS ' + '*' * nBlade)
        print('-- 0                        -- 1')
        print('-- rIn    = {0:>8.2f} cm     -- rOut   = {1:>8.2f} cm'.format(rIn*1e+2, rOut*1e+2))
        print('-- rMean0 = {0:>8.2f} cm     -- rMean1 = {0:>8.2f} cm'.format(rMean))
        print('*' * printLength) 

    # setting up output vectors 
    adimVec     = [rD, phi, psi, lam]
    rotationVec = [U0, U1]
    abs0Vec     = [Va0, Vt0, V0]
    rel0Vec     = [Wa0, Wt0, W0]
    abs1Vec     = [Va1, Vt1, V1]
    rel1Vec     = [Wa1, Wt1, W1]
    angleVec    = [alpha0, alpha1, beta0, beta1]
    thermo0     = [T0, P0, rho0, Tt0, Pt0, rhot0, M0, Mr0]
    thermo1     = [T1, P1, rho1, Tt1, Pt1, rhot1, M1, Mr1]

    return adimVec, rotationVec, abs0Vec, rel0Vec, abs1Vec, rel1Vec, angleVec, thermo0, thermo1