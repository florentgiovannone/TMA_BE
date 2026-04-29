import Footer from "../components/Footer"
import "../styles/style.css"
import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"

export default function UnderlyingTechnologyPage() {
  const navigate = useNavigate()
  const [showBackButton, setShowBackButton] = useState(false)

  useEffect(() => {
    const ref = document.referrer
    const sameOrigin = ref && ref.startsWith(window.location.origin)
    const hasReferrer = Boolean(sameOrigin && ref !== window.location.href)

    // Only show when we likely came from another page in this app.
    setShowBackButton(hasReferrer && window.history.length > 1)
  }, [])

  return (
    <>
      <main className="tma-gallery-page">
        <header className="tma-header tma-underlying-header">
          {showBackButton && (
            <button type="button" className="tma-underlying-back-button" onClick={() => navigate(-1)}>
              Go back
            </button>
          )}

          <div className="tma-header-inner">
            <h1 className="tma-page-title">Underlying Technology</h1>
            <p className="tma-page-subtitle">Overview of the Genie Tag.</p>
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

          <h2>Overview of the Genie Tag.</h2>
          <p>
            The Genie is a unique, patent pending, NFC technology designed to provide friction-free access and
            &apos;absolute proof of presence&apos; when accessing point-of-information services.
          </p>
          <p>
            This technology allows information providers enormous scope in the accurate delivery of information across a
            vast field of applications, and moreover, importantly it delivers to the provider accurate individual
            tracing information about how, when, where, and by whom* that information is accessed.
          </p>
          <p>
            The technology is un-fakeable, with inherent fortress-like security which allows providers the ability to
            rely absolutely on the integrity of the data it acquires.
          </p>
          <p>
            On the other side of the coin it allows information providers the ability to optimise the delivery of their
            information assets in a way that enhances the user experience, improves revenue generation, and manages
            costs.
          </p>
          <p>This translates into an enormous variety of commercial and social-benefit applications.</p>

          <p>Some examples of application include:</p>
          <ul>
            <li>Galleries</li>
            <li>Museums</li>
            <li>Restaurants &amp; hospitality services</li>
            <li>Event management</li>
            <li>Building safety</li>
            <li>Social care settings</li>
            <li>Health services management</li>
            <li>Visitor experiences management</li>
            <li>Advertising and marketing services</li>
            <li>Hotel/lodging facilities provision and safety</li>
            <li>Entertainment supply and management</li>
          </ul>

          <p>and many more.</p>

          <p>For further information contact:</p>
          <p>Poise Infotech Limited</p>

          <p>*subject to relevant privacy permission regulations.</p>
        </div>


      </main>
      <Footer />
    </>
  )
}
