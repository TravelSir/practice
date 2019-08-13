# -*- coding: utf-8 -*-
import time
from threading import Thread


def cpu_intensive():
  i = 0
  for _ in range(300000000):
    i += 1
  return True


def single_thread():
  start_time = time.time()
  for i in range(2):
    t = Thread(target=cpu_intensive)
    t.start()
    t.join()
  end_time = time.time()
  # print(f'single thread used {end_time-start_time}')
  print('single thread used {}'.format(end_time-start_time))


def multi_thread():
  thread_list = []
  start_time = time.time()
  for i in range(2):
    t = Thread(target=cpu_intensive)
    thread_list.append(t)
    t.start()
  for t in thread_list:
    t.join()
  end_time = time.time()
  # print(f'multi thread used {end_time-start_time}')
  print('multi thread used {}'.format(end_time-start_time))


if __name__ == "__main__":
  single_thread()
  multi_thread()
