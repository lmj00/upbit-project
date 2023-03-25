## 문제점
1. 웹소켓으로 현재가(Ticker)를 받아오는 함수를 apscheduler로 동작시켰으나, 서버가 실행되지 않고 스케줄러만 실행이 된다.
> BackgroundScheduler로 get_ticker를 실행할 수 없어 AsyncIOScheduler로 실행했으나, 서버와 동시에 돌리는 법을 찾지 못해 이 방법은 사용하지 않고 Django Background Tasks를 사용하기로 했다.