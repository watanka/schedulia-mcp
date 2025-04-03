## MCP Server that can arrange meeting through Host(Claude Desktop, Cursor)

###  Tools
- view_meeting_schedules(date): view meeting schedules
- view_meeting_requests(): view meeting requests
- respond_to_meeting_request(request_id, accept)
- send_meeting_request(): send meeting requests

### Demo
[video records]

### Examples
- view_meeting_schedules(date) prompts
- view_meeting_requests() prompts
- respond_to_meeting_request(request_id, accept)  prompts
- send_meeting_request()  prompts


### TODO
- smithery.ai에 mcp 등록 시, API키 발급받도록 설정.
- 외부 앱(google calendar) 연동
- 미팅 요청에 대한 알림기능
- 요청 수락 시간대 여러 개 지정 가능
- 미팅 확정은 호스트가 지정하도록 설정
- 백그라운드로 이메일 보내기


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
