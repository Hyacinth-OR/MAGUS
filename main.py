from Cards import *

def initialize():
    doac = Deck("All Cards", [])

    #  Card Effect Initializer
    sdamage = Effect("sdamage", "target", "damage", [])
    empty = Effect("empty","user","null",[])

    # Card Initializer
    fireball = DmgCard("Fireball", "Pyromancy", "Area", sdamage, 5)
    doac.add_card(fireball)
    molten_beam = Card("Molten Beam", "Pyromancy", "Target", empty)
    doac.add_card(molten_beam)

    gun = DmgCard("Gun", "Artificer", "Deals damage.", sdamage, 15)
    doac.add_card(gun)

    throw_rock = DmgCard("Throw Rock", "Basic", "Target", sdamage, 5)
    doac.add_card(throw_rock)
    return doac

def encounter(player):
    hand = player.hand
    enemy = Character("Target Dummy", 20, [], 1)
    fight = Encounter(player, [enemy])
    deck = player.deck
    deck.shuffle()
    hand.smartdraw(deck, "Gun")
    hand.smartdraw(deck, "Throw Rock")

    while(player.currhealth > 0):
        fight.corpseclear()
        if fight.victorycheck() == 1:
            main()
        print("1. Play Card\n2. Check Hand\n3. Check Enemies\n4. End Turn")
        act = input()
        if act == "1":
            hand.show_hand()
            cardtoplay = int(input())
            hand.play(hand.contents[cardtoplay - 1], fight)
        elif act == "2":
            hand.show_hand()
            print()
        elif act == "3":
            fight.checkenemies()
        elif act == "4":
            continue

        elif act == 5:
            break


def main():
    print("Initializing...")
    all_cards = initialize()
    player = Player("Player", 100, all_cards)

    print("Initialized.")
    print("Welcome to Magus!")
    menuchoice = 0
    while menuchoice != 3:
        print("What would you like to do?")
        print("1. View Collection\n2. Enter Testing Environment\n3. Exit")
        menuchoice = input()
        if menuchoice == "1":
            verbose = 0
            while int(verbose) <= 2:
                print("Would you like to display spell information, or just names?\n\t1. Display Spell Info")
                print("\t2. Names Only\n\t3. Exit")
                verbose = input()
                if verbose == "1":
                    all_cards.show_deck_verbose()
                elif verbose == "2":
                    all_cards.show_deck()

        if menuchoice == "2":
            print("Welcome to the testing environment!")
            encounter(player)

        else:
            exit()


main()