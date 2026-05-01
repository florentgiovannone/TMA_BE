import cyrusCylinderImage from "../assets/cyrus-cylinder.png"
import Footer from "../components/Footer"
import "../styles/style.css"
import AudioPlayer from "../components/AudioPlayer"
import pageAudio from "../assets/Audio/ElevenLabs_The_Cyrus_Cylinder.mp3"

export default function CyrusCylinderPage() {
  return (
    <>
      <main className="tma-gallery-page">
        <header className="tma-header">
          <div className="tma-header-inner">
            <h1 className="tma-page-title">The Cyrus Cylinder</h1>
            <p className="tma-page-subtitle">559-530 BCE from the Babylonian People</p>
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
          <img src={cyrusCylinderImage} alt="The Cyrus Cylinder" className="tma-painting-image" />

          <h2>About the Cyrus Cylinder.</h2>
          <p>
            The Cyrus Cylinder is a small barrel-shaped clay cylinder from the 6th century BCE, inscribed all around
            with a royal proclamation in Akkadian cuneiform using the Babylonian dialect. It dates to the period
            shortly after the Persian king Cyrus the Great (r. 559-530 BCE) captured Babylon in 539 BCE, bringing the
            Babylonian Empire into the expanding Achaemenid Persian state.
          </p>
          <p>
            The text describes how the previous Babylonian ruler, Nabonidus, had offended the gods, especially Marduk,
            the city-god of Babylon, by neglecting the proper cults and imposing harsh labour on the population.
            According to the inscription, Marduk then chose Cyrus as his champion, guiding him peacefully into Babylon
            and establishing him as the legitimate king accepted by both the gods and the people.
          </p>
          <p>
            Beyond this political theology, the Cylinder presents Cyrus as a restorer of order and piety: he claims to
            have ended forced labour, repaired the city walls of Babylon, reinstated displaced divine statues to their
            temples, and allowed various deported peoples to return to their homelands and rebuild their shrines. This
            last point is particularly famous because, in the Hebrew Bible, Cyrus is credited with ending the Babylonian
            exile of the Judeans and permitting them to rebuild the Temple in Jerusalem. For this reason some modern
            commentators have described the Cylinder as an early "declaration of human rights," although scholars more
            cautiously see it as a standard Babylonian royal propagandistic text adapted to justify new Persian rule.
          </p>
          <p>
            The object was discovered in the ruins of Babylon in 1879 during a British Museum excavation, and today the
            inscribed clay fragment is one of the most celebrated artefacts in the British Museum&apos;s collection,
            widely printed, reproduced, and cited in discussions of ancient empire, religion, and early ideas of
            tolerance.
          </p>

          <h2>About the Babylonian People</h2>
          <p>
            The Babylonians were the people of Babylonia, a major Mesopotamian civilization centered on the city of
            Babylon in what is now southern Iraq. Rooted in the older Sumerian and Akkadian cultures, the Babylonians
            spoke a dialect of Akkadian, a Semitic language, and wrote in cuneiform script on clay tablets, palace
            walls, and stelae.
          </p>
          <p>
            Their society was hierarchical, usually divided into elites such as the king, nobles, and high priests,
            ordinary free citizens (farmers, artisans, merchants), and slaves, with the family and temple-based urban
            institutions forming the backbone of daily life. The economy rested on intensive agriculture in the rich
            alluvial land between the Tigris and Euphrates rivers, supported by an elaborate system of canals, as well
            as long-distance trade that connected Babylon to Anatolia, the Levant, and the Gulf.
          </p>
          <p>
            Babylonian culture was deeply religious and literate, with temples and their priesthoods playing a central
            role in both spiritual and administrative life. The god Marduk rose to prominence as the chief deity of
            Babylon, especially in the period of the Old Babylonian Empire under Hammurabi and later the Neo-Babylonian
            Empire under kings such as Nebuchadnezzar II. The Babylonians built massive ziggurats (stepped temple
            towers), palaces adorned with glazed brick and animal reliefs, and ceremonial streets such as the Ishtar
            Gate processional way, all of which testify to their architectural and artistic sophistication.
          </p>
          <p>
            They also produced some of the earliest known legal codes, most famously the Code of Hammurabi, as well as
            rich literary traditions that include the Epic of Gilgamesh and vast collections of omens, lists, and
            scientific texts. Even under later foreign rulers, such as the Assyrians and the Achaemenid Persians,
            Babylon remained a key cultural and religious center, and its traditions continued to influence the religious
            and intellectual life of the wider Near East.
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
