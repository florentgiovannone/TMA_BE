import rosettaStoneImage from "../assets/rosetta-stone.png"
import Footer from "../components/Footer"
import "../styles/style.css"
import AudioPlayer from "../components/AudioPlayer"
import pageAudio from "../assets/Audio/ElevenLabs_The_Rosetta_Stone.mp3"

export default function RosettaStonePage() {
  return (
    <>
      <main className="tma-gallery-page">
        <header className="tma-header">
          <div className="tma-header-inner">
            <h1 className="tma-page-title">The Rosetta Stone</h1>
            <p className="tma-page-subtitle">196 BCE by the Cult of King Ptolemy V</p>
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
          <img src={rosettaStoneImage} alt="The Rosetta Stone" className="tma-painting-image" />

          <h2>About the The Rosetta stone.</h2>
          <p>
            The Rosetta Stone is a dark granodiorite stele inscribed with a single royal decree issued in 196 BCE
            during the reign of Ptolemy V Epiphanes, the young Macedonian-Greek king ruling over Egypt. The inscription
            appears in three scripts stacked in horizontal bands: the top register in hieroglyphic Egyptian, the middle
            in Demotic Egyptian, and the bottom in Ancient Greek. This trilingual text is essentially the same decree
            repeated in three forms, with only minor variations, making it the first known parallel text that allowed
            scholars to systematically match words and grammatical patterns between the known Greek language and the
            previously undeciphered Egyptian scripts.
          </p>
          <p>
            The stone is not a unique or especially ornate object by ancient Egyptian standards; it was one of many
            copies of this decree that were carved on stelae and set up in temples across Egypt to reinforce the
            king&apos;s authority and the backing of the priestly establishment. Over time the original slab broke, and the
            largest surviving fragment-what we now call the Rosetta Stone-was later reused as building stone, probably
            in the foundations of a fortress near the town of Rashid (Rosetta) in the Nile Delta. It lay embedded in
            the masonry for centuries until it was rediscovered in 1799 by French soldiers working on fortifications
            during Napoleon&apos;s campaign in Egypt.
          </p>
          <p>
            Once its trilingual nature was recognized, it became the key artifact that unlocked the decipherment of
            Egyptian hieroglyphs, especially through the work of scholars such as Thomas Young and, most famously,
            Jean-Francois Champollion in the early 19th century. Today the Rosetta Stone is one of the most iconic
            objects in the British Museum, not only as a gateway to ancient Egyptian language and culture, but also as
            a powerful symbol of how a single artifact can reshape entire fields of historical knowledge.
          </p>

          <h2>About the Cult of Ptolemy V.</h2>
          <p>
            The text on the Rosetta Stone reflects the cult of Ptolemy V Epiphanes as part of a wider Ptolemaic
            ruler-cult that fused pharaonic and Greek religious traditions. Ptolemy V, who came to the throne as a
            child in 204 BCE, belonged to the Macedonian-Greek dynasty that had ruled Egypt since Alexander the Great&apos;s
            conquest.
          </p>
          <p>
            To secure their grip on power, the Ptolemies carefully cultivated an image of themselves as legitimate
            pharaohs and divine or semi-divine figures, relying heavily on the support of the Egyptian priestly elite.
            The decree on the Rosetta Stone was issued by a council of priests at Memphis and records how Ptolemy V had
            shown generosity to the temples, reduced taxation on some religious institutions, and generally affirmed his
            role as Egypt&apos;s protector. In return, the priesthood declared their loyalty to the king and ordered that
            this decree be inscribed in the standard temple-ritual formats: hieroglyphs (the "writing of the gods"),
            Demotic (the script of everyday Egyptian administration), and Greek (the language of the new ruling elite).
          </p>
          <p>
            This cult of Ptolemy V was not merely political propaganda; it was part of a structured religious program in
            which the king was treated as a living god-king or at least as a divinely-favoured ruler. Laws, festivals,
            and temple rituals were arranged to celebrate his benefactions and military victories, and his image often
            appeared in divine company, sometimes in the guise of the "Lord of Victory" or as a new incarnation of the
            traditional pharaonic ideal. The decree also hints at the complex power-sharing between the Ptolemaic court
            and the priesthood, in which the state granted temple privileges and tax relief, while the priests bolstered
            royal authority through ritual and public veneration. Over time, Ptolemy V&apos;s name and image were
            incorporated into the official cult-titles used in temple inscriptions, embedding his divine persona into
            the calendar of rites and offerings.
          </p>
          <p>
            In this way, the Rosetta Stone is not only a linguistic key, but also a snapshot of the royal-cult ideology
            that helped bind the Greek-speaking monarchy to the deeply rooted religious world of ancient Egypt.
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
