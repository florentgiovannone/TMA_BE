import { Link, Route, Routes, useLocation } from "react-router-dom"
import AudioPlayer from "./components/AudioPlayer"
import ContactPage from "./pages/ContactPage"
import CyrusCylinderPage from "./pages/CyrusCylinderPage"
import EdmondDeBelamyPage from "./pages/EdmondDeBelamyPage"
import GalleryNouvionPage from "./pages/GalleryNouvionPage"
import HoaHakananaiPage from "./pages/HoaHakananaiPage"
import LewisChessmenPage from "./pages/LewisChessmenPage"
import MonaLisaPage from "./pages/MonaLisaPage"
import PrivacyPolicyPage from "./pages/PrivacyPolicyPage"
import QingmingFestivalPage from "./pages/QingmingFestivalPage"
import RoyalGameOfUrPage from "./pages/RoyalGameOfUrPage"
import RosettaStonePage from "./pages/RosettaStonePage"
import StarryNightPage from "./pages/StarryNightPage"
import SuttonHooHelmetPage from "./pages/SuttonHooHelmetPage"
import TwoFridasPage from "./pages/TwoFridasPage"
import UnderlyingTechnologyPage from "./pages/UnderlyingTechnologyPage"
import "./styles/style.css"
import { useEffect } from "react"

const PAGE_TITLES: Record<string, string> = {
  "/": "Take Me Around",
  "/gallery-nouvion-4738593893849": "The Fallen Madonna with the Big Boobies",
  "/along-the-river-during-qingming-festival-by-zhang-zeduan-attributed-12th-century":
    "Along the River During Qingming Festival",
  "/hoa-hakananai-a": "Hoa Hakananaiʻa",
  "/mona-lisa": "Mona Lisa",
  "/portrait-of-edmond-de-belamy": "Portrait of Edmond de Belamy",
  "/the-cyrus-cylinder": "The Cyrus Cylinder",
  "/the-lewis-chessmen": "The Lewis Chessmen",
  "/the-rosetta-stone": "The Rosetta Stone",
  "/the-royal-game-of-ur": "The Royal Game of Ur",
  "/the-starry-night": "The Starry Night",
  "/the-sutton-hoo-helmet": "The Sutton Hoo helmet",
  "/the-two-fridas": "The Two Fridas",
  "/underlying-technology": "Underlying Technology",
  "/contact": "Contact",
  "/privacy-policy": "Privacy Policy",
}

function PageTitleUpdater() {
  const location = useLocation()

  useEffect(() => {
    const pageTitle = PAGE_TITLES[location.pathname]
    document.title = pageTitle ? `${pageTitle} | Take Me Around` : "Take Me Around"
  }, [location.pathname])

  return null
}



function HomePage() {
  return (
    <main style={{ margin: "0 auto", maxWidth: 900, padding: "2rem 1rem" }}>
      <h1>Take Me Around</h1>
      <p>Open the gallery page from the link below.</p>
      <p>
        <Link to="/gallery-nouvion-4738593893849">Go to Nouvion gallery page</Link>
      </p>
      <p>
        <Link to="/along-the-river-during-qingming-festival-by-zhang-zeduan-attributed-12th-century">
          Go to Qingming Festival page
        </Link>
      </p>
      <p>
        <Link to="/hoa-hakananai-a">Go to Hoa Hakananaiʻa page</Link>
      </p>
      <p>
        <Link to="/mona-lisa">Go to Mona Lisa page</Link>
      </p>
      <p>
        <Link to="/portrait-of-edmond-de-belamy">Go to Portrait of Edmond de Belamy page</Link>
      </p>
      <p>
        <Link to="/the-cyrus-cylinder">Go to The Cyrus Cylinder page</Link>
      </p>
      <p>
        <Link to="/the-lewis-chessmen">Go to The Lewis Chessmen page</Link>
      </p>
      <p>
        <Link to="/the-rosetta-stone">Go to The Rosetta Stone page</Link>
      </p>
      <p>
        <Link to="/the-royal-game-of-ur">Go to The Royal Game of Ur page</Link>
      </p>
      <p>
        <Link to="/the-starry-night">Go to The Starry Night page</Link>
      </p>
      <p>
        <Link to="/the-sutton-hoo-helmet">Go to The Sutton Hoo helmet page</Link>
      </p>
      <p>
        <Link to="/the-two-fridas">Go to The Two Fridas page</Link>
      </p>
      <p>
        <Link to="/underlying-technology">Go to Underlying Technology page</Link>
      </p>
      <p>
        <Link to="/contact">Go to Contact page</Link>
      </p>
      <p>
        <Link to="/privacy-policy">Go to Privacy Policy page</Link>
      </p>
    </main>
  )
}

function App() {
  return (
    <>
      <PageTitleUpdater />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/gallery-nouvion-4738593893849" element={<GalleryNouvionPage />} />
        <Route
          path="/along-the-river-during-qingming-festival-by-zhang-zeduan-attributed-12th-century"
          element={<QingmingFestivalPage />}
        />
        <Route path="/hoa-hakananai-a" element={<HoaHakananaiPage />} />
        <Route path="/mona-lisa" element={<MonaLisaPage />} />
        <Route path="/portrait-of-edmond-de-belamy" element={<EdmondDeBelamyPage />} />
        <Route path="/the-cyrus-cylinder" element={<CyrusCylinderPage />} />
        <Route path="/the-lewis-chessmen" element={<LewisChessmenPage />} />
        <Route path="/the-rosetta-stone" element={<RosettaStonePage />} />
        <Route path="/the-royal-game-of-ur" element={<RoyalGameOfUrPage />} />
        <Route path="/the-starry-night" element={<StarryNightPage />} />
        <Route path="/the-sutton-hoo-helmet" element={<SuttonHooHelmetPage />} />
        <Route path="/the-two-fridas" element={<TwoFridasPage />} />
        <Route path="/underlying-technology" element={<UnderlyingTechnologyPage />} />
        <Route path="/contact" element={<ContactPage />} />
        <Route path="/privacy-policy" element={<PrivacyPolicyPage />} />
      </Routes>
    </>
  )
}

export default App
