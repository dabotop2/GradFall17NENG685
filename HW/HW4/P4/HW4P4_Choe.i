This models a simple NW neutron burst and models a simple city-scape.
c
c Simple NW det scenario.  A NW is set off on the edge of the city.  To start, let's create
c a scale model.  The key factors for the model: 
c
c 1) Model three "city blocks" of long apartment buldings.  The buildings are .3 m high,
c    .3m wide, and 1.0 m long separated by 0.15 m of air. The walls are .03 m thick concrete.
c    (All dimensions scaled by a factor of 10 now)
c 2) The flux is tallied inside of a car modeled as a 0.1 wide, 0.15 m tall, and 0.25 m long
c    aluminum box with 0.0025 m thick walls. The car is located on the far side of the 3rd
c    block from the source.
c 3) Add a volume flux tally to the inside of the car.
c 4) The source is modeled as a point fission source (Watt spectrum) from a HEU bomb.
c
c *******************************************************************************************
c  Cell Cards
c *******************************************************************************************
1 3 -2.2961415    -1 11     imp:n=1  $1st box
2 like 1 but trcl=(550 0 0)  $2nd box: duplicate the block1 and position at x=550cm
3 like 1 but trcl=(1000 0 0) $3rd box: duplicate the block1 and position at x=1000cm
4 2 -2.6989       -2 22     imp:n=1 $car1
5 like 4 but trcl=(875 0 0)  $2nd car: duplicate the car1 and position at x=875cm
6 like 4 but trcl=(1325 0 0) $2nd car: duplicate the car1 and position at x=875cm
7 4 -1.3           3 -111   imp:n=1 $Gound made of asphalt

c *******************************************************************************************
c Surfaces
c *******************************************************************************************
1   RPP 100 400      -500 500      0 300       $Block 1 outer
11  RPP 130 370      -470 470      30 270      $Block 1 inner
2   RPP 425 525      -125 125      0 150       $Car1 outer
22  RPP 427.5 522.5  -122.5 122.5  2.5 147.5   $Car1 inner
3   PZ  0                                      $Gound made of asphalt
111 RPP -150 15000 -550 550 -100 350           $Outer killzone 

c *******************************************************************************************
c Data Cards
c *******************************************************************************************
c Concrete, Regular, rho =2.300
m1 1001  -0.013742 $Concrete H
     8016  -0.046056 $Concrete O
     11023 -0.001747 $Concrete Na
     13027 -0.001745 $Concrete Al
     14000 -0.016620 $Concrete Si
     20000 -0.001521 $Concrete Ca
     26000 -0.000347 $Concrete Fe
c Aluminum, rho =2.6989
m2 13027 -0.060238 $Al
c Material3: new material for building, total_rho=2.2961415
c 30% Wood(rho =0.192), 20%Al(rho =0.53978), 20%steel(rho =1.564), 30%air(rho =0.0003615)
m3 1001  -0.006842 $Wood H
     6000  -0.004785 $Wood C
     7014  -0.000041 $Wood N
     8016  -0.003089 $Wood O
     12000 -0.000009 $Wood Mg
     16000 -0.000018 $Wood S
     19000 -0.000006 $Wood K
     20000 -0.000006 $Wood Ca
     13027 -0.012047 $Al
     6000  -0.000392 $Steel C
     26000 -0.016781 $Steal Fe
c     6000  -0.000000 $Air C
     7014  -0.000012 $Air N
     8016  -0.000003 $Air O
c     18000 -0.000000 $Air Ar
c Asphalt, rho=1.3
m4 1001    -0.080564 $Asphalt H
     6000  -0.055277 $Asphalt C
     7014  -0.000338 $Asphalt N
     8016  -0.000198 $Asphalt O
     16000 -0.000920 $Asphalt S
     23000 -0.000006 $Asphalt V
c     28000 -0.000000 $Asphalt Ni
c *******************************************************************************************
c Physics
c *******************************************************************************************
SDEF PAR=n POS 0 500 150 ERG=d4
SP4 -3 0.988 2.249
c *******************************************************************************************
c Tallies
c *******************************************************************************************
fc4 Flux in cars
f4:n 4 5 6
e4 1e-8 25ILOG 20
PRINT
MODE n
NPS 1E12