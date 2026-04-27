import Footer from "../components/Footer"
import "../styles/style.css"

export default function ContactPage() {
  return (
    <>
      <main className="tma-gallery-page">
        <header className="tma-header">
          <div className="tma-header-inner">
            <h1 className="tma-page-title">Contact</h1>
          </div>
        </header>

        <div className="tma-content">

          <section className="tma-contact-grid">
            <article className="tma-contact-card">
              <h2>Get in Touch</h2>
              <p>
                For partnerships, exhibitions, technical support, or any questions about Take Me Around, please contact
                us using the details below.
              </p>
              <p>
                <strong>Email:</strong> info@takemearound.com
              </p>
              <p>
                <strong>Phone:</strong> +44 (0)20 0000 0000
              </p>
            </article>

            <article className="tma-contact-card">
              <h2>Office Address</h2>
              <p>Take Me Around Ltd.</p>
              <p>Parkgate House, 33a Pratt Street</p>
              <p>London, NW1 0BG</p>
              <p>United Kingdom</p>
            </article>
          </section>

          <section className="tma-map-section">
            <h2>Find Us</h2>
            <div className="tma-map-frame-wrap">
              <iframe
                title="Take Me Around office map"
                className="tma-map-frame"
                src="https://www.google.com/maps?q=Parkgate+House,+33a+Pratt+Street,+NW1+0BG&output=embed"
                loading="lazy"
              />
            </div>
          </section>
        </div>
      </main>
      <Footer />
    </>
  )
}
