import random
import os
import platform


class Poker:
    def __init__(self, name, color, number):
        self.color = color
        self.number = number
        self.name = name


class Player:
    def __init__(self, name, chip):
        self.name = name
        self.chip = chip
        self.pokers = []


class Game:
    def __init__(self):
        self.pokers = self.init_pokers()
        self.computer, self.player = self.init_players()
        
    @staticmethod
    def exec_clear_screen_command():
        if 'windows' in platform.platform().lower():
            os.system('cls')
        else:
            os.system('clear')

    @staticmethod
    def init_pokers():
        """
        初始化一副牌，没有大小王，默认A的值为1
        :return:
        """

        pokers = []
        cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        colors = ['草花', '方片', '红桃', '黑桃']
        for i, card in enumerate(cards):
            for color in colors:
                poker = Poker(card, color, i + 1 if i <= 9 else 10)
                pokers.append(poker)
        return pokers

    @staticmethod
    def init_players():
        """
        初始化电脑庄家、玩家信息
        :return:
        """

        # 初始化电脑庄家
        while True:
            try:
                computer_chip = int(input('请设置庄家筹码：'))
                if computer_chip > 1000 or computer_chip < 1:
                    print('请输入1-1000之间的数字')
                else:
                    break
            except:
                print('请输入1-1000之间的数字')
        computer = Player('庄家', computer_chip)

        # 初始化玩家信息
        player_name = input('请设置玩家名称：')
        while True:
            try:
                player_chip = int(input('请设置玩家筹码：'))
                if player_chip > 1000 or player_chip < 1:
                    print('请输入1-1000之间的数字')
                else:
                    break
            except:
                print('请输入1-1000之间的数字')
        player = Player(player_name, player_chip)
        return computer, player

    def clear_screen(self):
        """
        刷屏
        :return:
        """
        self.exec_clear_screen_command()
        print('*' * 30, '   欢迎来到21点   ', '*' * 30, end='\n\n')
        print('庄家剩余筹码：', self.computer.chip, '\t', self.player.name, '剩余筹码：', self.player.chip, end='\n\n\n\n\n\n')

    def run(self):
        """
        游戏主进程
        :return:
        """

        while True:
            self.clear_screen()
            if self.player.chip <= 0:
                print('输光光啦，回去拿点钞票再来吧^_^')
                input()
                self.exec_clear_screen_command()
                break
            if self.computer.chip <= 0:
                print('打败庄家了，所有的筹码都是你的了^_^')
                input()
                self.exec_clear_screen_command()
                break

            bet = 0
            while True:
                try:
                    bet = int(input('请下注：'))
                    if bet > self.player.chip:
                        print('兄dei，看看自己的钱包吧，哪还有这么多？')
                    elif bet < 1:
                        print('咋滴呀，想空手套白狼？')
                    else:
                        break
                except:
                    print('请输入数字呦~')

            # 发牌
            for _ in range(2):
                poker = random.choice(self.pokers)
                self.computer.pokers.append(poker)
                self.pokers.remove(poker)
            for _ in range(2):
                poker = random.choice(self.pokers)
                self.player.pokers.append(poker)
                self.pokers.remove(poker)

            computer_point = sum([item.number for item in self.computer.pokers])
            player_point = sum([item.number for item in self.player.pokers])
            player_points = []
            computer_points = []
            # 玩家继续要牌吗
            while True:
                print('\n\n')
                print('当前手牌:', '\t'.join([card.color + card.name for card in self.player.pokers]), end='\t')

                if player_point > 21:
                    print('当前点数：爆牌！！！', end='\n\n\n')
                    break

                a_count = len(list(filter(lambda x: x.name == 'A', self.player.pokers)))
                if a_count > 0:
                    player_points.clear()
                    player_points.append(player_point)
                    for i in range(a_count):
                        player_points.append(player_point + 10 * (i + 1))
                    print('当前点数：', '/'.join([str(point) for point in player_points]))
                else:
                    print('当前点数：', player_point)

                if len(self.player.pokers) >= 5:
                    break

                get = input('还继续要牌吗？不要请输n/N。')
                if get.lower() != 'n':
                    poker = random.choice(self.pokers)
                    self.player.pokers.append(poker)
                    self.pokers.remove(poker)
                    player_point += self.player.pokers[-1].number
                else:
                    print('\n\n')
                    break

            # 电脑继续要牌吗
            while True:
                if computer_point in [19, 20, 21] or len(self.computer.pokers) >= 5:
                    break

                a_count = len(list(filter(lambda x: x.name == 'A', self.computer.pokers)))
                if a_count > 0:
                    computer_points.clear()
                    computer_points.append(computer_point)
                    for i in range(a_count):
                        computer_points.append(computer_point + 10 * (i + 1))

                if a_count > 0:
                    break_flag = False
                    for point in computer_points:
                        if 19 <= point <= 21:
                            break_flag = True
                            break
                    if break_flag:
                        break

                get = random.randint(0, 1)

                if computer_point < 21 and (computer_point < 15 or get > 0):
                    poker = random.choice(self.pokers)
                    self.computer.pokers.append(poker)
                    self.pokers.remove(poker)
                    computer_point += self.computer.pokers[-1].number
                else:
                    break

            # 计算点数
            if len(player_points) > 0:
                for point in player_points:
                    if point <= 21 and 21 - point < 21 - player_point:
                        player_point = point
            if len(computer_points) > 0:
                for point in computer_points:
                    if point <= 21 and 21 - point < 21 - computer_point:
                        computer_point = point

            # 开牌
            print(self.player.name, '手牌:', '\t'.join([card.color + card.name for card in self.player.pokers]),
                  end='\t')
            print('点数：', player_point, end='\n\n')

            print('庄家手牌:', '\t'.join([card.color + card.name for card in self.computer.pokers]), end='\t')
            print('点数：', computer_point, end='\n\n')

            if computer_point < player_point <= 21 or player_point <= 21 < computer_point:
                print('恭喜,', self.player.name, '胜！！！')
                self.player.chip += bet
                self.computer.chip -= bet
            else:
                print('抱歉，庄家胜出。')
                self.player.chip -= bet
                self.computer.chip += bet

            # 洗牌
            for card in self.player.pokers:
                self.pokers.append(card)
            for card in self.computer.pokers:
                self.pokers.append(card)
            self.player.pokers.clear()
            self.computer.pokers.clear()
            input()


if __name__ == '__main__':
    game = Game()
    game.run()
