import sys
from typing import List, Dict, Any
import pandas as pd
import ollama


def get_local_models_summary() -> pd.DataFrame:
    """
    Fetches the available local models from Ollama and formats 
    their metadata into a clean tabular DataFrame.
    """
    try:
        models_info = ollama.list()
        models = models_info.get('models', [])
    except Exception as e:
        print(f"❌ Error connecting to Ollama service: {e}")
        sys.exit(1)

    data_for_df = []
    for model in models:
        name = model.get('name')
        size_bytes = model.get('size', 0)
        size_gb = size_bytes / (1024**3)
        modified_at = model.get('modified_at')
        details = model.get('details', {})
        
        data_for_df.append({
            'Name': name,
            'Size (GB)': f"{size_gb:.2f}",
            'Modified At': modified_at,
            'Format': details.get('format'),
            'Family': details.get('family', 'N/A'),
            'Parameters': details.get('parameter_size'),
            'Quantization': details.get('quantization_level')
        })
    
    return pd.DataFrame(data_for_df)


def run_interactive_chat(model_name: str, system_prompt: str) -> None:
    """
    Handles the real-time CLI streaming chat loop with the targeted Ollama model.
    """
    messages = [{'role': 'system', 'content': system_prompt}]
    
    # Clean up model name for a cleaner console display
    display_name = model_name.split('/')[-1].replace(':', ' ').replace('_', ' ')
    
    print(f"\n💬 Connected to local model: {model_name}")
    print("برای خروج کلمه 'خداحافظ' را تایپ کنید.")
    print("-" * 60)

    while True:
        try:
            user_input = input("\nشما: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ['خداحافظ', 'exit', 'quit']:
                print("خداحافظ!")
                break

            messages.append({'role': 'user', 'content': user_input})
            print(f"🤖 {display_name}: ", end="", flush=True)

            # Stream the response chunk-by-chunk
            response_stream = ollama.chat(model=model_name, messages=messages, stream=True)
            
            current_assistant_response = ""
            for chunk in response_stream:
                content = chunk['message']['content']
                print(content, end="", flush=True)
                current_assistant_response += content
            print()

            messages.append({'role': 'assistant', 'content': current_assistant_response})

        except KeyboardInterrupt:
            print("\n\nخداحافظ!")
            break
        except Exception as e:
            print(f"\n❌ Chat Error: {e}")


if __name__ == "__main__":
    # 1. Fetch and display currently pulled local models
    print("📋 Fetching local Ollama models registry...")
    df_models = get_local_models_summary()
    if not df_models.empty:
        print(df_models.to_string(index=False))
    else:
        print("No local models found.")

    # 2. Configurations
    TARGET_MODEL = 'partai/dorna-llama3:8b-instruct-q4_0'
    
    SYSTEM_PROMPT = """
سوال و جواب های زیر را در نظر داشته باش تا در صورت پرسیدن طبق آن ها جواب دهی :
1- وقتی در مورد هویتت پرسیدند به اینصورت خودت را معرفی کن : 'من دستیار هوش مصنوعی اداره آموزش و پرورش دزفول هستم' وهدفم کمک به معلمان و دانش آموزان در امور اداری و آموزشی است 
2- اگر در مورد بخشنامه پروژه مهر پرسیدند در پاسخ میگویی 'فرصت پاسخگویی تا 31 مرداد است و باید مستندات طبق عناوین بیستگانه بایگانی شوند'
3- تعداد تک ماده مجاز برای دانش آموزان در مجموع دروس 3 پایه دوره دوم متوسطه، 4 درس می باشد که شرط آن کسب نمره حداقل 7 است
4- اگر در مورد فرم های زیر سوال شد به اینصورت پاسخ بده و اگر فرمی غیر از اینها بود بگو چنین فرمی در اداره ما وجود ندارد:
    - فرم 504: جناب آقای دوستی کارشناس کارگزینی در اتاق 21 
    - فرم درخواست معاونت : جناب آقای نادی کارشناس مسئول آموزش متوسطه در اتاق 31
    - فرم درخواست معاون پرورشی: جناب آقای ابیض معاون پرورشی در اتاق 5

نکته مهم: در هر پاسخ نگو من دستیار هوش مصنوعی اداره آموزش و پرورش دزفول هستم. فقط و فقط وقتی در مورد هویتت پرسیدند این جمله را بگو.
"""

    # 3. Start chat service
    run_interactive_chat(model_name=TARGET_MODEL, system_prompt=SYSTEM_PROMPT)
