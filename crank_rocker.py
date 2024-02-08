import pygame
import math


pygame.init()

WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Four Bar Linkage Mechanism Simulation")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
SCALING_FACTOR = 20
OFFSET_FACTOR = (100, 100)
ALLOWANCE_FACTOR = 0.005
LINK1_LENGTH = 10 * SCALING_FACTOR # Fixed
LINK2_LENGTH = 4 * SCALING_FACTOR # crank
LINK3_LENGTH = 10 * SCALING_FACTOR # couple
LINK4_LENGTH = 12 * SCALING_FACTOR # rocker
LINK2_ANGULAR_VELOCITY = 0.05  

rocker_x_history = []
rocker_y_history = []
crank_x_history = []
crank_y_history = []

def distance(x1, x2, y1, y2):
    return math.sqrt((x1-x2)**2 + (y2-y1)**2)

def draw_linkage(screen, theta):
    link1_x = WIDTH // 2 + OFFSET_FACTOR[0]
    link1_y = HEIGHT // 2 + OFFSET_FACTOR[1]
    h = math.sqrt(LINK2_LENGTH**2 + LINK1_LENGTH**2 - 2*LINK1_LENGTH*LINK2_LENGTH*math.sin(theta))
    try:
        alpha = math.atan((math.cos(theta)*LINK2_LENGTH)/(LINK1_LENGTH-LINK2_LENGTH*math.sin(theta))) - math.asin((LINK4_LENGTH**2 + h**2 - LINK3_LENGTH**2)/(2*LINK4_LENGTH*h))
    except Exception as e:
        raise ValueError("Error in linkage. Most probably the links are unable to move")

    link2_x = link1_x + LINK2_LENGTH * math.cos(theta)
    link2_y = link1_y - LINK2_LENGTH * math.sin(theta)
    link4_x = link1_x 
    link4_y = link1_y - LINK1_LENGTH
    link3_x = link4_x + LINK4_LENGTH * math.cos(alpha)
    link3_y = link4_y - LINK4_LENGTH * math.sin(alpha)

    rocker_x_history.append(link3_x)
    rocker_y_history.append(link3_y)
    crank_x_history.append(link2_x)
    crank_y_history.append(link2_y)

    check = distance(link2_x, link3_x, link2_y, link3_y)

    # print(f'Distance is : {check}')
    try: 
        abs(check-LINK3_LENGTH) <= ALLOWANCE_FACTOR*LINK3_LENGTH
    except:
        print(f'Error in calculations. Not a crank rocker')
    pygame.draw.line(screen, BLACK, (link1_x, link1_y), (link2_x, link2_y), 5)
    pygame.draw.line(screen, BLACK, (link1_x, link1_y), (link4_x, link4_y), 5)
    pygame.draw.line(screen, BLACK, (link2_x, link2_y), (link3_x, link3_y), 5)
    pygame.draw.line(screen, BLACK, (link4_x, link4_y), (link3_x, link3_y), 5)
    pygame.draw.circle(screen, RED, (link1_x, link1_y), 10)
    pygame.draw.circle(screen, RED, (link2_x, link2_y), 10)
    pygame.draw.circle(screen, RED, (link3_x, link3_y), 10)
    pygame.draw.circle(screen, RED, (link4_x, link4_y), 10)

    return True

clock = pygame.time.Clock()
theta1 = 0

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    theta1 += LINK2_ANGULAR_VELOCITY  

    error_check = draw_linkage(screen, theta1)
    if not error_check:
        running = False
    if len(rocker_x_history) > 1 and len(rocker_y_history) > 1:
        pygame.draw.lines(screen, BLUE, False, list(zip(rocker_x_history, rocker_y_history)), 2)
    if len(rocker_x_history) > 1 and len(rocker_y_history) > 1:
        pygame.draw.lines(screen, GREEN, False, list(zip(crank_x_history, crank_y_history)), 2)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
