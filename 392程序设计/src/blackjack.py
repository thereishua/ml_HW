import random

# 玩家，电脑，游戏流程利用上面向对象编程
# 要有测试功能的代码
class Player:
    def __init__(self,role):
        self.role = role
        self.hand_cards = []

    def add_card(self,card):
        self.hand_cards.append(card)

    def count_point(self):
        points = 0
        a_count = 0
        for card in self.hand_cards:
            if card == 'A':
                points += 11
                a_count += 1
            elif card in ["J","Q","K"]:
                points += 10
            else:
                points += card
        while points > 21 and a_count>0:
            points -= 10
            a_count -=1
        return points

    def bust(self):
        return self.count_point() > 21

    def blackjack(self):
        return len(self.hand_cards) == 2 and self.count_point() == 21


class Blackjack:
    def __init__(self):
        self.cards = ([i for i in range(2,11)] + ['A','J','Q','K'])*4
        self.cards_cur = self.cards.copy()
        self.player = Player('player')
        self.banker = Player('banker')

    def draw(self,player):
        if not self.cards_cur:
            self.cards_cur = self.cards
        card = random.choice(self.cards_cur)
        player.add_card(card)
        self.cards_cur.remove(card)
        return card

    def begin_game(self):
        for _ in range(2):
            self.draw(self.banker)
            self.draw(self.player)

    def play_game(self):
        self.begin_game()
        if self.banker.blackjack() and self.player.blackjack():
            print(f'{self.banker.hand_cards},{self.player.hand_cards},双方均为Blackjack，平局')
            return
        elif self.banker.blackjack():
            print(f'{self.banker.hand_cards}Blackjack,庄家赢')
            return
        elif self.player.blackjack():
            print(f'{self.player.hand_cards}Blackjack,玩家赢')

        # banker turn
        while self.banker.count_point() < 17:
            self.draw(self.banker)

        # player turn
        while True:
            print(f'banker:{self.banker.hand_cards[1:]},player:{self.player.hand_cards}\n是否抽牌(y/n)')
            cmd = input()
            if cmd == 'y' and not self.player.bust():
                self.draw(self.player)
                if self.player.bust():
                    break
            else:
                break

        banker_point = self.banker.count_point()
        player_point = self.player.count_point()

        if player_point > 21:
            print(f"庄家牌:{self.banker.hand_cards}:{banker_point},玩家牌:{self.player.hand_cards}:{player_point},庄家赢(玩家爆牌)")
        elif banker_point > 21:
            print(
                f"庄家牌:{self.banker.hand_cards}:{banker_point},玩家牌:{self.player.hand_cards}:{player_point},玩家赢(庄家爆牌)")
        elif player_point <= banker_point:
            print(f"庄家牌:{self.banker.hand_cards}:{banker_point},玩家牌:{self.player.hand_cards}:{player_point},庄家赢")
        else:
            print(f"庄家牌:{self.banker.hand_cards}:{banker_point},玩家牌:{self.player.hand_cards}:{player_point},玩家赢")

if __name__ == '__main__':
    while True:
        print('是否进行21点游戏(y/n)')
        ans = input()
        if ans == 'y':
            game = Blackjack()
            game.play_game()
        else:
            break