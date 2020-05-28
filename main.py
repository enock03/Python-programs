from classes.game import Person, Bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# Create Black Magic
fire = Spell("Fire", 10, 600, "black")
thunder = Spell("Thunder", 10, 600, "black")
blizzard = Spell("Blizzard", 10, 600, "black")
meteor = Spell("Meteor", 20, 1200, "black")
quake = Spell("Quake", 14, 800, "black")

# Create White Magic
cure = Spell("Cure", 12, 620, "white")
cura = Spell("Cura", 18, 1500, "white")

# Create Healing Items
potion = Item("Potion", "potion", "Heals 250 HP.", 250)
hi_potion = Item("Hi-Potion", "potion", "Heals 500 HP.", 500)
super_potion = Item("Super Potion", "potion", "Heals 1500 HP.", 1500)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member.", 9999)
mega_elixir = Item("Mega Elixir", "elixir", "Fully restores party's HP/MP.", 9999)

# Create Attack Items
bomb = Item("Bomb", "harm", "Deals 500 damage.", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]

enemy_spells = [fire, meteor, cure]

player_items = [{"item": potion, "quantity": 5}, {"item": hi_potion, "quantity": 3}, {"item": super_potion, "quantity": 2},
                {"item": elixir, "quantity": 1}, {"item": mega_elixir, "quantity": 1}, {"item": bomb, "quantity": 3}]

# Instantiate People
player1 = Person("Valos  ", 3260, 62, 142, 34, player_spells, player_items)
player2 = Person("Xandria", 4160, 75, 188, 34, player_spells, player_items)
player3 = Person("Felix  ", 3089, 45, 174, 34, player_spells, player_items)

enemy1 = Person("Imp    ", 1250, 130, 120, 15, enemy_spells, [])
enemy2 = Person("Cthulhu", 9999, 520, 324, 25, enemy_spells, [])
enemy3 = Person("Imp    ", 1250, 130, 120, 15, enemy_spells, [])

# Players list
players = [player1, player2, player3]

# Enemies list
enemies = [enemy1, enemy2, enemy3]

running = True      # Infinite loop for battle

# Check if battle is over
defeated_enemies = 0
defeated_players = 0

print(Bcolors.FAIL + "\n" + Bcolors.BOLD + "AN ENEMY ATTACKS!" + Bcolors.ENDC)

while running:
    print("\n")
    print("======================")
    print("\n")
    print("NAME                    HP                                      MP")

    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        not_valid = True        # Infinite loop to check input validation
        target_val = True        # Infinite loop for target validation

        while not_valid:
            player.choose_action()
            choice = input("     Choose action: ")
            try:
                choice = int(choice) - 1
            except:
                print("\nInvalid input. Only numbers are accepted.")
                continue
            if choice < 0 or choice > 2:
                print("\nInvalid input. You must select a valid action.")
                continue

            if choice == 0:
                while target_val:
                    n = 0 - 1
                    for enemy in enemies:
                        n += 1

                    dmg = player.generate_damage()

                    enemy = player.choose_target(enemies)

                    if enemy < -1 or enemy > n:
                        print("\nInvalid input. You must select a valid enemy.")
                        continue

                    if enemy == -1:
                        break

                    enemies[enemy].take_damage(dmg)
                    print("\n" + player.name.replace(" ", "") + " attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg,
                          "points of damage." + "\n")

                    if enemies[enemy].get_hp() == 0:
                        print(Bcolors.FAIL + enemies[enemy].name.replace(" ", "") + " has died." + Bcolors.ENDC)
                        defeated_enemies += 1
                        del enemies[enemy]

                        # Check if Player won
                        if defeated_enemies == 3:
                            print("\n" + Bcolors.OKGREEN + "You win!" + Bcolors.ENDC)
                            running = False
                            exit()

                    target_val = False
                    not_valid = False
            elif choice == 1:
                while not_valid:
                    player.choose_magic()
                    print("  Your MP:", Bcolors.OKBLUE + str(player.get_mp()) + "/" + str(player.get_max_mp()) + Bcolors.ENDC)
                    magic_choice = input("     Choose magic: (Enter 0 to go back) ")
                    try:
                        magic_choice = int(magic_choice) - 1
                    except:
                        print("\nInvalid input. Only numbers are accepted.")
                        continue
                    if magic_choice < -1 or magic_choice > 5:
                        print("\nInvalid input. You must select a valid spell.")
                        continue

                    elif magic_choice == -1:
                        break

                    spell = player.magic[magic_choice]

                    magic_dmg = spell.generate_damage()

                    current_mp = player.get_mp()

                    if spell.cost > current_mp:
                        print(Bcolors.FAIL + "\nNot enough MP..." + Bcolors.ENDC)
                        continue

                    if spell.type == "white":
                        player.heal(magic_dmg)
                        print(Bcolors.OKBLUE + "\n" + player.name.replace(" ", "") + " use " + spell.name + " and heals for",
                              str(magic_dmg), "HP." + Bcolors.ENDC + "\n")
                        player.reduce_mp(spell.cost)
                        not_valid = False
                    elif spell.type == "black":
                        while target_val:
                            n = 0 - 1
                            for enemy in enemies:
                                n += 1

                            enemy = player.choose_target(enemies)

                            if enemy < -1 or enemy > n:
                                print("\nInvalid input. You must select a valid enemy.")
                                continue

                            if enemy == -1:
                                break

                            enemies[enemy].take_damage(magic_dmg)

                            print(Bcolors.OKBLUE + "\n" + player.name.replace(" ", "") + " use " + spell.name + " and deals",
                                  str(magic_dmg), "points of damage to " + enemies[enemy].name.replace(" ", "") + "." + Bcolors.ENDC +
                                  "\n")
                            player.reduce_mp(spell.cost)

                            if enemies[enemy].get_hp() == 0:
                                print(Bcolors.FAIL + enemies[enemy].name.replace(" ", "") + " has died." + Bcolors.ENDC)
                                defeated_enemies += 1
                                del enemies[enemy]

                                # Check if Player won
                                if defeated_enemies == 3:
                                    print("\n" + Bcolors.OKGREEN + "You win!" + Bcolors.ENDC)
                                    running = False
                                    exit()

                            target_val = False
                            not_valid = False
            elif choice == 2:
                while not_valid:
                    player.choose_item()
                    item_choice = input("     Choose item: (Enter 0 to go back) ")
                    try:
                        item_choice = int(item_choice) - 1
                    except:
                        print("\nInvalid input. Only numbers are accepted.")
                        continue
                    if item_choice < -1 or item_choice > 5:
                        print("\nInvalid input. You must select a valid item.")
                        continue

                    elif item_choice == -1:
                        break

                    item = player.items[item_choice]["item"]

                    if player.items[item_choice]["quantity"] == 0:
                        print(Bcolors.FAIL + "\n" + "None " + item.name + " left..." + Bcolors.ENDC)
                        continue

                    player.items[item_choice]["quantity"] -= 1

                    if item.type == "potion":
                        player.heal(item.prop)
                        print(Bcolors.OKGREEN + "\n" + player.name.replace(" ", "") + " use " + item.name + " and heals for",
                              str(item.prop), "HP.", Bcolors.ENDC + "\n")
                        not_valid = False
                    elif item.type == "elixir":
                        if item.name == "Mega Elixir":
                            for i in players:
                                i.hp = i.max_hp
                                i.mp = i.max_mp
                            print(Bcolors.OKGREEN + "\n" + player.name.replace(" ", "") + " use " + item.name +
                                  " and fully restores party's HP/MP." + Bcolors.ENDC + "\n")
                        else:
                            player.hp = player.max_hp
                            player.mp = player.max_mp
                            print(Bcolors.OKGREEN + "\n" + player.name.replace(" ", "") + " use " + item.name +
                                  " and fully restores HP/MP." + Bcolors.ENDC + "\n")
                        not_valid = False
                    elif item.type == "harm":
                        while target_val:
                            n = 0 - 1
                            for enemy in enemies:
                                n += 1

                            enemy = player.choose_target(enemies)

                            if enemy < -1 or enemy > n:
                                print("\nInvalid input. You must select a valid enemy.")
                                continue

                            if enemy == -1:
                                break

                            enemies[enemy].take_damage(item.prop)

                            print(Bcolors.OKGREEN + "\n" + player.name.replace(" ", "") + " use " + item.name + " and deals",
                                  str(item.prop), "points of damage to " + enemies[enemy].name.replace(" ", "") + "." + "\n" +
                                  Bcolors.ENDC)

                            if enemies[enemy].get_hp() == 0:
                                print(Bcolors.FAIL + enemies[enemy].name.replace(" ", "") + " has died." + Bcolors.ENDC)
                                defeated_enemies += 1
                                del enemies[enemy]

                                # Check if Player won
                                if defeated_enemies == 3:
                                    print("\n" + Bcolors.OKGREEN + "You win!" + Bcolors.ENDC)
                                    running = False
                                    exit()

                            target_val = False
                            not_valid = False

    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            # Choose attack
            target = random.randrange(len(players))
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(Bcolors.FAIL + enemy.name.replace(" ", "") + " attacks", players[target].name.replace(" ", "") + " for",
                  enemy_dmg, "points of damage." + Bcolors.ENDC)

            if players[target].get_hp() == 0:
                print(Bcolors.FAIL + players[target].name.replace(" ", "") + " has died." + Bcolors.ENDC)
                for player in players:
                    if player.get_hp() == 0:
                        defeated_players += 1
                del players[target]

                # Check if Enemy won
                if defeated_players == 3:
                    print("\n" + Bcolors.FAIL + "Your enemies have defeated you!" + Bcolors.ENDC)
                    running = False
                    exit()

        elif enemy_choice == 1:
            # Choose magic
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(Bcolors.FAIL + enemy.name.replace(" ", "") + " use " + Bcolors.OKBLUE + spell.name + Bcolors.ENDC +
                      Bcolors.FAIL + " and heals for", str(magic_dmg), "HP." + Bcolors.ENDC)
            elif spell.type == "black":
                target = random.randrange(len(players))

                players[target].take_damage(magic_dmg)

                print(Bcolors.FAIL + enemy.name.replace(" ", "") + " use " + Bcolors.OKBLUE + spell.name + Bcolors.ENDC +
                      Bcolors.FAIL + " and deals", str(magic_dmg), "points of damage to " + players[target].name.replace(" ", "") +
                      "." + Bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(Bcolors.FAIL + players[target].name.replace(" ", "") + " has died." + Bcolors.ENDC)
                    for player in players:
                        if player.get_hp() == 0:
                            defeated_players += 1
                    del players[target]

                    # Check if Enemy won
                    if defeated_players == 3:
                        print("\n" + Bcolors.FAIL + "Your enemies have defeated you!" + Bcolors.ENDC)
                        running = False
                        exit()
