if __name__ == '__main__':
    import os, time
    _cur = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(_cur, '%s.txt' % int(time.time())), 'wb') as h:
        h.write(str(time.time()))