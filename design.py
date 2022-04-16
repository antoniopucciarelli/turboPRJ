# importing libraries
from turboClass import turboBlade
from turboCoeff import similarity
from geometry import bladeGenerator
import contextlib

# data
# constraints
mFlux = 100     # mass flux                [kg/s]
betaP = 1.45    # compression ratio        [--]
maxD  = 0.9     # maximum tip diameter     [m]
maxR  = maxD/2  # maximum tip radius       [m]

# inlet values
Pt0 = 1e+5      # inlet total pressure     [Pa]
Tt0 = 300       # inlet total temperature  [K]

# stage hypothesis
# reaction degree
rD = 0.5
# stage mean radius -> radius @ inlet blade midspan
rMean = 0.39
# rotor inlet tangential velocity
Vt0Umean = 0

# Vt0 = (1 - rD - lam/4) * Umean -> lam = 4 * (1 - rD - Vt0/Umean) 
# psi = lam / 2 
lam = (1 - rD - Vt0Umean) * 4 
psiTarget = lam / 2

# declaring blades
nRotorBlades = 30
nStatorBlades = 25

# output file generation
file_path = 'compressor_' + str(rD) + '_' + str(rMean) + '_' + str(nRotorBlades) + '_' + str(nStatorBlades) + '.txt'
with open(file_path, "w") as file:
    with contextlib.redirect_stdout(file):
        # generation of mean line properties to be used for the blade assembly 
        adimVec, bladeVec, rotationVec, V0vec, V1vec, V2vec, _, _, _, thermo0, thermo1, _, work = similarity.stageProperties(rD, psiTarget, rMean, mFlux, Tt0, Pt0, betaP, T1real=True, printout=True)

        # values allocation 
        nSection           = 50
        eta                = adimVec[2]
        omega              = rotationVec[1]
        b0                 = bladeVec[0]
        hubRadius          = rMean - b0/2
        rotorVaMeanInlet   = V0vec[0]
        rotorVtMeanInlet   = V0vec[1] 
        rotorVaMeanOutlet  = V1vec[0]
        rotorVtMeanOutlet  = V1vec[1]
        statorVaMeanInlet  = V1vec[0] 
        statorVtMeanInlet  = V1vec[1]
        statorVaMeanOutlet = V2vec[0]
        statorVtMeanOutlet = V2vec[1]
        Tt1                = thermo1[3]
        Pt1                = thermo1[4]

        # rotor study 
        # rotor object generation 
        print('\n\n-- ROTOR STUDY -- # blades {0:d}'.format(nRotorBlades))
        rotorBlade = turboBlade.blade(ID=1, turboType='rotor', nSection=nSection, inletBladeHeight=b0, outletBladeHeight=b0, inletHubRadius=hubRadius, outletHubRadius=hubRadius, omega=omega, nBlade=nRotorBlades)
        # blade dimensions allocation -> kinetics inlet
        rotorBlade.allocateKinetics(rMean=rMean, VtMean=rotorVtMeanInlet, VaMean=rotorVaMeanInlet, omega=omega, section='inlet')
        # blade dimensions allocation -> kinetics outlet
        rotorBlade.allocateKinetics(rMean=rMean, VtMean=rotorVtMeanOutlet, VaMean=rotorVaMeanOutlet, omega=omega, section='outlet')
        # blade dimensions allocation -> thermodynamics inlet/outlet
        rotorBlade.allocateThermodynamics(Tt0=Tt0, Pt0=Pt0, eta=eta)
        # rotor blade geometry allocation
        rotorBlade.generateGeometry(pos='data/airfoils/naca65.txt', STLname='rotor', plot=False, printout=False)
        # computing the best shape 
        rotorBlade.bladeGenerator(Pt0, Tt0, mFlux, STLname='rotor', plot=False, nMaxShape=1)

        # stator study 
        # stator object generation
        print('\n\n-- STATOR STUDY -- # blades {0:d}'.format(nStatorBlades))
        statorBlade = turboBlade.blade(ID=2, turboType='stator', nSection=nSection, inletBladeHeight=b0, outletBladeHeight=b0, inletHubRadius=hubRadius, outletHubRadius=hubRadius, omega=0, nBlade=nStatorBlades)
        # blade dimensions allocation -> kinetics inlet 
        statorBlade.allocateKinetics(rMean=rMean, VtMean=statorVtMeanInlet, VaMean=statorVaMeanInlet, omega=0, section='inlet')
        # blade dimension allocation -> kinetics outlet
        statorBlade.allocateKinetics(rMean=rMean, VtMean=statorVtMeanOutlet, VaMean=statorVaMeanOutlet, omega=0, section='outlet')
        # blade dimensions allocation -> thermodynamics inlet/outlet
        statorBlade.allocateThermodynamics(Tt0=Tt1, Pt0=Pt1, eta=eta)
        # copying flow properties from rotor outlet to stator inlet 
        statorBlade.copySection(blade=rotorBlade, fromSection='outlet', toSection='inlet')
        # stator blade geometry allocation
        statorBlade.generateGeometry(pos='data/airfoils/naca65.txt', STLname='stator', plot=False, printout=False)
        # computing the best shape 
        statorBlade.bladeGenerator(Pt1, Tt1, mFlux, STLname='stator', plot=False, nMaxShape=1)

        # .scad file generation 
        nRotorBlades  = rotorBlade.nBlade
        nStatorBlades = statorBlade.nBlade 
        rotorHub      = [rotorBlade.blade[0].chord, rotorBlade.blade[0].camber[0,0], rotorBlade.blade[0].camber[0,1], rotorBlade.blade[0].camber[0,2], rotorBlade.blade[0].camber[-1,0], rotorBlade.blade[0].camber[-1,1], rotorBlade.blade[0].camber[-1,2]]
        statorHub     = [statorBlade.blade[0].chord, statorBlade.blade[0].camber[0,0], statorBlade.blade[0].camber[0,1], statorBlade.blade[0].camber[0,2], statorBlade.blade[0].camber[-1,0], statorBlade.blade[0].camber[-1,1], statorBlade.blade[0].camber[-1,2]]
        b1            = b0 
        bladeGenerator.SCADsaving(nRotorBlades, nStatorBlades, rotorHub, statorHub, rMean, b0, b1, rotorPath='../container/rotor.stl', statorPath='../container/stator.stl', geometryPath='geometry/')

# plotting results
rotorBlade.printMeridional()
statorBlade.printMeridional()