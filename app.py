import streamlit as st
import pandas as pd

# ページのタイトルやアイコンを設定
st.set_page_config(page_title="ゴリクラ総合検索システム", page_icon="🦍", layout="centered")

st.title("🦍 ゴリクラ 総合検索システム")

# 📊 タブの作成（まずはメンバー検索が動くか確認）
tab1, tab2 = st.tabs(["👥 メンバー検索", "📖 ゴリクラ用語辞典"])

# ==========================================
# 【データ読み込み】Googleスプレッドシートからリアルタイム取得
# ==========================================
sheet_url = "https://docs.google.com/spreadsheets/d/1JEE6S3FZ3K1ACHgWL9hlWDMWF90Q_deZk8KkW3wFaeA/export?format=csv&gid=1344988261"

@st.cache_data(ttl=10)
def load_member_data():
    try:
        df = pd.read_csv(sheet_url)
        database = {}
        for _, row in df.iterrows():
            try:
                name = str(row.iloc[1]).strip()
                tag = str(row.iloc[2]).strip()
                season = str(row.iloc[3]).strip()
                nicknames_raw = str(row.iloc[4]).strip()
                
                nicknames = [name]
                if nicknames_raw and nicknames_raw != "nan":
                    for n in nicknames_raw.replace("、", ",").replace(" ", ",").split(","):
                        if n.strip():
                            nicknames.append(n.strip())
                
                database[name] = {
                    "tag": tag if tag != "nan" else "なし",
                    "season": season if season != "nan" else "不明",
                    "type": "メンバー",
                    "通称": nicknames
                }
            except:
                continue
        return database
    except Exception as e:
        st.error("スプレッドシートの読み込みに失敗しました。")
        return {}

member_database = load_member_data()

# ==========================================
# 【タブ1】メンバー検索の処理
# ==========================================
with tab1:
    st.header("👥 メンバー検索")
    st.write("ゲーマータグ、代表名、通称（あだ名）のどれからでも検索できます。")

    form_url = "https://docs.google.com/forms/d/135e8hQbnsHXjOpKhfEDMbXoBYoe1YuDizTWA0nF0Lxs/viewform"
    st.markdown("💡 **新メンバーや、検索しても名前が出ない方はこちらから登録してね！**")
    st.link_button("📝 メンバー情報 登録フォームを開く", form_url)
    st.write("---")

    if member_database:
        search_member = st.text_input("検索したいメンバー名・タグを入力してね：", placeholder="例: チョコビ、saba919919 など")

        if search_member:
            found_member = None
            found_name = ""

            for name, info in member_database.items():
                is_name_match = (search_member.lower() == name.lower())
                is_nickname_match = ("通称" in info and any(search_member.lower() == n.lower() for n in info["通称"]))
                is_tag_match = (search_member.lower() == str(info.get("tag", "")).lower())
                
                if is_name_match or is_nickname_match or is_tag_match:
                    found_member = info
                    found_name = name
                    break

            if found_member:
                st.success(f"### 🟢 {found_name} さんの情報が見つかりました！")
                st.markdown(f"**🆔 ゲーマータグ:** `{found_member.get('tag', 'なし')}`")
                st.markdown(f"**📅 参加時期:** {found_member.get('season', '不明')}")
                st.markdown(f"**👑 区分:** {found_member.get('type', 'メンバー')}")
                if "通称" in found_member and len(found_member["通称"]) > 1:
                    st.info(f"**💡 その他の通称:** {', '.join(found_member['通称'])}")
            else:
                st.error("❌ その名前やタグのメンバーは見つかりませんでした！上のフォームから登録をお願いします。")

# ==========================================
# 【タブ2】一旦空っぽにして確認
# ==========================================
with tab2:
    st.header("📖 ゴリクラ用語辞典")
    st.write("検索窓の復活を確認するため、一時的に中身を非表示にしています。")
