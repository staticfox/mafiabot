from time import sleep
import threading


def _defer(t, function, args):
    sleep(float(t))
    function(*args)


def defer(t, function, *args):
    threading.Thread(target=_defer, args=(t, function, args)).start()
