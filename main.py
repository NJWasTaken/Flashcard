import pygame
import os
import pandas as pd
import random

# Initialize pygame
pygame.init()

df = pd.read_csv('database.txt')
s = open('score.txt')
hs = int(s.readline())
s.close()
q = df['Question']
a = df['Answer']
s = open('score.txt','w')

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("FlashCard")
bg = pygame.image.load(os.path.join('assets','bg.jpg')).convert()
bg = pygame.transform.scale(bg,(800,600))

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up fonts
font = pygame.font.Font(None, 36)

# Set up variables
r = random.randint(0,(len(q)-1))
question = q[r]
user_input = ""
correct_text = a[r]
menu = True
entry = False
flash = False
score = 0

# Main game loop
while True:
    screen.fill(white)
    screen.blit(bg,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if flash == True:
                s.write(str(hs))
                pygame.quit()
            else:
                pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if flash == True: 
                if event.key == pygame.K_RETURN:
                    if user_input == correct_text:
                        score += 1
                        r = random.randint(0,(len(q)-1))
                        question = q[r]
                        user_input = ""
                        correct_text = a[r]
                    else:
                        user_input = ''
                        score -= score

                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_ESCAPE:
                    if score>hs:
                        hs = score
                        s.write(str(hs))
                    menu = True
                    flash = False
                    score = 0
                else:
                    user_input += event.unicode
            elif menu == True:
                if event.key == pygame.K_SPACE:
                    flash = True
                    menu = False
                elif event.key == pygame.K_SLASH:
                    entry = True
                    menu = False



    if entry:
        text_surface = font.render(user_input, True, white)
        screen.blit(text_surface, (width//2 - text_surface.get_width()//2, height//2 - 115))
        pygame.draw.rect(screen, white, (width//2 - text_surface.get_width()//2 -15, height//2 - 140, text_surface.get_width()+30, 60), 1)

        button_text = font.render("Q", True, white)
        screen.blit(button_text, (width//2 - button_text.get_width()//2, height//2 - 170))


    if flash:
        text_surface = font.render(user_input, True, white)
        screen.blit(text_surface, (width//2 - text_surface.get_width()//2, height//2 - 15))
        pygame.draw.rect(screen, white, (width//2 - text_surface.get_width()//2 -15, height//2 - 30, text_surface.get_width()+30, 60), 1)

  
        question_text = font.render(question, True, white)
        screen.blit(question_text, (width//2 -   question_text.get_width()//2, height//2 - 60))

        if score<hs:
            high_score_txt = font.render(str(hs),True,white)
        else:
            high_score_txt = font.render(str(score),True,white)
        streak = font.render(str(score),True,white)
        st_title = font.render('Score:',True,white)
        hs_title = font.render('High Score:',True,white)
        screen.blit(streak, (width//2 -280, height//2 + 240))
        screen.blit(st_title, (width//2 -305, height//2 + 210))
        screen.blit(high_score_txt, (width//2 +230, height//2 + 240))
        screen.blit(hs_title, (width//2 +180, height//2 + 210))

    pygame.display.flip()
