from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("TNSYSTEM1")
if not api_key:
    raise ValueError("⚠️ OPEN_AI_API が .env に設定されていません。")

client = OpenAI(api_key=api_key)

def analyze_theme(text):
    prompt = f"""
以下は市場調査の分析結果です。
この内容をもとに、Stable Diffusion向けの画像生成プロンプトを作成してください。
出力は英語で、カンマ区切りのキーワード形式で返してください。
---
{text}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたはプロのアートディレクター兼プロンプトエンジニアです。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        content = response.choices[0].message.content.strip()
        if not content:
            return "default art prompt, illustration, high quality"
        return content
    except OpenAIError as e:
        return f"⚠️ OpenAI API エラー: {e}"
    except Exception as e:
        return f"⚠️ 不明なエラーが発生しました: {e}"

