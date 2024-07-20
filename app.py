import time

import action


def log(msg: str, wait: float = 3):
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(ts, msg)
    if wait > 0:
        time.sleep(wait)


def run(times=100):
    action.Action.mouse_reset(True)

    # metrics
    enlist_times = 0
    white_times = 0
    blue_times = 0
    purple_times = 0
    yellow_times = 0
    red_times = 0
    start = time.time()

    for i in range(times):
        if action.Action.mouse_leaved():
            log("mouse has leaved the window, exit", 0)
            duration = int(time.time() - start)
            total = white_times + blue_times + purple_times + yellow_times + red_times
            print(f"\n duration={duration}s progress={i}/{times}"
                  f"\n statistics: enlist={enlist_times} white={white_times} blue={blue_times} "
                  f"purple={purple_times} yellow={yellow_times} red={red_times} total={total}\n")
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
            enlist_times += 1
            white_times += page.white_card
            blue_times += page.blue_card
            purple_times += page.purple_card
            yellow_times += page.yellow_card
            red_times += page.red_card
            log("enlist success")
            continue
        if page.red_card > 1 or page.yellow_card == 3:
            log("amazing event, wait for you", 0)
            return
        action.Action.give_up()
        log("give up")


def show():
    page = action.Page()
    page.im.save('screenshot.png')
    print(page)


if __name__ == '__main__':
    run()
    # show()
