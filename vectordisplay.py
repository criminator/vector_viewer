import pygame
import math
from enum import Enum
import random

class Text:
    pass

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, int):
            return Vector(self.x * other, self.y * other)
        elif isinstance(other, float):
            return Vector(self.x * other, self.y * other)
    
    def __str__(self):
        return f'Vector({self.x}, {self.y})'
    
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        else:
            raise TypeError("Cannot add scalar to a vector.")

    def addForce(self, vector):
        self.x += vector.x
        self.y += vector.y

    def newForce(self, force):
        self.x = force.x
        self.y = force.y
    
    def normalize(self):
        mag = math.sqrt(self.x**2 + self.y**2)
        newVect = Vector(self.x / mag, self.y / mag)
        return newVect
    
    def getmag(self):
        return math.sqrt(self.x**2 + self.y**2)

    def proj(self, other):
        if isinstance(other, Vector):
            print(f"DOT: {self * other}")
            return self * ((self * other) / other.getmag()**2)
        else:
            raise TypeError("Other parameter must be a vector.")

    def getnegate(self):
        return Vector(-self.x, -self.y)


class VectorField: # Class for the fields in which the user types in vectors
    def __init__(self, rect: pygame.Rect, text: str):
        self.rect = rect
        self.text = text


pygame.init()

Color = {
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'red': (255, 0, 0)
}

def randcolor():
    x = random.randint(0, 255)
    y = random.randint(0, 255)
    z = random.randint(0, 255)
    return (x, y, z)

# ----------------- Screen Setup ----------------- #
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 800
WIDTH, HEIGHT = 600, 600
MIDDLE_POINT = (WIDTH / 2, HEIGHT / 2)
STEP = HEIGHT / 20
# ------------------------------------------------ #

def make_grid(surf):
    for i in range(0, HEIGHT + 1, int(HEIGHT / 20)): # Horizontal lines
        pygame.draw.line(surf, (255,255,255), (0,i), (WIDTH, i))
    for i in range(0, WIDTH + 1, int(WIDTH / 20)): # Veritcal lines
        pygame.draw.line(surf, (255,255,255), (i,0), (i, HEIGHT))
    pygame.draw.line(surf, (255,255,255), (WIDTH / 2, HEIGHT), (WIDTH / 2, 0), 3)
    pygame.draw.line(surf, (255,255,255), (0, HEIGHT / 2), (WIDTH, HEIGHT / 2), 3)
    pygame.draw.circle(surf, (255,255,255), MIDDLE_POINT, 5)

def display_vector(surf, color: tuple[int], vect: Vector, point: tuple[int]) -> None:
    start = (point[0] + WIDTH / 2,point[1] + HEIGHT / 2)
    end = ((vect.x * STEP) + WIDTH / 2, (HEIGHT / 2) - (vect.y * STEP))
    pygame.draw.line(surf, color, start, end, 3)

    # Draw Arrow
    
    # Get angle
    angle = math.atan2(end[1] - start[1], end[0] - start[0])

    arrow_length = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)

    # Calculate the points for the arrowhead
    arrow_point1 = (
        end[0] - (STEP / 2) * math.cos(angle - math.pi / 6),
        end[1] - (STEP / 2) * math.sin(angle - math.pi / 6)
    )
    arrow_point2 = (
        end[0] - (STEP / 2) * math.cos(angle + math.pi / 6),
        end[1] - (STEP / 2) * math.sin(angle + math.pi / 6)
    )
    
    # Draw the arrowhead
    pygame.draw.polygon(surf, color, [end, arrow_point1, arrow_point2])

def displaygui(surf, inputs: list[VectorField], colors):
    med_text = pygame.font.SysFont("Arial", 22)
    small_text = pygame.font.SysFont("Arial", 18)
    text_surf = med_text.render("Vectors:", 1, (255,255,255))
    surf.blit(text_surf, (10, HEIGHT + 10))
    if len(inputs) == 0:
        rect = pygame.Rect(15 + text_surf.get_width() + 40, HEIGHT + 50 + (small_text.get_height() + 10) - 2, text_surf.get_width() + 80, small_text.get_height() + 8)
        text = '<5, 5>'
        inputs.append(VectorField(rect, text))
    vect_array = []
    for i, field in enumerate(inputs):
        vect = Vector(int(field.text[1]), int(field.text[4]))
        vect_array.append(vect)
        text_surface = small_text.render(f'Vector({vect.x}, {vect.y})', True, (255,255,255))
        surf.blit(text_surface, (10, HEIGHT + 50 + i * (small_text.get_height() + 10)))

    for i, item in enumerate(vect_array):
        display_vector(surf, colors[i], item, (0,0))
    '''
    for i, vect in enumerate(arr):
        text_surface = small_text.render(f'{i+1}. {str(vect)}', True, (255,255,255))
        inputs[f"box_{i}"] = pygame.Rect(15 + text_surf.get_width() + 40, HEIGHT + 50 + i * (small_text.get_height() + 10) - 2, text_surf.get_width() + 80, small_text.get_height() + 8)
        box_text = small_text.render(f'< , >', True, (255,255,255))
        surf.blit(text_surface, (10, HEIGHT + 50 + i * (small_text.get_height() + 10)))
        surf.blit(box_text, (inputs[f"box_{i}"].x + 5, inputs[f"box_{i}"].y + 3))
    for text_field in inputs.values():
        pygame.draw.rect(surf, (255,255,255), text_field, 2)
    '''



def main():
    
    screen = pygame.display.set_mode((WIDTH, SCREEN_HEIGHT))
    running = True

    vector = Vector(-3, 3)
    vect2 = Vector(4, 4)
    vect3 = Vector(9, 0)
    sumvect = vector + vect2

    # projvect = vect2.proj(vect3)

    vector_arr = [vector, vect2, sumvect]

    vectors = []

    colors = [(0,255,0), (255,0,0), (0,100,255), (150, 100, 0)]
    vect_colors = []

    count = 0
    for i in range(len(vector_arr)):
        if count > len(colors) - 1:
            count = 0
        vect_colors.append(colors[i])
        count += 1
    
    inputs = []

    active = False

    while running:
        screen.fill((0,0,0))

        for e in pygame.event.get():
            # print(e)
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                for box in inputs.values():
                    if box.collidepoint(e.pos):
                        print("BOX!")
            elif e.type == pygame.KEYDOWN:
                if active:
                    if e.key == pygame.K_RETURN:
                        print(f"Text changed")

        
        # Make grid
        make_grid(screen)

        '''
        for field in inputs.values():
            vectors.append(field)
        '''
        '''
        for i, item in enumerate(vector_arr):
            display_vector(screen, vect_colors[i], item, (0,0))
        '''
        

        displaygui(screen, inputs, vect_colors)

        pygame.display.flip()
            
    
    pygame.quit()

if __name__ == "__main__":
    main()
    