## 문제점
1. 웹소켓으로 현재가(Ticker)를 받아오는 함수를 apscheduler로 동작시켰으나, 서버가 실행되지 않고 스케줄러만 실행이 된다.
> BackgroundScheduler로 get_ticker를 실행할 수 없어 AsyncIOScheduler로 실행했으나, 서버와 동시에 돌리는 법을 찾지 못해 이 방법은 사용하지 않고 Django Background Tasks를 사용하기로 했다.


2. requests.exceptions.ConnectTimeout: HTTPSConnectionPool... Connection to api.upbit.com timed out. 에러가 떴다.
> [Connection 관리 / 기타](https://docs.upbit.com/docs/upbit-quotation-websocket#5-connection-%EA%B4%80%EB%A6%AC--%EA%B8%B0%ED%83%80)를 보면 `서버에서는 기본적으로 아무런 데이터도 수/발신 되지 않은 채 약 120초가 경과하면 Idle Timeout으로 WebSocket Connection을 종료합니다.`
>> await websocket.ping()으로 핑을 보내 연결이 끊기지 않도록 해결


3. 현재 consumer에서 웹소켓으로 코인 가격을 1초마다 전송하지만, 가격이 갱신되지 않은 코인들까지 전송하는 것은 너무 비효율적이고, 서버에 부하를 줄 수 있다고 생각했다.