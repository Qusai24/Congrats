import pygame
import random
import math
import pygame.mixer


# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 1080, 720

# Colors
black = (0, 0, 0)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

# Create the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fireworks Celebration")

# Load the background image
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (width, height))



class Firework:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.exploded = False
        self.particles = []
        self.color = random.choice(colors)

    def explode(self):
        self.exploded = True
        for _ in range(100):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 6)
            particle = Particle(self.x, self.y, self.color, angle, speed)
            self.particles.append(particle)

    def update(self):
        if not self.exploded:
            self.y -= 1
            if self.y <= height // 2:
                self.explode()
        else:
            for particle in self.particles:
                particle.update()

class Particle:
    
    def __init__(self, x, y, color, angle, speed):
        self.x = x
        self.y = y
        self.color = color
        self.angle = angle
        self.speed = speed
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        self.gravity = 0.2
        self.time = 0

    def update(self):
        self.time += 1
        self.dy += self.gravity * self.time * 0.1
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 2)

fireworks = []

def congratulations(name):
    global fireworks  # Declare fireworks as a global variable
    font = pygame.font.Font(None, 22)
    message = f"🎉🎓 Congratulations, {name}!\n"\
              "You made it.\n"\
              "can't be more proud of you!\n"\
              "I hope you catch your dreams\n"\
              "(and I'm sure they will come true)"
              

    text_rect = pygame.Rect(0, 0, width, 1)
    text_color = (255, 255, 255)  # Default text color

    text = font.render(message, True, text_color)
    text_rect.center = (width // 1, height // 1)
    
    running = True
    color_change_timer = 0
    color_index = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Blit the background image
        screen.blit(background_image, (0, 0))

        # Change text color every 0.5 seconds
        if pygame.time.get_ticks() - color_change_timer > 500:
            text_color = colors[color_index]
            text = font.render(message, True, text_color)
            color_index = (color_index + 1) % len(colors)
            color_change_timer = pygame.time.get_ticks()

        # Manually adjust text position to fit within the screen
        text_rect.center = (width // 2, height // 2)
        
        if random.randint(1, 10) == 1:
            firework = Firework(random.randint(0, width), height)
            fireworks.append(firework)

        for firework in fireworks:
            firework.update()
            for particle in firework.particles:
                particle.draw()

        screen.blit(text, text_rect)
        fireworks = [firework for firework in fireworks if not firework.exploded or len(firework.particles) > 0]

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

# Replace 'Your Name' with the actual name of the person graduating
graduate_name = "Majd"
congratulations(graduate_name)
