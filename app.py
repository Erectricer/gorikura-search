import streamlit as st
import pandas as pd

# ページのタイトルやアイコンを設定
st.set_page_config(page_title="ゴリクラ総合検索システム", page_icon="🦍", layout="centered")

st.title("🦍 ゴリクラ 総合検索システム")

# 📊 タブの作成（メンバー検索と用語辞典を切り替え）
tab1, tab2 = st.tabs(["👥 メンバー検索", "📖 ゴリクラ用語辞典"])

# ==========================================
# 【データ読み込み】Googleスプレッドシートからリアルタイム取得
# ==========================================
# あなたが作ってくれたスプレッドシートのCSVエクスポート用URL
sheet_url = "https://docs.google.com/spreadsheets/d/1JEE6S3FZ3K1ACHgWL9hlWDMWF90Q_deZk8KkW3wFaeA/export?format=csv&gid=1344988261"

@st.cache_data(ttl=10)  # 10秒ごとに最新のデータをスプレッドシートに見に行く設定
def load_member_data():
    try:
        # スプレッドシートをインターネット経由で直接読み込む
        df = pd.read_csv(sheet_url)
        
        # フォームの列名に合わせてデータを整理
        # ※もし実際の列名（タイムスタンプなど）とズレていたら自動調整します
        database = {}
        for _, row in df.iterrows():
            # フォームの項目名を取得（列の位置で判断）
            # 0:タイムスタンプ, 1:代表名, 2:ゲーマータグ, 3:参加時期, 4:通称・あだ名
            try:
                name = str(row.iloc[1]).strip()
                tag = str(row.iloc[2]).strip()
                season = str(row.iloc[3]).strip()
                nicknames_raw = str(row.iloc[4]).strip()
                
                # あだ名をカンマ「,」や読点「、」で区切ってリストにする
                nicknames = [name] # 自分自身の名前も検索対象に入れる
                if nicknames_raw and nicknames_raw != "nan":
                    # カンマやスペースで区切られているのを綺麗に分ける
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
        st.error(f"スプレッドシートの読み込みに失敗しました。URLの設定や共有範囲を確認してください。")
        return {}

member_database = load_member_data()


# ==========================================
# 【タブ1】メンバー検索の処理
# ==========================================
with tab1:
    st.header("👥 メンバー検索")
    st.write("ゲーマータグ、代表名、通称（あだ名）のどれからでも検索できます。")

    # 🔗 ユーザーが要望してくれた「Googleフォームへのリンク」を設置！
    form_url = "https://docs.google.com/forms/d/135e8hQbnsHXjOpKhfEDMbXoBYoe1YuDizTWA0nF0Lxs/viewform"
    st.markdown(f"💡 **新メンバーや、検索しても名前が出ない方はこちらから登録してね！**")
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
                is_tag_match = (search_member.lower() == info.get("tag", "").lower())
                
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
# 【タブ2】用語辞典の処理
# ==========================================
with tab2:
    st.header("📖 ゴリクラ用語辞典")
    st.write("ゴリクラ内で使われる独特な用語を検索したり、一覧で見ることができます。")

    # 用語データの登録
    dictionary_data = {
        "オプチャ": {"読み": "おぷちゃ", "解説": "チャット系SNS「LINE」における半匿名グループチャット機能。ゴリクラにおいては参加が義務化され、Discordと異なり多くの参加勢が入会しているため比較的常に通信が繰り広げられている。"},
        "肩関節族": {"読み": "かたかんせつぞく", "解説": "由来は最初期の参加勢「肩関節」氏から。長時間参加・大規模作業を行いワールドに多大な貢献を行う人物の総称。作業厨。"},
        "刑務所": {"読み": "けいむしょ", "解説": "裁判の結果により懲役義務が発生した場合に被告が収容される施設。全てのシーズンにあるわけではない"},
        "ゴリクラの掟": {"読み": "ごリクラのおきて", "解説": "多分毎日、12:00にオープンチャットに予約投稿されている文章。誰もが自由にイベントを企画してOKという掟。"},
        "裁判": {"読み": "さいばん", "解説": "ワールド内で発生した比較的重大な事案において、プレイヤーが集まり議論での解決を図る行為。傍聴も可能。"},
        "残念車": {"読み": "ざんねんしゃ", "解説": "春の大連続通話祭2026で発生した名言。「残念、車で行くのでｷｮﾑﾘです」を司会が誤読したことに由来する。"},
        "シーズン": {"読み": "しーずん", "解説": "ゴリクラの一区切り。元々は初代管理者がRealmsの更新を忘れ、ワールドにアクセスできなくなったことがシーズン制になった要因である。"},
        "選挙": {"読み": "せんきょ", "解説": "シーズン9において役職陣決定のために開催されたイベント。候補者による演説などもあった。"},
        "卒業": {"読み": "そつぎょう", "解説": "受験期などの事情により長期間ゴリクラを離れること。著者は卒業生の名前にちなんだものを食べたりする（ポテロングなど）。"},
        "大百科": {"読み": "だいひゃっか", "解説": "ゴリクラの公式ホームページ「ゴリクラ大百科」を指す"},
        "チャプター": {"読み": "ちゃぷたー", "解説": "シーズン11の開始の際、10シーズンを1チャプターとする制度として考案されたが、シーズン21開始時点で忘れ去られている可能性がある。"},
        "つちのこ構文": {"読み": "つちのここうぶん", "解説": "がの(つちのこ)氏による長文章。絵文字が多く用いられ、非常に目を引く文になっている。"},
        "つちのこぴぺ": {"読み": "つちのこぴぺ", "解説": "ビジネス文書のような丁寧な物言いでどことなくAIチックな長文章。実際にAIを用いている場合がある。"},
        "バックアップ": {"読み": "ばっくあっぷ", "解説": "ゲーム内時間を巻き戻すRealmsの機能。深刻な荒らしに見舞われた際によく用いられる。"},
        "面接": {"読み": "めんせつ", "解説": "新規参加者に対するGoogle formを用いたアンケート。オプチャで「/面接」と入力すると呼び出せる。"},
        "有益なゴミ": {"読み": "ゆうえきなごみ", "解説": "「鉄の原石」の別称。ゴーレムトラップ完成以降、精錬が必要な原石の価値が暴落したためついた蔑称。"}
    }

    search_word = st.text_input("用語を検索する：", placeholder="例: 残念車、有益なゴミ など")

    if search_word:
        found = False
        for word, data in dictionary_data.items():
            if search_word.lower() in word.lower() or search_word in data["読み"]:
                st.write(f"### 【{word}】（{data['読み']}）")
                st.info(data["解説"])
                found = True
        if not found:
            st.error("❌ その用語は見つかりませんでした。")
    else:
        st.write("---")
        st.write("💡 **用語一覧（クリックで開閉）**")
        for word, data in dictionary_data.items():
            with st.expander(f"【{word}】 （{data['読み']}）"):
                st.write(data["解説"])