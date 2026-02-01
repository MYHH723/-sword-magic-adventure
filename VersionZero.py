from random import *



def Menu():
    print('Welcome to the world with Sword and Magic')
    print('\n')
    print('Play : ', end = '')
    UserInput = input()
    while True:
        if UserInput.upper() in ['YES','CONTINUE','PLAY','START']:
            return True
        elif UserInput.upper() in ['NO','QUIT','END']:
            return False
        else:
            print('Sorry, please input a valid answer')
            print('Play : ', end = '')
            UserInput = input()

class Player():

     def __init__(self, Name):
               self.Name = Name
               self.__Health = 100
               self.__Alive = True
               self.__ATT = 10
               self.__Money = 0
     def CheckAlive(self):
          if self.__Health <= 0:
               self.__Alive = False
          if self.__Alive:
               return True
          else:
               print('SLAIN')
               return False
     def GetHealth(self):
          return self.__Health
     def SetHealth(self, value):
          self.__Health = self.__Health + value
     def GetAtt(self):
          return self.__ATT
     def SetAtt(self, value):
          self.__ATT = self.__ATT + value
     def Move(self):
          print('Which position you want to move?')
          print('Move : ', end = '')
          UserMovement = input()
          while True:
               if UserMovement.lower() in ['left','right','up','down']:
                    return UserMovement
               else:
                    print('Please enter a valid move')
                    print('Move : ', end = '')
                    UserMovement = input()
     def SetMoney(self, value):
          self.__Money = self.__Money + value
     def GetMoney(self):
          return self.__Money


class Trap():
     def __init__(self):
          self.Harm = randint(-100,-1)
     def Damage(self, player):
          player.SetHealth(self.Harm)
          trap_sounds = [
          "*CRUNCH!* A hidden trap snaps beneath your feet!",
          "*SNAP!* You hear the sharp crack of metal — a trap has sprung!",
          "*WHOOSH!* Arrows burst from the walls — it’s a trap!",
          "*CLICK!* The ground shifts beneath you… too late to escape!",
          "*THUD!* Pain surges through you as the trap strikes!",
          "*SIZZLE!* A burst of poison gas fills the air around you!",
          "*CLANG!* Iron spikes shoot up from the ground!"
          ]

          print(choice(trap_sounds))


class Merchant():
     def __init__(self):
          self.__item = {'Sword' : [randint(10,30), 15], 'Potion' : [5, 5]}
     def Sale(self, player):
          print("Hey young worrier! Don't you want to buy some equipment for the journey?")
          print("Sword : 15 coins")
          print("Potion : 5 coins")
          Purchase = input()
          while True:
               if Purchase.lower() in ['buy', 'yes']:
                    Purchase = True
                    print('Ah, splendid choice, my good sir! May fortune smile'
                          'upon your purchase — finest quality in all the lands,'
                          'I assure you.')
                    break
               elif Purchase.lower() in ['no', 'not buy']:
                    Purchase = False
                    print('Ah, I see, good sir. No matter — perhaps another time,'
                          'when the winds of fortune blow differently.'
                          'My stall shall ever be open should you change your mind.')
                    break
               else:
                    print('( Politely, with a humble tone )')
                    print('My apologies, good sir. I fear I did not'
                         'quite catch your words. Would you be so kind as to repeat what you said?')
                    Purchase = input()
          if Purchase:
               print('(Leaning forward across the wooden counter, voice low and inviting)')
               print('So then, traveler — what shall it be? A sword to strike down your'
                     'foes… or a potion to heal your wounds and bend fate to your favor?')
               choice = input()
               while True:
                    if choice.lower() in ['sword', 'potion']:
                         cost = self.__item[choice.capitalize()][1]
                         effect = self.__item[choice.capitalize()][0]
                    
                         if player.GetMoney() < cost:
                              print(f"(Merchant frowns slightly)\n Alas, you have only {player.GetMoney()} coins."
                                   f"You cannot afford the {choice}.")
                              return False

                         # Apply item effects
                         if choice == 'sword':
                              player.SetAtt(effect)
                              player.SetMoney(-cost)
                              print('(Bows slightly, a pleased grin spreading across his face)')
                              print(f"Ah, splendid! My thanks, good traveler. You’ve chosen a fine sword —"
                                   "balanced, sharp, and true. May it serve you well in all your battles ahead!")
                              break
                         elif choice == 'potion':
                              player.SetHealth(effect)
                              player.SetMoney(-cost)
                              print('(Bows slightly, smiling warmly)')
                              print(f"Ah, excellent choice, traveler! My thanks for your purchase." 
                                   "May this potion grant you strength, courage, or "
                                   "whatever boon your heart desires. Use it wisely on your journeys ahead!")
                              break
                    else:
                         print('(Merchant blinks in confusion, tilting his head slightly)')
                         print('My apologies, traveler… I fear I did not quite catch your words.'
                              ' Would you kindly repeat — was it a sword you seek… or a potion?')
                         choice = input()
          else:
               return Purchase

#Change the main program
#Makesure the Marchent class can run perfectly
#Update the trap class
#Done by 2025/11/1

#2025/11/1 Start to develop the rooms
#Develop thr rooms might be difficult now so I will develop mob class now

class Mob():

     def __init__(self):
          self.MobDic = {'Goblin Raider': [15, 15], 'Skeleton Warrior' : [20, 10], 'Dark Wolf' : [10 , 20]}
          self.MobName = choice(list(self.MobDic.keys()))
          self.MobHp = self.MobDic[self.MobName][0]
          self.MobATT = self.MobDic[self.MobName][1]
     def MobAttack(self,player):
          print(f"A {self.MobName} appears! It snarls and lunges toward you!")

          if player.GetAtt() > self.MobHp:
               kill_lines = [
               "You have slain the beast! The dungeon grows quieter...",
               "The mob collapses. Victory is yours!",
               "With a final blow, you defeat your enemy!",
               "The creature lets out a last cry and falls — you’ve won!",
               "You strike true! The monster lies defeated at your feet."
               ]

               print(choice(kill_lines))
          else:
               hurt_lines = [
               "The creature’s claws slash across your arm — you feel the sting of pain!",
               "You stumble back as the mob lands a solid hit!",
               "A sharp blow catches you off guard — your health drops!",
               "The monster snarls and strikes — you take damage!",
               "You feel the force of the attack crash into you — it hurts!"
               ]

               print(choice(hurt_lines))

               player.SetHealth(self.MobATT * -1)


# Today Mob class is finished
# Work on rooms next time

class Room(Merchant, Trap, Mob):

     def __init__(self):
          self.RoomType = ['Merchant_Room', 'Mob_Room', 'Trap_Room', 'Safe_Room']
          self.RoomName = choice(self.RoomType)
          Merchant.__init__(self)
          Trap.__init__(self)
          Mob.__init__(self)

     def Enter(self, player):

          print(f"You enter the {self.RoomName}... ")

          if self.RoomName == 'Merchant_Room':
               self.Sale(player)
          elif self.RoomName == 'Mob_Room':
               self.MobAttack(player)
          elif self.RoomName == 'Trap_Room':
               self.Damage(player)
          elif self.RoomName == 'Safe_Room':

               print('The room feels calm and safe... you take a moment to rest.')

#Develop the main program
#Ask for player's name
#Ask for plyer's next step

if __name__ == "__main__":
     Alive = True
     Win = False
     s = Menu()
     if s:
          p1 = Player('p1')
          Count = 0
          while Alive and Count <= 18:
               ThisRoom = Room()
               ThisRoom.Enter(p1)
               Alive = p1.CheckAlive()
               print(f"Name: {p1.Name} | HP: {p1.GetHealth()} | ATT: {p1.GetAtt()} | Coins: {p1.GetMoney()}")
               Count += 1
          if Alive:
               print('YOU WIN!!!!')
          else:
               print('FAIL!!!!')



     print(f"{'=' * 10} END GAME {'=' * 10}")