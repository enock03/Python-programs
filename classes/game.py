import random

class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.max_mp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print("\n     " + Bcolors.BOLD + self.name + Bcolors.BOLD)
        print(Bcolors.UNDERLINE + Bcolors.BOLD + "     ACTIONS:" + Bcolors.ENDC)
        for item in self.actions:
            print("         " + str(i) + ".", item)
            i += 1

    def choose_magic(self):
        i = 1
        print("\n     " + Bcolors.BOLD + self.name + Bcolors.BOLD)
        print(Bcolors.UNDERLINE + Bcolors.OKBLUE + Bcolors.BOLD + "     MAGIC:" + Bcolors.ENDC)
        for spell in self.magic:
            print("         " + str(i) + ".", spell.name, "(cost:", str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print("\n     " + Bcolors.BOLD + self.name + Bcolors.BOLD)
        print(Bcolors.UNDERLINE + Bcolors.OKGREEN + Bcolors.BOLD + "     ITEMS:" + Bcolors.ENDC)
        for item in self.items:
            print("         " + str(i) + ".", item["item"].name + ":", item["item"].description, "(x" +
                  str(item["quantity"]) + ")")
            i += 1

    def choose_target(self, enemies):
        not_valid = True
        while not_valid:
            i = 1
            print("\n     " + Bcolors.BOLD + self.name + Bcolors.BOLD)
            print(Bcolors.UNDERLINE + Bcolors.FAIL + Bcolors.BOLD + "    TARGET:" + Bcolors.ENDC)
            for enemy in enemies:
                if enemy.get_hp() != 0:
                    print("        " + str(i) + ".", enemy.name)
                    i += 1
            choice = input("    Choose target: (Enter 0 to go back) ")
            try:
                choice = int(choice) - 1
            except:
                print("\nInvalid input. Only numbers are accepted.")
                continue
            return choice

    def get_enemy_stats(self):
        hp_bar = ""
        hp_bar_ticks = (self.hp / self.max_hp) * 100 / 2

        while hp_bar_ticks > 0:
            hp_bar += "█"
            hp_bar_ticks -= 1

        while len(hp_bar) < 50:
            hp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.max_hp)
        current_hp = ""

        if len(hp_string) < 9:
            decreased = 9 - len(hp_string)

            while decreased > 0:
                current_hp += " "
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        print("                        __________________________________________________ ")
        print(Bcolors.BOLD + str(self.name) + "      " + current_hp + " |" + Bcolors.FAIL + hp_bar + Bcolors.ENDC + "|")

    def get_stats(self):
        hp_bar = ""
        hp_bar_ticks = (self.hp / self.max_hp) * 100 / 4
        mp_bar = ""
        mp_bar_ticks = (self.mp / self.max_mp) * 100 / 10

        while hp_bar_ticks > 0:
            hp_bar += "█"
            hp_bar_ticks -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        while mp_bar_ticks > 0:
            mp_bar += "█"
            mp_bar_ticks -= 1

        while len(mp_bar) < 10:
            mp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.max_hp)
        current_hp = ""

        if len(hp_string) < 9:
            decreased = 9 - len(hp_string)

            while decreased > 0:
                current_hp += " "
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        mp_string = str(self.mp) + "/" + str(self.max_mp)
        current_mp = ""

        if len(mp_string) < 5:
            decreased = 5 - len(mp_string)

            while decreased > 0:
                current_mp += " "
                decreased -= 1

            current_mp += mp_string
        else:
            current_mp = mp_string

        print("                        _________________________               __________ ")
        print(Bcolors.BOLD + str(self.name) + "      " + current_hp + " |" + Bcolors.OKGREEN + hp_bar + Bcolors.ENDC +
              "|       " + Bcolors.BOLD + current_mp + " |" + Bcolors.OKBLUE + mp_bar + Bcolors.ENDC + "|")

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        pct = self.hp / self.max_hp * 100

        if self.mp < spell.cost or spell.type == "white" and pct > 50:
            return self.choose_enemy_spell()
        else:
            return spell, magic_dmg
