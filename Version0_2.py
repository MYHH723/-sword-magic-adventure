import random
import tkinter as tk
from tkinter import ttk, messagebox
import time

# -------------------------- Game Global Constants Configuration --------------------------
PLAYER_INIT_HEALTH = 100
PLAYER_INIT_ATTACK = 10
MAX_ROOM_COUNT = 18
# Color Configuration (Medieval Style)
COLOR_BG = "#1a1a1a"       # Dark black background
COLOR_TEXT = "#f0e6d2"     # Cream-colored text
COLOR_ACCENT = "#c9a66b"   # Gold accent color
COLOR_DANGER = "#b73225"   # Red for danger
COLOR_SUCCESS = "#4a7a2c"  # Green for success
COLOR_ROOM = "#2d2d2d"     # Room panel background

# -------------------------- Player Class --------------------------
class Player:
    def __init__(self, name: str):
        self.name = name
        self._health = PLAYER_INIT_HEALTH
        self._is_alive = True
        self._attack = PLAYER_INIT_ATTACK
        self._money = 0

    def check_alive(self) -> bool:
        """Check if the player is alive and update survival status"""
        if self._health <= 0:
            self._is_alive = False
        return self._is_alive

    def get_health(self) -> int:
        """Get current health value"""
        return self._health

    def modify_health(self, value: int) -> None:
        """Modify health (can increase or decrease), ensure health doesn't go below 0"""
        self._health = max(0, self._health + value)

    def get_attack(self) -> int:
        """Get current attack power"""
        return self._attack

    def modify_attack(self, value: int) -> None:
        """Modify attack power (can increase or decrease)"""
        self._attack += value

    def modify_money(self, value: int) -> None:
        """Modify gold coins (can increase or decrease), ensure coins don't go below 0"""
        self._money = max(0, self._money + value)

    def get_money(self) -> int:
        """Get current gold coins"""
        return self._money

# -------------------------- Trap Class --------------------------
class Trap:
    TRAP_MESSAGES = [
        "*CRUNCH!* A hidden trap snaps beneath your feet!",
        "*SNAP!* You hear the sharp crack of metal — a trap has sprung!",
        "*WHOOSH!* Arrows burst from the walls — it's a trap!",
        "*CLICK!* The ground shifts beneath you… too late to escape!",
        "*THUD!* Pain surges through you as the trap strikes!",
        "*SIZZLE!* A burst of poison gas fills the air around you!",
        "*CLANG!* Iron spikes shoot up from the ground!"
    ]

    def __init__(self):
        """Initialize trap with random damage (1-100 HP loss)"""
        self.damage = random.randint(1, 100)

    def trigger(self, player: Player) -> str:
        """Trigger the trap, deal damage to player, return trap message"""
        player.modify_health(-self.damage)
        return random.choice(self.TRAP_MESSAGES)

# -------------------------- Merchant Class --------------------------
class Merchant:
    def __init__(self):
        """Initialize merchant's goods: {Name: [Effect Value, Price]}"""
        self.items = {
            'Sword': [random.randint(10, 30), 15],
            'Potion': [5, 5]
        }

    def trade_sword(self, player: Player) -> (bool, str):
        """Trade sword with player, return (trade success status, message)"""
        effect, cost = self.items['Sword']
        if player.get_money() < cost:
            return False, f"Alas, you have only {player.get_money()} coins! A sword costs {cost} coins."
        player.modify_attack(effect)
        player.modify_money(-cost)
        return True, f"Excellent choice! Your attack increases by {effect}!\nYou now have {player.get_attack()} attack power."

    def trade_potion(self, player: Player) -> (bool, str):
        """Trade potion with player, return (trade success status, message)"""
        effect, cost = self.items['Potion']
        if player.get_money() < cost:
            return False, f"Alas, you have only {player.get_money()} coins! A potion costs {cost} coins."
        player.modify_health(effect)
        player.modify_money(-cost)
        return True, f"Wisdom choice! Your health restores by {effect}!\nYou now have {player.get_health()} HP."

# -------------------------- Mob Class --------------------------
class Mob:
    MOB_DATA = {
        'Goblin Raider': [15, 15],
        'Skeleton Warrior': [20, 10],
        'Dark Wolf': [10, 20]
    }

    APPEAR_MESSAGES = [
        "A foul %s emerges from the shadows! It bares its fangs and prepares to strike!",
        "Behold! A %s blocks your path, hunger in its eyes!",
        "A wicked %s has found you! Steel yourself, brave warrior!"
    ]
    COUNTERATTACK_CHOICE = [
        "The %s lunges! Will you stand your ground and COUNTERATTACK?",
        "The %s strikes! Do you parry and counter in return?"
    ]
    SUCCESS_MESSAGES = [
        "Your blade rings true! You counter perfectly — the beast recoils in pain!",
        "A masterful parry! Your counterattack strikes true, the creature staggers!",
        "You outmaneuver the fiend! Your counter lands, and it cannot harm you!"
    ]
    FAIL_MESSAGES = [
        "Your counter misses! The beast overwhelms you — you suffer a grievous blow!",
        "You stumble! Your counter fails, and the enemy’s strike lands with extra fury!",
        "Foolish! Your guard is broken — the attack hits harder than you imagined!"
    ]
    KILL_MESSAGES = [
        "You have slain the beast! The dungeon grows quieter...",
        "The mob collapses. Victory is yours!",
        "With a final blow, you defeat your enemy!",
        "The creature lets out a last cry and falls — you’ve won!",
        "You strike true! The monster lies defeated at your feet."
    ]

    def __init__(self):
        """Initialize random mob with name, health and attack power"""
        self.name = random.choice(list(self.MOB_DATA.keys()))
        self.health = self.MOB_DATA[self.name][0]
        self.attack = self.MOB_DATA[self.name][1]

    def get_appear_msg(self) -> str:
        """Get random mob appearance message"""
        return random.choice(self.APPEAR_MESSAGES) % self.name

    def get_counter_choice_msg(self) -> str:
        """Get random counterattack choice message"""
        return random.choice(self.COUNTERATTACK_CHOICE) % self.name

    def battle(self, player: Player, counter_choice: bool) -> (str, int):
        """Battle with player, return (battle message, damage taken by player)"""
        # One-hit kill check: Player's attack >= Mob's health
        if player.get_attack() >= self.health:
            reward_gold = random.randint(5, 20)
            player.modify_money(reward_gold)
            msg = f"{random.choice(self.KILL_MESSAGES)}\nYou find {reward_gold} gold coins on the corpse!"
            return msg, 0

        if counter_choice:
            # Counterattack success rate: 30% + player's current attack power
            success_rate = 30 + player.get_attack()
            roll = random.randint(1, 100)
            if roll <= success_rate:
                # Successful counterattack: No damage + 5 gold coins reward
                player.modify_money(5)
                msg = f"{random.choice(self.SUCCESS_MESSAGES)}\nYou take NO damage! +5 Gold Coins! Your courage is rewarded!"
                return msg, 0
            else:
                # Failed counterattack: Take base damage + 5% extra damage
                extra_damage = int(self.attack * 0.05)
                total_damage = self.attack + extra_damage
                player.modify_health(-total_damage)
                msg = f"{random.choice(self.FAIL_MESSAGES)}\nThe attack hits hard! You lose {total_damage} HP (+5% extra damage)!"
                return msg, total_damage
        else:
            # No counterattack: Take normal damage
            player.modify_health(-self.attack)
            msg = f"You brace for the impact — the beast’s attack lands!\nYou take {self.attack} damage!"
            return msg, self.attack

# -------------------------- Room Class --------------------------
class Room:
    BASE_ROOM_TYPES = ['Merchant_Room', 'Mob_Room', 'Trap_Room', 'Safe_Room']

    def __init__(self, filter_type: str = None):
        """
        Initialize room with random type (filter specific type if needed)
        :param filter_type: Room type to exclude (prevent consecutive merchant rooms)
        """
        self.available_room_types = [r for r in self.BASE_ROOM_TYPES if r != filter_type]
        self.type = random.choice(self.available_room_types)
        self.merchant = Merchant() if self.type == 'Merchant_Room' else None
        self.trap = Trap() if self.type == 'Trap_Room' else None
        self.mob = Mob() if self.type == 'Mob_Room' else None

    def enter_safe(self, player: Player) -> str:
        """Enter safe room, restore player's health, return safe room message"""
        player.modify_health(5)
        return f"The room feels calm and safe... you take a moment to rest.\nYou restore 5 HP! Current HP: {player.get_health()}"

# -------------------------- Game GUI Main Class --------------------------
class SwordMagicGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sword and Magic - Dungeon Adventure")
        self.root.geometry("800x650")
        self.root.resizable(True, True)  # Enable resizing for fullscreen adaptation
        self.root.configure(bg=COLOR_BG)
        
        # Fullscreen status flag
        self.is_fullscreen = False
        
        # ========== Core: Set sword-shaped cursor (built-in pirate sword) ==========
        self.root.config(cursor="pirate")

        # Game state initialization
        self.player = None
        self.room_count = 0
        self.last_room_type = None
        self.is_alive = True
        self.current_room = None

        # Initialize UI styles
        self.init_styles()
        self.create_start_interface()
        
        # Bind F11 key to toggle fullscreen
        self.root.bind('<F11>', self.toggle_fullscreen)
        # Bind ESC key to exit fullscreen (only works in fullscreen mode)
        self.root.bind('<Escape>', lambda e: self.set_fullscreen(False) if self.is_fullscreen else None)

    def init_styles(self):
        """Initialize ttk styles to fix background color issues"""
        self.style = ttk.Style()
        self.style.theme_use("clam")
        # Configure Frame styles
        self.style.configure("Game.TFrame", background=COLOR_BG)
        self.style.configure("Status.TFrame", background=COLOR_ROOM)
        # Configure Label styles
        self.style.configure("Game.TLabel", background=COLOR_BG, foreground=COLOR_TEXT, font=("Times New Roman", 14))
        self.style.configure("Title.TLabel", background=COLOR_BG, foreground=COLOR_ACCENT, font=("Times New Roman", 40, "bold"))
        self.style.configure("Status.TLabel", background=COLOR_ROOM, foreground=COLOR_TEXT, font=("Times New Roman", 16))
        self.style.configure("StatusAccent.TLabel", background=COLOR_ROOM, foreground=COLOR_ACCENT, font=("Times New Roman", 16, "bold"))
        # Configure Button styles
        self.style.configure("Game.TButton", font=("Times New Roman", 14), padding=10, background=COLOR_ACCENT, foreground=COLOR_BG)
        self.style.configure("Fullscreen.TButton", font=("Times New Roman", 12), padding=5, background=COLOR_ACCENT, foreground=COLOR_BG)

    def toggle_fullscreen(self, event=None):
        """Toggle between fullscreen and windowed mode"""
        self.is_fullscreen = not self.is_fullscreen
        self.set_fullscreen(self.is_fullscreen)
        
    def set_fullscreen(self, fullscreen):
        """Set fullscreen status"""
        self.is_fullscreen = fullscreen
        self.root.attributes('-fullscreen', fullscreen)
        # Remove window border in fullscreen mode, restore in windowed mode
        if fullscreen:
            self.root.overrideredirect(True)
        else:
            self.root.overrideredirect(False)
            self.root.geometry("800x650")  # Restore default window size

    # -------------------------- UI Creation --------------------------
    def create_start_interface(self):
        """Create game start interface"""
        # Clear all widgets in current window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Fullscreen button - always display at top-right corner
        fullscreen_btn = ttk.Button(
            self.root, 
            text="⛶ Fullscreen (F11)", 
            command=self.toggle_fullscreen,
            style="Fullscreen.TButton"
        )
        fullscreen_btn.place(relx=0.98, rely=0.02, anchor='ne')
        
        # Game title
        title_label = ttk.Label(self.root, text="SWORD AND MAGIC", style="Title.TLabel")
        title_label.pack(pady=80)
        # Start prompt
        play_label = ttk.Label(self.root, text="Start Your Dungeon Adventure?", style="Game.TLabel")
        play_label.pack(pady=20)
        # Button frame
        btn_frame = ttk.Frame(self.root, style="Game.TFrame")
        btn_frame.pack(pady=30)
        # Start/Quit buttons
        ttk.Button(btn_frame, text="PLAY", command=self.enter_name_interface, style="Game.TButton").grid(row=0, column=0, padx=20)
        ttk.Button(btn_frame, text="QUIT", command=self.root.quit, style="Game.TButton").grid(row=0, column=1, padx=20)

    def enter_name_interface(self):
        """Create player name input interface"""
        # Clear all widgets in current window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Fullscreen button
        fullscreen_btn = ttk.Button(
            self.root, 
            text="⛶ Fullscreen (F11)", 
            command=self.toggle_fullscreen,
            style="Fullscreen.TButton"
        )
        fullscreen_btn.place(relx=0.98, rely=0.02, anchor='ne')
        
        # Interface title
        title_label = ttk.Label(self.root, text="Enter Your Warrior's Name", style="Title.TLabel")
        title_label.config(font=("Times New Roman", 28, "bold"))
        title_label.pack(pady=60)
        # Input frame
        input_frame = ttk.Frame(self.root, style="Game.TFrame")
        input_frame.pack(pady=30)
        # Name input box (default name: Hero)
        self.name_var = tk.StringVar(value="Hero")
        name_entry = ttk.Entry(input_frame, textvariable=self.name_var, font=("Times New Roman", 16), width=25)
        name_entry.grid(row=0, column=0, padx=10)
        name_entry.focus()
        # Confirm button
        ttk.Button(self.root, text="CONFIRM", command=self.init_game, style="Game.TButton").pack(pady=40)

    def create_game_interface(self):
        """Create main game interface"""
        # Clear all widgets in current window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Fullscreen button
        fullscreen_btn = ttk.Button(
            self.root, 
            text="⛶ Fullscreen (F11)", 
            command=self.toggle_fullscreen,
            style="Fullscreen.TButton"
        )
        fullscreen_btn.place(relx=0.98, rely=0.02, anchor='ne')
        
        # Top status bar - use relative layout for fullscreen adaptation
        status_frame = ttk.Frame(self.root, style="Status.TFrame", height=80)
        status_frame.pack(fill=tk.X, padx=20, pady=10)
        status_frame.propagate(False)
        
        # Player info - use grid weights to adapt to different screen sizes
        status_frame.grid_columnconfigure(0, weight=1)
        status_frame.grid_columnconfigure(1, weight=1)
        status_frame.grid_columnconfigure(2, weight=1)
        status_frame.grid_columnconfigure(3, weight=1)
        status_frame.grid_columnconfigure(4, weight=1)
        
        # Player info display
        ttk.Label(status_frame, text=f"Warrior: {self.player.name}", style="StatusAccent.TLabel").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.hp_label = ttk.Label(status_frame, text=f"HP: {self.player.get_health()}/{PLAYER_INIT_HEALTH}", style="Status.TLabel")
        self.hp_label.grid(row=0, column=1, padx=10, pady=10)
        self.att_label = ttk.Label(status_frame, text=f"ATT: {self.player.get_attack()}", style="Status.TLabel")
        self.att_label.grid(row=0, column=2, padx=10, pady=10)
        self.money_label = ttk.Label(status_frame, text=f"Coins: {self.player.get_money()}", style="StatusAccent.TLabel")
        self.money_label.grid(row=0, column=3, padx=10, pady=10)
        self.room_label = ttk.Label(status_frame, text=f"Rooms: {self.room_count}/{MAX_ROOM_COUNT}", style="Status.TLabel")
        self.room_label.grid(row=0, column=4, padx=10, pady=10, sticky=tk.E)
        
        # Middle content area - fill remaining space
        content_frame = ttk.Frame(self.root, style="Game.TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Game log text box - adapt to fullscreen size
        self.log_text = tk.Text(content_frame, font=("Times New Roman", 14), bg=COLOR_BG, fg=COLOR_TEXT,
                                padx=15, pady=15, wrap=tk.WORD, state=tk.DISABLED, relief=tk.FLAT)
        self.log_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Scrollbar for log text box
        scrollbar = ttk.Scrollbar(content_frame, command=self.log_text.yview)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        # Bottom button bar
        self.btn_frame = ttk.Frame(self.root, style="Game.TFrame")
        self.btn_frame.pack(fill=tk.X, padx=20, pady=10)

    # -------------------------- Game Logic --------------------------
    def init_game(self):
        """Initialize game data and start adventure"""
        player_name = self.name_var.get().strip() or "Hero"
        self.player = Player(player_name)
        self.room_count = 0
        self.last_room_type = None
        self.is_alive = True
        self.create_game_interface()
        self.add_log(f"=== Welcome, {self.player.name}! Your dungeon journey begins! ===")
        self.add_log(f"Initial Stats - HP: {self.player.get_health()} | ATT: {self.player.get_attack()} | Coins: {self.player.get_money()}")
        self.root.after(1000, self.explore_room)

    def explore_room(self):
        """Explore next room, game core loop"""
        if not self.is_alive or self.room_count >= MAX_ROOM_COUNT:
            self.game_over()
            return
        # Filter merchant room to prevent consecutive appearances
        filter_type = 'Merchant_Room' if self.last_room_type == 'Merchant_Room' else None
        self.current_room = Room(filter_type)
        self.last_room_type = self.current_room.type
        self.room_count += 1
        # Update status bar
        self.update_status()
        self.add_log(f"\n=== You enter the {self.current_room.type}... ===")
        # Handle different room types
        if self.current_room.type == 'Merchant_Room':
            self.merchant_room()
        elif self.current_room.type == 'Mob_Room':
            self.mob_room()
        elif self.current_room.type == 'Trap_Room':
            self.trap_room()
        elif self.current_room.type == 'Safe_Room':
            self.safe_room()

    def merchant_room(self):
        """Merchant room interaction logic"""
        self.add_log("Hey young warrior! Don't you want to buy some equipment for the journey?")
        self.add_log(f"Sword : 15 coins (Increases attack power) | Potion : 5 coins (Restores health)")
        self.clear_btns()
        ttk.Button(self.btn_frame, text="Buy Sword", command=lambda: self.buy_item("sword"), style="Game.TButton").grid(row=0, column=0, padx=10)
        ttk.Button(self.btn_frame, text="Buy Potion", command=lambda: self.buy_item("potion"), style="Game.TButton").grid(row=0, column=1, padx=10)
        ttk.Button(self.btn_frame, text="Leave", command=self.continue_explore, style="Game.TButton").grid(row=0, column=2, padx=10)

    def buy_item(self, item_type):
        """Handle item purchase logic"""
        if item_type == "sword":
            success, msg = self.current_room.merchant.trade_sword(self.player)
        else:
            success, msg = self.current_room.merchant.trade_potion(self.player)

        if success:
            self.add_log(f"\n[SUCCESS] {msg}", COLOR_SUCCESS)
        else:
            self.add_log(f"\n[FAILURE] {msg}", COLOR_DANGER)

        self.update_status()
        # Update buttons after purchase (prevent repeated purchases)
        self.clear_btns()
        ttk.Button(self.btn_frame, text="Leave", command=self.continue_explore, style="Game.TButton").grid(row=0, column=0, padx=10)

    def mob_room(self):
        """Mob room battle preparation logic"""
        mob = self.current_room.mob
        self.add_log(mob.get_appear_msg())
        self.add_log(mob.get_counter_choice_msg())
        self.clear_btns()
        ttk.Button(self.btn_frame, text="COUNTERATTACK", command=lambda: self.fight_mob(True), style="Game.TButton").grid(row=0, column=0, padx=10)
        ttk.Button(self.btn_frame, text="DEFEND", command=lambda: self.fight_mob(False), style="Game.TButton").grid(row=0, column=1, padx=10)

    def fight_mob(self, counter_choice):
        """Handle mob battle logic"""
        mob = self.current_room.mob
        msg, damage = mob.battle(self.player, counter_choice)
        self.add_log(f"\n{msg}")
        self.update_status()
        self.is_alive = self.player.check_alive()
        if not self.is_alive:
            self.add_log("\n[SLAIN] You have fallen in battle!", COLOR_DANGER)
        self.clear_btns()
        ttk.Button(self.btn_frame, text="Continue", command=self.continue_explore, style="Game.TButton").grid(row=0, column=0, padx=10)

    def trap_room(self):
        """Trap room trigger logic"""
        trap = self.current_room.trap
        msg = trap.trigger(self.player)
        self.add_log(f"\n[TRAP] {msg}")
        self.add_log(f"You lose {trap.damage} HP! Current HP: {self.player.get_health()}")
        self.is_alive = self.player.check_alive()
        if not self.is_alive:
            self.add_log("\n[SLAIN] You have fallen to a trap!", COLOR_DANGER)
        self.update_status()
        self.clear_btns()
        ttk.Button(self.btn_frame, text="Continue", command=self.continue_explore, style="Game.TButton").grid(row=0, column=0, padx=10)

    def safe_room(self):
        """Safe room rest logic"""
        msg = self.current_room.enter_safe(self.player)
        self.add_log(f"\n[SAFE] {msg}", COLOR_SUCCESS)
        self.update_status()
        self.clear_btns()
        ttk.Button(self.btn_frame, text="Continue", command=self.continue_explore, style="Game.TButton").grid(row=0, column=0, padx=10)

    def continue_explore(self):
        """Continue to next room"""
        self.clear_btns()
        self.add_log("\n----------------------------------------")
        self.root.after(500, self.explore_room)

    def game_over(self):
        """Handle game over logic, display final results"""
        self.clear_btns()
        if self.is_alive and self.room_count >= MAX_ROOM_COUNT:
            title = "VICTORY!"
            msg = f"🎉 CONGRATULATIONS {self.player.name}! 🎉\nYou have explored all {MAX_ROOM_COUNT} rooms and survived!\n\nFinal Stats:\nHP: {self.player.get_health()}\nATT: {self.player.get_attack()}\nCoins: {self.player.get_money()}"
            color = COLOR_SUCCESS
        else:
            title = "GAME OVER"
            msg = f"💀 {self.player.name}, You Have Fallen! 💀\nYou explored {self.room_count} rooms before your death.\n\nFinal Stats:\nHP: {self.player.get_health()}\nATT: {self.player.get_attack()}\nCoins: {self.player.get_money()}"
            color = COLOR_DANGER

        self.add_log(f"\n{msg}", color)
        # Play Again/Quit buttons
        ttk.Button(self.btn_frame, text="PLAY AGAIN", command=self.create_start_interface, style="Game.TButton").grid(row=0, column=0, padx=10)
        ttk.Button(self.btn_frame, text="QUIT", command=self.root.quit, style="Game.TButton").grid(row=0, column=1, padx=10)

    # -------------------------- Utility Methods --------------------------
    def add_log(self, text, color=COLOR_TEXT):
        """Add game log to text box with specified color"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, text + "\n\n")
        # Set text color
        self.log_text.tag_add("color", self.log_text.index("end-2l"), self.log_text.index("end-1l"))
        self.log_text.tag_config("color", foreground=color)
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)  # Auto scroll to bottom

    def clear_btns(self):
        """Clear all buttons in button frame"""
        for widget in self.btn_frame.winfo_children():
            widget.destroy()

    def update_status(self):
        """Update player status bar display"""
        self.hp_label.config(text=f"HP: {self.player.get_health()}/{PLAYER_INIT_HEALTH}")
        # Highlight HP in red when below 30
        self.hp_label.config(foreground=COLOR_DANGER if self.player.get_health() < 30 else COLOR_TEXT)
        self.att_label.config(text=f"ATT: {self.player.get_attack()}")
        self.money_label.config(text=f"Coins: {self.player.get_money()}")
        self.room_label.config(text=f"Rooms: {self.room_count}/{MAX_ROOM_COUNT}")

# -------------------------- Program Entry --------------------------
if __name__ == "__main__":
    root = tk.Tk()
    game = SwordMagicGameGUI(root)
    root.mainloop()