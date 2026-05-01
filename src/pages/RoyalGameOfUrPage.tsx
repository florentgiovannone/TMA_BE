import royalGameOfUrImage from "../assets/royal-game-of-ur.png"
import Footer from "../components/Footer"
import "../styles/style.css"
import AudioPlayer from "../components/AudioPlayer"
import pageAudio from "../assets/Audio/ElevenLabs_The_Royal_Game_of_Ur.mp3"

export default function RoyalGameOfUrPage() {
  return (
    <>
      <main className="tma-gallery-page">
        <header className="tma-header">
          <div className="tma-header-inner">
            <h1 className="tma-page-title">The Royal Game of Ur</h1>
            <p className="tma-page-subtitle">Circa 2600-2400 BCE, Sumeria</p>
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
          <img src={royalGameOfUrImage} alt="The Royal Game of Ur" className="tma-painting-image" />

          <h2>About  The Royal Game of Ur.</h2>
          <p>
            The Royal Game of Ur is one of the oldest known playable board games, dating back to the early third
            millennium BCE in ancient Mesopotamia. The name comes from the Sumerian city of Ur, where British
            archaeologist Sir Leonard Woolley discovered several beautifully inlaid game boards in royal tombs during
            excavations in the 1920s; the finest surviving example, now in the British Museum, is dated to about
            2600-2400 BCE, making it one of the earliest complete game boards ever found. The game is a two-player race
            game in which each player moves seven pieces along a twenty-square board, trying to get all their tokens
            off the board before the opponent does, using a set of four-sided dice (often described as tetratrahedron-shaped
            "throw sticks") to determine movement.
          </p>
          <p>
            The board itself is a striking, almost jewel-like object: a rectangular wooden frame inlaid with a pattern
            of twenty squares, arranged in three rows of four on one side and three rows of two on the other, linked
            by a central "bridge" of two squares. Many of the original Ur boards were decorated with shell, red
            limestone, and lapis lazuli, forming intricate geometric and rosette motifs that underline the game&apos;s
            association with elite, royal circles. The so-called "rosette" squares are especially important-they are
            safe spaces that protect pieces from being captured and sometimes grant the player an extra throw of the
            dice, adding a layer of both luck and strategy.
          </p>
          <p>
            The game&apos;s rules remained largely unknown until the 1980s, when the British-Museum curator Irving Finkel
            translated a Babylonian cuneiform tablet from around 177 BCE that describes how the game was played,
            including the meanings of the board&apos;s central twelve squares, which were linked to omens and individual
            fortunes (such as drawing "fine beer" or becoming "powerful like a lion"). This discovery allowed scholars
            to reconstruct a historically plausible version of the rules, and today the Royal Game of Ur is not only
            studied as a key example of early game design but also widely played by enthusiasts worldwide. Its
            influence can be traced through later "race-and-backgammon-type" games, and its survival across thousands
            of years makes it a powerful symbol of how ancient people used games for entertainment, ritual, and social
            bonding.
          </p>

          <h2>About The Sumerians</h2>
          <p>
            The Sumerians were the people of Sumer, the earliest known civilization in southern Mesopotamia, flourishing
            in what is now southern Iraq from roughly 4500-1900 BCE. They developed the world&apos;s first city-states-such
            as Ur, Uruk, and Eridu-centred on monumental temples (ziggurats) and complex irrigation systems that turned
            the marshy alluvial plain into rich farmland. Sumerian society was stratified, with a ruling elite of
            priests, kings, and scribes overseeing a population of farmers, herders, and artisans. Power was closely
            tied to religion, with the city-god and the temple-complex at the heart of political, economic, and ritual
            life.
          </p>
          <p>
            One of the Sumerians&apos; most transformative inventions was writing. They created cuneiform, a script of
            wedge-shaped marks pressed into wet clay tablets, initially for administrative and economic record-keeping
            but later used for literature, law, and religious texts. Through cuneiform, the Sumerians preserved some of
            the earliest literary works, including stories that later influenced the myths and epics of surrounding
            cultures, and they developed sophisticated systems of mathematics, law, and astronomy. Their city-states,
            though often independent and rivalrous, were tied together by shared language, religion, and urban culture,
            and they set the template for the later Mesopotamian civilizations of Akkad, Babylon, and Assyria.
          </p>
          <p>
            The Royal Game of Ur is strongly associated with the Sumerians, both because the earliest known complete
            boards come from the Sumerian city of Ur and because it fits into a broader Sumerian interest in games,
            gambling, and ritualized play that linked chance and fate with divine will. Game boards, dice, and tokens
            appear in Sumerian and later Mesopotamian contexts, sometimes used in oracles or divination, suggesting
            that games were not only leisure activities but also tools for understanding the gods&apos; messages. In this
            way, the Royal Game of Ur becomes a small but vivid window into the minds of the Sumerians: a people who
            combined practical innovation, bureaucratic precision, and religious imagination with a deep enjoyment of
            competition, pattern, and play.
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
