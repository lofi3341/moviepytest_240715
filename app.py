import streamlit as st
import os
import moviepy.editor as mp

# 動画から音声を抽出する関数
def extract_audio(video_path, temp_folder):
    video_name = os.path.basename(video_path)
    video_name_without_ext = os.path.splitext(video_name)[0]
    
    clip = mp.VideoFileClip(video_path)
    audio_path = os.path.join(temp_folder, f"{video_name_without_ext}_audio.wav")
    clip.audio.write_audiofile(audio_path, logger=None)  # 進捗バーを無効化
    
    return audio_path

# 動画から音声を無くす関数
def remove_audio(video_path, temp_folder):
    video_name = os.path.basename(video_path)
    video_name_without_ext = os.path.splitext(video_name)[0]
    
    clip = mp.VideoFileClip(video_path)
    video_without_audio_path = os.path.join(temp_folder, f"{video_name_without_ext}_no_audio.mp4")
    clip_without_audio = clip.set_audio(None)
    
    try:
        clip_without_audio.write_videofile(video_without_audio_path, logger=None, verbose=True)  # 進捗バーを無効化
    except Exception as e:
        raise IOError(f"MoviePy error: FFMPEG encountered the following error while writing file {video_without_audio_path}:\n{str(e)}")
    
    return video_without_audio_path

# メインのStreamlitアプリ
def main():
    st.title("動画処理アプリ")
    
    # ファイルアップローダー
    video_file = st.file_uploader("動画ファイルをアップロードしてください", type=['mp4', 'mov', 'avi'])
    
    if video_file is not None:
        # 書き込み可能なディレクトリにtempフォルダを作成
        temp_folder = "/tmp/temp"  # 書き込み可能なディレクトリを使用
        os.makedirs(temp_folder, exist_ok=True)
        
        # アップロードされた動画をtempフォルダに保存
        video_path = os.path.join(temp_folder, video_file.name)
        with open(video_path, "wb") as f:
            f.write(video_file.getbuffer())
        
        st.success(f"動画をアップロードしました: {video_file.name}")
        
        # 処理ボタン
        if st.button("動画を処理する"):
            # 音声を抽出
            try:
                audio_path = extract_audio(video_path, temp_folder)
                st.success(f"音声を抽出しました: {os.path.basename(audio_path)}")
            except Exception as e:
                st.error(f"音声抽出中にエラーが発生しました: {e}")
                return
            
            # 音声を無くした動画を生成
            try:
                video_without_audio_path = remove_audio(video_path, temp_folder)
                st.success(f"音声無し動画を保存しました: {os.path.basename(video_without_audio_path)}")
            except Exception as e:
                st.error(f"音声無し動画生成中にエラーが発生しました: {e}")
                return
            
            st.markdown("### 処理済みファイルのダウンロード:")
            
            # ダウンロードリンク
            with open(audio_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
                st.download_button(label="抽出された音声をダウンロード", data=audio_bytes, file_name=os.path.basename(audio_path))
                
            with open(video_without_audio_path, "rb") as video_file:
                video_bytes = video_file.read()
                st.download_button(label="音声無し動画をダウンロード", data=video_bytes, file_name=os.path.basename(video_without_audio_path))

# アプリの実行
if __name__ == "__main__":
    main()
