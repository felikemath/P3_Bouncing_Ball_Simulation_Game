import math
import sys, pygame
from pygame.locals import *


class ballclass():
    def __init__(self, id, imgfile, mass=1, init_speedxy=[6.0, 4.5], init_Loc_Offset=[400, 0]):
        ball_id = id
        self.ballimg = pygame.image.load(imgfile)  # .convert()
        self.ballrect = self.ballimg.get_rect()
        self.ballrect.left += int(init_Loc_Offset[0])  # initial position of ball
        self.ballrect.top += int(init_Loc_Offset[1])
        self.ballsize = self.ballimg.get_size()
        self.ballRadiusSqr = (self.ballsize[0] / 2) ** 2
        self.mass = mass
        self.speed = init_speedxy
        self.moveto = [0, 0]
        self.movetoResidual = [0, 0]

    def Is_Ball_in_Box_Range_Simple(self, boxrect):  # incomplete
        if self.ballrect.bottom < boxrect.top or self.ballrect.right < boxrect.left or self.ballrect.left > boxrect.right:
            return False
        return True

    def Check_Ball_Hit_BoxTopLeftCorner(self, boxrect):
        hitcorver = False
        xoff = boxrect.left - self.ballrect.centerx
        yoff = boxrect.top - self.ballrect.centery
        dist2centersqr = (xoff * xoff + yoff * yoff)
        if dist2centersqr <= self.ballRadiusSqr:
            hitcorver = True
        return hitcorver

    def Check_Ball_Hit_BoxTopRightCorner(self, boxrect):
        hitcorver = False
        xoff = boxrect.right - self.ballrect.centerx
        yoff = boxrect.top - self.ballrect.centery

        dist2centersqr = (xoff * xoff + yoff * yoff)
        if dist2centersqr <= self.ballRadiusSqr:
            hitcorver = True
        return hitcorver

    def Calc_BallSpeed_on_BoxTopLeftCorner(self, boxrect, boxspeed):
        xoff = self.ballrect.centerx - boxrect.left
        yoff = self.ballrect.centery - boxrect.top
        dist2center = math.sqrt(xoff * xoff + yoff * yoff)

        c2cdir = [xoff / dist2center, yoff / dist2center]
        tangentDir = [-yoff / dist2center, xoff / dist2center]

        # new relative speed in the horizontal direction, box speed equivalent to 1/10 of ball speed
        relativeballspeedx = self.speed[0] - boxspeed[0] / 10.0
        relativeballspeedy = self.speed[1]  # new relative speed keep unchanged in the horizontal direction

        #  find the new ballspeed projection component along "c2c", take negation, i.e. bounce back
        newballspeed_on_c2cdir = -(relativeballspeedx * c2cdir[0] + relativeballspeedy * c2cdir[1])
        #  find the relativeballspeed projection component along "tangent", unchanged
        newballspeed_on_tangentdir = relativeballspeedx * tangentDir[0] + relativeballspeedy * tangentDir[1]

        newballspeed_on_x = newballspeed_on_c2cdir * c2cdir[0] + newballspeed_on_tangentdir * tangentDir[0]
        newballspeed_on_y = newballspeed_on_c2cdir * c2cdir[1] + newballspeed_on_tangentdir * tangentDir[1]

        self.speed = [newballspeed_on_x, newballspeed_on_y]
        return

    def Calc_BallSpeed_on_BoxTopRightCorner(self, boxrect, boxspeed):
        xoff = self.ballrect.centerx - boxrect.right
        yoff = self.ballrect.centery - boxrect.top
        dist2center = math.sqrt(xoff * xoff + yoff * yoff)

        c2cdir = [xoff / dist2center, yoff / dist2center]
        tangentDir = [-yoff / dist2center, xoff / dist2center]

        # new relative speed in the horizontal direction, box speed equivalent to 1/10 of ball speed
        relativeballspeedx = self.speed[0] - boxspeed[0] / 10.0
        relativeballspeedy = self.speed[1]  # new relative speed keep unchanged in the vertical direction

        #  find the new ballspeed projection along "c2c", take negation, i.e. bound back
        newballspeed_on_c2cdir = -(relativeballspeedx * c2cdir[0] + relativeballspeedy * c2cdir[1])
        #  find the relativeballspeed projection along "tangent", unchanged
        newballspeed_on_tangentdir = relativeballspeedx * tangentDir[0] + relativeballspeedy * tangentDir[1]

        newballspeed_on_x = newballspeed_on_c2cdir * c2cdir[0] + newballspeed_on_tangentdir * tangentDir[0]
        newballspeed_on_y = newballspeed_on_c2cdir * c2cdir[1] + newballspeed_on_tangentdir * tangentDir[1]

        self.speed = [newballspeed_on_x, newballspeed_on_y]
        return


#  main program
def main():

    color_group = ['white', 'purple', 'green', 'red', 'blue', 'orange', 'gray', 'yellow', 'violet']

    pygame.init()
    size = width, height = 1024, 768  # 1280, 960  # 800, 640
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Bouncing Balls Game")

    # color_black = Color("black")
    color_black = (5, 32, 41)

    backgroundpic = pygame.image.load("resource/background1280x960.jpg")
    backgroundpicrect = backgroundpic.get_rect()

    box = pygame.image.load("resource/bat.jpg")
    boxsize = box.get_size()
    boxrect = box.get_rect()
    boxrect.left = width / 2 - boxsize[0] / 2
    boxrect.top = height - boxsize[1]
    boxmovespeed = [3, 0]

    # configuration: balls
    nBalls = 4
    imgfiles = ["resource/ball0.gif", "resource/ball1.gif", "resource/ball2.gif", "resource/ball3.gif", "resource/ball4.gif"]
    ballmass = [1.0, 4.0, 2.0, 1.0, 1.0]
    initSpeeds = [[6.0, 4.5], [-2.0, 3.0], [2.0, 3.5], [-4.0, -1.5], [-4.0, -1.5], [-2.0, -3]]
    initLocOffset = [[0, 0], [width/2, 0], [width*3/4, 0], [width*3/5, height/2], [width*2/5, height/5]]
    balls = []
    for i in range(nBalls):
        ball = ballclass(i, imgfiles[i], mass=ballmass[i], init_speedxy=initSpeeds[i], init_Loc_Offset=initLocOffset[i] )
        balls.append(ball)

    score = 0
    font = pygame.font.SysFont('Calibri', 20, False, False)
    clock = pygame.time.Clock()

    # global variable to track ball's collision status
    flagNeedResponse_Ball2Box = [True] * nBalls  #
    # touched_Ball2Box = [False] * (nBalls*nBalls)
    flagNeedResponse_Ball2Ball = [True] * (nBalls*nBalls)
    thresholdDist_Ball2Ball = [0] * (nBalls*nBalls)
    for j in range(nBalls - 1):
        for k in range(j + 1, nBalls):
            pair_index = j * nBalls + k
            thresholdDist_Ball2Ball[pair_index] = (balls[j].ballsize[0] + balls[k].ballsize[0]) / 2.0

    while True:
        clock.tick(120)  # 80
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)

        key_pressed = pygame.key.get_pressed()
        # If left arrow key is pressed, move the box toward left
        if key_pressed[K_LEFT]:
            # speed up when SHIFT key is pressed simultaneously
            if key_pressed[KMOD_SHIFT]:
                boxmovespeed[0] = 12
            else:
                boxmovespeed[0] = 6
            boxrect.left -= boxmovespeed[0]
            # clip the left edge of the box to the left boundary of the game
            if boxrect.left < 0:
                boxrect.left = 0
        # If right arrow key is pressed, move the box toward right
        if key_pressed[K_RIGHT]:
            # speed up when SHIFT key is pressed simultaneously
            if key_pressed[KMOD_SHIFT]:
                boxmovespeed[0] = 12
            else:
                boxmovespeed[0] = 6
            boxrect.left += boxmovespeed[0]
            # clip the the box to be within the right boundary of the game
            if boxrect.left > width - boxsize[0]:
                boxrect.left = width - boxsize[0]

        for i in range (nBalls):
            # update balls[i].movetoResidual and balls[1].movetoResidual
            balls[i].movetoResidual[0] += (balls[i].speed[0] - int(balls[i].speed[0]))
            balls[i].movetoResidual[1] += (balls[i].speed[1] - int(balls[i].speed[1]))
            balls[i].moveto[0] = int(balls[i].speed[0]) + int(balls[i].movetoResidual[0])
            balls[i].moveto[1] = int(balls[i].speed[1]) + int(balls[i].movetoResidual[1])
            # update balls[i].ballrect
            balls[i].ballrect = balls[i].ballrect.move(balls[i].moveto)
            # update balls[i].movetoResidual
            balls[i].movetoResidual[0] -= int(balls[i].movetoResidual[0])
            balls[i].movetoResidual[1] -= int(balls[i].movetoResidual[1])

            if balls[i].ballrect.left <= 0:
                if balls[i].speed[0] < 0.0:
                    balls[i].speed[0] = -balls[i].speed[0]
                    balls[i].movetoResidual[0] = 0.0
                    # print("INFO: Ball i hit the left wall", " left=", balls[i].ballrect.left, balls[i].speed, balls[i].movetoResidual, balls[i].moveto)

            if balls[i].ballrect.right >= width:
                if balls[i].speed[0] > 0.0:
                    balls[i].speed[0] = -balls[i].speed[0]
                    balls[i].movetoResidual[0] = 0.0
                    # print("INFO: Ball i hit the right wall", " right=", balls[i].ballrect.right, balls[i].speed, balls[i].movetoResidual, balls[i].moveto)

            if balls[i].ballrect.top <= 0:
                if balls[i].speed[1] < 0.0:
                    balls[i].speed[1] = -balls[i].speed[1]
                    balls[i].movetoResidual[1] = 0.0
                    # print("INFO: Ball i hit the top wall", " top=", balls[i].ballrect.top, balls[i].speed, balls[i].movetoResidual, balls[i].moveto)

            if balls[i].ballrect.bottom >= height:
                if balls[i].speed[1] > 0.0:
                    balls[i].speed[1] = -balls[i].speed[1]
                    balls[i].movetoResidual[1] = 0.0
                    score -= 10
                    # print("INFO: Ball i hit the bottom wall", " bottom=", balls[i].ballrect.bottom, balls[i].speed, balls[i].movetoResidual, balls[i].moveto)

            if balls[i].Is_Ball_in_Box_Range_Simple(boxrect):
                # print('ball {}  Is_Ball_in_Box_Range_Simple = True'.format(i))
                if flagNeedResponse_Ball2Box[i]:
                    #     check if within
                    if balls[i].ballrect.centerx >= boxrect.left and balls[i].ballrect.centerx <= boxrect.right:
                        if balls[i].speed[1] > 0.0:
                            balls[i].speed[1] = -balls[i].speed[1]
                            balls[i].movetoResidual[1] = 0.0
                            score += 10
                            flagNeedResponse_Ball2Box[i] = False
                    elif balls[i].Check_Ball_Hit_BoxTopLeftCorner(boxrect) == True:
                        # print("INFO: BallA hit top left corver of box")
                        balls[i].Calc_BallSpeed_on_BoxTopLeftCorner(boxrect, boxmovespeed)
                        score += 20
                        flagNeedResponse_Ball2Box[i] = False
                    elif balls[i].Check_Ball_Hit_BoxTopRightCorner(boxrect) == True:
                        # print("INFO: BallA hit top right corver of box")
                        balls[i].Calc_BallSpeed_on_BoxTopRightCorner(boxrect, boxmovespeed)
                        score += 20
                        flagNeedResponse_Ball2Box[i] = False
            else:
                flagNeedResponse_Ball2Box[i] = True

        # handle ball-ball collision
        for j in range(nBalls-1):
            for k in range(j+1, nBalls):
                pair_index = j * nBalls + k  # flat 2D indices into a 1D index
                
                c2cDistX = balls[j].ballrect.centerx - balls[k].ballrect.centerx
                c2cDistY = balls[j].ballrect.centery - balls[k].ballrect.centery
                distance = math.sqrt(c2cDistX * c2cDistX + c2cDistY * c2cDistY)

                # touched_Ball2Box[pair_index] = (distance <= thresholdDist_Ball2Ball[pair_index])
                # if not touched_Ball2Box[pair_index]:
                if distance > thresholdDist_Ball2Ball[pair_index]:
                    flagNeedResponse_Ball2Ball[pair_index] = True
                else:
                    # inside the ball-ball touch range
                    if flagNeedResponse_Ball2Ball[pair_index]:
                        # calculate new balls[j].speed and balls[k].speed (new direction)
                        c2cdirection = [c2cDistX / distance, c2cDistY / distance]   # j - k, from k to j
                        normc2cdirection = [-c2cdirection[1], c2cdirection[0]]   #

                        # determine balls j's and k's original speed along the c2c directions
                        origSpeed_on_c2c_J = balls[j].speed[0] * c2cdirection[0] + balls[j].speed[1] * c2cdirection[1]
                        origSpeed_on_c2c_K = balls[k].speed[0] * c2cdirection[0] + balls[k].speed[1] * c2cdirection[1]

                        # calculate the new speed along the c2c direction
                        newSpeed_on_c2c_J = ((balls[j].mass - balls[k].mass) * origSpeed_on_c2c_J + 2 * balls[k].mass * origSpeed_on_c2c_K) \
                                            / (balls[j].mass + balls[k].mass)
                        newSpeed_on_c2c_K = ( 2 * balls[j].mass * origSpeed_on_c2c_J - (balls[j].mass - balls[k].mass) * origSpeed_on_c2c_K) \
                                            / (balls[j].mass + balls[k].mass)

                        # The following two lines are valid for equal mass only
                        # newSpeed_on_c2c_J = origSpeed_on_c2c_K  # exchange
                        # newSpeed_on_c2c_K = origSpeed_on_c2c_J  # exchange

                        # now determine ball j's and k's original speed along the norm directions
                        origSpeed_on_Norm_J = balls[j].speed[0] * normc2cdirection[0] + balls[j].speed[1] * normc2cdirection[1]
                        origSpeed_on_Norm_K = balls[k].speed[0] * normc2cdirection[0] + balls[k].speed[1] * normc2cdirection[1]


                        # now calculate ball j's new speed along X-axis
                        balls[j].speed[0] = newSpeed_on_c2c_J * c2cdirection[0] + origSpeed_on_Norm_J * normc2cdirection[0]
                        # now calculate ball j's new speed along Y-axis
                        balls[j].speed[1] = newSpeed_on_c2c_J * c2cdirection[1] + origSpeed_on_Norm_J * normc2cdirection[1]

                        # now calculate ball k's new speed along X-axis
                        balls[k].speed[0] = newSpeed_on_c2c_K * c2cdirection[0] + origSpeed_on_Norm_K * normc2cdirection[0]
                        # now calculate ball k's new speed along Y-axis
                        balls[k].speed[1] = newSpeed_on_c2c_K * c2cdirection[1] + origSpeed_on_Norm_K * normc2cdirection[1]

                        balls[j].movetoResidual = [0.0, 0.0]
                        balls[k].movetoResidual = [0.0, 0.0]

                        # numberTouched += 1
                        flagNeedResponse_Ball2Ball[pair_index] = False
                        # print(balls[k].speed)
        k_e = 0
        for i in range (nBalls):
            # update balls[i].movetoResidual and balls[1].movetoResidual
            k_e += (balls[i].speed[0] ** 2 + balls[i].speed[1] ** 2) * balls[i].mass / 2

        text = font.render("Leve {}, Total score = {}".format(1, score), True, (255, 255, 255))
        screen.fill(color_black)
        screen.blit(backgroundpic, backgroundpicrect)
        screen.blit(box, boxrect)
        for i in range(nBalls):
            screen.blit(balls[i].ballimg, balls[i].ballrect)
        screen.blit(text, [width-300, 10])
        pygame.display.flip()
        # pygame.display.update()


if __name__ == '__main__':
    main()
