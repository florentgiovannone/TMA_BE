import suttonHooHelmetImage from "../assets/sutton-hoo-helmet.png"
import Footer from "../components/Footer"
import "../styles/style.css"
import AudioPlayer from "../components/AudioPlayer"
import pageAudio from "../assets/Audio/ElevenLabs_The_Sutton_Hoo_helmet.mp3"

export default function SuttonHooHelmetPage() {
  return (
    <>
      <main className="tma-gallery-page">
        <header className="tma-header">
          <div className="tma-header-inner">
            <h1 className="tma-page-title">The Sutton Hoo helmet</h1>
            <p className="tma-page-subtitle">Circa 620 to 625 CE by Anglo-Saxon armorers</p>
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
          <img src={suttonHooHelmetImage} alt="The Sutton Hoo helmet" className="tma-painting-image" />

          <h2>About the Helmet.</h2>
          <p>
            The Sutton Hoo helmet is one of the most iconic objects to survive from early medieval Europe, an
            elaborately decorated Anglo-Saxon iron helmet discovered in 1939 in the ship-burial at Sutton Hoo in
            Suffolk, England. The helmet is thought to have been buried there around 620-625 CE, in the grave of a
            high-status leader-most likely King Raedwald of East Anglia-and it combines both practical armour and
            sumptuous, symbolic display. Weighing about 2.5 kg, the helmet&apos;s core is made of iron, covered with thin
            sheets of tinned bronze that were stamped with intricate designs, then further embellished with a crest,
            eyebrows, a nose-and-mouth piece, and three dragon-style heads, turning the warrior&apos;s face into a roaring,
            almost supernatural mask.
          </p>
          <p>
            When excavated, the helmet had collapsed under the weight of the burial chamber and lay in hundreds of
            corroded fragments, mixing iron rust with the now-greenish tinned bronze and loose garnets. Conservators
            painstakingly reassembled it like a 3D jigsaw, using the positional evidence from the dig; the
            reconstructed version you see in the British Museum is a composite of the original fragments mounted on a
            supportive framework. The surviving panels show a rich array of imagery: two figural scenes (often called
            "The Dancing Warriors" and "The Fallen Warrior"), interlaced animal patterns, and decorative elements that
            echo the spiral and zoomorphic styles of early Germanic and Insular art. The helmet&apos;s articulated cheek
            and neck guards could be pulled flush with the face mask, fully enclosing the wearer, and the interior
            still bears traces of a leather lining, suggesting it was worn in life before being placed in the grave as
            a royal heirloom.
          </p>
          <p>
            Beyond its function as battlefield protection, the Sutton Hoo helmet clearly served as a symbol of royal
            power and prestige, blazing with light-catching metal and shining garnets in the feasting hall and on the
            battlefield. Some scholars have even suggested that its elaborate form anticipates later European crowns,
            blurring the line between helmet and crown in the symbolic vocabulary of kingship. Today it is regarded as
            one of the most important Anglo-Saxon artefacts ever found, a masterpiece of both metallurgy and visual
            storytelling that embodies the martial, ritual, and artistic world of early English kingship.
          </p>

          <h2>About the Anglo-Saxons</h2>
          <p>
            The Anglo-Saxons were the Germanic peoples who settled in lowland Britain from the 5th century CE onward,
            forming the kingdoms that would eventually become England. They came mainly from what is now Denmark,
            northern Germany, and the Low Countries-groups such as the Angles, Saxons, and Jutes-and over time they
            established a patchwork of small, rival kingdoms like East Anglia, Kent, Mercia, Northumbria, and Wessex.
            These kingdoms were initially pagan, warrior-oriented polities, in which loyalty to kings and warlords, and
            the ability to fight effectively, formed the backbone of social order. The Sutton Hoo ship-burial, with its
            helmet, weapons, shield, ship, and treasures, reflects the values of such a society: a world of elite
            warriors, rich grave-goods, and ritualised displays of power staged in the shadow of both pagan belief and
            the slowly spreading Christian faith.
          </p>
          <p>
            By the 7th century, many Anglo-Saxon rulers had converted to Christianity, often through contacts with the
            Roman Church and the Irish mission, but they did not simply abandon their older customs. Instead, they
            blended the two worlds: scriptoria in monasteries produced beautifully illuminated manuscripts, while still
            valuing the heroic poetry and warrior imagery that appear, for example, in the decorative schemes of objects
            like the Sutton Hoo helmet. The Anglo-Saxons developed a distinct artistic style, characterised by
            interlaced animals, spirals, and tightly woven decorative patterns, which appears across metalwork,
            jewellery, stone crosses, and manuscripts such as the Lindisfarne Gospels. This style, sometimes called
            Insular art, shows how the Anglo-Saxons combined local Germanic traditions with continental and Mediterranean
            influences to create something uniquely their own.
          </p>
          <p>
            Anglo-Saxon society was also highly structured and hierarchical, built around the king, the warrior
            nobility, the free peasantry, and the clergy. Power rested on the ability to command loyal followings,
            distribute wealth in gifts and feasts, and defend the land from enemies. The hoards and rich burials such
            as Sutton Hoo testify to the importance of status and material display, while the later written records-such
            as the Anglo-Saxon Chronicle and legal codes like those of King Aethelberht of Kent-show how these
            communities were experimenting with law, administration, and literacy. The Sutton Hoo helmet, therefore, is
            not just a technical marvel of early metalworking; it is a concrete expression of the Anglo-Saxon worldview-a
            world where kingship, warfare, ritual, artistry, and the memory of the dead were all bound together in the
            gleaming, fierce image of the warrior king.
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
