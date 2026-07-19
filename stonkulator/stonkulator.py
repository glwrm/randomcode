import json
import time
import random
import os
from pynput import keyboard
running = True

COLORS = {
	"RED": "\033[1;31m",
	"BLUE": "\033[1;34m",
	"CYAN": "\033[1;36m",
	"GREEN": "\033[0;32m",
	"YELLOW": "\033[0;33m",
	"WHITE": "\033[1;37m",
	"BLACK": "\033[1;30m",
	"RESET": "\033[0;0m",
	"BOLD": "\033[;1m",
	"REVERSE": "\033[;7m",
	"NORMAL": "\033[0;35m"
}

MILESTONE_THRESHOLDS = {
	"Hobo": 0,
	"Trader": 10_000,
	"Broker": 50_000,
	"Investor": 100_000,
	"Stonker": 500_000,
	"Millionaire": 1_000_000,
	"Tycoon": 5_000_000,
	"Rich Guy": 10_000_000,
	"Industrialist": 50_000_000,
	"Magnate": 100_000_000,
	"Capitalist": 500_000_000,
	"Billionare": 1_000_000_000
}

EASY_SHARELIMITS = {
	"Hobo": 50,
	"Trader": 100,
	"Broker": 150,
	"Investor": 200,
	"Stonker": 300,
	"Millionare": 400,
	"Tycoon": 600,
	"Rich Guy": 800,
	"Industrialist": 1000,
	"Magnate": 1500,
	"Capitalist": 2000,
	"Billionare": 2500
}

MEDIUM_SHARELIMITS = {
	"Hobo": 30,
	"Trader": 60,
	"Broker": 90,
	"Investor": 120,
	"Stonker": 180,
	"Millionare": 240,
	"Tycoon": 360,
	"Rich Guy": 480,
	"Industrialist": 650,
	"Magnate": 800,
	"Capitalist": 950,
	"Billionare": 1200
}

HARD_SHARELIMITS = {
	"Hobo": 15,
	"Trader": 30,
	"Broker": 45,
	"Investor": 60,
	"Stonker": 90,
	"Millionare": 120,
	"Tycoon": 180,
	"Rich Guy": 250,
	"Industrialist": 330,
	"Magnate": 420,
	"Capitalist": 500,
	"Billionare": 600
}

def format_duration(seconds):
	parts = []
	days, seconds = divmod(seconds, 86400)
	hours, seconds = divmod(seconds, 3600)
	minutes, seconds = divmod(seconds, 60)

	if days > 0:
		parts.append(f"{days}d")
	if hours > 0 or days > 0:
		parts.append(f"{hours}h")
	if minutes > 0 or hours > 0 or days > 0:
		parts.append(f"{minutes}m")
	parts.append(f"{seconds:.0f}s")

	return ' '.join(parts)

def cls():
	os.system("cls" if os.name == "nt" else "clear")

def on_press(key):
	global running
	try:
		if key.char == "b":
			player_portfolio.buy(game.stockslist[game.selected_stock])
			game.update()
		elif key.char == "s":
			player_portfolio.sell(game.stockslist[game.selected_stock])
			game.update()
		elif key.char == "p":
			game.pause()
			game.render_screen()
		elif key.char == "q":
			running = False
		elif key.char == "l":
			game.save()
		elif key.char == "c":
			game.notifications = []
			game.update()
		elif key.char == "B":
			player_portfolio.buy_all(game.stockslist[game.selected_stock])
			game.update()
		elif key.char == "S":
			player_portfolio.sell_all(game.stockslist[game.selected_stock])
			game.update()
	except AttributeError:
		if key == keyboard.Key.up:
			game.selected_stock -= 1 if game.selected_stock != 0 else 0
			game.update()
		elif key == keyboard.Key.down:
			game.selected_stock += 1 if game.selected_stock != len(game.stockslist) - 1 else 0
			game.update()

class Stock:
	def __init__(self, companyname, name, maxremove, maxadd, startprice, updateinterval):
		self.companyname = companyname
		self.name = name
		self.max_remove = maxremove
		self.max_add = maxadd
		self.change = 0
		self.price = startprice
		self.previous_price = startprice
		self.update_interval = updateinterval
		self.last_update = time.time()
		self.history = []
		
	def update_price(self):
		now = time.time()
		if now - self.last_update >= self.update_interval:
			self.previous_price = self.price
			change = round(random.uniform(self.max_remove, self.max_add), 2)
			new_price = round(self.price + change, 2)
			self.history.append(new_price)

			if new_price != self.price:
				self.price = max(1, new_price)
				self.change = self.price - self.previous_price

			if len(self.history) > 20:
				self.history.pop(0)

			self.last_update = now
	
	def __str__(self):
		return self.name

class Difficulty:
	def __init__(self, name, startingcash, volatility, allow_pause, sharelimits):
		self.name = name
		self.startcash = startingcash
		self.volatility = volatility
		self.allow_pause = allow_pause
		self.sharelimits = sharelimits

class Portfolio:
	def __init__(self, name, startcash, sharelimits, holdings):
		self.name = name
		self.title = "Hobo"
		self.cash = startcash
		self.holdings = holdings
		self.sharelimits = sharelimits
	
	def buy(self, stock):
		if stock.price <= self.cash:
			if self.holdings.get(stock.name, 0) + 1 <= self.sharelimits[self.title]:
				self.cash -= stock.price
				self.holdings[stock.name] = self.holdings.get(stock.name, 0) + 1
				game.notify(f"{COLORS['GREEN']}You bought a share of {stock.name} for {stock.price:.2f}.")
			else:
				game.notify(f"{COLORS['RED']}You cannot buy a share of {stock.name}! It exceeds the limit.")
		else:
			game.notify(f"{COLORS['RED']}You cannot afford that!")
	
	def sell(self, stock):
		if self.holdings.get(stock.name, 0) != 0:
			self.cash += stock.price
			self.holdings[stock.name] = self.holdings.get(stock.name, 0) - 1
			game.notify(f"{COLORS['GREEN']}You sold a share of {stock} for {stock.price:.2f}.")
		else:
			game.notify(f"{COLORS['RED']}You don't have any shares of that stock!")
	
	def buy_all(self, stock):
		price = stock.price
		already_owned = self.holdings.get(stock.name, 0)
	
		remaining_cap = self.sharelimits[self.title] - already_owned
		affordable_shares = int(self.cash // price)
		amount_to_buy = min(remaining_cap, affordable_shares)
	
		if amount_to_buy <= 0:
			game.notify(f"{COLORS['RED']}Can't buy any more of {stock.name}. Either you're broke or at the limit.")
			return
	
		self.cash -= amount_to_buy * price
		self.holdings[stock.name] = already_owned + amount_to_buy
		game.notify(f"{COLORS['GREEN']}Bought {amount_to_buy} shares of {stock.name} at ${price:.2f} each.")
  
	def sell_all(self, stock):
		if player_portfolio.holdings[stock.name] <= 0:
			game.notify(f"{COLORS['RED']}You don't own any shares of {stock.name}.")
			return

		total = player_portfolio.holdings[stock.name] * stock.price
		self.cash += total
		game.notify(f"{COLORS['GREEN']}Sold all {player_portfolio.holdings[stock.name]} shares of {stock.name} for ${total:.2f}.")
		self.holdings[stock.name] = 0

	
	def update_title(self):
		for title, threshold in sorted(MILESTONE_THRESHOLDS.items(), key=lambda x: x[1]):
			if self.cash >= threshold:
				self.title = title

class Game:
	def __init__(self, difficulty, stocks, portfolio, playtime):
		self.difficulty = difficulty
		self.stocks = stocks
		self.portfolio = portfolio
		self.time = playtime
		self.paused = False
		self.notifications = []
		self.selected_stock = 0
		self.stocks = stocks
		self.stockslist = list(self.stocks.values())
	
	def pause(self):
		if self.difficulty.allow_pause:
			self.paused = not self.paused
	
	def save(self):
		save = {
			"cash": player_portfolio.cash,
			"difficulty": game.difficulty.name,
			"holdings": player_portfolio.holdings,
			"playtime": game.time,
			"portfolio_name": player_portfolio.name,
			"stocks": {stock.name: stock.price for stock in stocklist.values()}
		}

		with open("stonkulatordata.json", "w", encoding="utf-8-sig") as f:
			json.dump(save, f, indent=4)
	
	def update(self):
		if self.paused == False:
			for i in self.stocks.values():
				i.update_price()
		player_portfolio.update_title()
		self.render_screen()

	def render_screen(self):
		cls()
		if self.difficulty.allow_pause:
			pause_status = "RUNNING" if not self.paused else "PAUSED "
		else:
			pause_status = "       "
		timestamp = format_duration(self.time)

		print("╔════════════════════════════════════════════════════════════════════╦═════════════════════════════════════════════════╗")
		print(f"║ 💼 Portfolio: {self.portfolio.name:<15}{' ' * (26 - len(f'self.portfolio.title:<12'))}{' ' * (17 - len(f'{timestamp}'))} Total playtime: {timestamp}  ║    [P] Pause │ [Q] Quit │ [↑↓] Select Stock     ║")
		print(f"║ 💰 Cash: ${self.portfolio.cash:,.2f}{' ' * (16 - len(f'{self.portfolio.cash:,.2f}'))}🏆 Milestone: {self.portfolio.title:<18}{pause_status}  ║  [B] Buy | [S] Sell | [C] Clear Notifications   ║")
		print("╠════════════════════════════════════════════════════════════════════╣     [Shift+S] Sell All │ [Shift+B] Buy All      ║")
		print("║ STOCK │ NAME             │ PRICE   │ CHANGE  │ OWNED │ NEXT UPDATE ║                    [L] Save                     ║")
		print("║───────┼──────────────────┼─────────┼─────────┼───────┼─────────────║═════════════════════════════════════════════════╝")

		for i, stock in enumerate(self.stockslist):
			name = stock.companyname[:18]
			price = f"${stock.price:,.2f}"
			change_str = f"{stock.change:+.2f}"
			owned = player_portfolio.holdings.get(stock.name, 0)
			time_left = max(0, stock.update_interval - (time.time() - stock.last_update))
			next_update = format_duration(time_left)
			arrow = ">" if i == self.selected_stock else " "

			print(f"║ {arrow}{stock.name:<5}│ {name:<16} │ {price:<7} │ {change_str:<7} │"
				f" {owned:<5} │ {next_update:<1}          ║")

		print("╠════════════════════════════════════════════════════════════════════╣")
		print("╠═════════════════════════ 📢 Notifications ═════════════════════════╣")
		if self.notifications == []:
			print(f"║ {'You have no new notifications.':<57}          ║")
		for message in self.notifications:
			print(f"║ {message} ║")
		print("╚" + "═" * 68 + "╝")

	def notify(self, message, spaces=73):
		if len(self.notifications) >= 15:
			self.notifications.pop(0)
		self.notifications.append(f"{message:<{spaces}}{COLORS['RESET']}")

difficulties = {
	"easy": Difficulty("easy", 5000, 1.2, True, EASY_SHARELIMITS),
	"medium": Difficulty("medium", 1000, 1.4, True, MEDIUM_SHARELIMITS),
	"hard": Difficulty("hard", 250, 1.7, False, HARD_SHARELIMITS)
}

stocklist = {
	"DEZ": Stock("Dez's Bindles", "DEZ", -5, 5, 30, 2),
	"AGG": Stock("AntiGG", "AGG", -2, 4, 60, 5),
	"DAR": Stock("Green Lobster", "DAR", -15, 15, 10, 1),
	"STB": Stock("StuffBytes", "STB", -2.5, 3, 45, 4)
}

def tutorial():
	cls()
	playerinput = input("Play tutorial? (Y/N)\n")
	validinput = False
	while not validinput:
		if playerinput.lower() == "y":
			validinput = True
			time.sleep(1)
			print("Welcome to Stonkulator!\n")
			time.sleep(1.5)
			
			print("\nIn this game, you're a day trader trying to flip stocks for profit.")
			time.sleep(2)

			print("\nYou start with a small amount of cash depending on the difficulty.")
			time.sleep(2)

			print("\nEvery few seconds, stock prices change randomly.")
			time.sleep(1.5)
			
			print("\nBuy low. Sell high. Repeat.")
			time.sleep(1.5)
			
			print("\n Each stock has a limit to how many shares you can own.")
			print("These limits grow as you hit cash milestones like $100k or $1M.")
			time.sleep(2.5)

			print("\n Tip: Some stocks are riskier. Big gains... or big losses.")
			time.sleep(2)

			print("\nYou can pause the market to analyze prices before making decisions.")
			time.sleep(2)

			print("\n Your progress can be saved by pressing S, and it autosaves every 5 minutes.")
			time.sleep(2)

			print("\nThat's it! Let's make some stonks.")
			time.sleep(1.5)
		elif playerinput.lower() == "n":
			print("Skipping tutorial.")
			time.sleep(1)
			validinput = True

try:
	with open("stonkulatordata.json", "r", encoding="utf-8-sig") as file:
		print("Loading...")
		time.sleep(1.5)
		save = json.load(file)
		print("Save file loaded.")
		try:
			customdata = open("customdata.json", "r", encoding="utf-8-sig")
			time.sleep(0.5)
			print("Custom data file loaded.")
			if customdata.get("enabled", False):
				for stock in customdata.get("stocks", []):
					stocklist[stock.name] = Stock(stock["companyname"], stock["name"], stock["maxremove"], stock["maxadd"], stock["startprice"], stock["updateinterval"])
				for difficulty in customdata.get("difficulty", []):
					difficulties[difficulty.name] = Difficulty(stock["name"], stock["startingcash"], stock["volatility"], stock["allow_pause"], stock["sharelimits"])
			else:
				print("Custom data file disabled. Use \"enabled\": true to enable the custom data.")
		except FileNotFoundError:
			print("Custom data file not found.")
		time.sleep(1)
		player_portfolio = Portfolio(save["portfolio_name"], save["cash"], difficulties[save["difficulty"]].sharelimits, save["holdings"])
		for symbol, saved_price in save["stocks"].items():
			if symbol in stocklist:
				stocklist[symbol].price = saved_price
		game = Game(difficulties[save["difficulty"]], stocklist, player_portfolio, save["playtime"])
		time.sleep(0.5)
		print("Game objects created.")
except FileNotFoundError:
	tutorial()
	print("No save file found. Creating one...")
	with open("stonkulatordata.json", "x+", encoding="utf-8-sig") as file:
		validinput = False
		while not validinput:
			playerinput = input("Select a difficulty (Easy, Medium, or Hard):\n")
			try:
				selected_difficulty = difficulties[playerinput.lower()]
				player_portfolio = Portfolio(input("Enter a name for your portfolio:\n"), selected_difficulty.startcash, selected_difficulty.sharelimits, {})
				game = Game(selected_difficulty, stocklist, player_portfolio, 0)
				save = {
					"cash": game.difficulty.startcash,
					"difficulty": game.difficulty.name,
					"holdings": {},
					"playtime": 0,
					"portfolio_name": player_portfolio.name,
					"stocks": {}
				}
				json.dump(save, file)
				validinput = True
			except KeyError:
				print("That difficulty doesn't exist. Please select one of the available difficulties.")
				validinput = False

cls()

last_auto_save = time.time()
last_update = time.time()

listener = keyboard.Listener(on_press=on_press)
listener.start()

while running:
	game.update()
	game.time += 1
	time.sleep(1)

	now = time.time()
	if now - last_auto_save >= 300:
		game.save()
		game.notify("Game auto-saved!", 66)
		last_auto_save = now

game.save()
print("")
print(f"{COLORS['GREEN']}Game saved. Quitting!{COLORS['RESET']}")
time.sleep(2)
cls()
quit()
