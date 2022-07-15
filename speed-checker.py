import datetime, os, socket, time

import sub_checker as sc

FREQ = 100

def get_host_ip():
    a = socket.gethostbyname(socket.getfqdn())
    return a

def ping_test():
    test_ping_address = "8.8.8.8"
    response = os.system("ping -c 1 " + test_ping_address + " > /dev/null 2>&1")
    if response == 0:
        return response
    else:
        return "Fail"

'''def main_test():

    servers = ["8.8.8.8","8.8.4.4"]
# If you want to test against a specific server
# servers = [1234]
    x=0
    for x in range(0, 2):
        s = speedtest.Speedtest()
        s.get_servers(servers)
        s.get_best_server()
        s.download()
        s.upload()
        s.results.share()
        results_dict = s.results.dict()
    print(results_dict)

    return True
'''
def download():
    pass

def upload():
    pass

def test_once():

    time_a = datetime.datetime.now()
    curtime = time_a.strftime("%a %b %d %w %Y at %H:%M:%S")

    try:
        print("About to ping...")
        ping = ping_test()
        print(3, "About to download...")
        down = download()
        print(3, "About to upload...")
        upload_speed = upload()
   #     result = main_test()
        newline = ", ".join([curtime, str(ping),
                             str(down), str(upload_speed)]) + '\n'
    except Exception as exc:
        print("It didn't work! " + str(exc))
        newline = ", ".join([curtime, exc.__repr__()]) + '\n'
        ping = down = upload_speed = 0

    time_b = datetime.datetime.now()

    print("Test completed, result:")
    print(newline)

    time_diff = (FREQ * 60) - (time_b - time_a).total_seconds()
    if time_diff < 0:
        time_diff = 0  # hope we catch up eventually

    return newline, time_diff, {'ping': ping, 'down': down, 'up': upload_speed}


def main():

    while True:
        newline, time_diff, _ = test_once()
        with open("logging_speed_test.txt", 'a') as record:
            record.write(newline)
        time.sleep(time_diff)

#    print("importing: ", sc.TestUpload())


if __name__ == '__main__':
    main()
