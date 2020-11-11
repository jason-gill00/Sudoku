import pygame

pygame.init()
win = pygame.display.set_mode((400,400))
pygame.display.set_caption("TESTING")

win.fill((255,255,255))

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            keypress = event.key
            if keypress >=32 and keypress<=126:
                key = chr(keypress)
                # if int(key)>=1 and int(key)<=9:
                #     print(key)
                if key in ['1','2','3','4','5','6','7','8','9']:
                    print(key)




#
# def event():
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#
#         if event.type = pygame.KEYDOWN:
#             return event.key

# def getCharacter():
#     keyinput = pygame.key.get_pressed()
#     character = "NULL"
#     pygame.event.pump()
#     keypress =
