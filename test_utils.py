from image_generator import generate_images
from utils import save_images, load_gallery, get_today_count, add_today_count
from datetime import datetime
import os

def test_generation_limit():
    print("=== 1️⃣ 生成制限テスト ===")
    # 現在の今日カウントを取得
    today_count = get_today_count()
    print(f"今日の生成枚数: {today_count}")

    # 5枚制限を確認
    if today_count >= 5:
        print("⚠️ 今日の生成上限に達しています。追加生成は不可")
    else:
        remaining = 5 - today_count
        print(f"残り生成可能枚数: {remaining} 枚")
        # 仮に1枚生成
        add_today_count(1)
        print(f"1枚追加後の今日の生成枚数: {get_today_count()}")

def test_save_and_gallery():
    print("\n=== 2️⃣ 画像保存・ギャラリーテスト ===")
    # ダミー画像生成（ここでは image_generator で生成）
    prompt = "A futuristic eco-friendly city skyline at sunset, digital art"
    images = generate_images(prompt, num_images=1, steps=20)

    if not images:
        print("❌ 画像生成に失敗しました")
        return

    # 保存
    folder = os.path.join("generated_images", datetime.now().strftime("%Y%m%d_%H%M%S"))
    paths = save_images(images, folder=folder)
    print(f"✅ {len(paths)} 枚の画像を保存しました: {paths}")

    # ギャラリー読み込み
    gallery = load_gallery()
    print(f"🖼️ ギャラリーに読み込まれた画像数: {len(gallery)}")
    for img_path in gallery:
        print(f" - {img_path}")

if __name__ == "__main__":
    test_generation_limit()
    test_save_and_gallery()
