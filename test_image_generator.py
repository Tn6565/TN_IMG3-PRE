from image_generator import generate_images

def main():
    # テスト用プロンプト
    prompt = "A futuristic eco-friendly city skyline at sunset, highly detailed, digital art"

    # 画像生成（枚数1、ステップ数20）
    images = generate_images(prompt, num_images=1, steps=20, width=512, height=512)

    # 成功したか確認
    if images:
        # 保存せずに表示だけする場合
        images[0].show()
        print("✅ 画像生成テスト成功！")
    else:
        print("❌ 画像生成テスト失敗。出力が空でした。")

if __name__ == "__main__":
    main()
