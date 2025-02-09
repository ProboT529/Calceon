import pygame, os, random, csv, json
from pygame import mixer
from data import questions

#upgrades ideas: unlock shooting magic = gun(STAFF), faster bullets, more bullets (aka better gun(STAFF!!!)), shooting through walls (no wall collisions for bullets hehe), faster move speed, stop time, sword...
#dont forget to remove all prints
#add splashing sound when moving, just add a delay to it like when shooting!

mixer.init()
pygame.init()

DEV_MODE_ON = False

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Calceon')
pygame.display.set_icon(pygame.image.load('data/img/Entity/player/1/idle/1.png').convert_alpha())

#data


if os.path.isfile('data/save_file.json'):
  with open('data/save_file.json') as save_file:
    save_data = json.load(save_file)
else:
  data = {
  'story_started' : False,
  'story_finished' : False,
  'level' : 1,
  'stage' : 1,
  'death_counter' : 0,
  'NOTEBOOKS_COLLECTED' : 0,
  'notebook_collected_temp' : False,
  'question_params' : [0,0,0,0,0,0],
  'tempList' : [0,0,0,0,0,0,0,0,0,0],
  'question_window' : False,
  'question_loaded' : False,
  'question_answered' : False,
  'correct_answers_story' : 0,
  'wrong_answers_story' : 0,
  'max_streak_story' : 0,
  'streak_story' : 0,
  'max_streak' : 0,
  'upgradeMagicCollision' : False,
  }
  with open('data/save_file.json', 'w') as save_file:
    json.dump(data, save_file)
  with open('data/save_file.json') as save_file:
    save_data = json.load(save_file)



#framerate  
clock = pygame.time.Clock()
FPS = 60

#define game variable
#og tile size - TILE_SIZE = 50
COLS = 16
ROWS = 12
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 51
level = save_data['level']
stage = save_data['stage']
#books_collected = 0 ADD LATER
MAX_LEVELS = 20
NOTEBOOKS_COLLECTED = save_data['NOTEBOOKS_COLLECTED'] #TO DO - make the abilities tied to the amount of notebooks collected so far (gui with progress bar etc etc xdd)
music_playing = True
outro_page = 1


#define player action variables
move_left = False
move_right = False
move_up = False
move_down = False
last_move = 'right'
shoot = False
projectile_speed = 5
start_game = False
start_practice = False
start_intro = False
menu = False
question_found = False
player_answer = 0
correct_answers = 0
wrong_answers = 0
streak = 0

click_cooldown = 0

snow_cooldown = 0
frame_indexFG = 0

story_started = save_data['story_started']
story_finished = save_data['story_finished']
death_counter = save_data['death_counter']
notebook_collected_temp = save_data['notebook_collected_temp']
question_params = save_data['question_params']
question_type = question_params[0]
question = question_params[1]
option0 = question_params[2]
option1 = question_params[3]
option2 = question_params[4]
correct_answer = question_params[5]
tempList = save_data['tempList']
question_window = save_data['question_window']
question_loaded = save_data['question_loaded']
question_answered = save_data['question_answered']
correct_answers_story = save_data['correct_answers_story']
wrong_answers_story = save_data['wrong_answers_story']
max_streak_story = save_data['max_streak_story']
streak_story = save_data['streak_story']
max_streak = save_data['max_streak']
#upgradeSpeed = save_data['upgradeSpeed']
#upgradeStaff = save_data['upgradeStaff']
#upgradeMagic = save_data['upgradeMagic']
#upgradeMagic2 = save_data['upgradeMagic2']
upgradeMagicCollision = save_data['upgradeMagicCollision']
#upgradePSpeed = save_data['upgradePSpeed']
#upgradePCooldown = save_data['upgradePCooldown']
#upgradePAmount = save_data['upgradePAmount']
#upgradeHealth = save_data['upgradeHealth']
#upgradeTimeStop = save_data['upgradeTimeStop']

#LOADING ASSETS--------------------------

#-load music-
pygame.mixer.music.load('data/music/In The Mines - Marek Havlíček, Valerie Hrubá.wav')
pygame.mixer.music.set_volume(1)
#pygame.mixer.music.set_volume(0.01)
pygame.mixer.music.play(-1, 0, 0)
#question_music = pygame.mixer.Sound('data/music/kahoot.wav')
#question_music.set_volume(0.01)
projectile_fx = pygame.mixer.Sound('data/music/projectile.wav')
projectile_fx.set_volume(3)
#movement_fx_channel = pygame.mixer.Channel(1)
#movement_fx = pygame.mixer.Sound('data/music/slime.wav')
#death_fx = pygame.mixer.Sound('data/music/oof.wav')
#death_fx.set_volume(0.01)


#-load images-
#button images
title_img = pygame.image.load('data/img/Button/titleDEMO.png').convert_alpha()
newgame_img = pygame.image.load('data/img/Button/newgame.png').convert_alpha()
continue_img = pygame.image.load('data/img/Button/continue.png').convert_alpha()
practice_img = pygame.image.load('data/img/Button/practice.png').convert_alpha()
story_mode_img = pygame.image.load('data/img/Button/story_mode.png').convert_alpha()
game_over_img = pygame.image.load('data/img/Button/game_over.png').convert_alpha()
settings_img = pygame.image.load('data/img/Button/settings.png').convert_alpha()
mute_img = pygame.image.load('data/img/Button/mute.png').convert_alpha()
unmute_img = pygame.image.load('data/img/Button/unmute.png').convert_alpha()
exit_img = pygame.image.load('data/img/Button/exit.png').convert_alpha()
return_img = pygame.image.load('data/img/Button/return.png').convert_alpha()
retry_img = pygame.image.load('data/img/Button/retry.png').convert_alpha()
option0_img = pygame.image.load('data/img/Button/option0.png').convert_alpha()
option1_img = pygame.image.load('data/img/Button/option1.png').convert_alpha()
option2_img = pygame.image.load('data/img/Button/option2.png').convert_alpha()
option0_imgW = pygame.image.load('data/img/Button/option0W.png').convert_alpha()
option1_imgW = pygame.image.load('data/img/Button/option1W.png').convert_alpha()
option2_imgW = pygame.image.load('data/img/Button/option2W.png').convert_alpha()
option0_imgL = pygame.image.load('data/img/Button/option0L.png').convert_alpha()
option1_imgL = pygame.image.load('data/img/Button/option1L.png').convert_alpha()
option2_imgL = pygame.image.load('data/img/Button/option2L.png').convert_alpha()
correct_img = pygame.image.load('data/img/Button/correct.png').convert_alpha()
wrong_img = pygame.image.load('data/img/Button/wrong.png').convert_alpha()
streak_img = pygame.image.load('data/img/Button/streak.png').convert_alpha()
streak_img_story = pygame.image.load('data/img/Button/streak_story.png').convert_alpha()
counting_bg_img = pygame.image.load('data/img/Button/counting_bg.png').convert_alpha()
counting_bg_story_img = pygame.image.load('data/img/Button/counting_bg_story.png').convert_alpha()
task_window_img = pygame.image.load('data/img/Button/task_window.png').convert_alpha()
tutorial1_img = pygame.image.load('data/img/Button/tutorial1.png').convert_alpha()
tutorial2_img = pygame.image.load('data/img/Button/tutorial2.png').convert_alpha()
tutorial3_img = pygame.image.load('data/img/Button/tutorial3.png').convert_alpha()
tutorial4_img = pygame.image.load('data/img/Button/tutorial4.png').convert_alpha()
credits_img = pygame.image.load('data/img/Button/credits.png').convert_alpha()
feedbackQR_img = pygame.image.load('data/img/Button/feedbackQR.png').convert_alpha()

#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
  img = pygame.image.load(f'data/img/Tiles/{x}.png').convert_alpha()
  img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
  img_list.append(img)

#projectile
projectile_img = pygame.image.load('data/img/Weapon/projectile/player.png').convert_alpha()
#health
health_drop_img = pygame.image.load('data/img/Items/health/0.png').convert_alpha()
#magic
magic_drop_img = pygame.image.load('data/img/Items/magic/0.png').convert_alpha()
#small magic
small_magic_drop_img = pygame.image.load('data/img/Items/small_magic/0.png').convert_alpha()
#book
book_img = pygame.image.load('data/img/Items/book/0.png').convert_alpha()
item_drops = {
  'health'  : health_drop_img,
  'magic' : magic_drop_img,
  'small_magic' : small_magic_drop_img,
  'book' : book_img
}

#define font
font = pygame.font.SysFont('Comic Sans', 30)
medium_font = pygame.font.SysFont('Comic Sans', 25)
small_font = pygame.font.SysFont('Comic Sans', 20)

#function to draw text
def draw_text(text, font, text_col, x, y, img_width):
  img = font.render(text, True, text_col)
  img_width2 = img.get_rect().w
  if img_width == -1:
    screen.blit(img, (x, y))
  else:
    screen.blit(img, (x + (img_width - img_width2) // 2, y))

def draw_warped_text(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2
    # get the height of the font
    fontHeight = font.size("Tg")[1]
    while text:
        i = 1
        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break
        # determine maximum width of line
        while font.size(text[:i])[0] < (rect.width - 7) and i < len(text):
            i += 1
        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1
        # render the line and blit it to the surface
        image = font.render(text[:i], aa, color)
        surface.blit(image, (rect.left + 7, y))
        y += fontHeight + lineSpacing
        # remove the text we just blitted
        text = text[i:]
    return text

#function to draw background
def draw_bg():
  screen.blit(pygame.image.load(f'data/img/Background/{level}.png').convert_alpha(), (0, 0))

#function to draw foreground
def draw_fg():
  global frame_indexFG
  global snow_cooldown
  if snow_cooldown < 0:
    if frame_indexFG < 9:
      frame_indexFG += 1
      snow_cooldown = 10
    else:
      frame_indexFG = 0
      snow_cooldown = 10
  else:
    snow_cooldown -= 1
  screen.blit(pygame.image.load(f'data/img/Foreground/{frame_indexFG}.png').convert_alpha(), (0, 0))

#function to reset level
def reset_level():
  enemy_group.empty()
  projectile_group.empty()
  item_drops_group.empty()
  book_group.empty()
  exit_group.empty()

  #create empty tile list
  data = []
  for row in range(ROWS):
    r = [-1] * COLS
    data.append(r)

  return data


class Character(pygame.sprite.Sprite):
  def __init__(self, char_type, x, y, scale, speed, direction, tile_size, magic, health):
      pygame.sprite.Sprite.__init__(self)
      self.alive = True
      self.char_type = char_type
      self.speed = speed
      self.move_left = False
      self.move_right = False
      self.move_up = False
      self.move_down = False
      self.last_move = 'right'
      self.magic = magic
      self.maxmagic = self.magic
      self.dmg_cooldown = 0
      self.shoot_cooldown = 0
      self.projectile_speed = projectile_speed
      self.health = health
      self.maxhealth = self.health
      self.animation_list = []
      self.frame_index = 0
      self.action = 0
      self.direction = direction
      self.tile_size = tile_size
      self.update_time = pygame.time.get_ticks()
      self.roll = False
      self.drop = False
      #ai variables
      self.move_counter = 0
      if self.direction == 1 or self.direction == -1:
        self.line_of_sight = pygame.Rect(0, 0, 150, 50)
      else:
        self.line_of_sight = pygame.Rect(0, 0, 50, 150)
      self.idling = False
      self.idling_counter = 0

      #load all images for the character
      animation_types = ['idle', 'move', 'death']

      for animation in animation_types:
        #reset temporary list of images
        temp_list = []
        #count number of files in the folder, so you dont have to do it manually!
        if self.char_type == 'enemy3':
          num_of_frames = len(os.listdir(f'data/img/Entity/enemy2/{stage}/{animation}'))
        elif self.char_type == 'player':
          num_of_frames = len(os.listdir(f'data/img/Entity/player/1/{animation}'))
        else:
          num_of_frames = len(os.listdir(f'data/img/Entity/{self.char_type}/{stage}/{animation}'))
        for i in range(num_of_frames):
          if self.char_type == 'enemy3':
            img = pygame.image.load(f'data/img/Entity/enemy2/{stage}/{animation}/{i}.png').convert_alpha()
          elif self.char_type == 'player':
            img = pygame.image.load(f'data/img/Entity/player/1/{animation}/{i}.png').convert_alpha()
          else:
            img = pygame.image.load(f'data/img/Entity/{self.char_type}/{stage}/{animation}/{i}.png').convert_alpha()
          img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
          temp_list.append(img)
        self.animation_list.append(temp_list)
      
      self.image = self.animation_list[self.action][self.frame_index]
      self.rect = self.image.get_rect()
      self.rect.center = (x, y)
      self.width = self.image.get_width()
      self.height = self.image.get_height()
  
  def update(self):
    #update defined functions/methods of the object
    self.update_animation()
    self.check_alive()
    #update cooldown
    if self.shoot_cooldown > 0:
      self.shoot_cooldown -= 1


  def move(self, move_left, move_right, move_up, move_down):
    #reset movement variables (d means delta, which is the change of movement)
    dx = 0
    dy = 0

    #assign movement variables if moving left or right
    if self.move_left:
      dx = -self.speed
      self.direction = -1
    if self.move_right:
      dx = self.speed
      self.direction = 1
    if self.move_up:
      dy = -self.speed
      self.direction = -2
    if self.move_down:
      dy = self.speed
      self.direction = 2

    #check for collision
    for tile in world.obstacle_list: #itirate through all the tiles in the obstacle list
      #check collision in the x direction
      if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
        dx = 0
        #check if the ai hit the tile and make it turn around
        if self.char_type == 'enemy' or self.char_type == 'enemy2' or self.char_type == 'enemy3':
          self.direction *= -1
          self.move_counter = 0
      #check collision in the y direction
      if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
        dy = 0
        #check if the ai hit the tile and make it turn around
        if self.char_type == 'enemy' or self.char_type == 'enemy2' or self.char_type == 'enemy3':
          self.direction *= -1
          self.move_counter = 0



    #ADD THIS LATER check for collision with lava part 12 10 mins!!!!!!!!



    question_activation = False
    if pygame.sprite.spritecollide(self, book_group, True):
      question_activation = True
    
    #check for collision with exit portal
    level_complete = False
    if pygame.sprite.spritecollide(self, exit_group, False) and notebook_collected_temp:
      level_complete = True

    for enemy in enemy_group:
      if pygame.Rect.colliderect(player.rect, enemy.rect):
        if self.dmg_cooldown > 0:
          self.dmg_cooldown -= 1
        
        if self.dmg_cooldown == 0 and enemy.health > 0:
          self.dmg_cooldown = 30
          if enemy.char_type == 'enemy2' or enemy.char_type == 'enemy3':
            player.health -= 5
          player.health -= 5


    #check for collision with border
    if self.rect.bottom + dy > SCREEN_HEIGHT:
      dy = SCREEN_HEIGHT - self.rect.bottom
    elif self.rect.top + dy < 0:
      dy = 0 + self.rect.top
    elif self.rect.left + dx < 0:
      dx = 0 + self.rect.left
    elif self.rect.right + dx > SCREEN_WIDTH:
      dx = SCREEN_WIDTH - self.rect.right
    
#    if dx != 0 or dy != 0:
#      if not movement_fx_channel.get_busy():
#        movement_fx_channel.play(movement_fx)
#    else:
#      movement_fx_channel.stop()

    #update rectangle position
    self.rect.x += dx
    self.rect.y += dy

    return level_complete, question_activation

  def shoot(self, parent):
      if self.shoot_cooldown == 0 and self.magic > 0:
        self.shoot_cooldown = 40 #cooldown
        self.magic -= 1 #reduces magic
        projectile_fx.play(0, 0, 0)
        if self.direction == 1 or self.direction == -1:
          projectile = Projectile(parent, self.rect.centerx + (0.8 * self.rect.size[0] * self.direction), self.rect.centery, self.projectile_speed, self.direction)
        else:
          projectile = Projectile(parent, self.rect.centerx, self.rect.centery + (0.3 * self.rect.size[1] * self.direction), self.projectile_speed, self.direction)

  def ai(self):
    #checks if the character and the player are both alive
    if self.alive and player.alive:
      #assigns a movement bool based on direction
      if self.idling == False and random.randint(1, 1000) == 42:
        self.update_action(0)
        self.idling = True
        self.idling_counter = 50
      
      #check if the ai line of sight is colliding with the player
      if self.line_of_sight.colliderect(player.rect):
          if self.char_type != 'enemy2' or self.char_type != 'enemy3':
            #stop moving and face the player
            self.update_action(0) #0 = idle
            #SHOOT THEM
            self.shoot(self.char_type)
      else:
        if self.idling == False:
          if self.direction == -1:
            self.move_left = True
            self.move_right = self.move_up = self.move_down = False
          elif self.direction == 1:
            self.move_right = True
            self.move_left = self.move_up = self.move_down = False
          elif self.direction == -2:
            self.move_up = True
            self.move_left = self.move_right = self.move_down = False
          elif self.direction == 2:
            self.move_down = True
            self.move_left = self.move_right = self.move_up = False
          #calls the move method with the variables
          self.move(self.move_left, self.move_right, self.move_up, self.move_down)
          self.update_action(1) #1 = moving
          self.move_counter += 1

          if self.move_counter > self.tile_size:
            self.direction *= -1
            self.move_counter = 0
            if self.char_type == 'enemy3':
              if self.direction == -1:
                self.direction = -2
              elif self.direction == -2:
                self.direction = 1
              elif self.direction == 1:
                self.direction = 2
              elif self.direction == 2:
                self.direction = -1
        else:
          self.idling_counter -= 1
          if self.idling_counter == 0:
            self.idling = False
      
      #update ai vision as the ai moves
      if self.move_left or self.move_right or (self.direction == -1 or self.direction == 1):
        self.line_of_sight.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
      elif self.move_up or self.move_down or (self.direction == -2 or self.direction == 2):
        self.line_of_sight.center = (self.rect.centerx, self.rect.centery + 37.5 * self.direction)
      if self.char_type == 'enemy2' or self.char_type == 'enemy3':
        self.line_of_sight.center = (-50, 0)
      #TEMPORARY HITBOX LINE OF SIGHT pygame.draw.rect(screen, 'GREEN', self.line_of_sight, 1)

  def update_animation(self):
    #update image based on frame
    self.image = self.animation_list[self.action][self.frame_index]

    #define timer, and check how much time passed since last update
    COOLDOWN = 60
    if pygame.time.get_ticks() - self.update_time > COOLDOWN:
      self.frame_index += 1
      self.update_time = pygame.time.get_ticks()
    #if the list runs out, it starts at the beginning again
    if self.frame_index >= len(self.animation_list[self.action]):
      if self.action == 3:
        self.frame_index = len(self.animation_list[self.action]) - 1
      else:
        self.frame_index = 0
  
  def update_action(self, new_action):
    #check if the new action is different to previous one
    if new_action != self.action:
      self.action = new_action
      #update the animation settings
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()

  def check_alive(self):
    if self.health <= 0:
      self.health = 0
      self.speed = 0
      self.alive = False
      self.update_action(2)
      if self.drop == False and (self.char_type == 'enemy' or self.char_type == 'enemy2' or self.char_type == 'enemy3'):
        #death_fx.play()
        ranDrop = random.randint(1,10)
        self.drop = True
        if ranDrop > 5:
          if player.health != player.maxhealth:
            item_drop = Collectible('health', self.rect.x, self.rect.y)
            item_drops_group.add(item_drop)
            self.drop = True
          else:
            item_drop = Collectible('magic', self.rect.x, self.rect.y)
            item_drops_group.add(item_drop)
            self.drop = True
        else:
            item_drop = Collectible('small_magic', self.rect.x, self.rect.y)
            item_drops_group.add(item_drop)
            self.drop = True


  #draws the player - CHANGE WITH UPDATED SYMMETRICAL PICTURES FOR UP AND DOWN MOVEMENT
  def draw(self):
    if self.move_left or self.last_move == 'left':
      screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
    elif self.move_right or self.last_move == 'right':
      screen.blit(pygame.transform.flip(self.image, False, False), self.rect)
    elif self.move_up or self.last_move == 'up':
      screen.blit(pygame.transform.flip(pygame.transform.rotate(self.image, 90), False, False), self.rect)
    elif self.move_down or self.last_move == 'down':
      screen.blit(pygame.transform.flip(pygame.transform.rotate(self.image, 90), False, True), self.rect)
    else:
      screen.blit(self.image, self.rect)
    #TEMPORARY HITBOX - remove the line under this, shows the rectangle around entities
    #pygame.draw.rect(screen, 'RED', self.rect, 1)

class World():
  def __init__(self):
    self.obstacle_list = []

  def process_data(self, data):
    #iterate through each value in level data file
    for y, row in enumerate(data):
      for x, tile in enumerate(row):
        if tile >= 0:
          img = img_list[tile]
          img_rect = img.get_rect()
          img_rect.x = x * TILE_SIZE #gives x position
          img_rect.y = y * TILE_SIZE #gives y position
          tile_data = (img, img_rect)
          if tile >= 0 and tile <= 18: #the other number (3 in this case) depends on how many textures you have for a block of the same function (f.e. wall)
            self.obstacle_list.append(tile_data)
          elif tile == 34: #create player /w healthbar
            player = Character('player', x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE / 2, 1, 5, 1, TILE_SIZE, 10, 100)
            health_bar = HealthBar(9, 9, player.health, player.maxhealth)
          elif tile == 35: #create enemies #H
            #create enemy
            enemy = Character('enemy', x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE / 2, 1, 5, 1, 50, 8, 100)
            enemy_group.add(enemy)
          elif tile == 36: #V
            #create enemy
            enemy = Character('enemy', x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE / 2, 1, 5, 2, 50, 8, 100)
            enemy_group.add(enemy)
          elif tile == 37: #H
            #create enemy that damages upon touch
            enemy = Character('enemy2', x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE / 2, 1, 5, 1, 50, 0, 50)
            enemy_group.add(enemy)
          elif tile == 38: #V
            #create enemy that damages upon touch
            enemy = Character('enemy2', x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE / 2, 1, 5, 2, 50, 0, 50)
            enemy_group.add(enemy)
          elif tile == 39: #SQUARE LEFT
            #create enemy that shoots
            enemy = Character('enemy3', x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE / 2, 1, 5, 2, 20, 0, 100)
            enemy_group.add(enemy)
          elif tile == 50:
            self.obstacle_list.append(tile_data)
          elif tile == 43:
            #creates magic drop
            item_drop = Collectible('magic', x * TILE_SIZE, y * TILE_SIZE)
            item_drops_group.add(item_drop)
          elif tile == 44:
            #create health drop
            item_drop = Collectible('health', x * TILE_SIZE, y * TILE_SIZE)
            item_drops_group.add(item_drop)
          elif tile == 45 and not notebook_collected_temp and not question_loaded and not question_answered:
            #creates book
            item_drop = Collectible('book', x * TILE_SIZE, y * TILE_SIZE)
            book_group.add(item_drop)
          elif tile == 47: #create exit
            exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
            exit_group.add(exit)
   
    return player, health_bar

          #continue with elif tile >= x and tile <= y for other tiles such as water, lava, etc etc you get it
      
  def draw(self):
    for tile in self.obstacle_list:
      screen.blit(tile[0], tile[1])

class HealthBar():
  def __init__(self, x, y , health, maxhealth):
    self.x = x
    self.y = y
    self.health = health
    self.maxhealth = maxhealth

  def draw(self, health):
    #update with new health
    self.health = health

    #calculate health ratio
    ratio = self.health / self.maxhealth

    pygame.draw.rect(screen, 'BLACK', (self.x-2, self.y-2, 154, 24))
    pygame.draw.rect(screen, (63,63,63), (self.x, self.y, 150, 20))
    pygame.draw.rect(screen, 'RED', (self.x, self.y, 150 * ratio, 20))

class Projectile(pygame.sprite.Sprite):

  def __init__(self, parent, x, y, speed, direction):
    self.group = projectile_group
    self.parent = parent
    pygame.sprite.Sprite.__init__(self, self.group)
    self.speed = speed # one of the upgrades will be the speed of the bullets
    if self.parent != 'player':
      self.image = pygame.image.load(f'data/img/Weapon/projectile/{stage}.png').convert_alpha()
    else:
      self.image = projectile_img
    self.rect = self.image.get_rect() #doesnt matter which one cuz all of them are the same resolution
    self.rect.center = (x, y)
    self.direction = direction

  def update(self):
    #TEMPORARY HITBOX
    #pygame.draw.rect(screen, 'RED', self.rect, 1)
    #move projectile
    if self.direction == 1 or self.direction == -1:
      self.rect.x += (self.direction * self.speed * 1.5)
    else:
      self.rect.y += (self.direction * self.speed * 0.5 * 1.5)
    #check if projectile is off screen
    if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0:
      self.kill()
    
    #check collision with tiles
    for tile in world.obstacle_list:
      if tile[1].colliderect(self.rect):
        if self.parent != 'player' or upgradeMagicCollision == False:
          self.kill()

    #check collision with characters
    if self.parent == "player":
      for enemy in enemy_group:
        if pygame.sprite.spritecollide(enemy, projectile_group, False):
          if enemy.alive:
            self.kill()
            enemy.health -= 50
            #print(enemy.health)
    elif self.parent == "enemy":
      if pygame.sprite.spritecollide(player, projectile_group, False):
        if player.alive:
          self.kill()
          player.health -= 25
          #print(player.health)
#      for enemy in enemy_group:
#        if pygame.sprite.spritecollide(enemy, projectile_group, False):
#          if enemy.alive:
  
class Decoration(pygame.sprite.Sprite): #aight this is for when you need to code in decorations, dont do it for the demo (via part 9, around 33 mins)

  def __init__(self, img, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = img
    self.rect = self.image.get_rect()
    self.rect.midtop = (x + TILE_SIZE // 2, y)

class Lava(pygame.sprite.Sprite): #aight this is for when you need to code in decorations, dont do it for the demo (via part 9, around 33 mins)

  def __init__(self, img, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = img
    self.rect = self.image.get_rect()
    self.rect.midtop = (x + TILE_SIZE // 2, y)
  
class Exit(pygame.sprite.Sprite): #aight this is for when you need to code in decorations, dont do it for the demo (via part 9, around 33 mins)

  def __init__(self, img, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = img
    self.rect = self.image.get_rect()
    self.rect.midtop = (x + TILE_SIZE // 2, y)

class Collectible(pygame.sprite.Sprite):

  def __init__(self, item_type, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.item_type = item_type
    self.image = item_drops[self.item_type]
    self.rect = self.image.get_rect()
    self.rect.center = (x + TILE_SIZE // 2, y + TILE_SIZE // 2)

  def update(self):
    #check if player has picked up the drop
    if pygame.sprite.collide_rect(self, player):
      #check what kind of drop it was
      if self.item_type == 'health' and player.health < player.maxhealth:
        player.health += 25
        if player.health > player.maxhealth:
          player.health = player.maxhealth
        #print(player.health)
        self.kill()
      elif self.item_type == 'magic' and player.magic < player.maxmagic:
        player.magic += 3
        if player.magic > player.maxmagic:
          player.magic = player.maxmagic
        #print(player.magic)
        self.kill()
      elif self.item_type == 'small_magic' and player.magic < player.maxmagic:
        player.magic += 1
        if player.magic > player.maxmagic:
          player.magic = player.maxmagic
        #print(player.magic)
        self.kill()

#GO THROUGH THIS CODE, UNDERSTAND IT AND CHANGE IT ACCORDING TO THE OTHER NAMES YOU USED THROUGHOUT THE PROGRAM INSIDE THE CLASSES
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

class ScreenFade():
  def __init__(self, direction, color, speed):
    self.direction = direction
    self.color = color
    self.speed = speed
    self.fade_counter = 0

  def fade(self):
    fade_complete = False
    self.fade_counter += self.speed
    if self.direction == 1: #whole screen fade
      pygame.draw.rect(screen, self.color, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
      pygame.draw.rect(screen, self.color, (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT)) 
    elif self.direction == 2: #vertical fade down
      pygame.draw.rect(screen, self.color, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
    if self.fade_counter >= 700: #even though it should be height, the screen is wider so it's just a safety precaution
      fade_complete = True
    
    return fade_complete

#create screen fades
start_fade = ScreenFade(1, (160,32,240), 10)
death_fade = ScreenFade(2, (0,0,0), 15)

#create buttons PLAY WITH THE COORDINATES LATER ACCORDING TO THE MAIN MENU SKETCH YOU PREPARE
newgame_button = Button(SCREEN_WIDTH // 2 - 275, SCREEN_HEIGHT // 2 - 80, newgame_img, 2)
continue_button = Button(SCREEN_WIDTH // 2 - 275, SCREEN_HEIGHT // 2 - 10, continue_img, 2)
continue_button_P = Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 70, continue_img, 2)
practice_button = Button(SCREEN_WIDTH // 2 - 275, SCREEN_HEIGHT // 2 + 60, practice_img, 2)
settings_button = Button(SCREEN_WIDTH // 2 - 275, SCREEN_HEIGHT // 2 + 130, settings_img, 2)
mute_button = Button(SCREEN_WIDTH // 2 - 275, SCREEN_HEIGHT // 2 + 130, mute_img, 2)
unmute_button = Button(SCREEN_WIDTH // 2 - 275, SCREEN_HEIGHT // 2 + 130, unmute_img, 2)
exit_button = Button(SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 + 130, exit_img, 2)
return_button_P = Button(50, 50, return_img, 2)
return_button = Button(SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2, return_img, 2)
respawn_button = Button(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 25, retry_img, 1)
restartStreak_button = Button(SCREEN_WIDTH // 2 - 320, 400, retry_img, 1)
credits_button = Button(700, 500, credits_img, 2)

option0_button = Button(SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 + 200, option0_img, 1)
option1_button = Button(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 + 200, option1_img, 1)
option2_button = Button(SCREEN_WIDTH // 2 + 125, SCREEN_HEIGHT // 2 + 200, option2_img, 1)
option0_W = Button(SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 + 200, option0_imgW, 1)
option1_W = Button(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 + 200, option1_imgW, 1)
option2_W = Button(SCREEN_WIDTH // 2 + 125, SCREEN_HEIGHT // 2 + 200, option2_imgW, 1)
option0_L = Button(SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 + 200, option0_imgL, 1)
option1_L = Button(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 + 200, option1_imgL, 1)
option2_L = Button(SCREEN_WIDTH // 2 + 125, SCREEN_HEIGHT // 2 + 200, option2_imgL, 1)

#create sprite groups
enemy_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
item_drops_group = pygame.sprite.Group()
book_group = pygame.sprite.Group()
#add another group for decoration and lava?
exit_group = pygame.sprite.Group()

#create empty tile list
world_data = []
for row in range(ROWS):
  r = [-1] * COLS
  world_data.append(r)

run = True
while run:

  #limits how quick the game runs
  clock.tick(FPS)

  if not start_game and not start_practice: #and not DEV_MODE_ON:
    #main menu

    screen.blit(story_mode_img, (350, 0))
    menuRectangle = pygame.Rect(0, 0, 351, 600)
    pygame.draw.rect(screen, 'PURPLE', menuRectangle)
    pygame.draw.line(screen, "PURPLE", (400, 0), (300, 600), 100)
    screen.blit(title_img, (SCREEN_WIDTH // 2 - 320, 75))
    draw_text('ZPĚTNÁ VAZBA', font, 'WHITE', 550, 300, 200)
    screen.blit(feedbackQR_img, (550,350))
    #add buttons
    if newgame_button.draw(screen):
      level = save_data['level'] = 1
      stage = save_data['stage'] = 1
      death_counter = save_data['death_counter'] = 0
      NOTEBOOKS_COLLECTED = save_data['NOTEBOOKS_COLLECTED'] = 0
      notebook_collected_temp = save_data['notebook_collected_temp'] = False
      story_started = save_data['story_started'] = True
      story_finished = save_data['story_finished'] = False
      correct_answers_story = save_data['correct_answers_story'] = 0
      wrong_answers_story = save_data['wrong_answers_story'] = 0
      streak_story = save_data['streak_story'] = 0
      #upgradeSpeed = save_data['upgradeSpeed'] = False
      #upgradeStaff = save_data['upgradeStaff'] = False
      #upgradeMagic = save_data['upgradeMagic'] = False
      #upgradeMagic2 = save_data['upgradeMagic2'] = False
      upgradeMagicCollision = save_data['upgradeMagicCollision'] = False
      #upgradePSpeed = save_data['upgradePSpeed'] = False
      #upgradePCooldown = save_data['upgradePCooldown'] = False
      #upgradePAmount = save_data['upgradePAmount'] = False
      #upgradeHealth = save_data['upgradeHealth'] = False
      #upgradeTimeStop = save_data['upgradeTimeStop'] = False
      question_activation = False
      question_window = save_data['question_window'] = False
      question_loaded = save_data['question_loaded'] = False
      question_answered = save_data['question_answered'] = False
      click_cooldown = 0
      start_game = True
      start_intro = True
      with open(f'data/level/level{level}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';') #the tutorial uses , as the delimiter, idk why its this here but oh well
        for x, row in enumerate(reader):
          for y, tile in enumerate(row):
            world_data[x][y] = int(tile) #int cuz it gives back string
      world = World()
      player, health_bar = world.process_data(world_data)
    
    if story_started and not story_finished:
      if continue_button.draw(screen):
        level = save_data['level']
        stage = save_data['stage']
        death_counter = save_data['death_counter']
        notebook_collected_temp = save_data['notebook_collected_temp']
        question_params = save_data['question_params']
        question_type = question_params[0]
        question = question_params[1]
        option0 = question_params[2]
        option1 = question_params[3]
        option2 = question_params[4]
        correct_answer = question_params[5]
        tempList = save_data['tempList']
        question_window = save_data['question_window']
        question_loaded = save_data['question_loaded']
        question_answered = save_data['question_answered']
        correct_answers_story = save_data['correct_answers_story']
        wrong_answers_story = save_data['wrong_answers_story']
        max_streak_story = save_data['max_streak_story']
        streak_story = save_data['streak_story']
        max_streak = save_data['max_streak']
        start_game = True
        start_intro = True
        with open(f'data/level/level{level}_data.csv', newline='') as csvfile:
          reader = csv.reader(csvfile, delimiter=';') #the tutorial uses , as the delimiter, idk why its this here but oh well
          for x, row in enumerate(reader):
            for y, tile in enumerate(row):
              world_data[x][y] = int(tile) #int cuz it gives back string
        world = World()
        player, health_bar = world.process_data(world_data)

    if practice_button.draw(screen):
      start_practice = True
      question_loaded = False
      question_answered = False
      start_intro = True
      #print('huh')
    
    if music_playing:
      if mute_button.draw(screen):
        pygame.mixer.music.pause()
        music_playing = False
    else:
      if unmute_button.draw(screen):
        pygame.mixer.music.unpause()
        music_playing = True
    #TEMPORARY if settings_button.draw(screen):
      #print('heh')
    
    if exit_button.draw(screen):
      run = False

  elif menu == True and start_game == True:
    #pause menu
    screen.fill((160,32,0))
    
    #add buttons
    if continue_button_P.draw(screen):
      menu = False
    if return_button.draw(screen):
      menu = False
      start_game = False
      if question_answered and player_answer == correct_answer:
        question_window = False
        NOTEBOOKS_COLLECTED += 1
        #pygame.mixer.music.unpause()
        #question_music.stop()
        notebook_collected_temp = save_data['notebook_collected_temp'] = True
        question_answered = False
        question_loaded = False
        click_cooldown = 0
      save_data['story_started'] = story_started = True
      save_data['level'] = level
      save_data['stage'] = stage
      save_data['death_counter'] = death_counter
      save_data['NOTEBOOKS_COLLECTED'] = NOTEBOOKS_COLLECTED
      save_data['notebook_collected_temp'] = notebook_collected_temp
      save_data['question_window'] = question_window
      save_data['question_loaded'] = question_loaded
      save_data['question_params'] = question_params
      save_data['tempList'] = tempList
      save_data['question_answered'] = question_answered
      save_data['correct_answers_story'] = correct_answers_story
      save_data['wrong_answers_story'] = wrong_answers_story
      save_data['max_streak_story'] = max_streak_story
      save_data['streak_story'] = streak_story
      save_data['max_streak'] = max_streak
      save_data['upgradeMagicCollision'] = upgradeMagicCollision
      world_data = reset_level()
  
  elif (question_window == True and menu == False and start_game == True) or start_practice:
    #question gui
    screen.fill((255,255,255))
    if click_cooldown < 50 and click_cooldown > 0:
      if player_answer == correct_answer:
        pygame.draw.line(screen, "GREEN", (0, 0), (0, 600), 50)
        pygame.draw.line(screen, "GREEN", (800, 0), (800, 600), 50)
        pygame.draw.line(screen, "GREEN", (0, 0), (800, 0), 50)
        pygame.draw.line(screen, "GREEN", (0, 600), (800, 600), 50)
      else:
        pygame.draw.line(screen, "RED", (0, 0), (0, 600), 50)
        pygame.draw.line(screen, "RED", (800, 0), (800, 600), 50)
        pygame.draw.line(screen, "RED", (0, 0), (800, 0), 50)
        pygame.draw.line(screen, "RED", (0, 600), (800, 600), 50)

    if question_loaded == False:
      while not question_found:
        question_type, question, option0, option1, option2, correct_answer = questions.questions()
        if question not in tempList:
          tempList2 = tempList
          for i in range(0, 9):
            tempList2[i] = tempList[i+1]
          tempList2.append(question)
          del tempList2[9]
          tempList = tempList2
          #print(tempList)
          break
      if start_game:
        question_params = [question_type, question, option0, option1, option2, correct_answer]
      
      question_loaded = True
      question_answered = False

    screen.blit(pygame.image.load(f'data/img/Questions/{question}.png').convert_alpha(), (SCREEN_WIDTH // 2 - 150, 150))
    task_window = screen.blit(task_window_img, (200, 30))
    if question <= 9:
      task = 'Jaké číslo bude v barevném poli?'
    elif question <= 14:
      task = 'Jaký je součet čísel v barevných polích?'
    elif question <= 19:
      task = 'Kolik kostiček je ve stavbě?'
    elif question <= 24:
      task = 'Kolik kostiček je vidět seshora?'
    elif question <= 29:
      task = 'Kolik kostek je nutno doplnit, aby vzniknul kvádr?'
    elif question <= 34:
      task = 'Jaké bude číslo v barevném políčku?'
    elif question <= 40:
      task = 'Doplň řadu.'
    #(task, small_font, 'BLACK', 200, 65, 400)
    draw_warped_text(screen, task, 'BLACK', task_window, medium_font)
    if start_practice:
      screen.blit(counting_bg_img, (SCREEN_WIDTH // 2 - 360, 190))
    else:
      screen.blit(counting_bg_story_img, (SCREEN_WIDTH // 2 - 360, 190))
    #add buttons
    if option0_button.draw(screen) and not question_answered:
      player_answer = 0
      click_cooldown = 50
      if player_answer == correct_answer:
        #print('CORRECT!')
        if start_practice:
          correct_answers += 1
          streak += 1
          if streak > max_streak:
            max_streak = streak
        else:
          correct_answers_story += 1
          streak_story += 1
          if streak_story > max_streak_story:
            max_streak_story = streak_story          
        question_answered = True
      else:
        #print('WRONG')
        if start_practice:
          wrong_answers += 1
          streak = 0
        else:
          wrong_answers_story += 1
          streak_story = 0
        question_answered = True
    if option1_button.draw(screen) and not question_answered:
      player_answer = 1
      click_cooldown = 50
      if player_answer == correct_answer:
        #print('CORRECT!')
        if start_practice:
          correct_answers += 1
          streak += 1
          if streak > max_streak:
            max_streak = streak
        else:
          correct_answers_story += 1
          streak_story += 1
          if streak_story > max_streak_story:
            max_streak_story = streak_story          
        question_answered = True
      else:
        #print('WRONG')
        if start_practice:
          wrong_answers += 1
          streak = 0
        else:
          wrong_answers_story += 1
          streak_story = 0
        question_answered = True
    if option2_button.draw(screen) and not question_answered:
      player_answer = 2
      click_cooldown = 50
      if player_answer == correct_answer:
        #print('CORRECT!')
        if start_practice:
          correct_answers += 1
          streak += 1
          if streak > max_streak:
            max_streak = streak
        else:
          correct_answers_story += 1
          streak_story += 1
          if streak_story > max_streak_story:
            max_streak_story = streak_story          
        question_answered = True
      else:
        #print('WRONG')
        if start_practice:
          wrong_answers += 1
          streak = 0
        else:
          wrong_answers_story += 1
          streak_story = 0
        question_answered = True
    
    Woptions = {0:option0_W, 1:option1_W, 2:option2_W}
    Loptions = {0:option0_L, 1:option1_L, 2:option2_L}

    if question_answered:
      if player_answer != correct_answer:
        Loptions[player_answer].draw(screen)
        if Woptions[correct_answer].draw(screen) and click_cooldown == 0:
          question_answered = False
          question_loaded = False
        else:
          if click_cooldown > 0:
            click_cooldown -= 1
      else:
        if Woptions[player_answer].draw(screen) and click_cooldown == 0:
          if start_game == True:
            question_window = False
            NOTEBOOKS_COLLECTED += 1
            #pygame.mixer.music.unpause()
            #question_music.stop()
            notebook_collected_temp = save_data['notebook_collected_temp'] = True
          question_answered = False
          question_loaded = False
        else:
          if click_cooldown > 0:
            click_cooldown -= 1

    #at the end so it shows on top of the image of the button

    draw_text(str(option0), font, 'BLACK', option0_button.rect.x, option0_button.rect.y + 2, option0_button.rect.width)
    draw_text(str(option1), font, 'BLACK', option1_button.rect.x, option1_button.rect.y + 2, option0_button.rect.width)
    draw_text(str(option2), font, 'BLACK', option2_button.rect.x, option2_button.rect.y + 2, option0_button.rect.width)

    if start_practice:
      screen.blit(correct_img, (SCREEN_WIDTH // 2 - 345, 200))
      screen.blit(wrong_img, (SCREEN_WIDTH // 2 - 345, 270))
      screen.blit(streak_img, (SCREEN_WIDTH // 2 - 345, 340))
      correct_answers_text = draw_text(str(correct_answers), font, 'GREEN', SCREEN_WIDTH // 2 - 290, 200 + 2, 50)
      wrong_answers_text = draw_text(str(wrong_answers), font, 'RED', SCREEN_WIDTH // 2 - 290, 270 + 2, 50)
      streak_count_text = draw_text(str(streak), font, 'ORANGE', SCREEN_WIDTH // 2 - 290, 340 + 2, 50)
    else:
      screen.blit(correct_img, (SCREEN_WIDTH // 2 - 345, 200))
      screen.blit(wrong_img, (SCREEN_WIDTH // 2 - 345, 270))
      screen.blit(streak_img_story, (SCREEN_WIDTH // 2 - 345, 340))
      correct_answers_text = draw_text(str(correct_answers_story), font, 'GREEN', SCREEN_WIDTH // 2 - 290, 200 + 2, 50)
      wrong_answers_text = draw_text(str(wrong_answers_story), font, 'RED', SCREEN_WIDTH // 2 - 290, 270 + 2, 50)
      streak_count_text = draw_text(str(streak_story), font, 'PURPLE', SCREEN_WIDTH // 2 - 290, 340 + 2, 50)

    if start_practice:
      if return_button_P.draw(screen):
        question_answered = False
        question_loaded = False
        start_practice = False
      if restartStreak_button.draw(screen):
        correct_answers = 0
        wrong_answers = 0
        streak = 0
        question_loaded = False

  elif story_started and story_finished: #DEV_MODE_ON:
    #TEMPORARY TO DO this is the ending outro for when the player finishes the demo, change it in the future
    if outro_page == 1 and death_fade.fade():
        screen.blit(title_img, (SCREEN_WIDTH // 2 - 120, 100))
        screen.blit(book_img, (SCREEN_WIDTH // 2 - 50, 250))
        screen.blit(correct_img, (SCREEN_WIDTH // 2 - 50, 310))
        screen.blit(wrong_img, (SCREEN_WIDTH // 2 - 50, 370))
        screen.blit(streak_img_story, (SCREEN_WIDTH // 2 - 50, 430))
        screen.blit(pygame.image.load(f'data/img/Entity/player/1/death/0.png').convert_alpha(), (SCREEN_WIDTH // 2 - 50, 490))
        draw_text(str(NOTEBOOKS_COLLECTED), font, 'LIGHT BLUE', SCREEN_WIDTH // 2, 250, 50)
        draw_text(str(correct_answers_story), font, 'GREEN', SCREEN_WIDTH // 2, 310, 50)
        draw_text(str(wrong_answers_story), font, 'RED', SCREEN_WIDTH // 2, 370, 50)
        draw_text(str(max_streak_story), font, 'PURPLE', SCREEN_WIDTH // 2, 430, 50)
        draw_text(str(death_counter), font, 'DARK GREY', SCREEN_WIDTH // 2, 490, 50)
        if credits_button.draw(screen):
          death_fade.fade_counter = 0
          outro_page = 2

    elif outro_page == 2:
      screen.blit(title_img, (SCREEN_WIDTH // 2 - 120, 100))
      screen.fill((64,64,64))
      #titulky/credits
      draw_text('TVŮRCE HRY', font, 'WHITE', SCREEN_WIDTH // 2, 150, 0)
      draw_text('Jan Buriánek', font, 'WHITE', SCREEN_WIDTH // 2, 200, 0)

      draw_text('SPECIÁLNÍ PODĚKOVÁNÍ', font, 'WHITE', SCREEN_WIDTH // 2, 300, 0)
      draw_text('Marku Havlíčkovi a Valerii Hrubé', font, 'WHITE', SCREEN_WIDTH // 2, 350, 0)
      draw_text('...za poskytnutí hudby pro hru', medium_font, 'WHITE', SCREEN_WIDTH // 2, 400, 0)

      draw_text('2025', medium_font, 'WHITE', SCREEN_WIDTH // 2, 550, 0)


      draw_warped_text(screen, 'Tato hra vznikla jako součást seminární práce na téma Matematické Hry v roce 2025 na Gymnáziu Teplice', 'WHITE', screen.get_rect(), font)
      if credits_button.draw(screen):
        menu = False
        save_data['death_counter'] = death_counter
        save_data['NOTEBOOKS_COLLECTED'] = NOTEBOOKS_COLLECTED
        save_data['notebook_collected_temp'] = notebook_collected_temp
        save_data['question_window'] = question_window
        save_data['question_loaded'] = question_loaded
        save_data['question_params'] = question_params
        save_data['tempList'] = tempList
        save_data['question_answered'] = question_answered
        save_data['correct_answers_story'] = correct_answers_story
        save_data['wrong_answers_story'] = wrong_answers_story
        save_data['max_streak_story'] = max_streak_story
        save_data['streak_story'] = streak_story
        save_data['max_streak'] = max_streak
        save_data['upgradeMagicCollision'] = upgradeMagicCollision
        world_data = reset_level()
        start_game = False
        DEV_MODE_ON = False

  else:

    #draw background
    draw_bg()
    #draw world map
    world.draw()

    for enemy in enemy_group:
      enemy.ai()
      enemy.update()
      enemy.draw()

    #update and draw groups
    projectile_group.update()
    item_drops_group.update()
    book_group.update()
    exit_group.update()
    projectile_group.draw(screen)
    item_drops_group.draw(screen)
    book_group.draw(screen)
    if notebook_collected_temp:
      exit_group.draw(screen)
    
    #creates the player, calls the functions of player LAST SO ITS ON TOP OF THE OTHER STUFF
    player.update()
    player.draw()

    #draw foreground on certain stages
    if stage == 4:
      draw_fg()

    #menu ingame
    surfaceL = pygame.Surface((800,40), pygame.SRCALPHA)
    if stage == 1:
      surfaceL.fill((64,64,64))
    elif stage == 2:
      surfaceL.fill((0,76,66))
    elif stage == 3:
      surfaceL.fill((96,71,35))
    elif stage == 4:
      surfaceL.fill((170,211,230))
    elif stage == 5:
      surfaceL.fill((64,64,64))
    screen.blit(surfaceL, (0,0))
    #show health
    health_bar.draw(player.health)
    #draw_text(f'Zdraví', small_font, 'WHITE', 9, 4, 150)
    #show magic
    for x in range(player.magic):
      screen.blit(projectile_img, (775 - (x * 10), 12))
    #draw_text('Magie', small_font, 'WHITE', 713, 0, -1)
    #show level
    levelT = level % 5
    if levelT == 0:
      levelT = 5
    draw_text(f'{stage} - {levelT}', font, 'WHITE', 0, -3, 800)

    if level == 1:
      #tutorial1 = screen.blit(pygame.transform.scale(tutorial1_img, (int(tutorial1_img.get_width() * 2), int(tutorial1_img.get_height() * 2))), (200, 450))
      tutorial1 = screen.blit(tutorial1_img, (250, 450))
      tutorial2 = screen.blit(tutorial2_img, (300, 100))
    elif level == 2:
      tutorial3 = screen.blit(tutorial3_img, (50, 200))
      tutorial4 = screen.blit(tutorial4_img, (550, 200))

    #show intro
    if start_intro == True:
      if start_fade.fade():
        start_intro = False
        start_fade.fade_counter = 0

    #update player actions
    if player.alive:
      #shoot projectiles
      if shoot:
        player.shoot('player')
      if player.move_left or player.move_right:
        player.update_action(1) #move
      else:
        player.update_action(0) #idle
      level_complete, question_activation = player.move(move_left, move_right, move_up, move_down)
      if level_complete:
        start_intro = True
        notebook_collected_temp = False
        level += 1
        if level <= 5:
          stage = 1
        elif level <= 10:
          stage = 2
        elif level <= 15:
          stage = 3
        elif level <= 20:
          stage = 4
        elif level <= 25:
          stage = 5
        #print(stage, 'STAGE')
        save_data['level'] = level
        save_data['stage'] = stage
        save_data['death_counter'] = death_counter
        save_data['NOTEBOOKS_COLLECTED'] = NOTEBOOKS_COLLECTED
        save_data['notebook_collected_temp'] = notebook_collected_temp
        save_data['question_window'] = question_window
        save_data['question_loaded'] = question_loaded
        save_data['question_params'] = question_params
        save_data['tempList'] = tempList
        save_data['question_answered'] = question_answered
        save_data['correct_answers_story'] = correct_answers_story
        save_data['wrong_answers_story'] = wrong_answers_story
        save_data['max_streak_story'] = max_streak_story
        save_data['streak_story'] = streak_story
        save_data['max_streak'] = max_streak
        world_data = reset_level()
        if level <= MAX_LEVELS:
          with open(f'data/level/level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';') #the tutorial uses , as the delimiter, idk why its this here but oh well
            for x, row in enumerate(reader):
              for y, tile in enumerate(row):
                world_data[x][y] = int(tile) #int cuz it gives back string
          world = World()
          player, health_bar = world.process_data(world_data)
        else:
          save_data['story_finished'] = story_finished = True
      if question_activation:
        question_type, question, option0, option1, option2, correct_answer = questions.questions()
        question_window = True
        #pygame.mixer.music.pause()
        #question_music.play(-1, 0, 0)

    else:
      player.update_action(2)
      if death_fade.fade():
        screen.blit(game_over_img, (SCREEN_WIDTH // 2 - 120, 100))
        if respawn_button.draw(screen):
          death_counter += 1
          death_fade.fade_counter = 0
          start_intro = True
          world_data = reset_level()
          with open(f'data/level/level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';') #the tutorial uses , as the delimiter, idk why its this here but oh well
            for x, row in enumerate(reader):
              for y, tile in enumerate(row):
                world_data[x][y] = int(tile) #int cuz it gives back string
          world = World()
          player, health_bar = world.process_data(world_data)

  for event in pygame.event.get():
    #quit game
    if event.type == pygame.QUIT:
      run = False

    # if pressed keys
    if start_game:
      if event.type == pygame.KEYDOWN:
          if player.alive:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
              player.move_left = True
              player.move_right = player.move_up = player.move_down = False
              player.last_move = 'left'
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
              player.move_right = True
              player.move_left = player.move_up = player.move_down = False
              player.last_move = 'right'
            if event.key == pygame.K_w or event.key == pygame.K_UP:
              player.move_up = True
              player.move_left = player.move_right = player.move_down = False
              player.last_move = 'up'
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
              player.move_down = True
              player.move_left = player.move_right = player.move_up = False
              player.last_move = 'down'
            if event.key == pygame.K_SPACE:
              shoot = True
            if event.key == pygame.K_ESCAPE:
              if menu:
                menu = False
                #print('menu on screen')
              else:
                menu = True
                #print('menu DOWN')

      #if letting go of keys
      if event.type == pygame.KEYUP:
          if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            player.move_left = False
          if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            player.move_right = False
          if event.key == pygame.K_w or event.key == pygame.K_UP:
            player.move_up = False
          if event.key == pygame.K_s or event.key == pygame.K_DOWN:
            player.move_down = False
          if event.key == pygame.K_SPACE:
            shoot = False

  pygame.display.update()

save_data['story_started'] = story_started
save_data['level'] = level
save_data['stage'] = stage
save_data['death_counter'] = death_counter
save_data['NOTEBOOKS_COLLECTED'] = NOTEBOOKS_COLLECTED
save_data['notebook_collected_temp'] = notebook_collected_temp
save_data['question_window'] = question_window
save_data['question_loaded'] = question_loaded
save_data['question_params'] = question_params
save_data['tempList'] = tempList
save_data['question_answered'] = question_answered
save_data['correct_answers_story'] = correct_answers_story
save_data['wrong_answers_story'] = wrong_answers_story
save_data['max_streak_story'] = max_streak_story
save_data['streak_story'] = streak_story
save_data['max_streak'] = max_streak
save_data['upgradeMagicCollision'] = upgradeMagicCollision

with open('data/save_file.json', 'w') as save_file:
  json.dump(save_data, save_file)

pygame.quit()
