from random import shuffle

        
def make_teams(registered_players):
    delta = 100.0
    while delta > 0.5: 
        shuffle(registered_players)
        red_team = registered_players[:5]
        yellow_team = registered_players[5:]
        red_strength = 0
        yellow_strength = 0
        for player in red_team:
            red_strength += player.player.value
        for player in yellow_team:
            yellow_strength += player.player.value
        delta = abs(red_strength - yellow_strength)
    return red_team, yellow_team, red_strength, yellow_strength, delta
        
        

