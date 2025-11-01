import replicate
import os
from dotenv import load_dotenv
from PIL import Image
import requests
from io import BytesIO

# --- .env 読み込み ---
load_dotenv()

# --- APIトークン取得 ---
REPLICATE_API_TOKEN = os.getenv("TNREPLICATE_EX")
if not REPLICATE_API_TOKEN:
    raise ValueError("❌ REPLICATE_API_TOKEN が読み込めませんでした。'.env' ファイルを確認してください。")
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# --- モデルバージョンを.envから取得 ---
MODEL_VERSION = os.getenv("stable")
if not MODEL_VERSION:
    raise ValueError("❌ STABLE_DIFFUSION_MODEL_VERSION が読み込めませんでした。'.env' ファイルを確認してください。")

# --- モデルIDにバージョンを反映 ---
MODEL_ID = f"stability-ai/stable-diffusion:{MODEL_VERSION}"

def generate_images(prompt, num_images=1, steps=30, width=512, height=512):
    """
    Replicate APIを利用して、指定したバージョンのStable Diffusionモデルで画像生成する
    """
    results = []
    for i in range(num_images):
        print(f"🎨 [{i+1}/{num_images}] 画像生成中...")
        try:
            output = replicate.run(
                MODEL_ID,
                input={
                    "prompt": prompt,
                    "num_inference_steps": steps,
                    "width": width,
                    "height": height
                }
            )

            if isinstance(output, list) and output:
                img_url = output[0]
                response = requests.get(img_url)
                image = Image.open(BytesIO(response.content))
                results.append(image)
                print("✅ 画像生成成功！")
            else:
                print("⚠️ 出力が空でした。Replicate APIのレスポンスを確認してください。")

        except Exception as e:
            print(f"❌ 画像生成中にエラーが発生しました: {e}")

    return results
