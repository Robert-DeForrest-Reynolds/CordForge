from CordForge import *


# Initial send of dashboard, all other functions are replys/edits of the sent message
async def entry(user_card:Card) -> Card:
    await user_card.add_button(f"Money: {user_card.user.wallet}", give_money, [])


async def give_money(user_card:Card, interaction) -> None:
    user_card.user.wallet += 1
    await bot.home(user_card, interaction)


player_traits = [
    # [trait name, trait value]
    ["wallet", 0.00],
]
bot = Cord(entry_command="cmd",
           entry=entry,
           player_traits=player_traits)
bot.launch()