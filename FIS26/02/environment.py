from definitions import *

# Construction of Simulation Objects

class Environment(object):
    """
    Represents the environment in which the simulation occurs
    """
    def __init__(self, mode, debug):
        """
        Initializes environment and set debug mode True or False

        :param debug: Set debug condition True or False.
        :type debug: bool.
        """
        
        self.time = 0
        self.laps = 0
        self.mode = mode
        self.debug = debug
        self.create_environment()
        
    def create_environment(self):
        """
        Creates the construction blocks for the environment and 
        set them in the field.

        :param None: None.
        :type None: None.
        """

        vs.rate(FREQUENCY)
        self.create_base()
        self.create_bar()
        self.create_middle_module()
        self.create_station()
        self.create_wheel()
        self.create_falling_block()

        if self.mode == "TEST_BLOCK":
            self.create_test_block()
        if self.mode == "EVALUATION_OBJECT":
            self.create_evaluation_object()

    def rotate_environment(self, angle, axis, origin):
        """
        Rotates the entire environment for different views.

        :param angle: Rotation angle of the environment.
        :type angle: float.
        :param axis: Rotation axis of the environment.
        :type axis: vpython.vec.
        :param origin: CIR of the environment.
        :type origin: vpython.vec.
        """

        # Coordinates vs.vec (z, y, x)

        self.base_part_1.rotate(angle = angle, axis = axis, origin = origin)
        self.base_part_2.rotate(angle = angle, axis = axis, origin = origin)
        self.base_part_3.rotate(angle = angle, axis = axis, origin = origin)
        self.base_part_4.rotate(angle = angle, axis = axis, origin = origin)
        self.lower_bar.rotate(angle = angle, axis = axis, origin = origin)
        self.upper_bar.rotate(angle = angle, axis = axis, origin = origin)
        self.middle_module_1.rotate(angle = angle, axis = axis, origin = origin)
        self.middle_module_2.rotate(angle = angle, axis = axis, origin = origin)
        self.station.rotate(angle = angle, axis = axis, origin = origin)
        self.support.rotate(angle = angle, axis = axis, origin = origin)
        self.support_1.rotate(angle = angle, axis = axis, origin = origin)
        self.support_2.rotate(angle = angle, axis = axis, origin = origin)
        self.support_3.rotate(angle = angle, axis = axis, origin = origin)
        self.support_bar_1.rotate(angle = angle, axis = axis, origin = origin)
        self.support_bar_2.rotate(angle = angle, axis = axis, origin = origin)
        self.support_block_1.rotate(angle = angle, axis = axis, origin = origin)
        self.support_block_2.rotate(angle = angle, axis = axis, origin = origin)
        self.wheel_1.rotate(angle = angle, axis = axis, origin = origin)
        self.wire_1.rotate(angle = angle, axis = axis, origin = origin)
        self.wire_3.rotate(angle = angle, axis = axis, origin = origin)
        self.wire_4.rotate(angle = angle, axis = axis, origin = origin)
        self.falling_block.rotate(angle = angle, axis = axis, origin = origin)

        if self.mode == "TEST_BLOCK":
            self.test_block.rotate(angle = angle, axis = axis, origin = origin)
        if self.mode == "EVALUATION_OBJECT":
            self.evaluation_object.rotate(angle = angle, axis = axis, origin = origin)

    def action(self, axis, origin):

        self.time += dt

        if self.mode == "WITHOUT":
            thetadot = self.time * thetadotdot_wm
            theta = thetadot * dt

            wire_vel = self.time * wire_acceleration_wm
            distance = wire_vel * dt

        if self.mode == "TEST_BLOCK":
            thetadot = self.time * thetadotdot_tb
            theta = thetadot * dt

            wire_vel = self.time * wire_acceleration_tb
            distance = wire_vel * dt

            self.test_block.rotate(angle = theta, axis = axis, origin = origin)
            
        if self.mode == "EVALUATION_OBJECT":
            thetadot = self.time * thetadotdot_eo
            theta = thetadot * dt

            wire_vel = self.time * wire_acceleration_eo
            distance = wire_vel * dt

            self.evaluation_object.rotate(angle = theta, axis = axis, origin = origin)

        self.wire_4.size += vs.vec(distance, 0 ,0)
        self.falling_block.pos -= vs.vec(0, distance, 0)
        self.station.rotate(angle = theta, axis = axis, origin = origin)
        self.support.rotate(angle = theta, axis = axis, origin = origin)
        self.laps += theta

        if self.laps > 10*math.pi:
            self.reset(self.time)

    def reset(self, time):

        self.time = 0            # Begin Time
        self.laps = 0       # Number of laps given

        self.base_part_1.visible = False
        self.base_part_2.visible = False
        self.base_part_3.visible = False
        self.base_part_4.visible = False
        self.lower_bar.visible = False
        self.upper_bar.visible = False
        self.middle_module_1.visible = False
        self.middle_module_2.visible = False
        self.station.visible = False
        self.support.visible = False
        self.support_1.visible = False
        self.support_2.visible = False
        self.support_3.visible = False
        self.support_bar_1.visible = False
        self.support_bar_2.visible = False
        self.support_block_1.visible = False
        self.support_block_2.visible = False
        self.wheel_1.visible = False
        self.wire_1.visible = False
        self.wire_2.visible = False
        self.wire_3.visible = False
        self.wire_4.visible = False
        self.falling_block.visible = False
    
        if self.mode == "TEST_BLOCK":
            self.test_block.visible = False
        if self.mode == "EVALUATION_OBJECT":
            self.evaluation_object.visible = False

        self.create_environment()

    def create_base(self):
        """
        Creates the construction blocks for the base and 
        set them in the environment.

        :param None: None.
        :type None: None.
        """

        # Coordinates vs.vec (z, y, x)

        self.base_part_1 = box(pos = vs.vec(0, 3*BASE_HEIGHT/2, BASE_WIDTH/3) + vs.vec(0, -Y_OFFSET, 0),
                          size = vs.vec(2*BASE_WIDTH/3, BASE_HEIGHT, BASE_HEIGHT),
                          color = color.white)

        self.base_part_2 = box(pos = vs.vec(BASE_WIDTH/4, BASE_HEIGHT/2, math.sqrt(3)*BASE_WIDTH/4) + vs.vec(0, -Y_OFFSET, 0),
                          size = vs.vec(BASE_WIDTH, BASE_HEIGHT, BASE_HEIGHT),
                          color = color.white)

        self.base_part_3 = box(pos = vs.vec(-BASE_WIDTH/4, BASE_HEIGHT/2, math.sqrt(3)*BASE_WIDTH/4) + vs.vec(0, -Y_OFFSET, 0),
                          size = vs.vec(BASE_WIDTH, BASE_HEIGHT, BASE_HEIGHT),
                          color = color.white)

        self.base_part_4 = cylinder(pos = vs.vec(0, 0, math.sqrt(3)*BASE_WIDTH/2) + vs.vec(0, -Y_OFFSET, 0),
                        axis = vs.vec(0,1,0),
                        size = vs.vec(BASE_HEIGHT, BASE_HEIGHT, BASE_HEIGHT), 
                        color = color.white)

        self.base_part_2.rotate(angle = math.pi/3, axis = vs.vec(0, 1, 0), origin = self.base_part_2.pos)
        self.base_part_3.rotate(angle = -math.pi/3, axis = vs.vec(0, 1, 0), origin = self.base_part_3.pos)

    def create_bar(self):
        """
        Creates the construction blocks for the vertical bar and 
        set them in the environment.

        :param None: None.
        :type None: None.
        """

        # Coordinates vs.vec (z, y, x)

        self.lower_bar = cylinder(pos = vs.vec(0, 2*BASE_HEIGHT, BASE_WIDTH/3) + vs.vec(0, -Y_OFFSET, 0),
                        axis = vs.vec(0,1,0),
                        size = vs.vec(LOWER_BAR_HEIGHT, LOWER_BAR_RADIUS, LOWER_BAR_RADIUS), 
                        color = color.white)

        self.upper_bar = cylinder(pos = vs.vec(0, 2*BASE_HEIGHT + LOWER_BAR_HEIGHT, BASE_WIDTH/3) + vs.vec(0, -Y_OFFSET, 0),
                        axis = vs.vec(0,1,0),
                        size = vs.vec(UPPER_BAR_HEIGHT, UPPER_BAR_RADIUS, UPPER_BAR_RADIUS), 
                        color = color.white)
        
    def create_middle_module(self):
        """
        Creates the construction blocks for the middle rotating module and 
        set them in the environment.

        :param None: None.
        :type None: None.
        """

        # Coordinates vs.vec (z, y, x)

        self.middle_module_1 = cylinder(pos = vs.vec(0, 2*BASE_HEIGHT + LOWER_BAR_HEIGHT, BASE_WIDTH/3) + vs.vec(0, -Y_OFFSET, 0),
                            axis = vs.vec(0,1,0),
                            size = vs.vec(MIDDLE_MODULE_HEIGHT, MIDDLE_MODULE_RADIUS, MIDDLE_MODULE_RADIUS), 
                            color = color.white)

        self.middle_module_2 = cylinder(pos = vs.vec(0, 2*BASE_HEIGHT + LOWER_BAR_HEIGHT + MIDDLE_MODULE_HEIGHT, BASE_WIDTH/3) + vs.vec(0, -Y_OFFSET, 0),
                            axis = vs.vec(0,1,0),
                            size = vs.vec(MIDDLE_MODULE_HEIGHT, MIDDLE_MODULE_RADIUS/2, MIDDLE_MODULE_RADIUS/2), 
                            color = color.white)
        
    def create_station(self):
        """
        Creates the construction blocks for the upper station 
        where the objects are placed and set them in the environment.

        :param None: None.
        :type None: None.
        """

        # Coordinates vs.vec (z, y, x)

        self.station = box(pos = vs.vec(0, 2*BASE_HEIGHT + 2*LOWER_BAR_HEIGHT, BASE_WIDTH/3) + vs.vec(0, -Y_OFFSET, 0),
                        size = vs.vec(UPPER_STATION_LENGHT, BASE_HEIGHT, UPPER_STATION_WIDTH),
                        color = color.white)

        self.support = box(pos = vs.vec(0, 2*BASE_HEIGHT + 2*LOWER_BAR_HEIGHT + UPPER_STATION_HEIGHT, BASE_WIDTH/3) + vs.vec(0, -Y_OFFSET, 0),
                        size = vs.vec(BLOCK_SUPPORT_LENGHT, BLOCK_SUPPORT_HEIGHT, BLOCK_SUPPORT_WIDTH),
                        color = color.white)

    def create_wheel(self):
        """
        Creates the construction blocks for the wheel support and 
        the proper wheel, set them in the environment.

        :param None: None.
        :type None: None.
        """

        # Coordinates vs.vec (z, y, x)

        self.support_block_1 = cylinder(pos = vs.vec(0, 2*BASE_HEIGHT + LOWER_BAR_HEIGHT/2, BASE_WIDTH/3 - BAR_SUPPORT_HEIGHT/4) + vs.vec(0, -Y_OFFSET, 0),
                                axis = vs.vec(0, 0, 1),
                                size = vs.vec(BAR_SUPPORT_HEIGHT, BAR_SUPPORT_RADIUS, BAR_SUPPORT_RADIUS), 
                                color = color.white)

        self.support_bar_1 = cylinder(pos = vs.vec(WHEEL_SUPPORT_BAR_HEIGHT/2, 2*BASE_HEIGHT + LOWER_BAR_HEIGHT/2, BASE_WIDTH/3 + BAR_SUPPORT_HEIGHT/2) + vs.vec(0, -Y_OFFSET, 0),
                                axis = vs.vec(-1, 0, 0),
                                size = vs.vec(WHEEL_SUPPORT_BAR_HEIGHT, WHEEL_SUPPORT_BAR_RADIUS, WHEEL_SUPPORT_BAR_RADIUS), 
                                color = color.white)

        self.support_block_2 = cylinder(pos = vs.vec(WHEEL_SUPPORT_BAR_HEIGHT/2, 2*BASE_HEIGHT + LOWER_BAR_HEIGHT/2, BASE_WIDTH/3 - BAR_SUPPORT_HEIGHT/4) + vs.vec(0, -Y_OFFSET, 0),
                                axis = vs.vec(0, 0, 1),
                                size = vs.vec(BAR_SUPPORT_HEIGHT, BAR_SUPPORT_RADIUS, BAR_SUPPORT_RADIUS), 
                                color = color.white)

        self.support_bar_2 = cylinder(pos = vs.vec(WHEEL_SUPPORT_BAR_HEIGHT/2, 2*BASE_HEIGHT, BASE_WIDTH/3) + vs.vec(0, -Y_OFFSET, 0),
                                axis = vs.vec(0, 1, 0),
                                size = vs.vec(WHEEL_SUPPORT_BAR_HEIGHT/6, 0.8*WHEEL_SUPPORT_BAR_RADIUS, 0.8*WHEEL_SUPPORT_BAR_RADIUS), 
                                color = color.white)

        self.support_1 = box(pos = vs.vec(WHEEL_SUPPORT_BAR_HEIGHT/2, 2*BASE_HEIGHT + WHEEL_SUPPORT_BAR_HEIGHT/6, BASE_WIDTH/3) + vs.vec(0, -Y_OFFSET, 0),
                        size = vs.vec(WHEEL_SUPPORT_WIDTH, WHEEL_SUPPORT_HEIGHT - WHEEL_RADIUS, WHEEL_SUPPORT_WIDTH),
                        color = color.white)

        self.support_2 = box(pos = vs.vec(WHEEL_SUPPORT_BAR_HEIGHT/2, WHEEL_SUPPORT_HEIGHT + 2*BASE_HEIGHT + WHEEL_SUPPORT_BAR_HEIGHT/6, BASE_WIDTH/3 + WHEEL_SUPPORT_WIDTH/2 - (WHEEL_SUPPORT_WIDTH - WHEEL_SUPPORT_INNER_SECTION)/4) + vs.vec(0, -Y_OFFSET, 0),
                        size = vs.vec(3*WHEEL_SUPPORT_WIDTH, 2.5*WHEEL_SUPPORT_HEIGHT, WHEEL_SUPPORT_WIDTH),
                        color = color.white)

        self.support_3 = box(pos = vs.vec(WHEEL_SUPPORT_BAR_HEIGHT/2, WHEEL_SUPPORT_HEIGHT + 2*BASE_HEIGHT + WHEEL_SUPPORT_BAR_HEIGHT/6, BASE_WIDTH/3 - WHEEL_SUPPORT_WIDTH/2 + (WHEEL_SUPPORT_WIDTH - WHEEL_SUPPORT_INNER_SECTION)/4) + vs.vec(0, -Y_OFFSET, 0),
                        size = vs.vec(3*WHEEL_SUPPORT_WIDTH, 2.5*WHEEL_SUPPORT_HEIGHT, WHEEL_SUPPORT_WIDTH),
                        color = color.white)

        self.wheel_1 = cylinder(pos = vs.vec(WHEEL_SUPPORT_BAR_HEIGHT/2, self.middle_module_1.pos.y + Y_OFFSET, BASE_WIDTH/3 - WHEEL_INNER_SECTION/2) + vs.vec(0, -Y_OFFSET, 0),
                                axis = vs.vec(0, 0, 1),
                                size = vs.vec(WHEEL_INNER_SECTION, WHEEL_RADIUS, WHEEL_RADIUS), 
                                color = color.white)

    def create_falling_block(self):
        """
        Creates the construction blocks for the falling cylinder, with the respective
        wires attached to it.

        :param None: None.
        :type None: None.
        """

        # Coordinates vs.vec (z, y, x)

        pivot = self.wheel_1.pos + vs.vec(0, WHEEL_RADIUS/2, WHEEL_INNER_SECTION/2)
        pivot -= self.middle_module_1.pos + vs.vec(0, MIDDLE_MODULE_HEIGHT/2, MIDDLE_MODULE_RADIUS/2)
        pivot_n = pivot.norm()

        self.wire_1 = cylinder(pos = self.middle_module_1.pos + vs.vec(0, MIDDLE_MODULE_HEIGHT/2, MIDDLE_MODULE_RADIUS/2),
                               axis = pivot_n,
                               size = vs.vec(pivot.mag, WIRE_RADIUS, WIRE_RADIUS),
                               color = color.blue)

        self.wire_2 = ring(pos = self.middle_module_1.pos + vs.vec(0, MIDDLE_MODULE_HEIGHT/2, 0), 
                                axis = vs.vec(0,1,0), 
                                radius = MIDDLE_MODULE_RADIUS/2 + WIRE_RADIUS/2, 
                                thickness = WIRE_RADIUS/2,
                                color = color.blue)
        
        self.wire_3 = curve(radius = WIRE_RADIUS/2,
                            color = color.blue)
        for t in numpy.arange(0, math.pi/2, 0.01):
            self.wire_3.append(pos = (self.wheel_1.pos.x + WHEEL_RADIUS*math.sin(t)/2, 
                                      self.wheel_1.pos.y + WHEEL_RADIUS*math.cos(t)/2, 
                                      self.wheel_1.pos.z + WHEEL_INNER_SECTION/2))

        self.wire_4 = cylinder(pos = self.wheel_1.pos + vs.vec(WHEEL_RADIUS/2, 0, WHEEL_INNER_SECTION/2),
                               axis = vs.vec(0, -1, 0),
                               size = vs.vec(3*BASE_HEIGHT, WIRE_RADIUS, WIRE_RADIUS),
                               color = color.blue)

        self.falling_block = cylinder(pos = self.wire_4.pos - vs.vec(0, 2*BASE_HEIGHT, 0),
                                      axis = vs.vec(0, -1, 0),
                                      size = vs.vec(BASE_HEIGHT, 0.7*BAR_SUPPORT_RADIUS, 0.7*BAR_SUPPORT_RADIUS),
                                      color = color.red)

    def create_test_block(self):

        self.test_block = box(pos = vs.vec(0, 2*BASE_HEIGHT + 2*LOWER_BAR_HEIGHT + UPPER_STATION_HEIGHT + BLOCK_SUPPORT_HEIGHT, BASE_WIDTH/3) + vs.vec(0, -Y_OFFSET, 0),
                              size = vs.vec(BLOCK_SUPPORT_LENGHT, 0.8*BLOCK_SUPPORT_HEIGHT, BLOCK_SUPPORT_WIDTH),
                              color = color.blue)

    def create_evaluation_object(self):

        self.evaluation_object = cylinder(pos = vs.vec(-BLOCK_SUPPORT_LENGHT/2, 2*BASE_HEIGHT + 2*LOWER_BAR_HEIGHT + 1.5*UPPER_STATION_HEIGHT + BLOCK_SUPPORT_WIDTH/2, BASE_WIDTH/3) + vs.vec(0, -Y_OFFSET, 0),
                                axis = vs.vec(1, 0, 0),
                                size = vs.vec(BLOCK_SUPPORT_LENGHT, BLOCK_SUPPORT_WIDTH, BLOCK_SUPPORT_WIDTH), 
                                color = color.orange)