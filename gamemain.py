import pygame
from datetime import datetime
import heapq
import copy

#initialising game
pygame.init()


screenlength = 600
screenwidth  = 600

screen = pygame.display.set_mode((screenwidth,screenlength))

pygame.display.set_caption("Flappybird")

bird = pygame.image.load('logo.png')

logo = bird
pygame.display.set_icon(logo)

playerimage = bird

#coordinates of the bird
playerX = 100
playerY = 100

#for each x and y, (x,starty) to (x,endy) and (startx,y) to (endx,y) needs to be drawn

def drawgrid():
	size = 420
	startx=100
	endx  =520
	starty=100
	endy  =520
	font = pygame.font.Font('freesansbold.ttf', 22) 

	x = 100
	y = 100
	text = font.render('Press S to START/PAUSE GAME', True, (0,0,0), (200,200,200))
	text_rect = text.get_rect()
	text_rect.center = (270,40)
	screen.blit(text,text_rect)
	text = font.render('Press C to Clear paths', True, (0,0,0), (200,200,200))
	text_rect = text.get_rect()
	text_rect.center = (218,70)
	screen.blit(text,text_rect)


	while True:
		br = (x>520)
		if br == True:
			break

		pygame.draw.line(screen, (0,0,0), (startx,y), (endx, y), 1)
		pygame.draw.line(screen, (0,0,0), (x,starty), (x, endy), 1)
		x+=30
		y+=30
	screen.blit(playerimage,(playerX,playerY))

class mapcubestocolor(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 
 


mapcubetoclr = mapcubestocolor()
mapcubetoclr.add(((0,0),(600,600)), (0,100,200))


def h(pos1x, pos1y, pos2x, pos2y): #manhattan distance as the heuristic

	ans = 0;
	if pos1x > pos2x:
		ans+=(pos1x-pos2x)
	else:
		ans+=(pos2x-pos1x)

	ans//=30

	if pos1y > pos2y:
		ans+=((pos1y-pos2y)//30)
	else:
		ans+=((pos2y-pos1y)//30)
	
	return ans

def validchild(currentstatex,currentstatey):
	if (currentstatex >= 100 and currentstatex < 520) and (currentstatey >= 100 and currentstatey < 520):
		if (((currentstatex,currentstatey),(30,30)) not in mapcubetoclr) or (mapcubetoclr[((currentstatex,currentstatey),(30,30))] != (0,0,0) and mapcubetoclr[((currentstatex,currentstatey),(30,30))] != (100,0,0)):
			return True
	return False





def getSuccessors(currentstatex, currentstatey):
	successors = []
	if(validchild(currentstatex+30,currentstatey)):
		successors.append((currentstatex+30,currentstatey))

	if(validchild(currentstatex-30,currentstatey)):
		successors.append((currentstatex-30,currentstatey))


	if(validchild(currentstatex,currentstatey+30)):
		successors.append((currentstatex,currentstatey+30))


	if(validchild(currentstatex,currentstatey-30)):
		successors.append((currentstatex,currentstatey-30))
		
	return successors


def astar(mapcubetoclr, curcubex, curcubey):
	# print("implement astar search algo from ", (playerX,playerY))
	# print(" to ", (curcubex,curcubey))
	# print("h ", h(curcubex,curcubey,playerX,playerY))
	countexpanded = 0
	
	vis = []

	path = []

	fringe = [(h(playerX,playerY,curcubex,curcubey),(playerX,playerY),path)]
	heapq.heapify(fringe)

	#f(node),node, path before here
    #we start at the starting state node and then implement bfs until we find the goal state node

    
	while len(fringe) != 0:
		# print(len(fringe))
		if(len(fringe) == 0):
			break
		currf , (currStatex, currStatey), currpath = heapq.heappop(fringe)
		# print(currStatex,currStatey)
		# fringe.remove((currf,(currStatex,currStatey),currpath))
		# print("expanded ",currStatex,currStatey)
		vis.append((currStatex,currStatey))
		countexpanded+=1

		if ((currStatex == curcubex) and (currStatey == curcubey)):
			path=currpath
			path.append((currStatex,currStatey))
			break
		
		children = copy.deepcopy(getSuccessors(currStatex,currStatey))
		tempPath=copy.deepcopy(currpath)
		tempPath.append((currStatex,currStatey))
		for childx,childy in  children:
			if((childx,childy) not in vis):
				pushthis = (len(tempPath)+h(childx,childy,curcubex,curcubey),(childx,childy),tempPath)
				# print(pushthis)
				
				heapq.heappush(fringe,pushthis)

	for x,y in path:
		mapcubetoclr[((x,y),(30,30))] = (100,0,0)
	if len(path) == 0:
  		print("expanded ",countexpanded, " steps, couldn't find a path!")  	
	return path


if __name__ == "__main__":


	running = True


	start = False

	while running:
		
		screen.fill(mapcubetoclr[((0,0),(600,600))])

		for x in mapcubetoclr:
			pygame.draw.rect(screen,mapcubetoclr[x] ,x)
			

		drawgrid()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONUP:
				positionx,positiony = event.pos
				curcubex = positionx-(positionx-100)%30
				curcubey = positiony-(positiony-100)%30

				if (curcubex < 100 or curcubey < 100) or ((curcubex >= 520 or curcubey >= 520)):
					print("come back inside")
				else:
					if start and ((curcubex == playerX and curcubey == playerY) or validchild(curcubex,curcubey) == False):
						print("Not allowed here")


					else:

						if start == False:
							# obstacles
							
							if ((curcubex,curcubey),(30,30)) in mapcubetoclr:
								if mapcubetoclr[((curcubex,curcubey),(30,30))] != (0,100,200):
									mapcubetoclr[((curcubex,curcubey),(30,30))] = (0,100,200)
								else:
									mapcubetoclr[((curcubex,curcubey),(30,30))] = (0,0,0)

							else:
								mapcubetoclr.add(((curcubex,curcubey),(30,30)), (0,0,0))
							# make (curcubex, curcubey) as new obstacle

							print("obstacle added/removed at cube ", (curcubex, curcubey))


						else:

							if len(astar(mapcubetoclr, curcubex, curcubey)) == 0:
								print("Sorry, I am not allowed to jump :( ")
							else:
								
								playerX = curcubex
								playerY = curcubey

								print("reach cube ", (curcubex,curcubey))


			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_LEFT:
					if playerX == 100:
						print("stay in, little birdie!")
					else:
						playerX-=30
						if ((playerX,playerY),(30,30)) in mapcubetoclr and mapcubetoclr[((playerX,playerY),(30,30))] == (0,0,0):
							playerX+=30
							print("No Illegal movements, birdie!")
						print("playerX = ", playerX, " playerY = ", playerY)
				elif event.key == pygame.K_RIGHT:
					if playerX == 490:
						print("stay in, little birdie!")
					else:
						playerX+=30
						if ((playerX,playerY),(30,30)) in mapcubetoclr and mapcubetoclr[((playerX,playerY),(30,30))] == (0,0,0):
							playerX-=30
							print("No Illegal movements, birdie!")
						print("playerX = ", playerX, " playerY = ", playerY)
				elif event.key == pygame.K_DOWN:
					if playerY == 490:
						print("stay in, little birdie!")
					else:
						playerY+=30
						if ((playerX,playerY),(30,30)) in mapcubetoclr and mapcubetoclr[((playerX,playerY),(30,30))] == (0,0,0):
							playerY-=30
							print("No Illegal movements, birdie!")
						print("playerX = ", playerX, " playerY = ", playerY)
				elif event.key == pygame.K_UP:
					if playerY == 100:			
						print("stay in, little birdie!")
					else:
						playerY-=30

						if ((playerX,playerY),(30,30)) in mapcubetoclr and mapcubetoclr[((playerX,playerY),(30,30))] == (0,0,0):
							playerY+=30
							print("No Illegal movements, birdie!")
						print("playerX = ", playerX, " playerY = ", playerY)
				elif event.key == pygame.K_s:
					if start == False:
						start = True
					else:
						start = False
				elif event.key == pygame.K_c:
					for x in mapcubetoclr:
						if mapcubetoclr[x] == (100,0,0):
							mapcubetoclr[x] = (0,100,200)

			# elif even.KEYUP
		
		pygame.display.update()
