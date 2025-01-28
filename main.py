import pygame
from Elements import Button, Scale, CanSat, Text, ForceDiagram, DrawGraph

pygame.init()
dimensions = (1000, 800)
w,h = dimensions
screen = pygame.display.set_mode(dimensions)
pygame.display.set_caption('CanSat Simulator')

hit_raw_time = None
hit_para_time = None
raw_vs_values, para_vs_values = None, None
condition_1, condition_2 = False, False
run_simulation = False
setup_simulation = True
flight_stats = False
graph_state = False
scale_padding = 35
scale_max = 5
gravity = 9.81
mass = 0.4
parachute_upthrust = 3.18
wind = 0

run_button = Button(w // 2 - 125, (h // 2) - 200, 250, 50, 'Run')
scale = Scale(dimensions, scale_max, scale_padding)

scale_up = Button((w // 2) + 75, (h // 2) - 100, 50, 50, '+')
scale_down = Button((w // 2), (h // 2) - 100, 50, 50, '-')
scale_text = Text(f'Scale:  {scale_max}00 m', (w // 2) - 150, (h // 2) - 75, 24)

para_up = Button((w // 2) + 75, (h // 2), 50, 50, '+')
para_down = Button((w // 2), (h // 2), 50, 50, '-')
para_text = Text(f'Parachute Upthrust:  {parachute_upthrust}N', (w // 2) - 250, (h // 2) + 25, 24)

grav_up = Button((w // 2) + 75, (h // 2) + 100, 50, 50, '+')
grav_down = Button((w // 2), (h // 2) + 100, 50, 50, '-')
grav_text = Text(f'Acceleration due to Gravity:  {gravity}m/s^2', (w // 2) - 350, (h // 2) + 125, 24)

mass_up = Button((w // 2) + 75, (h // 2) + 300, 50, 50, '+')
mass_down = Button((w // 2), (h // 2) + 300, 50, 50, '-')
mass_text = Text(f'Mass:  {mass}kg', (w // 2) - 150, (h // 2) + 325, 24)

wind_up = Button((w // 2) + 75, (h // 2) + 200, 50, 50, '+')
wind_down = Button((w // 2), (h // 2) + 200, 50, 50, '-')
wind_text = Text(f'Horizontal Wind:  {wind} m/s <->', (w // 2) - 250, (h // 2) + 225, 24)

cansat_raw = CanSat(dimensions, scale_padding, scale_max, 100, mass, 250, 0, (0, 0, 255), False, gravity, parachute_upthrust, wind)
cansat_p1 = CanSat(dimensions, scale_padding, scale_max, 100, mass, 550, 0, (0, 255, 0), True, gravity, parachute_upthrust, wind)

raw_get_graphs = Button(250, 710, 100, 50, 'Get Graphs')
para_get_graphs = Button(650, 710, 100, 50, 'Get Graphs')

clock = pygame.time.Clock()

def asfromvs(v_s_values):
    asv = []
    for value in v_s_values:
        asv.append([(value[0] / value[1]), value[1]])
    
    return asv

def ssfromvs(v_s_values):
    ssv = []

    for value in v_s_values:
        ssv.append([(value[0] * value[1]), value[1]])
    
    return ssv

while True:
    screen.fill((255,255, 255))
    if setup_simulation:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

            if run_button.is_Clicked(event):
                setup_simulation = False
                run_simulation = True
                flight_stats = False
                initial_time = pygame.time.get_ticks()
                
            
            if scale_up.is_Clicked(event):
                scale_max += 1
                scale = Scale(dimensions, scale_max, scale_padding)
                scale_text = Text(f'Scale: {scale_max}00 m', (w // 2) - 150, (h // 2) - 75, 24)
            
            if scale_down.is_Clicked(event):
                scale_max -= 1
                scale = Scale(dimensions, scale_max, scale_padding)
                scale_text = Text(f'Scale: {scale_max}00 m', (w // 2) - 150, (h // 2) - 75, 24)
            
            if para_up.is_Clicked(event):
                parachute_upthrust += 0.1
                parachute_upthrust = round(parachute_upthrust, 2)
                para_text = Text(f'Parachute Upthrust:  {parachute_upthrust}N', (w // 2) - 250, (h // 2) + 25, 24)
                cansat_raw = CanSat(dimensions, scale_padding, scale_max, 100, mass, 250, 35, (0, 0, 255), False, gravity, parachute_upthrust, wind)
                cansat_p1 = CanSat(dimensions, scale_padding, scale_max, 100, mass, 550, 35, (0, 255, 0), True, gravity, parachute_upthrust, wind)
            
            if para_down.is_Clicked(event):
                parachute_upthrust -= 0.1
                parachute_upthrust = round(parachute_upthrust, 2)
                para_text = Text(f'Parachute Upthrust:  {parachute_upthrust}N', (w // 2) - 250, (h // 2) + 25, 24)
                cansat_raw = CanSat(dimensions, scale_padding, scale_max, 100, mass, 250, 35, (0, 0, 255), False, gravity, parachute_upthrust, wind)
                cansat_p1 = CanSat(dimensions, scale_padding, scale_max, 100, mass, 550, 35, (0, 255, 0), True, gravity, parachute_upthrust, wind)
            
            if grav_down.is_Clicked(event):
                gravity -= 0.01
                gravity = round(gravity, 3)
                grav_text = Text(f'Acceleration due to Gravity:  {gravity}m/s^2', (w // 2) - 350, (h // 2) + 125, 24)
                cansat_raw = CanSat(dimensions, scale_padding, scale_max, 100, mass, 250, 35, (0, 0, 255), False, gravity, parachute_upthrust, wind)
                cansat_p1 = CanSat(dimensions, scale_padding, scale_max, 100, mass, 550, 35, (0, 255, 0), True, gravity, parachute_upthrust, wind)
            
            if grav_up.is_Clicked(event):
                gravity += 0.01
                gravity = round(gravity, 3)
                grav_text = Text(f'Acceleration due to Gravity:  {gravity}m/s^2', (w // 2) - 350, (h // 2) + 125, 24)
                cansat_raw = CanSat(dimensions, scale_padding, scale_max, 100, mass, 250, 35, (0, 0, 255), False, gravity, parachute_upthrust, wind)
                cansat_p1 = CanSat(dimensions, scale_padding, scale_max, 100, mass, 550, 35, (0, 255, 0), True, gravity, parachute_upthrust, wind)
            
            if wind_up.is_Clicked(event):
                wind += 1
                if wind < 0:
                    wind_text = Text(f'Horizontal Wind:  {wind} m/s <--', (w // 2) - 250, (h // 2) + 225, 24)
                elif wind == 0:
                    wind_text = Text(f'Horizontal Wind:  {wind} m/s <->', (w // 2) - 250, (h // 2) + 225, 24)
                else:
                    wind_text = Text(f'Horizontal Wind:  {wind} m/s -->', (w // 2) - 250, (h // 2) + 225, 24)
                cansat_raw = CanSat(dimensions, scale_padding, scale_max, 100, mass, 250, 35, (0, 0, 255), False, gravity, parachute_upthrust, wind)
                cansat_p1 = CanSat(dimensions, scale_padding, scale_max, 100, mass, 550, 35, (0, 255, 0), True, gravity, parachute_upthrust, wind)
            
            if wind_down.is_Clicked(event):
                wind -= 1
                if wind < 0:
                    wind_text = Text(f'Horizontal Wind:  {wind} m/s <--', (w // 2) - 250, (h // 2) + 225, 24)
                elif wind == 0:
                    wind_text = Text(f'Horizontal Wind:  {wind} m/s <->', (w // 2) - 250, (h // 2) + 225, 24)
                else:
                    wind_text = Text(f'Horizontal Wind:  {wind} m/s -->', (w // 2) - 250, (h // 2) + 225, 24)
                cansat_raw = CanSat(dimensions, scale_padding, scale_max, 100, mass, 250, 35, (0, 0, 255), False, gravity, parachute_upthrust, wind)
                cansat_p1 = CanSat(dimensions, scale_padding, scale_max, 100, mass, 550, 35, (0, 255, 0), True, gravity, parachute_upthrust, wind)

            if mass_down.is_Clicked(event):
                mass -= 0.1
                mass = round(mass, 1)
                mass_text = Text(f'Mass:  {mass}kg', (w // 2) - 150, (h // 2) + 325, 24)
                cansat_raw = CanSat(dimensions, scale_padding, scale_max, 100, mass, 250, 35, (0, 0, 255), False, gravity, parachute_upthrust, wind)
                cansat_p1 = CanSat(dimensions, scale_padding, scale_max, 100, mass, 550, 35, (0, 255, 0), True, gravity, parachute_upthrust, wind)

            if mass_up.is_Clicked(event):
                mass += 0.1
                mass = round(mass, 1)
                mass_text = Text(f'Mass:  {mass}kg', (w // 2) - 150, (h // 2) + 325, 24)
                cansat_raw = CanSat(dimensions, scale_padding, scale_max, 100, mass, 250, 35, (0, 0, 255), False, gravity, parachute_upthrust, wind)
                cansat_p1 = CanSat(dimensions, scale_padding, scale_max, 100, mass, 550, 35, (0, 255, 0), True, gravity, parachute_upthrust, wind)


        run_button.Draw(screen)
        run_button.Animate()
        scale_up.Draw(screen)
        scale_up.Animate()
        scale_down.Draw(screen)
        scale_down.Animate()
        scale_text.Draw(screen)

        para_up.Draw(screen)
        para_up.Animate()
        para_down.Draw(screen)
        para_down.Animate()
        para_text.Draw(screen)

        grav_up.Draw(screen)
        grav_up.Animate()
        grav_down.Draw(screen)
        grav_down.Animate()
        grav_text.Draw(screen)

        wind_up.Draw(screen)
        wind_up.Animate()
        wind_down.Draw(screen)
        wind_down.Animate()
        wind_text.Draw(screen)

        mass_up.Draw(screen)
        mass_up.Animate()
        mass_down.Draw(screen)
        mass_down.Animate()
        mass_text.Draw(screen)

    elif run_simulation:
        delta_time = (pygame.time.get_ticks() - initial_time) / 1000 # Get the delta_time for 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                
                pygame.quit()
                quit()
        
        # Apply physics for both CanSats independently
        raw_time, raw_vs_values = cansat_raw.ApplyPhysics(delta_time)
        parachute_time, para_vs_values = cansat_p1.ApplyPhysics(delta_time)

        if raw_time is not None and hit_raw_time is None:
            hit_raw_time = raw_time
            condition_1 = True
            
        
        if parachute_time is not None and hit_para_time is None:
            hit_para_time = parachute_time
            condition_2 = True
        
        screen.fill((255, 255, 255))  # screen
        scale.Draw(screen)  # Draw the scale
        cansat_raw.Draw(screen)  # Draw the first CanSat
        cansat_p1.Draw(screen)  # Draw the second CanSat

        if condition_1 and condition_2:
            run_simulation = False
            setup_simulation = False
            flight_stats = True

        
    
    elif flight_stats:
        pygame.time.delay(2000)
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                
                pygame.quit()
                quit()
            
            if raw_get_graphs.is_Clicked(event):
                flight_stats = False
                graph_state= True
                graph = 'raw'
            
            if para_get_graphs.is_Clicked(event):
                flight_stats = False
                graph_state = True
                graph = 'para'
            
        cansat1statsbox = pygame.Rect(50, 50, 400, 600)
        cansat2statsbox = pygame.Rect(500, 50, 400, 600)
        pygame.draw.rect(screen, (200, 200, 200), cansat1statsbox)
        pygame.draw.rect(screen, (200, 200, 200), cansat2statsbox)

        
        raw_distance_travelled = scale_max * 100
        para_distance_travelled = scale_max * 100


        raw_average_velocity = (scale_max * 100) / hit_raw_time
        para_average_velocity = (scale_max * 100) / hit_para_time

        raw_average_acceleration = raw_average_velocity / hit_raw_time
        para_average_acceleration = para_average_velocity / hit_para_time

        raw_average_velocity, para_average_velocity = round(raw_average_velocity, 4), round(para_average_velocity, 4)
        raw_average_acceleration, para_average_acceleration = round(raw_average_acceleration, 4), round(para_average_acceleration, 4)

        raw_diagram = ForceDiagram(mass, gravity, 0, 250, 550, 200, wind)
        para_diagram = ForceDiagram(mass, gravity, parachute_upthrust, 700, 550, 200, wind)

        raw_title = Text(f'Without Parachute', 75, 100, 56)
        para_title = Text(f'With Parachute', 550, 100, 56)

        raw_flight_time = Text(f'Flight Time: {hit_raw_time} s', 100, 250, 32)
        para_flight_time = Text(f'Flight Time: {hit_para_time} s', 550, 250, 32)

        raw_flight_velocity = Text(f'Avg Velocity: {raw_average_velocity} m/s', 100, 300, 32)
        para_flight_velocity = Text(f'Avg Velocity: {para_average_velocity} m/s', 550, 300, 32)

        raw_flight_acceleration = Text(f'Avg Acceleration: {raw_average_acceleration} m/s^2', 100, 350, 32)
        para_flight_acceleration = Text(f'Avg Acceleration: {para_average_acceleration} m/s^2', 550, 350, 32)

        raw_flight_distance = Text(f'Displacement: {raw_distance_travelled} m', 100, 400, 32)
        para_flight_distance = Text(f'Displacement: {para_distance_travelled} m', 550, 400, 32)

        

        



        raw_title.Draw(screen)
        para_title.Draw(screen)
        raw_flight_time.Draw(screen)
        para_flight_time.Draw(screen)
        raw_flight_velocity.Draw(screen)
        para_flight_velocity.Draw(screen)
        raw_flight_acceleration.Draw(screen)
        para_flight_acceleration.Draw(screen)
        raw_flight_distance.Draw(screen)
        para_flight_distance.Draw(screen)
        raw_diagram.Draw(screen)
        para_diagram.Draw(screen)
        raw_get_graphs.Draw(screen)
        raw_get_graphs.Animate()
        para_get_graphs.Draw(screen)
        para_get_graphs.Animate()
        


    elif graph_state:
        screen.fill((255, 255, 255))
        if graph == 'raw':
            vgraphtodraw = DrawGraph(raw_vs_values, dimensions, (150, 250), (165, 165), 'v (m/s)', (0, 255, 0), 10)
            agraphtodraw = DrawGraph(asfromvs(raw_vs_values), dimensions, (500, 250), (165, 165), 'a (m/s^2)', (0, 0, 255), 10)
            sgraphtodraw = DrawGraph(ssfromvs(raw_vs_values), dimensions, (800, 250), (165, 165), 's (m)', (255, 0, 0), 10)
        elif graph == 'para':
            vgraphtodraw = DrawGraph(para_vs_values, dimensions, (150, 250), (165, 165), 'v (m/s)', (0, 255, 0), 10)
            agraphtodraw = DrawGraph(asfromvs(para_vs_values), dimensions, (500, 250), (165, 165), 'a (m/s^2)', (0, 0, 255),  10)
            sgraphtodraw = DrawGraph(ssfromvs(para_vs_values), dimensions, (800, 250), (165, 165), 's (m)', (255, 0, 0), 10)
        
        vgraphtodraw.Sketch(screen)
        agraphtodraw.Sketch(screen)
        sgraphtodraw.Sketch(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
