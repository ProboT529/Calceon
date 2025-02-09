import random

answers0 = [[173, 153, 163, 0], [51, 47, 32, 1], [44, 48, 50, 2], [151, 121, 111, 1], [70, 71, 72, 2], [1, 2, 3, 0], [14, 15, 7, 0], [153, 154, 155, 2], [269, 236, 301, 2], [8, 9, 10, 0], [18, 19, 20, 0], [9, 10, 11, 1], [-2, 0, 2, 2], [5, 7, 9, 2], [38, 39, 40, 0], [13, 14, 15, 1], [15, 16, 17, 2], [9, 11, 12, 1], [11, 12, 13, 0] ,[10, 12, 14, 1], [8, 9, 10, 0], [9, 10, 11, 1], [6, 7, 8, 0], [5, 7, 9, 1], [5, 6, 7, 2], [20, 22, 24, 2], [32, 33, 34, 1], [36, 37, 38, 0], [11, 12, 13, 2], [19, 20, 21, 1], [24, 27, 30, 1], [60, 64, 72, 1], [42, 44, 46, 0], [32, 34, 36, 0], [-60, -42, -34, 1], [24, 30, 34, 1], [55, 66, 76, 0], [8, 12, 14, 0], [118, 149, 159, 2], [18, 34, 42, 1], [12, 20, 22, 2]]

#later add the function taking an argument for the type of exercise the user wants to do / the type of exercise depending on the level
def questions():

  option0 = option1 = option2 = ''
  correct_answer = 0

  question_type = 0
  #question_type = random.randint(0, 2) #0 = three options, 1 = open answer, 2 = multiple choice
  #if question_type == 0:
  question = random.randint(0,40)
  option0 = answers0[question][0]
  option1 = answers0[question][1]
  option2 = answers0[question][2]
  correct_answer = answers0[question][3]
  '''elif question_type == 1:
    question = random.randint(0,1)
    option0 = answers1[question][0]
    option1 = answers1[question][1]
    option2 = answers1[question][2]
    correct_answer = answers1[question][3]
  else:
    question = random.randint(0,1)
    option0 = answers2[question][0]
    option1 = answers2[question][1]
    option2 = answers2[question][2]
    correct_answer = answers2[question][3]'''
  
  return question_type, question, option0, option1, option2, correct_answer

question_type, question, option0, option1, option2, correct_answer = questions()
#print(question_type, question, option0, option1, option2, correct_answer)
