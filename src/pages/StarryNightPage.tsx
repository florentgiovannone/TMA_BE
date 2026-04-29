import starryNightImage from "../assets/starry-night.png"
import Footer from "../components/Footer"
import "../styles/style.css"
import AudioPlayer from "../components/AudioPlayer"
import pageAudio from "../assets/Audio/ElevenLabs_The_Starry_Night.mp3"

export default function StarryNightPage() {
  return (
    <>
      <main className="tma-gallery-page">
        <header className="tma-header">
          <div className="tma-header-inner">
            <h1 className="tma-page-title">The Starry Night</h1>
            <p className="tma-page-subtitle">June 1889 by Vincent van Gogh</p>
          </div>
        </header>

        <a
          href="/underlying-technology"
          className="tma-banner-link"
        >
          <p className="tma-banner-text">
            <strong>
              When you have explored the page below, please click on this banner to find out about the unique
              underlying technology that enables this solution, and the multiple benefits it offers an exhibition
              curator, museum, and gallery.
            </strong>
          </p>
        </a>

        <div className="tma-content">
          <AudioPlayer src={pageAudio} />
          <img src={starryNightImage} alt="The Starry Night by Vincent van Gogh" className="tma-painting-image" />

          <h2>About the painting.</h2>
          <p>
            The Starry Night is one of Vincent van Gogh&apos;s most celebrated works and a defining image of
            post-impressionist art. Painted in 1889 while Van Gogh was staying at the asylum in Saint-Remy-de-Provence,
            it shows a night sky alive with movement: swirling blue currents, glowing stars, a bright crescent moon,
            and a small village resting quietly below. The scene feels at once peaceful and restless, as if the entire
            sky is in motion while the world beneath remains still.
          </p>
          <p>
            The contrast between the turbulent sky and the calm town gives the painting its powerful emotional tension.
            The tall cypress tree in the foreground rises like a dark flame, linking the earth to the heavens and
            adding to the painting&apos;s dramatic sense of motion and feeling. Rather than presenting a simple view of the
            countryside, Van Gogh transforms the landscape into something almost spiritual, where nature seems charged
            with energy and meaning.
          </p>
          <p>
            Although it is often read as a scene of solitude or inner unrest, the painting is also a work of deep
            imagination and observation. Van Gogh did not paint a literal night sky exactly as it appeared; instead, he
            reimagined it into a visionary composition full of rhythm, color, and intensity. The result is a painting
            that feels both deeply personal and universally moving, capturing awe, beauty, and emotional force all at
            once.
          </p>

          <h2>About the artist.</h2>
          <p>
            Vincent van Gogh was a Dutch Post-Impressionist painter who created a vast body of emotionally intense work
            in just over a decade, and his bold colors and swirling brushstrokes helped pave the way for modern art
            movements like Expressionism. Born on March 30, 1853, in Zundert, Netherlands, he came from a Protestant
            family and worked in various jobs, including as an art dealer and preacher, before turning to painting at
            age 27.
          </p>
          <p>
            What sets van Gogh apart is his raw, personal style that captured inner feelings through vivid colors,
            thick impasto paint, and dramatic forms. He produced over 2,000 works, including about 860 oil paintings,
            often in intense bursts despite ongoing struggles with mental illness and poverty. His early works, like
            The Potato Eaters, focused on rural peasants in dark, earthy tones, but later pieces exploded with bright
            hues after he moved to France.
          </p>
          <p>
            As a painter, van Gogh created some of the most recognized images in art history, such as The Starry Night,
            Sunflowers, The Bedroom, and Wheat Field with Cypresses. He experimented with techniques like heavy
            brushwork and unstable pigments, which gave his canvases texture and energy but sometimes caused color
            changes over time. He painted self-portraits obsessively, using them to explore his own turmoil, and drew
            heavily from nature and everyday scenes.
          </p>
          <p>
            Van Gogh also faced great personal hardship. Supported by his brother Theo, he lived in the Netherlands,
            then Arles and Saint-Remy in France, where he cut off part of his ear in 1888 during a breakdown. He spent
            time in an asylum but kept painting prolifically, creating over 150 works there; he died in 1890 at age 37
            from a self-inflicted gunshot wound in Auvers-sur-Oise.
          </p>
          <p>
            In short, Vincent van Gogh was a tormented genius whose work, unrecognized in his lifetime, now influences
            artists worldwide for its emotional power and visual innovation.
          </p>
        </div>

        <a
          href="/underlying-technology"
          className="tma-banner-link"
        >
          <p className="tma-banner-text">
            <strong>Click this banner to discover more about technology used to create this page.</strong>
          </p>
        </a>
      </main>
      <Footer />
    </>
  )
}
