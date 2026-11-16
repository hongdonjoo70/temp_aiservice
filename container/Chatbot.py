from common import model, client, gpt_num_tokens, makeup_response
import math

class Chatbot:
    def __init__(self, system_role, instruction, use_model=model.gemini):
        # context 초기화 및 대화 문맥 생성
        self.model = use_model
        self.max_token_size = 1024  # 모델별 최대 토큰 수 제한
        self.context = [
            {"role": "system", "content": f"{system_role}\n\n{instruction}"}  # 지시 추가
        ]
    # 누적 token 수가 임계점을 넘지 않도록 제어
    def handle_token_limit(self, response):
        try:
            if hasattr(response, "usage") and response.usage is not None:
                total_tokens = response.usage.total_tokens
            elif isinstance(response, dict):
                total_tokens = response.get("usage", {}).get("total_tokens", 0)
            else:
                total_tokens = 0

            if total_tokens > self.max_token_size:
                remove_size = math.ceil(len(self.context) / 10)
                # system message는 유지
                self.context = ([self.context[0]] + self.context[remove_size + 1:])
        except Exception as e:
            print(f'handle_token_limit exception : {e}')


    def add_user_message(self, message: str):
        """사용자 메시지를 context에 추가"""
        self.context.append({"role": "user", "content": message})

    def send_request(self):  
        try:
            # 현재 context의 max_token 크기를 벗어날 때 처리
            if gpt_num_tokens(self.context) > self.max_token_size:
                self.context.pop()
                return makeup_response('메시지를 조금 짧게 보내 줄래?')            
            
            response = client.chat.completions.create(
                model=self.model,
                messages=self.context,
                temperature=0.5,
                top_p=1,
                max_tokens=2048
            ).model_dump()
            print(f"DEBUG raw response: {response}")  #
            return response
        except Exception as e:
            print(f'Exception 오류({type(e)}) 발생 : {e}')
            return makeup_response('죄송합니다. API 요청 중 오류가 발생했습니다.')

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
        print(last_msg)
        return last_msg