import pygame
pygame.init()
font = pygame.font.Font(None, 25)

active_colour = (150, 150, 150)
inactive_colour = (50, 50, 50)
disabled_colour = (200, 200, 200)

class Button:
    def __init__(self, x_position, y_position, width, height, text=''):
        self.x, self.y = x_position, y_position
        self.width, self.height = width, height
        self.default_colour = inactive_colour
        self.hover_colour = active_colour
        self.current_colour = self.default_colour
        self.text_surface = font.render(text, True, (255, 255, 255))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def is_Clicked(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:

                return True

        return False

    def Draw(self, screen):
        pygame.draw.rect(screen, self.current_colour, self.rect)
        screen.blit(self.text_surface, self.text_surface.get_rect(center = self.rect.center))

    def Animate(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.current_colour = tuple(min(c + 10, hc) for c, hc in zip(self.current_colour, self.hover_colour))
        else:
            self.current_colour = tuple(max(c - 10, dc) for c, dc in zip(self.current_colour, self.default_colour))

    
    def Disable(self):
        self.disabled = True

class Scale:
    def __init__(self, screen_dimensions, scale_max, padding):        
        self.screen_width, self.screen_height = screen_dimensions
        self.scale_limit = scale_max
        self.padding = padding
        self.font = font

    def calculate_coords(self):
        """Calculate coordinates the scale lines."""
        x_coords, y_coords = [], []
        x_coords_labels, y_coords_labels = [], []

        # Calculate x-coordinates
        for i in range(0, self.scale_limit + 1, 1):  # Include scale_limit for the max point
            x_coords.append(self.padding + (self.screen_width - 2 * self.padding) // self.scale_limit * i)
            x_coords_labels.append((i * 100))
        
        # Calculate y-coordinates (from bottom to top)
        for j in range(0, self.scale_limit + 1, 1):  # Include scale_limit for the max point
            y_coords.append(self.screen_height - self.padding - (self.screen_height - 2 * self.padding) // self.scale_limit * j)
            y_coords_labels.append((j * 100))


        return x_coords, y_coords, x_coords_labels, y_coords_labels

    def Draw(self, screen):
        """Draw the scale on the given Pygame screen."""
        x_coords, y_coords, x_labels, y_labels = self.calculate_coords()
        x_labels = [i for i in range(self.scale_limit + 1)]
        y_labels = [i for i in range(self.scale_limit + 1)]


        # Draw vertical lines and x-axis labels
        for x, label in zip(x_coords, x_labels):
            label *= 100
            pygame.draw.line(screen, (200, 200, 200), (x, self.screen_height - self.padding), (x, self.padding), 1)
            # Position labels slightly below the x-axis
            screen.blit(self.font.render(str(label), True, (255, 0, 0)), (x - 10, self.screen_height - self.padding + 5))

        # Draw horizontal lines and y-axis labels
        for y, label in zip(y_coords, y_labels):
            label *= 100
            pygame.draw.line(screen, (200, 200, 200), (self.padding, y), (self.screen_width - self.padding, y), 1)
            # Position labels slightly to the left of the y-axis
            screen.blit(self.font.render(str(label), True, (255, 0, 0)), (self.padding - 30, y - 10))

        # Draw axes
        pygame.draw.line(screen, (255, 0, 0), (self.padding, self.screen_height - self.padding), (self.screen_width - self.padding, self.screen_height - self.padding), 2)  # X-axis
        pygame.draw.line(screen, (255, 0, 0), (self.padding, self.screen_height - self.padding), (self.padding, self.padding), 2)  # Y-axis

class CanSat:
    def __init__(self, dimensions, scale_padding, scale_max, size, mass, x_pos, y_pos, colour, has_parachute, gravity, parachute_upthrust, wind):
        self.width, self.height = size, size
        self.screen_width, self.screen_height = dimensions
        self.padding = scale_padding
        self.scale_max = scale_max
        self.ratio = (self.screen_height - self.padding) / (self.scale_max*100)
        self.x, self.y = x_pos, y_pos
        self.mass = mass
        self.colour = colour
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.parachute_upthrust = parachute_upthrust  # The parachute's upthrust
        self.has_parachute = has_parachute
        self.velocity_y = 0  # Starting with no vertical velocity
        self.gravity = gravity
        self.wind = wind
        self.windstopped = False
        self.finaltime = None
        self.u = 0
        # Load images for CanSat with and without parachute
        self.image_no_parachute = pygame.image.load('cansat.png')
        self.image_parachute = pygame.image.load('cansat_parachute.png')
        self.v_s_values = []
        # Scale images to the size of the CanSat object
        self.image_no_parachute = pygame.transform.scale(self.image_no_parachute, (self.width, self.height))
        self.image_parachute = pygame.transform.scale(self.image_parachute, (self.width, self.height))

    def ApplyPhysics(self, delta_time):
        if self.has_parachute == False:
            self.acceleration = self.gravity
        else:
            self.acceleration = self.gravity - (self.parachute_upthrust / self.mass)

        self.velocity_y = self.u + (self.acceleration * delta_time)
        self.displacement = (self.u * delta_time) + (0.5 * self.acceleration * delta_time**2)
        self.scaled_displacement = self.displacement * self.ratio
        self.u = self.velocity_y
        # Calculate effective acceleration
        self.v_s_values.append([self.velocity_y, delta_time])
        
        # Calculate new vertical position using y = y_0 + v * t
        new_y = self.rect.y + self.scaled_displacement

        # Check for collision with the ground (baseline)
        if new_y + self.rect.height >= self.screen_height - self.padding:
            # Snap to the baseline and stop motion
            self.rect.bottom = self.screen_height - self.padding
            self.velocity_y = 0 # Stop vertical velocity on impact
            if self.finaltime is None:
                return delta_time, self.v_s_values

        else:
            # Apply the new position if not on the ground
            self.rect.y = new_y

            # Apply wind force to horizontal movement (x-axis) ONLY when CanSat is in the air
            wind_force = self.wind * (self.screen_width - 2 * self.padding) / self.scale_max / 100

            # Update horizontal position (x-axis) using wind force
            self.rect.x += wind_force * delta_time

        # Prevent CanSat from going off the screen horizontally (screen width boundaries)
        if self.rect.left < self.padding:
            self.rect.left = self.padding
        elif self.rect.right > self.screen_width - self.padding:
            self.rect.right = self.screen_width - self.padding

        return None, self.v_s_values

    def Draw(self, screen):
        # Choose the correct image based on whether the parachute is deployed
        if self.has_parachute:
            image = self.image_parachute
        else:
            image = self.image_no_parachute

        # Draw the image at the current position
        screen.blit(image, self.rect)


class Text:
    def __init__(self, text, x, y, size):
        self.text = text
        self.x, self.y = x,y 
        self.font = pygame.font.Font(None, size)
        self.textsurface = self.font.render(self.text, True, (0, 0, 0))

    def Draw(self, screen):
        screen.blit(self.textsurface, (self.x, self.y))



class ForceDiagram:
    def __init__(self, mass, gravity, upthrust, x, y, max_size, wind):
        self.weight = mass * gravity  # Weight (in N)
        self.upthrust = upthrust  # Upthrust (in N)
        self.wind = wind  # Wind (in N)
        self.x, self.y = x, y  # Position of the circle (center)
        self.max_size = max_size  # Max size for scaling the diagram
        
        # Scale factors for visual representation
        self.scale_factor = 20  # Adjust this value to change the scale of the arrows
        
        # Lengths of arrows (scaled by force magnitude)
        self.weight_length = self.weight * self.scale_factor
        self.upthrust_length = self.upthrust * self.scale_factor
        self.wind_length = abs(self.wind) * self.scale_factor

    def Draw(self, screen):
        # Draw the body (circle)
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 15)

        # Draw the weight arrow (downward force)
        weight_end = (self.x, self.y + self.weight_length)  # Endpoint of the weight arrow
        pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), weight_end, 5)  # Red arrow, 5 px thickness

        # Draw the upthrust arrow (upward force)
        upthrust_end = (self.x, self.y - self.upthrust_length)  # Endpoint of the upthrust arrow
        pygame.draw.line(screen, (0, 255, 0), (self.x, self.y), upthrust_end, 5)  # Green arrow, 5 px thickness

        # Draw the wind arrow (horizontal force)
        if self.wind > 0:
            wind_end = (self.x + self.wind_length, self.y)  # Wind goes right
            pygame.draw.line(screen, (0, 0, 255), (self.x, self.y), wind_end, 5)  # Blue arrow
        elif self.wind < 0:
            wind_end = (self.x - self.wind_length, self.y)  # Wind goes left
            pygame.draw.line(screen, (0, 0, 255), (self.x, self.y), wind_end, 5)  # Blue arrow


class DrawGraph:
    def __init__(self, v_s_values, screen_dimensions, graph_position, graph_size, ylabel, colour, padding=10):
        self.velocity_time_values = v_s_values  # List of (velocity, time) tuples
        self.screen_width, self.screen_height = screen_dimensions
        self.graph_x, self.graph_y = graph_position  # Top-left position of the graph
        self.graph_width, self.graph_height = graph_size
        self.padding = padding  # Space around the graph within its bounding box
        self.ylabeltxt = ylabel
        self.colour = colour

    def transform_to_screen(self, velocity, time, max_velocity, max_time):
        """Transform graph values (velocity, time) to screen coordinates."""
        # Scale velocity and time to fit the graph dimensions
        x = self.graph_x + self.padding + (time / max_time) * (self.graph_width - 2 * self.padding)
        y = self.graph_y + self.graph_height - self.padding - (velocity / max_velocity) * (self.graph_height - 2 * self.padding)
        return x, y

    def draw_axes(self, screen, max_velocity, max_time):
        """Draw the graph axes and labels."""
        # Draw X-axis (Time)
        pygame.draw.line(screen, (0, 0, 0), 
                         (self.graph_x + self.padding, self.graph_y + self.graph_height - self.padding),
                         (self.graph_x + self.graph_width - self.padding, self.graph_y + self.graph_height - self.padding), 2)
        # Draw Y-axis (Velocity)
        pygame.draw.line(screen, (0, 0, 0), 
                         (self.graph_x + self.padding, self.graph_y + self.padding),
                         (self.graph_x + self.padding, self.graph_y + self.graph_height - self.padding), 2)

        # Add labels for axes
        font = pygame.font.Font(None, 20)
        time_label = font.render("Time (s)", True, (0, 0, 0))
        velocity_label = font.render(self.ylabeltxt, True, (0, 0, 0))

        screen.blit(time_label, (self.graph_x + self.graph_width // 2, self.graph_y + self.graph_height + 50))
        screen.blit(velocity_label, (self.graph_x - 70, self.graph_y + self.graph_height // 2))

    def Sketch(self, screen):
        """Draw the graph based on velocity-time values."""
        if not self.velocity_time_values:
            return  # Nothing to plot if no data

        # Find maximum velocity and time for scaling
        max_velocity = max(v for v, _ in self.velocity_time_values)
        max_time = sum(t for _, t in self.velocity_time_values)  # Total time elapsed

        # Draw axes
        self.draw_axes(screen, max_velocity, max_time)

        # Draw graph points and lines
        prev_point = None
        total_time = 0
        for velocity, delta_time in self.velocity_time_values:
            total_time += delta_time
            current_point = self.transform_to_screen(velocity, total_time, max_velocity, max_time)

            # Draw a line connecting the previous point to the current point
            if prev_point:
                pygame.draw.line(screen, self.colour, prev_point, current_point, 2)

            # Update the previous point
            prev_point = current_point



