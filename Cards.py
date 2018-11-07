import random

class Card:

    def __init__(self, name, element, desc, effect,cost):
        self.name = name  # The name of the card
        self.element = element  # The element(s) associated with it
        self.effect = effect  # What it does when activated.
        self.desc = desc
        self.target = self.effect.target
        self.cost = cost

    def info(self):
        print(self.name)
        #print("\tType: ", self.type)
        print("\tElement: ", self.element)
        print("\tEffect: ", self.desc)

    def processEffect(self, encounter):
        if self.effect.name == "sdamage":
            if self.target == "Target":
                encounter.checkenemies()
                enemy = int(input())
                self.target = encounter.enemies[enemy-1]
                self.effect.sdamage(self)
            if self.target == "Area":
                for enemy in encounter.enemies:
                    self.target = enemy
                    self.effect.sdamage(self)




class DmgCard(Card):

    def __init__(self, name, element, desc, effect, damage, cost):
        self.name = name  # The name of the card
        self.element = element  # The element(s) associated with it
        self.effect = effect  # What it does when activated.
        self.desc = desc
        self.target = self.effect.target
        self.cost = cost
        self.damage = damage

    def info(self):
        print(self.name)
        # print("\tType: ", self.type)
        print("\tElement: ", self.element)
        print("\tEffect: ", self.desc)
        print("\tDamage: ", self.damage)
        print("\tMana Cost: ", self.cost)


class Effect:

    def __init__(self,name,  target, type, tags):
        self.name = name
        self.target = target  # What are we gonna be hitting?
        self.type = type  # Damage dealing, shielding, healing, debuffs etc...
        self.tags = tags  # modifiers such as piercing, holy, etc

    def sdamage(self, card):  # deals simple damage with normal armor take into account.
        print(card.target.name, " receives ", card.damage, " damage.")
        card.target.armorharm(card.damage)


class Deck:

    def __init__(self, name, contents):
        self.name = name
        self.contents = contents

    def show_deck(self):
        print("Contents of ", self.name, ":")
        for card in self.contents:
            print(card.name)

    def show_deck_verbose(self):
        for card in self.contents:
            card.info()

    def add_card(self, card):
        new_contents = self.contents
        new_contents.append(card)
        self.contents = new_contents

    def shuffle(self):
        random.shuffle(self.contents)

    def draw(self):
        topdeck = self.contents.pop()
        print("You draw: ", topdeck.name)
        return topdeck

    def smartdraw(self, cardname):
        empty = Effect("empty", "user", "null", [])
        mycard = Card("DEBUG", "YOU'RE NOT SUPPOSED TO SEE THIS", "Area", empty, 0)
        for card in self.contents:
            if cardname == card.name:
                mycard = card
                self.contents.remove(card)
        print("You draw: ", mycard.name)
        return mycard


class Hand:

    def __init__(self, contents):
        self.contents = contents

    def draw(self, Deck, amount):

        for i in range(amount):
            self.contents.append(Deck.draw())

    def smartdraw(self,Deck,card):
        self.contents.append(Deck.smartdraw(card))

    def show_hand(self):
        i = 1
        for card in self.contents:
            print(i, ": ",card.name, "  ")
            i += 1

    def play(self, card, encounter):
        if encounter.player.mana < card.cost:
            print("You don't have enough mana to play that card!")

        else:
            print("You play: ", card.name)
            encounter.player.modMana(card.cost)
            card.processEffect(encounter)
            self.movecardtodeck(card, encounter.player.hand, encounter.player.discard)


    def movecardtodeck(self,card, deckfrom , deckto):
        deckto.contents.append(card)
        for i in deckfrom.contents:
            if i == card:
                deckfrom.contents.remove(card)


class Character:

    def __init__(self,name, health, deck, position):
        self.name = name
        self.maxhealth = health
        self.currhealth = health
        self.deck = deck
        self.hand = Hand([])
        self.armor = 0
        self.player = 0
        self.position = position
        self.mana = 0
        self.discard = Deck("Discard", [])
        self.astral = Deck("Astral Plane", [])

    def armorharm(self, amount): # Subtracts armor from total damage taken
        if self.armor == 0:
            self.takeharm(amount)
        else:
            self.armor = self.armor - amount
            if self.armor < 0:
                amount = self.armor * -1
                self.takeharm(amount)

    def takeharm(self, amount):  # The amount of damage a character takes after all defense calculations
        self.currhealth = self.currhealth - amount

    def mortality_check(self):
        if self.currhealth <= 0:
            print(self.name, " dies.")
            if self.player == 1:
                return 1

    def modMana(self, modifier):
        self.mana = self.mana - modifier;

    def refilldeck(self):
        if len(self.deck.contents) == 0:
            print("Discard shuffled into draw.")
            random.shuffle(self.discard.contents)
            self.deck.contents = self.discard.contents
            self.discard.contents.clear()






class Player(Character):

    def __init__(self, name, health, deck):
        self.name = name
        self.maxhealth = health
        self.currhealth = health
        self.deck = deck
        self.hand = Hand([])
        self.mana = 0;
        self.armor = 0
        self.player = 1
        self.position = 0
        self.discard = Deck("Discard", [])
        self.astral = Deck("Astral Plane", [])


class Encounter:  # Represents a room with the player, and enemies in it.

    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies  # list of enemies in encounter

    def corpseclear(self):  # removes all dead enemies from the board at the top of the turn.
        for enemy in self.enemies:
            if enemy.currhealth <= 0:
                del self.enemies[enemy.position-1]
                print("The corpse of ", enemy.name, " vanishes!")

    def victorycheck(self): # if no bodies remain, the game is over.
        if len(self.enemies) == 0:
            print("You win!")
            print("-----------------------------------\n\n")
            return 1

    def checkenemies(self):
        for enemy in self.enemies:
            print(enemy.position, ": ", self.enemies[enemy.position-1].name, "(",
                  self.enemies[enemy.position-1].currhealth,"/", self.enemies[enemy.position-1].maxhealth, ")")

            print()
    def botmove(self, enemy):
        print(enemy.name, " strikes you with its dummy arms!")
        self.player.takeharm(20)
