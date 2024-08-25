import time
import sys
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
        print(f"\n statistics: "
              f"\n duration={duration}s progress={i}/{times} enlist={self.enlist_times}"
              f"\n white={self.white_times} blue={self.blue_times} purple={self.purple_times} "
              f"yellow={self.yellow_times} red={self.red_times} total={total}\n")


def run(m: Metrics, times: int) -> int:
    action.Action.move_title(False)

    # metrics
    continues_fail = 0
    for i in range(times):
        if action.Action.mouse_leaved():
            log("mouse has leaved the window, exit", 0)
            return i
        action.Action.move_title()
        page = action.Page()
        print(page)

        if page.is_unknown_status():
            if i == 0 and page.is_correct_bottom():  # only for first loop
                action.Action.move_bottom(True)  # click for first check
                log("click to enter window", 0)
                continue

            continues_fail += 1
            if continues_fail >= 30:
                log("continues fail, exit", 0)
                return i
            if page.need_confirm():
                action.Action.confirm_give_up()
                log("confirm give up")
                continue
            log("unknown status", 1)
            continue
        continues_fail = 0

        if page.purple_card == 3 or page.yellow_card > 0 or page.red_card > 0:
            action.Action.increase_bet()
            log("increase bet", 1)
        # if page.white_card + page.blue_card == 3:
        #     log("ordinary event, wait for next try", 0)
        #     return i
        if page.need_gold:  # 抽卡
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
            return i
        action.Action.give_up()
        log("give up")
    return times


def debug():
    page = action.Page()
    page.im.save('screenshot.png')
    print(page)


def main():
    m = Metrics()
    times = run(m, 1000)
    m.print(times, 1000)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        time.sleep(1)
        debug()
    else:
        main()
