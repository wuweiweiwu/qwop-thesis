from genetic_algo import Genetic
from game_detector import GameDetector


if __name__ == '__main__':


    game = GameDetector()
    genetic = Genetic(20, .01, .7, 10)
    genetic.run(5)


    # scores = []
    # colors = []
    # counter = 1
    # times = []
    #
    # while not is_end():
    #     scr = get_score()
    #     print scr
    #
    #     test_mag = abs(scr) if abs(scr) < 5 else 5
    #
    #     if len(scores) > 0 and abs(scores[-1] - scr) > test_mag:
    #         print 'prediction wrong'
    #         scr = scores[-1]
    #         colors.append('r')
    #     else:
    #         colors.append('g')
    #
    #     scores.append(scr)
    #     time.sleep(.1)
    #
    #     times.append(counter)
    #     counter = counter + 1
    #
    # plt.scatter(times, scores, c=colors)
    # plt.show()
