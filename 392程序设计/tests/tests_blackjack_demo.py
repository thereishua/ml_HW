import pytest
from src.blackjack import Player,Blackjack

@pytest.fixture
def fresh_player():
    return Player('test')


@pytest.fixture
def fresh_game():
    return Blackjack()


@pytest.fixture
def player_with_cards(fresh_player):
    def _player_with_cards(cards):
        fresh_player.hand_cards = cards.copy()
        return fresh_player
    return _player_with_cards


class TestPlayerCount:
    def test_ace(self, player_with_cards):
        # A+A+9 = 21 (11+1+9)
        player = player_with_cards(['A', 'A', 9])
        assert player.count_point() == 21

        # A+A+A+8 = 21 (1+1+1+8)
        player = player_with_cards(['A', 'A', 'A', 8])
        assert player.count_point() == 21

        # A+A+A+A+7 = 21 (1+1+1+1+7)
        player = player_with_cards(['A', 'A', 'A', 'A', 7])
        assert player.count_point() == 21

    def test_edge_cases(self, player_with_cards):
        # 空手牌
        player = player_with_cards([])
        assert player.count_point() == 0

        # 只有A牌
        player = player_with_cards(['A'])
        assert player.count_point() == 11

        # 爆牌情况
        player = player_with_cards([10, 10, 10])
        assert player.count_point() == 30


class TestBlackjack:
    def test_game_initialization(self, fresh_game):
        game = fresh_game
        assert hasattr(game, 'player')
        assert hasattr(game, 'banker')
        assert hasattr(game, 'cards_cur')
        assert len(game.cards_cur) > 0

    def test_draw_card(self, fresh_game):
        game = fresh_game
        initial_hand_size = len(game.player.hand_cards)

        game.draw(game.player)

        assert len(game.player.hand_cards) == initial_hand_size + 1

    @pytest.mark.parametrize("draw_count", [1, 2, 5])
    def test_multiple_draws(self, fresh_game, draw_count):
        game = fresh_game
        initial_deck_size = len(game.cards_cur)

        for _ in range(draw_count):
            game.draw(game.player)

        assert len(game.cards_cur) == initial_deck_size - draw_count
        assert len(game.player.hand_cards) == draw_count