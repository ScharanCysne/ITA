from definitions import *

# Construction of Simulation Objects

pedestal = box( pos=pedestal_top-vs.vec(0,hpedestal/2,offset),
                size=vs.vec(wpedestal,1.1*hpedestal,wpedestal),
                color=color.white)

base = box( pos=pedestal_top-vs.vec(0,hpedestal+tbase/2,offset),
            size=vs.vec(wbase,tbase,wbase),
            color=pedestal.color)

axis1 = cylinder( pos=pedestal_top - vs.vec(0,0,offset), 
                 axis=vs.vec(0,0,1),
                 size=vs.vec(offset,d/4,d/4), 
                 color=pedestal.color)

pipe1 = cylinder( pos=pedestal_top-vs.vec(0,-d,(3*d)/2),
                  axis=vs.vec(0,-1,0),
                  size=vs.vec(L1display,d,d), 
                  color=color.red)

pipe1.rotate( angle=thetazero, axis=vs.vec(0,0,1), origin=vs.vec(axis1.pos.x, axis1.pos.y, pipe1.pos.z) )

pivot1 = vs.vec(axis1.pos.x, axis1.pos.y, 0)

axis2 = vs.sphere(pos=pedestal_top-vs.vec(0,L1,(3*d)/2), 
                  axis=vs.vec(0,0,1), 
                  radius=d/2, 
                  color=pipe1.color )

axis2.rotate( angle= thetazero, axis=vs.vec(0,0,1), origin=vs.vec(axis1.pos.x, axis1.pos.y, axis2.pos.z) )

pipe2 = cylinder( pos = pedestal_top - vs.vec(0,L1,0),
                  axis = vs.vec(1, 0, 0),
                  size = vs.vec(L2display, d, d),
                  color = pipe1.color)

pipe2.rotate( angle= thetazero, axis=vs.vec(0,0,1), origin=vs.vec(axis2.pos.x, axis2.pos.y, axis2.pos.z) )

# Simulation Execution

while t < 10:

    vs.rate(FREQUENCY) 
    
    thetadotdot = Tdotdot(theta)
    thetadot += thetadotdot*dt
    dtheta = thetadot*dt
    theta += thetadot*dt

    pipe1.rotate( angle=dtheta, axis=vs.vec(0,0,1), origin=pivot1 )
    axis2.rotate( angle=dtheta, axis=vs.vec(0,0,1), origin=pivot1 )
    pipe2.rotate( angle=dtheta, axis=vs.vec(0,0,1), origin=pivot1 )
    pipe2.pos = axis2.pos
    
    t = t+dt

    period_int_entry.append(period(t))
    x_position_entry.append(axis2.pos.x)
    time_frame_entry.append(t)

plt.plot(time_frame_entry, x_position_entry)
# naming the x axis 
plt.xlabel('Time - axis') 
# naming the y axis 
plt.ylabel('Period - axis') 
# giving a title to my graph 
plt.title('Variable Mass in L Shape Pendullum') 
# function to show the plot 
plt.show()