import monaLisaImage from "../assets/mona-lisa.png"
import Footer from "../components/Footer"
import "../styles/style.css"
import AudioPlayer from "../components/AudioPlayer"
import pageAudio from "../assets/Audio/ElevenLabs_Mona_Lisa.mp3"
export default function MonaLisaPage() {
  return (
    <>
      <main className="tma-gallery-page">
        <header className="tma-header">
          <div className="tma-header-inner">
            <h1 className="tma-page-title">Mona Lisa</h1>
            <p className="tma-page-subtitle">1503-1519 by Leonardo da Vinci</p>
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
          <img src={monaLisaImage} alt="Mona Lisa by Leonardo da Vinci" className="tma-painting-image" />
          <h2>About the painting.</h2>
          <p>
            Mona Lisa (also known as La Gioconda) is a half-length portrait oil painting on a poplar wood panel,
            created by Leonardo da Vinci sometime between about 1503 and 1519. It is widely regarded as one of the
            most famous and instantly recognizable paintings in the world, housed today in the Louvre Museum in Paris,
            where it draws millions of visitors each year. The work depicts a woman seated in a balanced, upright pose,
            her arms softly folded across her lap, her gaze meeting the viewer&apos;s eyes with a sense of quiet
            confidence and subtle intimacy. Her face is rendered through a series of delicate, translucent glazes that
            build up layers of light and shadow, giving her skin an almost lifelike warmth and a sense of
            psychological presence that feels remarkably modern.
          </p>
          <p>
            The sitter&apos;s famous "enigmatic smile" is one of the painting&apos;s most discussed features. It appears to
            shift depending on where the viewer looks, sometimes seeming to blooming into warmth, at other times
            retreating into ambiguity. This elusive expression is achieved through Leonardo&apos;s sfumato technique-a
            method of gradual, smoky transitions between colors and tones that eliminates sharp outlines and softens
            contours. Around the figure, a dreamlike landscape unfolds: winding rivers, distant bridges, and soft,
            hazy mountains rise and fade into a pale, atmospheric sky, creating a sense of depth and mystery that wraps
            the woman in nature rather than placing her against a static backdrop. The harmonious integration of the
            portrait and the landscape turns the Mona Lisa into more than a likeness; it becomes a meditation on
            personality, perception, and the subtle boundary between human presence and the world beyond.
          </p>
          <p>
            Over the centuries, the painting has also gained legendary status through its history-its theft in 1911,
            its role as a cultural icon in literature and popular media, and its monetary value (often cited as one of
            the most valuable paintings ever insured). Yet beyond its fame and notoriety, the Mona Lisa remains a
            pivotal work of Renaissance art, a benchmark for portraiture that influenced generations of painters and
            continues to be studied for its technical mastery, psychological nuance, and quiet emotional power.
          </p>

          <h2>About the artist.</h2>
          <p>
            Leonardo da Vinci was one of the greatest figures of the Italian Renaissance because he excelled in art,
            science, engineering, anatomy, and design all at once. Born in 1452 near Vinci in Tuscany, he was trained
            in Florence in the workshop of Andrea del Verrocchio, where he learned painting, sculpture, and technical
            skills that shaped his whole career.
          </p>
          <p>
            What makes Leonardo especially important is that he did not see art and science as separate fields. He
            studied the human body, light, motion, water, and nature so closely that his drawings and paintings often
            feel both beautiful and intensely realistic. His notebooks reveal an endlessly curious mind filled with
            observations, diagrams, and ideas for machines, which is why people still call him a true "Renaissance
            man".
          </p>
          <p>
            As a painter, Leonardo created some of the most famous works in Western art, including the Mona Lisa and
            The Last Supper. He was known for experimenting with oil paint, soft shading, and atmospheric backgrounds,
            especially through the technique called sfumato, which made his figures look gentle and alive. Even though
            many of his projects were unfinished or lost, the work that survives shows extraordinary precision,
            imagination, and control.
          </p>
          <p>
            Leonardo also made major contributions beyond painting. He studied anatomy through careful dissections,
            designed machines and weapons, and sketched ideas that foreshadowed later inventions such as flying
            machines and armored vehicles. In 1516 he moved to France under the patronage of Francis I, and he died
            there in 1519, leaving behind a legacy that still shapes how people think about creativity and genius.
          </p>
          <p>
            In short, Leonardo da Vinci was not just a famous artist; he was a thinker who tried to understand how the
            world worked and then turned that understanding into art. That is why his name remains one of the most
            admired in history.
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
