from machine import Pin, Timer

# 初始化 LED 引脚
led = Pin("LED", Pin.OUT)

# 当前占空比（0-100）
duty = 50

# 使用全局变量来模拟计数器
toggle_led_counter = 0

# 定义一个回调函数来模拟 PWM 控制
def toggle_led(timer):
    global led, duty, toggle_led_counter

    if toggle_led_counter < duty:
        led.value(1)  # 开灯
    else:
        led.value(0)  # 关灯

    toggle_led_counter += 1

    if toggle_led_counter >= 100:
        toggle_led_counter = 0

# 启动定时器，每隔 10 毫秒回调一次
timer = Timer()
timer.init(period=10, mode=Timer.PERIODIC, callback=toggle_led)

print("Program started. Send commands in format 'PWM <duty>'.")

# 主循环接收用户输入命令
while True:
    try:
        user_input = input()  # 从串口接收用户输入
        #print(f"Received command: {user_input}")

        if user_input.startswith("PWM"):
            try:
                duty_value = float(user_input.split(" ")[1])

                # 检查占空比是否在 0 到 100 范围内
                if 0 <= duty_value <= 100:
                    duty = int(duty_value)  # 更新占空比例值
                    print("OK")
                else:
                    print("NG")
            except (IndexError, ValueError):
                print("NG")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        break

