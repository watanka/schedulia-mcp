

Host(Claude Desktop, Cursor)를 통해 미팅 시간을 잡아주는 MCP 서버

[스케쥴 서버 정보](../schedule-server/README.md)


###  api endpoint
- view_meeting_schedules(date): 일, 주, 월에 잡혀있는 일정 확인
- view_meeting_requests()
- respond_to_meeting_request(request_id, accept)
- send_meeting_request()


요청 양식
받는 사람 정보
이메일


미팅 요청을 받는 사람이 앱에 가입이 되어있지 않을 경우, 이메일로 발송
```
이메일 양식
[] 님께서 []님께 미팅을 요청하셨습니다.
가능한 시간대는 [ ]입니다.
[scheduling]앱 사용하기 링크
```

### TODO
- API 키 만들어서, 유저 정보 식별하기
- smithery.ai에 mcp 등록 시, API키 발급받도록 설정.
- 외부 앱(google calendar) 연동
- 미팅 요청에 대한 알림기능
- 요청 수락 시간대 여러 개 지정 가능
- 미팅 확정은 호스트가 지정하도록 설정
- 백그라운드로 이메일 보내기


TEST 스크립트


```
# view_meeting_schedules
유저 ID 식별 후, (API KEY로 식별 예정)
[날짜/시간]에 잡힌 미팅 스케쥴 알려줘
```

```
request_meeting 사용해서 미팅 요청 보내고 싶어.
{받는 사람 이메일 주소}에게 미팅 요청 보내고 싶어.

가능한 시간대는 [ 날짜/시간대1, ... ,]야. 미팅 이름은 {미팅이름}이고, 자세한 설명은 {description}이야.
```

미팅 요청을 수락하기 위해서는 회원가입이 필요함.
회원가입 시, 받은 요청들 회원명으로 등록.
