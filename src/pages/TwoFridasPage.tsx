import twoFridasImage from "../assets/two-fridas.png"
import Footer from "../components/Footer"
import "../styles/style.css"
import AudioPlayer from "../components/AudioPlayer"
import pageAudio from "../assets/Audio/ElevenLabs_The_Two_Fridas.mp3"

export default function TwoFridasPage() {
  return (
    <>
      <main className="tma-gallery-page">
        <header className="tma-header">
          <div className="tma-header-inner">
            <h1 className="tma-page-title">The Two Fridas</h1>
            <p className="tma-page-subtitle">1939 by Frida Kahlo</p>
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
          <img src={twoFridasImage} alt="The Two Fridas by Frida Kahlo" className="tma-painting-image" />

          <h2>About the painting.</h2>
          <p>
            The Two Fridas is one of Frida Kahlo&apos;s largest and most iconic paintings, completed in 1939 at a moment
            of intense personal and emotional upheaval. The work shows two versions of the artist seated side by side
            on a bench, holding hands, their bodies linked by a single exposed vein that connects their hearts.
          </p>
          <p>
            The figures mirror each other yet differ in dress and expression: one is dressed in a traditional Tehuana
            outfit associated with Mexican indigenous culture, while the other wears a white European-style dress,
            creating a visual contrast between Mexican identity and colonial heritage.
          </p>
          <p>
            The painting is widely interpreted as a reflection of Kahlo&apos;s inner duality-caught between her Mexican
            roots and European ancestry, between strength and vulnerability, between the self she presented to the world
            and the self that suffered privately.
          </p>
          <p>
            The exposed anatomy, the visible hearts, and the blood staining the white dress directly reference pain,
            heartbreak, and the fragility of the human body, themes that recur throughout her art.
          </p>
          <p>
            The Two Fridas also coincides with the period of her divorce from artist Diego Rivera, which deepened its
            emotional resonance as a portrayal of emotional rupture, self-examination, and the struggle to hold oneself
            together after a major loss.
          </p>

          <h2>About the artist.</h2>
          <p>
            The Two Fridas was painted by Frida Kahlo (1907-1954), a Mexican artist whose work is celebrated for its
            raw emotional honesty, surreal symbolism, and deep engagement with questions of identity, gender, and the
            body.
          </p>
          <p>
            Born in Coyoacan, Mexico City, Kahlo developed a distinctive style that blended elements of Mexican folk
            art, indigenous symbolism, and European modernism, often using self-portraits to explore her physical
            suffering, emotional turmoil, and political beliefs.
          </p>
          <p>
            A serious bus accident in her youth left her with lifelong chronic pain and numerous surgeries, experiences
            that profoundly shaped her art and gave her a unique perspective on the body as both a site of suffering
            and a canvas for expression.
          </p>
          <p>
            Kahlo&apos;s life and work were closely tied to the Mexican cultural and political landscape of the early 20th
            century. She was married to the muralist Diego Rivera, whose influence and turbulence color much of her
            imagery, yet she steadfastly developed a voice that was unmistakably her own.
          </p>
          <p>
            In The Two Fridas, her fusion of personal narrative and symbolic language turns the canvas into a visual
            autobiography, where the two figures are not just two versions of Frida but also a statement about the
            fractured nature of identity, the costs of love lost, and the resilience required to survive.
          </p>
          <p>
            Through this painting and many others, Kahlo became a central figure in modern art, especially for later
            generations of feminist and Latin American artists who see her as both a cultural icon and a deeply human
            storyteller.
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
