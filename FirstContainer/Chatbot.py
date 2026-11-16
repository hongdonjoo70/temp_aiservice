from common import model, client

class Chatbot:
    def __init__(self, system_role="You are a helpful assistant", use_model=model.basic):
        """context 초기화 및 시스템 역할 설정"""
        self.model = use_model
        self.context = [
            {"role": "system", "content": system_role}
        ]

    def add_user_message(self, message: str):
        """사용자 메시지를 context에 추가"""
        self.context.append({"role": "user", "content": message})

    def send_request(self):
        """현재 context를 API에 전송하고 응답 받기"""
        response = client.chat.completions.create(
            model=self.model,
            messages=self.context
        ).model_dump()
        return response

    def add_response_message(self, response: dict):
        """응답 메시지를 context에 추가"""
        assistant_msg = response["choices"][0]["message"]
        self.context.append({
            "role": assistant_msg["role"],
            "content": assistant_msg["content"]
        })

    def get_last_response(self) -> str:
        """마지막 응답 내용을 콘솔에 출력 후 반환"""
        last_msg = self.context[-1]["content"]
        # print(last_msg)
        return last_msg