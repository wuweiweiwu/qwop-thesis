import matplotlib.pyplot as plt
import collections

def main():
    f = open('scores.txt', 'r')
    lines = f.readlines()
    x = [i for i in range(len(lines))]
    y = []
    for line in lines:
        # counter = collections.Counter(line)
        # y.append(counter.most_common(1)[0][1])
        y.append(int(line))
    plt.scatter(x, y)
    plt.show()

if __name__ == '__main__':
    main()
