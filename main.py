import pygame
import os
import pandas as pd
import random
import getpass

os.environ["GOOGLE_API_KEY"] = '' #Google api key goes here

with open('database.txt') as f:
    lis = f.readlines()
lis = lis[1:]

from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-pro")



# Initialize pygame
pygame.init()

df = pd.read_csv('database.txt')
s = open('score.txt')
hs = int(s.readline())
hs_c = hs
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
    prompt = "You are an examiner and are an expert at exam correction. Here is a list of questions and answers: "+str(lis)+" Use this list as a database to check whether an answer is correct or not. You should only reply with \
    'Correct' or 'Wrong' as your response to my answer. You should say that my answer is correct even if my answer doesnt perfectly match that in the database, but is close enough to mean the same thing. \
    Example: Q: Who painted the Mona Lisa?, A: da Vinci, Database Answer: Leonardo da Vinci. You may still respond with correct for this. Evaluate my answer accurately and strictly. Here is the question I must answer:"+str(q[r])+" Here is my answer:"+str(user_input)+". Respond with Correct or Wrong."
    
    screen.fill(white)
    screen.blit(bg,(0,0))
    back = font.render("< Back", True, white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            s.write(str(hs))
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if flash == True: 
                if event.key == pygame.K_RETURN:
                    try: 
                        result = llm.invoke(prompt)

                        if result.content == "Correct":
                            if score == hs:
                                hs+=1
                            score += 1
                            r = random.randint(0,(len(q)-1))
                            question = q[r]
                            user_input = ""
                            correct_text = a[r]

                        elif result.content == "Wrong":
                            user_input = ''
                            score -= score
                    except:
                        user_input = ''
                    else:
                        print(result.content)
                
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_ESCAPE:
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

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if menu:
                if x in range(355,445) and y in range(240,275):
                    menu = False
                    flash = True
                elif x in range(325,485) and y in range(295,325):
                    menu = False
                    entry = True
                elif x in range(295,510) and y in range(380,420):
                    hs = 0
            elif flash:
                if x in range(40,100) and y in range(40,80):
                    flash = False
                    menu = True

    if menu:
        title = font.render("FlashCard", True, (100,100,255))
        screen.blit(title, (width//2 - title.get_width()//2, height//2 - 170))

        op1 = font.render("Start", True, white)
        screen.blit(op1, (width//2 - op1.get_width()//2, height//2 - 50))
        op2 = font.render("Entry Mode", True, white)
        screen.blit(op2, (width//2 - op2.get_width()//2, height//2 ))

        res_title = font.render("Reset High Score", True, white)
        screen.blit(res_title, (width//2 - res_title.get_width()//2, height//2 + 90))

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

        screen.blit(back, (50,50))
  
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
