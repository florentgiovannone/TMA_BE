import fallenMadonnaImage from "../assets/fallen-madonna.png"
import Footer from "../components/Footer"
import "../styles/style.css"
import AudioPlayer from "../components/AudioPlayer"
import pageAudio from "../assets/Audio/ElevenLabs_The_Fallen_Madonna_with_the_Big_Boobies.mp3"

export default function GalleryNouvionPage() {
  return (
    <>
      <main className="tma-gallery-page">
        <header className="tma-header">
          <div className="tma-header-inner">
            <h1 className="tma-page-title">
              The Fallen Madonna with the Big Boobies
            </h1>
            <p className="tma-page-subtitle">
              1795 by Hertog van Klomp
            </p>
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
            src={fallenMadonnaImage}
            alt="The Fallen Madonna with the Big Boobies by Hertog van Klomp"
            className="tma-painting-image"
          />



          <h2>About the painting.</h2>
          <p>
            The work was completed in 1795 as the result of a commission by the French ambassador to the Batavian
            Republic, Charles-Francois Delacroix. Delacroix was a client of the notable art dealer Thomas Harvey after
            he had seen a flattering portrait of Harvey&apos;s wife painted by Hertog. It is rumoured the Fallen Madonna
            was made as a portrait of Delacroix&apos;s mistress, Alice de Quoi-sur-Balcon.
          </p>
          <p>
            It is the only known surviving work of art by Hertog van Klomp, by virtue of it leaving Holland for
            Bordeaux with Delacroix upon his retirement, and thus escaping the later all-consuming fire at Hertog&apos;s
            studio.
          </p>
          <p>
            Following the death of Delacroix, the painting was sold to cover the significant debts owed by Delacroix&apos;s
            Bordeaux estate, to a local Bordeaux wine merchant.
          </p>
          <p>
            The Fallen Madonna was thus lost to public knowledge for just over 200 years, until it re-appeared after
            being sold at auction in 2018, and was put on display in a bar in Nouvion, North-West France. There is
            speculation that the auction was a &apos;set-up&apos;, with the sale appearing to be fixed at a nominal amount to
            minimise french inheritance tax payable at the time, with a comprehensive back-story in place and widely
            published through contemporary sources to obscure its real provenance and value.
          </p>
          <p>
            The painting remains one of the few late-rococo period masterpieces in private hands, on display to the
            public.
          </p>

          <h2>About the artist.</h2>
          <p>
            Hertog van Klomp was born in Rotterdam in 1767 to Robert Jacob Gordon, a Dutch seafarer; explorer, artist,
            naturalist and officer in the Dutch East India company, and to Margiela Margolies daughter to Willem and
            Sophia Margolies, he, a local grain merchant native to Rotterdam.
          </p>
          <p>
            Shortly after the birth &apos;Jacob&apos; set sail to the East Indies. He lost all contact with his family, and
            Mariela believed him to be lost at sea. She was left without means of support, and she raised the infant
            Hertog on her own within the orbit of her parents&apos; wider family. She struggled financially most of their
            life together, living from undocumented and haphazard income. In 1776 Mariela died, the cause of death
            believed to be syphilis, a common illness in the city. Hertog was left orphaned at the age of 9.
          </p>
          <p>
            Rather than be committed to an orphanage, Hertog was taken into his aunt&apos;s family by his mother&apos;s eldest
            sister Fokje van Klomp. He dropped his own surname, Gordon, and was given that of his new family and adopted
            father, Sicco van Klomp.
          </p>
          <p>
            The teenage Hertog exhibited a prodigious artistic talent, by when aged 17, he was apprenticed to the art
            dealer Thomas Harvey. Harvey used him to develop connections with local artists and studios from whom he
            sourced works to import back to Norwich, England. This also allowed Hertog to develop his own interests and
            style (late-rococo influenced Neoclassical), painting his own works, and occasionally distributing them
            through his ever growing network of connections to supplement his income.
          </p>
          <p>
            As France&apos;s grip on power tightened over the Batavian Republic, Napoleon Bonaparte assumed power and
            created the Kingdom of Holland by installing Louis Napoleon as king.
          </p>
          <p>
            As fire spread through parts of Rotterdam in 1809, as a result of civil unrest and rioting due to protests
            against Louis Bonaparte&apos;s drafting of orphans into military service, flames caused widespread destruction
            and casualties.
          </p>
          <p>
            Hertog van Klomp died trapped in his studio, engulfed by flames. He perished alongside all but a handful of
            his works, leaving the world with little record with which to celebrate his important achievements as an
            artist.
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
