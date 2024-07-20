import time

import action
import random


def log(msg: str, wait: float = 3):
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(ts, msg)
    if wait > 0:
        wait += random.randint(1, 300) / 1000
        time.sleep(wait)


class Metrics:
    def __init__(self):
        self.enlist_times = 0
        self.white_times = 0
        self.blue_times = 0
        self.purple_times = 0
        self.yellow_times = 0
        self.red_times = 0
        self.start = time.time()

    def print(self, i, times):
        duration = int(time.time() - self.start)
        total = self.white_times + self.blue_times + self.purple_times + self.yellow_times + self.red_times
        print(f"\n duration={duration}s progress={i}/{times}"
              f"\n statistics: enlist={self.enlist_times} white={self.white_times} blue={self.blue_times} "
              f"purple={self.purple_times} yellow={self.yellow_times} red={self.red_times} total={total}\n")


def run(times=1000):
    action.Action.mouse_reset(True)

    # metrics
    m = Metrics()
    for i in range(times):
        if action.Action.mouse_leaved():
            log("mouse has leaved the window, exit", 0)
            m.print(i, times)
            return
        action.Action.mouse_reset()
        page = action.Page()
        print(page)
        if page.is_unknown_status():
            if page.need_confirm():
                action.Action.confirm_give_up()
                log("confirm give up")
                continue
            log("unknown status", 1)
            continue
        if page.purple_card == 3 or page.yellow_card > 0 or page.red_card > 0:
            action.Action.increase_bet()
            log("increase bet", 1)
        if page.need_gold:
            action.Action.enlist()
            m.enlist_times += 1
            m.white_times += page.white_card
            m.blue_times += page.blue_card
            m.purple_times += page.purple_card
            m.yellow_times += page.yellow_card
            m.red_times += page.red_card
            log("enlist success")
            continue
        if page.red_card > 1 or page.yellow_card == 3:
            log("amazing event, wait for you", 0)
            m.print(i, times)
            return
        action.Action.give_up()
        log("give up")
    m.print(times, times)


def show():
    page = action.Page()
    page.im.save('screenshot.png')
    print(page)


if __name__ == '__main__':
    run()
    # show()
