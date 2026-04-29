import qingmingFestivalImage from "../assets/qingming-festival.png"
import Footer from "../components/Footer"
import "../styles/style.css"
import AudioPlayer from "../components/AudioPlayer"
import pageAudio from "../assets/Audio/ElevenLabs_Along_the_River_During_Qingming_Festival.mp3"

export default function QingmingFestivalPage() {
  return (
    <>
      <main className="tma-gallery-page">
        <header className="tma-header">
          <div className="tma-header-inner">
            <h1 className="tma-page-title">Along the River During Qingming Festival</h1>
            <p className="tma-page-subtitle">12th century by Zhang Zeduan (attributed)</p>
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

          <img
            src={qingmingFestivalImage}
            alt="Along the River During Qingming Festival detail"
            className="tma-painting-image"
          />

          <h2>About the painting.</h2>
          <p>
            Along the River During the Qingming Festival is one of the most iconic and ambitious works in the history
            of Chinese painting, a monumental handscroll that unfolds as a sweeping visual narrative of daily life in
            the Northern Song-dynasty capital, Bianliang (modern-day Kaifeng), along the banks of the Bian River.
            Created in the early 12th century, the scroll captures a bustling urban world in extraordinary detail,
            portraying a continuous, panoramic view that stretches from the rural outskirts into the dense heart of
            the city. Along its length, viewers encounter hundreds of figures-merchants haggling over goods, laborers
            hauling cargo, officials in official robes, and travelers passing through the city gates-each rendered with
            individualized gestures and activities, suggesting a society in constant motion.
          </p>
          <p>
            The streets are lined with shops, teahouses, inns, and workshops, while the river itself teems with boats
            of all sizes, from small fishing skiffs to large cargo vessels. Bridges, pagodas, city walls, and
            temporary market stalls appear alongside domestic scenes of families at home or villagers working in the
            fields, forming a rich tapestry of social, economic, and cultural life. The composition is carefully
            structured as a rhythmic progression from right to left, weaving together moments of calm and activity, as
            the landscape shifts from open countryside to tightly packed urban blocks. At the heart of the scroll
            stands the famous wooden "Rainbow Bridge," an arched structure that arches over the river like an elegant
            arc; around it, a dramatic vignette unfolds in which a large boat tilts dangerously as it approaches the
            bridge, threatening to collide with the structure while onlookers scramble and shout, lending the scene a
            vivid sense of immediacy and tension.
          </p>
          <p>
            Beyond its artistic brilliance, Along the River During the Qingming Festival functions as an invaluable
            historical document, preserving details of architecture, clothing, transportation, and urban planning that
            help scholars reconstruct the lived experience of an 11th- to 12th-century Chinese metropolis. The
            painting&apos;s scale, precision, and narrative depth make it not only a masterpiece of technical achievement
            but also a window into the rhythms, conflicts, and everyday joys of life in one of the world&apos;s most
            sophisticated pre-modern cities.
          </p>

          <h2>About the artist.</h2>
          <p>
            The original scroll is traditionally attributed to Zhang Zeduan (ca. 1085-1145), a court painter active
            during the Northern Song dynasty, though surviving biographical details about him are sparse and often
            inferred from later accounts rather than firsthand records. What is clear from his surviving work is a
            remarkable eye for both the grand scale of urban space and the smallest human details, suggesting that he
            was likely trained in the imperial painting academy, where precision, composition, and draughtsmanship were
            rigorously cultivated. His mastery of linear perspective, subtle shifts in scale, and complex overlapping
            rows of figures show a deep understanding of spatial organization far beyond simple decorative ornament.
          </p>
          <p>
            Zhang Zeduan&apos;s Along the River During the Qingming Festival stands out for the way it balances
            documentary realism with an almost cinematic sense of movement. Rather than presenting a static, idealized
            cityscape, he arranges the scroll so that scenes unfold gradually, inviting the viewer to "walk" through
            the city and discover new vignettes with each turn of the handscroll. The care with which he renders
            individual faces, postures, and activities-down to the way a boatman leans into his oar or a merchant
            adjusts his robes-suggests both acute observation and a genuine interest in the full spectrum of human
            life, from the powerful to the humble.
          </p>
          <p>
            In the centuries that followed, Zhang&apos;s composition became a model for later generations of painters in
            imperial China. During the Ming and Qing dynasties, numerous artists produced new versions of the scroll,
            enlarging the scale, adding luxury pavilions, imperial processions, or more elaborate festivities, each
            adapting the composition to suit their own tastes and patrons&apos; expectations.
          </p>
          <p>
            As a result, multiple copies and reinterpretations of Along the River During the Qingming Festival exist
            today, each offering its own variant on the original theme. Yet the Song-dynasty version, now housed in
            the Palace Museum in Beijing, remains the foundational and most revered exemplar of this tradition,
            continuing to shape how scholars, artists, and the public alike understand both the visual culture and the
            social world of China&apos;s high medieval period.
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
