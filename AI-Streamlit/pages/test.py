from openai import OpenAI
from openai import AuthenticationError, RateLimitError
from dotenv import load_dotenv

load_dotenv()
    
def test_openai_key():
    try:
        # 간단한 질문을 보내고 응답을 받아옵니다.
        response = client.chat.completions.create(
            model="gpt-4",  # 또는 "gpt-3.5-turbo" 등 사용할 모델
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, can you tell me if this API key is working?"}
            ]
        )
        
        # 응답이 정상적으로 오면 API 키가 유효한 것으로 판단
        if response and response.choices:
            print("API 키가 정상적으로 작동합니다!")
            print("응답:", response.choices[0].message.content)
        else:
            print("API 키는 유효하지만, 응답을 받아오지 못했습니다.")
    
    except AuthenticationError:
        print("API 키가 유효하지 않습니다. 올바른 키를 입력했는지 확인하세요.")
    except RateLimitError:
        print("API 요청 한도를 초과했습니다. 잠시 후 다시 시도하세요.")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

# 테스트 실행
test_openai_key()