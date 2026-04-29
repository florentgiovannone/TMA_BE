import lewisChessmenImage from "../assets/lewis-chessmen.png"
import Footer from "../components/Footer"
import "../styles/style.css"
import AudioPlayer from "../components/AudioPlayer"
import pageAudio from "../assets/Audio/ElevenLabs_The_Lewis_Chessmen.mp3"

export default function LewisChessmenPage() {
  return (
    <>
      <main className="tma-gallery-page">
        <header className="tma-header">
          <div className="tma-header-inner">
            <h1 className="tma-page-title">The Lewis Chessmen</h1>
            <p className="tma-page-subtitle">A Norse Artisan</p>
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
          <img src={lewisChessmenImage} alt="The Lewis Chessmen" className="tma-painting-image" />

          <h2>About the The Lewis Chessmen.</h2>
          <p>
            The Lewis Chessmen are a group of small, intricately carved medieval gaming pieces, most of which were
            made from walrus ivory and a few from whale tooth, believed to date from around 1150-1200 CE. They were
            discovered in 1831 hidden in a sandbank on the Isle of Lewis in the Outer Hebrides of Scotland, where they
            had been buried in a hoard that originally contained 94 objects: 78 chess pieces, 14 tablemen (used for
            backgammon-like games), and one belt buckle. Today, most of the collection-82 pieces-is held by the British
            Museum in London, while 11 chessmen are displayed at the National Museum of Scotland in Edinburgh, with at
            least one piece in a private collection.
          </p>
          <p>
            The pieces show the classic medieval European chess set in a highly characterful form: seated kings and
            queens, bishops with mitres, knights on horseback, warders (rooks) and pawns shaped like slender,
            obelisk-like blocks. The kings and queens sit on ornate thrones, often with long beards, elaborate
            headgear, and folds of rich robes, while the warders stand grimly biting their shields, some with fierce,
            almost berserker-like faces. The individuality of the carvings-each figure with a slightly different
            expression, posture, or costume detail-suggests that the workshop that produced them was staffed by skilled
            artisans who treated these luxury game-pieces as small works of art, not mass-produced toys. Scholars
            generally believe the hoard represents parts of at least four separate chess sets, possibly stored or
            traded together, and they were likely made in western Norway, most probably in Trondheim, a major centre of
            walrus-ivory carving at the time.
          </p>
          <p>
            At the time the chessmen were buried in the 12th or early 13th century, the Western Isles of Scotland were
            under the overlordship of the Norwegian crown, so the objects sit at the intersection of Scandinavian
            craftsmanship and the wider Gaelic-Norse world. They testify to the popularity of chess across northern
            Europe, as well as to long-distance trade in luxury materials such as walrus ivory, which was hunted in the
            North Atlantic and carved into precious objects for wealthy elites.
          </p>
          <p>
            The Lewis Chessmen have become some of the most famous and beloved medieval artefacts in Britain, endlessly
            reproduced in books, replicas, and even modern chess sets, and they continue to captivate audiences with
            their miniature, almost theatrical cast of kings, queens, bishops, knights, and warders frozen in play.
          </p>

          <h2>About The Norse</h2>
          <p>
            The Norse (often called Vikings in popular usage) were the seafaring peoples of Scandinavia-Norway, Sweden,
            and Denmark-during the Viking Age (roughly 793-1066 CE), known for their ship-building skills, long-distance
            voyages, and profound impact on medieval Europe. Originating from rural farming communities, the Norse sailed
            far beyond their homelands, establishing settlements in the British Isles, Iceland, Greenland, and even parts
            of North America, as well as trading and raiding routes that stretched from the Baltic and Russia to the
            Mediterranean and the Middle East. Their society was organized around extended kinship groups, local chieftains,
            and warrior-aristocrats, with a strong emphasis on personal honour, skill in battle, and loyalty to one&apos;s
            lord and kin.
          </p>
          <p>
            Culturally and spiritually, the Norse followed a complex pagan belief system centred on gods such as Odin,
            Thor, and Freyja, alongside a rich oral tradition of myths, sagas, and poetry that preserved both heroic
            narratives and reflections on fate, bravery, and mortality. Writing in runic script on stone, wood, and
            metal, they recorded names, commemorations, and sometimes magical or protective formulas, while their
            long-ship burial and grave-goods traditions show deep concern for the afterlife. Over time, from the 10th
            century onward, increasing contact with Christian Europe and the political advantages of alliance with
            Christian rulers led many Norse communities to convert to Christianity, blending older customs with the new
            faith in distinctive ways.
          </p>
          <p>
            The Norse also left a powerful material legacy in the forms of carvings, metalwork, and games. The Lewis
            Chessmen, though found in Scotland, are Scandinavian in style and origin, crafted in the Norse-controlled
            or Norse-influenced North Sea world, and they reflect the Norse love of competitive board games such as
            hnefatafl and, later, chess itself. These games were not merely pastimes; they were associated with
            strategy, status, and the warrior values of foresight, patience, and decisive action. Through objects like
            the chessmen, the Norse world-its trade networks, artistic tastes, and cultural bridges to the Gaelic and
            Christian realms-remains vividly visible in the present.
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
