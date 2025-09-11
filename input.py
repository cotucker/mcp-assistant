import threading
import queue
from asr import asr

def text_query(q: queue.Queue):
    query = input("\nQuery: ").strip()
    q.put(query)

def voice_query(q: queue.Queue):
    query = asr()
    q.put(query)

def get_query() -> str:
    result_queue = queue.Queue()
    keyboard_thread = threading.Thread(
        target=text_query, args=(result_queue,), daemon=True
    )
    mic_thread = threading.Thread(
        target=voice_query, args=(result_queue,), daemon=True
    )

    keyboard_thread.start()
    mic_thread.start()

    search_query = result_queue.get()
    return search_query


if __name__ == "__main__":
    print(f"Result: {get_query()}")

