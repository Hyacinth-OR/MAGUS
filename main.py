from Cards import *

def initialize():
    doac = Deck("All Cards", [])

    #  Card Effect Initializer
    sdamage = Effect("sdamage", "Target", "damage", [])
    empty = Effect("empty","user","null",[])

    # Card Initializer
    fireball = DmgCard("Fireball", "Pyromancy", "Area", sdamage, 5, 5)
    doac.add_card(fireball)

    molten_beam = DmgCard("Molten Beam", "Pyromancy", "Target", sdamage, 10, 5)
    doac.add_card(molten_beam)

    gun = DmgCard("Gun", "Artificer", "Deals damage.", sdamage, 15, 5)
    doac.add_card(gun)

    throw_rock = DmgCard("Throw Rock", "Basic", "Target", sdamage, 5, 5)
    doac.add_card(throw_rock)



    return doac


def encounter(player):
    hand = player.hand
    enemy = Character("Target Dummy", 25, [], 1)
    enemy2 = Character("Fragile Target Dummy", 5, [], 2)
    enemylist = []
    enemylist.append(enemy)
    enemylist.append(enemy2)
    fight = Encounter(player, enemylist)
    deck = player.deck
    deck.shuffle()
    hand.smartdraw(deck, "Gun")
    player.mana = 10
    while(player.currhealth > 0):
        player.refilldeck()
        print("Cards in deck: ", len(player.deck.contents))
        fight.corpseclear()
        if fight.victorycheck() == 1:
            main()
        print("Mana: ",player.mana, "\t Health: ", player.currhealth)
        print("1. Play Card\n2. Check Hand\n3. Check Enemies\n4. Check Discard\n5. End Turn")
        act = input()
        if act == "0":
            deck.show_deck()

        elif act == "1":
            if len(hand.contents) > 0:
                hand.show_hand()
                cardtoplay = int(input())
                hand.play(hand.contents[cardtoplay - 1], fight)
            else:
                player.refilldeck()

                hand.draw(deck, 1)

        elif act == "2": # Check Hand
            print("Your hand:")
            hand.show_hand()
            print()
        elif act == "3": # Look at enemies
            fight.checkenemies()
        elif act == "4": # See what you've discarded
            player.discard.show_deck()
        elif act == "5": # End Turn
            player.refilldeck()
            if(len(deck.contents)) > 0:
                hand.draw(deck, 1)
            player.mana += 10
            if player.mana >= 10:
                player.mana = 10
            fight.botmove(enemy)
    print("You died, better luck next time!")
    main()





def main():
    print("Initializing...")
    all_cards = initialize()
    demo_deck = Deck("Deck",[all_cards.contents[2],all_cards.contents[3]])
    player = Player("Player", 100, demo_deck)

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
                else:
                    main()

        if menuchoice == "2":
            print("Welcome to the testing environment!")
            encounter(player)

        else:
            exit()


main()
