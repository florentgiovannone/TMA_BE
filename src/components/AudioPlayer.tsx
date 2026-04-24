import fallenMadonnaAudio from "../assets/fallen-madonna-florence.mp3"

export default function AudioPlayer() {
  const audioUrl = import.meta.env.VITE_AUDIO_URL || fallenMadonnaAudio

  return (
    <audio className="tma-audio-player" controls src={audioUrl}>
      Your browser does not support the audio element.
    </audio>
  )
}
