import hoaHakananaiImage from "../assets/hoa-hakananai.png"
import Footer from "../components/Footer"
import "../styles/style.css"
import AudioPlayer from "../components/AudioPlayer"
import pageAudio from "../assets/Audio/ElevenLabs_The_Hoa_Hakananaiʻa.mp3"

export default function HoaHakananaiPage() {
  return (
    <>
      <main className="tma-gallery-page">
        <header className="tma-header">
          <div className="tma-header-inner">
            <h1 className="tma-page-title">Hoa Hakananaiʻa</h1>
            <p className="tma-page-subtitle">Circa 1000-1200 CE from the Rapa Nui People</p>
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
          <img src={hoaHakananaiImage} alt="Hoa Hakananaiʻa moai statue" className="tma-painting-image" />

          <h2>About the Hoa Hakananaiʻa.</h2>
          <p>
            Hoa Hakananaiʻa is a monumental moai (ancestral statue) from Rapa Nui, best known today as the large
            stone figure on display in the British Museum in London. The name Hoa Hakananaiʻa is often glossed as
            "lost, hidden, or stolen friend" in the Rapa Nui language, a title that now feels deeply symbolic given
            its removal from the island. Carved roughly between about 1000 and 1200 CE from a block of dark grey-brown
            volcanic rock (commonly described as basalt, though not fully petrologically confirmed), the statue stands
            about 2.42 metres high, spans about 96 cm across the shoulders, and weighs around 4.2 tonnes. Its form
            follows the classic Rapa Nui moai type: an oversized head, elongated face, strong brows, and a compact,
            almost column-like body, yet its setting and decoration give it exceptional cultural significance.
          </p>
          <p>
            The statue originally stood erected at Orongo, a ceremonial village perched on the rim of the Rano Kau
            volcanic crater in the southwest of the island. In the 19th century it was still in place, partly buried
            inside a small stone "house" or shrine, facing inland toward the crater while the doorway and the
            statue&apos;s back looked out over the sea. On its back and shoulders, Hoa Hakananaiʻa is covered with
            intricate petroglyphs linked to the later bird-man cult (tangata manu), including stylised bird figures,
            vulva-shaped female symbols (komari), and ceremonial dance paddles (ao), motifs that point to its use in
            rituals surrounding the island&apos;s annual bird-man competition. The combination of its monumental front and
            its densely carved back makes it one of the most complex and visually rich moai known, offering a rare
            window into how ancestor-statues could be integrated into changing religious practices over time.
          </p>
          <p>
            Hoa Hakananai'a was removed from Orongo in 1868 by the crew of the British ship HMS Topaze and taken to
            the United Kingdom, where it was later given to the British Museum. Its departure from Rapa Nui has become
            a focal point in debates about museum ethics and the restitution of cultural heritage, as many Rapa Nui
            today view the statue less as a colonial acquisition and more as a sacred ancestor figure forcibly taken
            from the island. In recent years, the status of Hoa Hakananaiʻa has been re-examined in light of new
            historical research and Rapa Nui voices, highlighting both its aesthetic power and the difficult history of
            its removal.
          </p>

          <h2>About the Rapa Nui People</h2>
          <p>
            The Rapa Nui (the Indigenous Polynesian people of Easter Island) are the descendants of seafarers who
            settled this remote island in the eastern Pacific, likely around 1000-1200 CE, making theirs one of the
            most isolated Polynesian societies. Their language, Rapa Nui, is closely related to other Eastern
            Polynesian tongues, and today many Rapa Nui also speak Chilean Spanish, since the island has been
            administered as part of Chile since the 19th century. The modern Rapa Nui population numbers just over
            7,000, with about 60 percent identifying as Rapa Nui, and a significant portion of the community also
            living on the mainland, maintaining strong cultural ties while navigating life in contemporary Chilean
            society.
          </p>
          <p>
            The best-known aspect of Rapa Nui culture is the hundreds of moai-monolithic human figures carved from
            volcanic rock and set up on large stone platforms called ahu across the island between roughly 1250 and
            1500 CE. The moai were understood as the living faces of ancestors, invested with mana (spiritual power),
            and their placement on the ahu linked the living community to the world of the dead. As environmental
            pressures and shifting political structures reshaped Rapa Nui society, the older moai cult gradually gave
            way to the bird-man cult at Orongo, in which leadership and spiritual authority were determined through an
            annual competition involving the first man to retrieve the egg of the sooty tern from nearby Motu Nui
            islet. This transition is subtly present in objects such as Hoa Hakananaiʻa, which bears the bird-man
            imagery on its back, reflecting the way Rapa Nui beliefs could adapt rather than simply collapse.
          </p>
          <p>
            Over the 19th and 20th centuries, the Rapa Nui people endured devastating losses from introduced diseases,
            slave-raiding raids, and political marginalization, which dramatically reduced the population and disrupted
            traditional knowledge such as the Rongorongo script-a unique system of glyphs whose meaning has not been
            fully recovered. Yet Rapa Nui culture has never disappeared; instead, it has been actively revitalized
            through language-reclamation projects, dance and music (hakaraka), tattooing traditions, and the ongoing
            stewardship of the island&apos;s archaeological sites. Today, Rapa Nui themselves are at the forefront of
            conversations about how monuments like Hoa Hakananaiʻa should be understood-not only as objects of global
            fascination but as living parts of Indigenous memory, belief, and identity.
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
