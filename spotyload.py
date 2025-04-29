import os, concurrent.futures, pyoutube, pspotify

 # Caminho base onde as músicas serão salvas (exemplo: pen drive em E:\)
BASE_DOWNLOAD_PATH = "C:\\Users\\VIPEXGRU029\\Music\\musica_teste"  # Utilize duas barras invertidas para o caminho correto

def main():
    # Solicita a URL da playlist do Spotify
    playlist_url = input("Cole o link da playlist do Spotify: ").strip()
    playlist_id = pspotify.extract_playlist_id(playlist_url)
    if not playlist_id:
        print("❌ Link inválido!")
        return

    # Solicita o nome da pasta onde as músicas serão salvas
    folder_name = input("Informe o nome da pasta onde as músicas serão salvas (deixe vazio para usar o nome da playlist): ").strip()
    if not folder_name:
        folder_name = pspotify.get_playlist_name(playlist_id)
    
    # Cria o caminho final de download unindo o BASE_DOWNLOAD_PATH e o nome da pasta
    final_download_path = os.path.join(BASE_DOWNLOAD_PATH, folder_name)
    os.makedirs(final_download_path, exist_ok=True)
    print(f"As músicas serão salvas em: {final_download_path}")

    # Obtém as músicas da playlist do Spotify
    print("\n🔍 Obtendo músicas da playlist...")
    tracks = pspotify.get_spotify_tracks(playlist_id)
    if not tracks:
        print("❌ Nenhuma música encontrada!")
        return
    
    total_tracks = len(tracks)
    print(f"🎵 Total de músicas na playlist do Spotify: {total_tracks}")

    # Verifica quantas músicas já foram baixadas (arquivos .mp3)
    local_files = [f for f in os.listdir(final_download_path) if f.lower().endswith('.mp3')]
    local_count = len(local_files)
    print(f"💾 Músicas já baixadas: {local_count}")

    if local_count >= total_tracks:
        print("✅ Todas as músicas já foram baixadas!")
        return
    else:
        # Assume que as músicas foram baixadas na mesma ordem da playlist
        tracks_to_download = tracks[local_count:]
        print(f"⬇️ Baixando {len(tracks_to_download)} músicas faltantes...")

    # Utiliza multithreading para processar os downloads em paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
        futures = [executor.submit(pyoutube.process_track, track, final_download_path) for track in tracks_to_download]
        concurrent.futures.wait(futures)
    
    print("\nConcluído!")

if __name__ == "__main__":
    main()
