import defaultAudio from "../assets/Audio/ElevenLabs_The_Fallen_Madonna_with_the_Big_Boobies.mp3"

type AudioPlayerProps = {
  src?: string
}

export default function AudioPlayer({ src }: AudioPlayerProps) {
  return (
    <audio className="tma-audio-player" controls src={src ?? defaultAudio}>
      Your browser does not support the audio element.
    </audio>
  )
}
