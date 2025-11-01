import streamlit as st
from datetime import datetime
from prompt_builder import analyze_theme
from image_generator import generate_images
from utils import save_images, load_gallery, get_today_count, add_today_count
import pyperclip
import torch
import os

# --- ページ設定 ---
st.set_page_config(page_title="🎨 画像生成スタジオ", page_icon="🖼️", layout="wide")
st.markdown("<h1 style='text-align:center;'>🎨 市場調査連携 画像生成スタジオ</h1>", unsafe_allow_html=True)

# --- セッションステート初期化 ---
if "retry_flag" not in st.session_state:
    st.session_state.retry_flag = False
if "generating" not in st.session_state:
    st.session_state.generating = False

# --- レイアウト ---
col_input, col_gallery = st.columns([1.2, 1.8])

with col_input:
    st.markdown("### 📝 市場調査結果をペースト")
    user_text = st.text_area(
        "市場調査レポート内容", height=200, placeholder="市場調査アプリの出力を貼り付けてください。"
    )

    st.markdown("### ⚙️ 生成設定")
    num_images = st.slider("生成する画像枚数", 1, 5, 2)
    steps = st.slider("生成ステップ数（品質）", 10, 100, 30)
    width = st.number_input("幅 (px)", value=512, step=64)
    height = st.number_input("高さ (px)", value=512, step=64)

    if not torch.cuda.is_available():
        st.warning("⚠️ GPUが見つかりません。生成速度が遅くなります。")

    # --- 生成制限チェック ---
    today_count = get_today_count()
    remaining = 5 - today_count
    st.markdown(f"**本日残り生成可能枚数: {remaining} 枚**")

    generate_button_placeholder = st.empty()

    def run_generation():
        st.session_state.generating = True
        try:
            # --- プロンプト生成 ---
            with st.spinner("🎨 プロンプトを生成中..."):
                prompt = analyze_theme(user_text)
                st.success("プロンプト生成完了！")

            with st.expander("🧠 生成されたプロンプト（英語）", expanded=False):
                st.code(prompt, language="markdown")
                if st.button("📋 プロンプトをコピー"):
                    pyperclip.copy(prompt)
                    st.toast("コピーしました！")

            # --- 画像生成 ---
            with st.spinner("🪄 画像生成中..."):
                images = generate_images(prompt, num_images=num_images, steps=steps, width=width, height=height)
                if images:
                    folder = os.path.join("generated_images", datetime.now().strftime("%Y%m%d_%H%M%S"))
                    paths = save_images(images, folder=folder)
                    add_today_count(len(images))
                    st.balloons()
                    st.success(f"🎉 {len(paths)}枚の画像を生成し保存しました！")
                else:
                    st.error("❌ 画像生成に失敗しました。Replicate APIのレスポンスを確認してください。")
                    if st.button("🔄 再試行"):
                        st.session_state.retry_flag = True
        except Exception as e:
            st.error("❌ エラーが発生しました。Replicate APIやネットワークを確認してください。")
            st.text(f"詳細: {e}")
            if st.button("🔄 再試行"):
                st.session_state.retry_flag = True
        finally:
            st.session_state.generating = False

    # --- ボタン押下条件 ---
    if remaining <= 0:
        st.warning("⚠️ 本日の生成上限（5枚）に達しました。明日までお待ちください。")
    else:
        if (st.button("🚀 画像を生成する", use_container_width=True) or st.session_state.retry_flag) and not st.session_state.generating:
            if not user_text.strip():
                st.warning("市場調査結果を入力してください。")
            elif num_images > remaining:
                st.warning(f"⚠️ 今日残り生成可能枚数は {remaining} 枚です。")
            else:
                st.session_state.retry_flag = False
                run_generation()

with col_gallery:
    st.markdown("### 🖼️ ギャラリー")
    gallery = load_gallery()
    if gallery:
        n_cols = 3 if len(gallery) > 3 else len(gallery)
        cols = st.columns(n_cols)
        for i, img_path in enumerate(gallery):
            timestamp = datetime.fromtimestamp(os.path.getmtime(img_path)).strftime("%m/%d %H:%M")
            with cols[i % n_cols]:
                try:
                    st.image(img_path, caption=f"{timestamp}", use_container_width=True)
                except Exception as e:
                    st.warning(f"⚠️ 画像の読み込みに失敗しました: {img_path}")
    else:
        st.info("まだ保存済み画像はありません。")
