import concurrent.futures, time
from asr import asr

def text_query():
    query = input("\nQuery: ").strip()
    return query

def voice_query():
    return asr()

def get_query() -> str:
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_keyboard = executor.submit(text_query)
        future_mic = executor.submit(voice_query)
        for future in concurrent.futures.as_completed([future_keyboard, future_mic]):
            try:
                result = future.result()
                if result:
                    search_query = result
                    break
            except Exception as e:
                print(f"В одном из потоков произошла ошибка: {e}")       
        return f"Result: {search_query}"



if __name__ == "__main__":
    print(get_query())

