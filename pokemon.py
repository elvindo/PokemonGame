import random
import tkinter as tk

class Pokemon:
    def __init__(self, name, type, max_hp, moves):
        self.name = name
        self.type = type
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.moves = moves

    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0

    def is_knocked_out(self):
        return self.current_hp == 0

    def attack(self, move, target):
        effectiveness = self.calculate_effectiveness(move.type, target.type)
        damage = int(move.power * effectiveness)
        target.take_damage(damage)
        return damage, effectiveness

    def calculate_effectiveness(self, move_type, target_type):
        effectiveness_chart = {
            'fire': {'fire': 0.5, 'water': 0.5, 'grass': 2.0, 'electric': 1.0},
            'water': {'fire': 2.0, 'water': 0.5, 'grass': 0.5, 'electric': 1.0},
            'grass': {'fire': 0.5, 'water': 2.0, 'grass': 0.5, 'electric': 1.0},
            'electric': {'fire': 1.0, 'water': 2.0, 'grass': 0.5, 'electric': 0.5}
        }
        # Default effectiveness for moves not in the chart
        return effectiveness_chart.get(move_type, {}).get(target_type, 1.0)

class Move:
    def __init__(self, name, type, power):
        self.name = name
        self.type = type
        self.power = power

class BattleLog:
    def __init__(self):
        self.log_text = ""

    def add_log(self, log):
        self.log_text += log + "\n"

class BattleSimulator:
    def __init__(self, player, opponent, battle_log):
        self.player_pokemon = player.pokemon
        self.opponent_pokemon = opponent.pokemon
        self.battle_log = battle_log

    def simulate_battle(self):
        while not self.player_pokemon.is_knocked_out() and not self.opponent_pokemon.is_knocked_out():
            player_move = random.choice(self.player_pokemon.moves)
            opponent_move = random.choice(self.opponent_pokemon.moves)

            player_damage, player_effectiveness = self.player_pokemon.attack(player_move, self.opponent_pokemon)
            opponent_damage, opponent_effectiveness = self.opponent_pokemon.attack(opponent_move, self.player_pokemon)

            self.battle_log.add_log(f"{self.player_pokemon.name} using {player_move.name}, dealing {player_damage} damage to {self.opponent_pokemon.name}, "
                                    f"Effectiveness: {player_effectiveness}")
            self.battle_log.add_log(f"{self.opponent_pokemon.name} using {opponent_move.name}, dealing {opponent_damage} damage to {self.player_pokemon.name}, "
                                    f"Effectiveness: {opponent_effectiveness}")

            self.player.check_battle_result()

            if not self.player_pokemon.is_knocked_out() and not self.opponent_pokemon.is_knocked_out():
                # Continue the battle with the next round
                self.opponent_attack()

        if self.player_pokemon.is_knocked_out():
            self.battle_log.add_log(f"{self.player_pokemon.name} is KO'd, {self.opponent_pokemon.name} WINS")
        else:
            self.battle_log.add_log(f"{self.opponent_pokemon.name} is KO'd, {self.player_pokemon.name} WINS")

    def opponent_attack(self):
        # Simulate opponent's attack
        opponent_move = random.choice(self.opponent_pokemon.moves)
        player_damage, player_effectiveness = self.player_pokemon.attack(opponent_move, self.opponent_pokemon)
        self.battle_log.add_log(f"{self.opponent_pokemon.name} using {opponent_move.name}, dealing {player_damage} damage to {self.player_pokemon.name}, "
                                f"Effectiveness: {player_effectiveness}")
        self.player.check_battle_result()

class Player:
    def __init__(self, pokemon, battle_log):
        self.pokemon = pokemon
        self.battle_log = battle_log

    def choose_move(self, move):
        opponent_move = random.choice(self.pokemon.moves)

        if move.type != 'normal':
            # If it's not a normal move, then it's a skill
            self.battle_log.add_log(f"{self.pokemon.name} using {move.name}, dealing {player_damage} damage to {self.opponent_pokemon.name}, "
                                    f"Effectiveness: {player_effectiveness}")
        else:
            player_damage, player_effectiveness = self.pokemon.attack(move, self.opponent_pokemon)
            self.battle_log.add_log(f"{self.pokemon.name} using {move.name}, dealing {player_damage} damage to {self.opponent_pokemon.name}, "
                                    f"Effectiveness: {player_effectiveness}")

        self.check_battle_result()

    def check_battle_result(self):
        if self.pokemon.is_knocked_out():
            self.battle_log.add_log(f"{self.pokemon.name} is KO'd, {self.opponent_pokemon.name} WINS")
        elif self.opponent_pokemon.is_knocked_out():
            self.battle_log.add_log(f"{self.opponent_pokemon.name} is KO'd, {self.pokemon.name} WINS")

class BattleApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Pokemon Battle Simulator")

        self.charizard = Pokemon(name="Charizard", type="fire", max_hp=120, moves=[Move("Flamethrower", "fire", 35)])
        self.blastoise = Pokemon(name="Blastoise", type="water", max_hp=130, moves=[Move("Hydro Pump", "water", 40)])

        self.battle_log = BattleLog()

        # Pilih lawan secara acak, pastikan tidak sama dengan Pokemon pemain
        self.opponent_pokemon = random.choice([p for p in [self.charizard, self.blastoise] if p != self.charizard])

        self.player = Player(self.charizard, self.battle_log)
        self.player.opponent_pokemon = self.opponent_pokemon  # Fix the missing attribute

        self.battle_button = tk.Button(self.master, text="Attack", command=self.attack)
        self.battle_button.pack()

        self.defense_button = tk.Button(self.master, text="Defense", command=self.defense)
        self.defense_button.pack()

        self.skill_button = tk.Button(self.master, text="Skill", command=self.skill)
        self.skill_button.pack()

        self.battle_log_text = tk.Text(self.master, height=10, width=50)
        self.battle_log_text.pack()

    def attack(self):
        move = random.choice(self.player.pokemon.moves)
        self.player.choose_move(move)
        self.update_log()
        self.opponent_attack()

    def defense(self):
        self.battle_log.add_log(f"{self.player.pokemon.name} used Defense. No damage taken.")
        self.update_log()
        self.opponent_attack()

    def skill(self):
        skill_move = Move("Special Skill", "normal", 40)  # Define your special skill move
        self.player.choose_move(skill_move)
        self.update_log()
        self.opponent_attack()

    def opponent_attack(self):
        opponent_move = random.choice(self.opponent_pokemon.moves)
        player_damage, player_effectiveness = self.player.pokemon.attack(opponent_move, self.opponent_pokemon)
        self.battle_log.add_log(f"{self.opponent_pokemon.name} using {opponent_move.name}, dealing {player_damage} damage to {self.player.pokemon.name}, "
                                f"Effectiveness: {player_effectiveness}")
        self.player.check_battle_result()

    def update_log(self):
        self.battle_log_text.delete(1.0, tk.END)
        self.battle_log_text.insert(tk.END, f"{self.player.pokemon.name} HP: {self.player.pokemon.current_hp}\n")
        self.battle_log_text.insert(tk.END, f"{self.opponent_pokemon.name} HP: {self.opponent_pokemon.current_hp}\n")
        self.battle_log_text.insert(tk.END, self.battle_log.log_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = BattleApp(root)
    root.mainloop()