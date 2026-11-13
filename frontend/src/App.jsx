import { useState, useRef, useEffect } from 'react'
import breedDetails from './data/breedDetails'


import {
  ArrowRight,
  Upload,
  Camera,
  Leaf,
  Menu,
  ChevronRight,
  Scan,
  ShieldCheck,
  Sparkles,
  ImagePlus,
} from 'lucide-react'

import heroImg from './assets/heroSection.avif'

import bargurImg from './assets/bargur.avif'
import dangiImg from './assets/Dangi.webp'
import girImg from './assets/Gir.avif'
import hallikarImg from './assets/Hallikar.avif'
import himachaliPahariImg from './assets/Himachali Pahari.webp'
import kangayamImg from './assets/Kangayam.avif'
import mewatiImg from './assets/Mewati.webp'
import motuImg from './assets/motu.webp'
import nariImg from './assets/Nari.webp'
import ongoleImg from './assets/Ongole.avif'
import podaThirupuImg from './assets/Poda Thirupu.webp'
import ponwarImg from './assets/ponwar.webp'
import pulikulamImg from './assets/Pulikulam.avif'
import purneaImg from './assets/Purnea.webp'
import redKandhariImg from './assets/Red kandhari.webp'
import siriImg from './assets/siri.webp'
import tharparkarImg from './assets/Tharparkar.webp'
import umblacheryImg from './assets/Umblachery.webp'

const breeds = [
  'Bargur',
  'Dangi',
  'Gir',
  'Hallikar',
  'Himachali Pahari',
  'Kangayam',
  'Mewati',
  'Nari',
  'Ongole',
  'Poda Thirupu',
  'Pulikulam',
  'Purnea',
  'Red Kandhari',
  'Tharparkar',
  'Umblachery',
  'Motu',
  'Ponwar',
  'Siri',
]




// Navbar section 



function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const closeMenu = () => setMobileMenuOpen(false)

  return (
    <nav className="sticky top-0 z-50 border-b border-green-100 bg-white/95 backdrop-blur">

      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">

        {/* LOGO */}
        <a href="#" onClick={closeMenu} className="flex items-center gap-2">
          <div className="rounded-xl bg-green-800 p-2 text-white">
            <Leaf size={23} />
          </div>

          <div>
            <h1 className="text-xl font-bold tracking-tight text-green-950">
              Cattle<span className="text-green-700">Vision</span>
            </h1>

            <p className="text-[10px] tracking-widest text-gray-500">
              AI BREED IDENTIFICATION
            </p>
          </div>
        </a>

        {/* DESKTOP NAVIGATION */}
        <div className="hidden items-center gap-9 text-sm font-medium text-gray-600 md:flex">
          <a href="#" className="text-green-800">Home</a>

          <a href="#identify" className="transition hover:text-green-800">
            Identify Breed
          </a>

          <a href="#breeds" className="transition hover:text-green-800">
            Breed Library
          </a>

          <a href="#about" className="transition hover:text-green-800">
            About
          </a>
        </div>

        {/* DESKTOP BUTTON */}
        <a
          href="#identify"
          className="hidden items-center gap-2 rounded-full bg-green-800 px-6 py-3 text-sm font-semibold text-white transition hover:bg-green-900 md:flex"
        >
          Get Started <ArrowRight size={16} />
        </a>

        {/* MOBILE MENU BUTTON */}
        <button
          type="button"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-label="Toggle navigation menu"
          aria-expanded={mobileMenuOpen}
          className="rounded-lg p-2 text-green-900 transition hover:bg-green-50 md:hidden"
        >
          {mobileMenuOpen ? '✕' : <Menu size={25} />}
        </button>

      </div>

      {/* MOBILE NAVIGATION */}
      {mobileMenuOpen && (
        <div className="border-t border-green-100 bg-white px-6 py-5 shadow-lg md:hidden">

          <div className="flex flex-col gap-5 text-sm font-medium text-gray-700">

            <a href="#" onClick={closeMenu} className="hover:text-green-800">
              Home
            </a>

            <a href="#identify" onClick={closeMenu} className="hover:text-green-800">
              Identify Breed
            </a>

            <a href="#breeds" onClick={closeMenu} className="hover:text-green-800">
              Breed Library
            </a>

            <a href="#about" onClick={closeMenu} className="hover:text-green-800">
              About
            </a>

            <a
              href="#identify"
              onClick={closeMenu}
              className="mt-2 flex items-center justify-center gap-2 rounded-full bg-green-800 px-6 py-3 font-semibold text-white hover:bg-green-900"
            >
              Get Started <ArrowRight size={16} />
            </a>

          </div>

        </div>
      )}

    </nav>
  )
}






// hero section 











function Hero() {
  return (
    <section className="overflow-hidden bg-[#f6f8ef]">

      <div className="mx-auto grid max-w-7xl items-center gap-10 px-5 pt-16 pb-16 sm:px-6 sm:py-20 md:grid-cols-2 md:gap-12 md:py-28">

        {/* Left Content */}
        <div>

          {/* Badge */}
          <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-green-200 bg-white px-3 py-2 text-xs font-medium text-green-800 sm:mb-6 sm:px-4 sm:text-sm">
            <Sparkles size={16} />
            Artificial Intelligence Powered
          </div>

          {/* Heading */}
          <h1 className="text-3xl font-bold leading-tight tracking-tight text-green-950 sm:text-4xl md:text-6xl">
            Know Your Cattle.
            <span className="mt-2 block text-green-700">
              Identify Their Breed.
            </span>
          </h1>

          {/* Description */}
          <p className="mt-5 max-w-lg text-sm leading-7 text-gray-600 sm:mt-6 sm:text-base sm:leading-8 md:text-lg">
            Discover the breed of your cattle using artificial intelligence.
            Upload an image and let CattleVision identify it using our
            MobileNetV2-based classification model.
          </p>

          {/* Buttons */}
          <div className="mt-7 flex flex-col gap-3 sm:mt-9 sm:flex-row sm:flex-wrap sm:gap-4">

            <a
              href="#identify"
              className="flex w-full items-center justify-center gap-2 rounded-full bg-green-800 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-green-900/10 transition hover:-translate-y-1 hover:bg-green-900 sm:w-auto sm:px-7 sm:py-4 sm:text-base"
            >
              Identify Your Cattle
              <ArrowRight size={18} />
            </a>

            <a
              href="#breeds"
              className="flex w-full items-center justify-center gap-2 rounded-full border border-green-800 bg-white px-6 py-3.5 text-sm font-semibold text-green-900 transition hover:bg-green-50 sm:w-auto sm:px-7 sm:py-4 sm:text-base"
            >
              Explore Breeds
              <ChevronRight size={18} />
            </a>

          </div>

          {/* Statistics */}
          <div className="mt-10 flex items-center justify-between gap-3 sm:mt-12 sm:justify-start sm:gap-8">

            <div className="min-w-0">
              <h3 className="text-2xl font-bold text-green-900 sm:text-3xl">
                18
              </h3>
              <p className="text-xs leading-5 text-gray-500 sm:text-sm">
                Cattle Breeds
              </p>
            </div>

            <div className="h-10 w-px shrink-0 bg-green-200 sm:h-12" />

            <div className="min-w-0">
              <h3 className="text-2xl font-bold text-green-900 sm:text-3xl">
                AI
              </h3>
              <p className="text-xs leading-5 text-gray-500 sm:text-sm">
                Powered Detection
              </p>
            </div>

            <div className="h-10 w-px shrink-0 bg-green-200 sm:h-12" />

            <div className="min-w-0">
              <h3 className="text-2xl font-bold text-green-900 sm:text-3xl">
                24/7
              </h3>
              <p className="text-xs leading-5 text-gray-500 sm:text-sm">
                Accessible
              </p>
            </div>

          </div>

        </div>

        {/* Right Image */}
        <div className="relative mt-2 sm:mt-4 md:mt-0">

          <div className="absolute -right-8 -top-8 h-64 w-64 rounded-full bg-green-200/40 blur-3xl" />

          <div className="relative overflow-hidden rounded-[28px] border-[6px] border-white shadow-2xl sm:rounded-[35px] sm:border-8">
            <img
              src={heroImg}
              alt="Cattle in a natural environment"
              className="h-[260px] w-full object-cover sm:h-[380px] md:h-[500px]"
            />
          </div>

          {/* Recognition Badge */}
          <div className="absolute bottom-3 left-3 flex items-center gap-2 rounded-xl bg-white p-3 shadow-xl sm:-bottom-6 sm:-left-5 sm:gap-3 sm:rounded-2xl sm:p-4">

            <div className="rounded-lg bg-green-100 p-2 text-green-800 sm:rounded-xl sm:p-3">
              <Scan size={22} />
            </div>

            <div>
              <p className="text-xs font-bold text-green-950 sm:text-sm">
                Smart Breed Recognition
              </p>
              <p className="text-[10px] text-gray-500 sm:text-xs">
                Powered by MobileNetV2
              </p>
            </div>

          </div>

        </div>

      </div>
    </section>
  )
}









// IdentifySection





function IdentifySection() {
  const [selectedImage, setSelectedImage] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [dragActive, setDragActive] = useState(false)

  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // CAMERA STATES
  const [cameraOpen, setCameraOpen] = useState(false)
  const [cameraError, setCameraError] = useState('')

  const videoRef = useRef(null)
  const cameraStreamRef = useRef(null)

  // BREED INFORMATION
  const currentBreedDetails = prediction
    ? breedDetails[prediction.predicted_breed]
    : null

  // =========================================
  // ANALYZE IMAGE USING FASTAPI
  // =========================================

  const handleAnalyze = async () => {
  if (!selectedImage || loading) return

  setLoading(true)
  setError('')
  setPrediction(null)

  try {
    const formData = new FormData()
    formData.append('file', selectedImage)

    const response = await fetch(
      'http://127.0.0.1:8000/predict',
      {
        method: 'POST',
        body: formData,
      }
    )

    const data = await response.json()

    if (!response.ok) {

      // Non-cattle image detection
      if (
        response.status === 422 &&
        data.detail?.includes('No cattle detected')
      ) {
        throw new Error(
          'NO_CATTLE_DETECTED'
        )
      }

      throw new Error(
        data.detail || 'Prediction failed. Please try again.'
      )
    }

    setPrediction(data)

  } catch (err) {

    if (err.message === 'NO_CATTLE_DETECTED') {

      setError(
        'No cattle detected. Please upload a clear image containing a cow. CattleVision can identify only supported cattle breeds.'
      )

    } else if (err instanceof TypeError) {

      setError(
        'Unable to connect to the prediction server. Please check whether the backend is running.'
      )

    } else {

      setError(
        err.message || 'Something went wrong. Please try again.'
      )

    }

  } finally {
    setLoading(false)
  }
}

  // =========================================
  // HANDLE IMAGE SELECTION
  // =========================================

  const handleImage = (file) => {
    if (!file) return

    const allowedTypes = [
      'image/jpeg',
      'image/png',
      'image/webp',
    ]

    if (!allowedTypes.includes(file.type)) {
      alert('Please upload a JPG, PNG, or WEBP image.')
      return
    }

    if (file.size > 10 * 1024 * 1024) {
      alert('Image size must be less than 10 MB.')
      return
    }

    if (previewUrl) {
      URL.revokeObjectURL(previewUrl)
    }

    setSelectedImage(file)
    setPreviewUrl(URL.createObjectURL(file))

    setPrediction(null)
    setError('')
  }

  // =========================================
  // OPEN LIVE CAMERA
  // =========================================

  const startCamera = async () => {
    setCameraError('')

    if (!navigator.mediaDevices?.getUserMedia) {
      setCameraError(
        'Camera access is unavailable. Please use localhost or HTTPS.'
      )
      setCameraOpen(true)
      return
    }

    try {
      if (cameraStreamRef.current) {
        cameraStreamRef.current
          .getTracks()
          .forEach((track) => track.stop())
      }

      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: { ideal: 'environment' },
        },
        audio: false,
      })

      cameraStreamRef.current = stream
      setCameraOpen(true)

    } catch (err) {
      let message = 'Unable to access the camera.'

      if (err.name === 'NotAllowedError') {
        message = 'Camera permission denied. Please allow camera access.'
      } else if (err.name === 'NotFoundError') {
        message = 'No camera was found on this device.'
      } else if (err.name === 'NotReadableError') {
        message = 'Camera is already being used by another application.'
      }

      setCameraError(message)
      setCameraOpen(true)
    }
  }

  // =========================================
  // CONNECT CAMERA STREAM
  // =========================================

  useEffect(() => {
    if (
      !cameraOpen ||
      !videoRef.current ||
      !cameraStreamRef.current
    ) {
      return
    }

    const video = videoRef.current

    video.srcObject = cameraStreamRef.current

    video.play().catch(() => {
      setCameraError('Unable to start the camera preview.')
    })

    return () => {
      video.srcObject = null
    }

  }, [cameraOpen])

  // =========================================
  // CLOSE CAMERA
  // =========================================

  const closeCamera = () => {
    if (cameraStreamRef.current) {
      cameraStreamRef.current
        .getTracks()
        .forEach((track) => track.stop())

      cameraStreamRef.current = null
    }

    if (videoRef.current) {
      videoRef.current.srcObject = null
    }

    setCameraOpen(false)
  }

  // =========================================
  // CAPTURE PHOTO
  // =========================================

  const capturePhoto = () => {
    const video = videoRef.current

    if (
      !video ||
      !video.videoWidth ||
      !video.videoHeight
    ) {
      setCameraError('Camera is not ready. Please try again.')
      return
    }

    const canvas = document.createElement('canvas')

    canvas.width = video.videoWidth
    canvas.height = video.videoHeight

    const context = canvas.getContext('2d')

    if (!context) {
      setCameraError('Unable to capture the photograph.')
      return
    }

    context.drawImage(
      video,
      0,
      0,
      canvas.width,
      canvas.height
    )

    canvas.toBlob(
      (blob) => {
        if (!blob) {
          setCameraError('Failed to capture the photograph.')
          return
        }

        const capturedFile = new File(
          [blob],
          `cattle_${Date.now()}.jpg`,
          {
            type: 'image/jpeg',
          }
        )

        closeCamera()
        handleImage(capturedFile)

      },
      'image/jpeg',
      0.92
    )
  }

  // =========================================
  // CLEAN UP CAMERA
  // =========================================

  useEffect(() => {
    return () => {
      if (cameraStreamRef.current) {
        cameraStreamRef.current
          .getTracks()
          .forEach((track) => track.stop())
      }
    }
  }, [])

  // =========================================
  // HANDLE DRAG AND DROP
  // =========================================

  const handleDrop = (event) => {
    event.preventDefault()
    setDragActive(false)

    const file = event.dataTransfer.files[0]
    handleImage(file)
  }

  // =========================================
  // REMOVE IMAGE
  // =========================================

  const removeImage = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl)
    }

    setSelectedImage(null)
    setPreviewUrl(null)

    setPrediction(null)
    setError('')
  }

  // =========================================
  // RESET WORKSPACE
  // =========================================

  const resetWorkspace = () => {
    removeImage()
  }

  // =========================================
  // UI
  // =========================================

  return (
    <section
      id="identify"
      className="bg-[#f0f3eb] px-4 py-14 sm:px-6 sm:py-20"
    >

      <div className="mx-auto max-w-7xl">

        {/* ================================= */}
        {/* CAMERA MODAL */}
        {/* ================================= */}

        {cameraOpen && (

          <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 p-4">

            <div className="w-full max-w-xl overflow-hidden rounded-2xl bg-white shadow-2xl">

              <div className="flex items-center justify-between border-b border-gray-100 p-5">

                <div>
                  <h3 className="text-lg font-bold text-green-950">
                    Capture Cattle Image
                  </h3>

                  <p className="mt-1 text-xs text-gray-500">
                    Position the cattle inside the camera frame.
                  </p>
                </div>

                <button
                  type="button"
                  onClick={closeCamera}
                  aria-label="Close camera"
                  className="flex h-9 w-9 items-center justify-center rounded-full bg-gray-100 text-gray-600 transition hover:bg-red-100 hover:text-red-600"
                >
                  <span className="text-xl">&times;</span>
                </button>

              </div>

              {/* LIVE CAMERA */}

              <div className="relative overflow-hidden bg-black">

                {cameraError ? (

                  <div className="flex min-h-[280px] items-center justify-center p-8 text-center">

                    <div>
                      <Camera
                        size={40}
                        className="mx-auto text-gray-400"
                      />

                      <p className="mt-4 text-sm font-semibold text-white">
                        Camera unavailable
                      </p>

                      <p className="mt-2 text-xs leading-6 text-gray-300">
                        {cameraError}
                      </p>
                    </div>

                  </div>

                ) : (

                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className="aspect-video w-full object-cover"
                  />

                )}

              </div>

              {/* CAMERA BUTTONS */}

              <div className="flex gap-3 p-5">

                <button
                  type="button"
                  onClick={closeCamera}
                  className="flex-1 rounded-lg border border-gray-200 px-4 py-3 text-sm font-semibold text-gray-600 transition hover:bg-gray-50"
                >
                  Cancel
                </button>

                {cameraError ? (

                  <button
                    type="button"
                    onClick={startCamera}
                    className="flex-1 rounded-lg bg-green-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-green-800"
                  >
                    Try Again
                  </button>

                ) : (

                  <button
                    type="button"
                    onClick={capturePhoto}
                    className="flex flex-1 items-center justify-center gap-2 rounded-lg bg-green-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-green-800"
                  >
                    <Camera size={17} />
                    Capture Photo
                  </button>

                )}

              </div>

            </div>

          </div>

        )}

        {/* ================================= */}
        {/* SECTION HEADING */}
        {/* ================================= */}

        <div className="mb-10">

          <div className="mb-4 flex items-center gap-3">
            <span className="h-px w-8 bg-green-800/30" />

            <span className="text-[11px] font-bold uppercase tracking-[0.2em] text-green-800/70">
              The Workspace
            </span>
          </div>

          <h2 className="text-3xl font-bold tracking-tight text-green-950 md:text-4xl">
            Identify a breed in seconds
          </h2>

          <p className="mt-3 max-w-xl text-sm leading-6 text-gray-500">
            Upload a cattle image and discover its breed using
            our AI-powered identification system.
          </p>

        </div>

        {/* ================================= */}
        {/* UPLOAD AND PREVIEW */}
        {/* ================================= */}

        <div
          className={`grid gap-5 ${
            selectedImage
              ? 'lg:grid-cols-2'
              : 'grid-cols-1'
          }`}
        >

          {/* UPLOAD CARD */}

          <div className="min-w-0 rounded-2xl border border-gray-100 bg-white p-4 shadow-sm sm:p-6">

            <div className="mb-5 flex items-center justify-between">

              <h3 className="text-sm font-bold text-green-950">
                Upload your image
              </h3>

              <span className="text-[10px] font-bold tracking-widest text-gray-400">
                01 / INPUT
              </span>

            </div>

            {/* UPLOAD AREA */}

            <label
              onDragOver={(event) => {
                event.preventDefault()
                setDragActive(true)
              }}
              onDragLeave={() => setDragActive(false)}
              onDrop={handleDrop}
              className={`flex min-h-[190px] cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed p-6 text-center transition sm:min-h-[220px] ${
                dragActive
                  ? 'border-green-700 bg-green-50'
                  : 'border-green-200 bg-[#fbfcfa] hover:border-green-600 hover:bg-green-50'
              }`}
            >

              <input
                type="file"
                accept="image/jpeg,image/png,image/webp"
                className="hidden"
                onChange={(event) => {
                  handleImage(event.target.files[0])
                  event.target.value = ''
                }}
              />

              <div className="rounded-xl bg-green-100 p-3 text-green-800">
                <Upload size={22} />
              </div>

              <h4 className="mt-4 text-sm font-bold text-green-950">
                Drop a cattle image here
              </h4>

              <p className="mt-1 text-xs text-gray-400">
                or browse files
              </p>

              <span className="mt-4 rounded-lg bg-green-950 px-5 py-2 text-xs font-semibold text-white transition hover:bg-green-900">
                Browse Files
              </span>

              <p className="mt-3 text-[10px] text-gray-400">
                JPG, JPEG, PNG, WEBP · Maximum 10 MB
              </p>

            </label>

            {/* SELECTED FILE */}

            {selectedImage && (

              <div className="mt-4 flex items-center justify-between gap-3 rounded-xl border border-green-100 bg-green-50 p-3">

                <div className="flex min-w-0 items-center gap-3">

                  <div className="rounded-lg bg-green-100 p-2 text-green-800">
                    <ImagePlus size={18} />
                  </div>

                  <div className="min-w-0">

                    <p className="truncate text-xs font-semibold text-green-950">
                      {selectedImage.name}
                    </p>

                    <p className="mt-1 text-[10px] text-gray-500">
                      {(selectedImage.size / (1024 * 1024)).toFixed(2)} MB
                    </p>

                  </div>

                </div>

                <button
                  type="button"
                  onClick={removeImage}
                  disabled={loading}
                  title="Remove image"
                  aria-label="Remove uploaded image"
                  className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-gray-500 transition hover:bg-red-100 hover:text-red-600 disabled:opacity-40"
                >
                  <span className="text-xl leading-none">
                    &times;
                  </span>
                </button>

              </div>

            )}

            {/* UPLOAD FOOTER */}

            <div className="mt-4 flex items-center justify-between text-xs">

              <button
                type="button"
                onClick={startCamera}
                className="flex items-center gap-2 font-semibold text-green-900 transition hover:text-green-600"
              >
                <Camera size={14} />
                Use Camera
              </button>

              <span className="text-gray-400">
                18 supported breeds
              </span>

            </div>

          </div>

          {/* ================================= */}
          {/* IMAGE PREVIEW */}
          {/* ================================= */}

          {selectedImage && (

            <div className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">

              <div className="mb-5 flex items-center justify-between">

                <h3 className="text-sm font-bold text-green-950">
                  Image preview
                </h3>

                <span className="text-[10px] font-bold tracking-widest text-gray-400">
                  02 / REVIEW
                </span>

              </div>

              <div className="h-[200px] overflow-hidden rounded-xl bg-green-50 sm:h-[260px]">

                <img
                  src={previewUrl}
                  alt="Uploaded cattle preview"
                  className="h-full w-full object-cover"
                />

              </div>

              <div className="mt-4 flex items-center gap-2 text-[11px] font-semibold text-green-800">

                <span className="h-2 w-2 rounded-full bg-green-500" />

                Image uploaded successfully

              </div>

              <button
                type="button"
                onClick={handleAnalyze}
                disabled={!selectedImage || loading}
                className="mt-4 flex w-full items-center justify-center gap-2 rounded-lg bg-green-950 py-3 text-xs font-bold text-white transition hover:bg-green-900 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading
                  ? 'Analyzing Image...'
                  : 'Analyze Image'
                }

                {!loading && <ArrowRight size={15} />}

              </button>

              <p className="mt-3 text-[10px] text-gray-400">
                Your image will be analyzed using the trained
                MobileNetV2 model.
              </p>

            </div>

          )}

        </div>

        {/* ========================================= */}
        {/* REDESIGNED AI PREDICTION SUMMARY */}
        {/* ========================================= */}

        {selectedImage && (

          <div className="mt-6 space-y-6">

            {/* ================================= */}
            {/* PREDICTION SUMMARY */}
            {/* ================================= */}

            <div className="overflow-hidden rounded-2xl bg-[#073b26] p-6 text-white shadow-lg md:p-8">

              {/* LOADING */}

              {loading ? (

                <div className="py-12 text-center">

                  <div className="mx-auto h-10 w-10 animate-spin rounded-full border-4 border-green-300 border-t-transparent" />

                  <h3 className="mt-5 text-lg font-bold">
                    Analyzing Your Cattle Image
                  </h3>

                  <p className="mt-2 text-sm text-green-200">
                    MobileNetV2 is identifying the cattle breed...
                  </p>

                </div>

              ) : error ? (

                /* ERROR */

                <div className="py-5">

                  <h3 className="text-xl font-bold text-red-300">
                    Prediction Failed
                  </h3>

                  <p className="mt-3 text-sm text-green-100">
                    {error}
                  </p>

                  <button
                    type="button"
                    onClick={handleAnalyze}
                    className="mt-5 rounded-lg bg-white px-5 py-3 text-sm font-bold text-green-950 transition hover:bg-green-100"
                  >
                    Try Again
                  </button>

                </div>

              ) : prediction ? (

                <>

                  <div className="grid gap-10 lg:grid-cols-2 lg:items-center">

                    {/* MAIN PREDICTION */}

                    <div>

                      <span className="inline-flex items-center gap-2 rounded-md border border-green-400/30 bg-green-900/40 px-3 py-2 text-[10px] font-bold uppercase tracking-widest text-green-200">

                        <span className="h-2 w-2 rounded-full bg-green-400" />

                        AI Identification Result

                      </span>

                      <h2 className="mt-5 text-3xl font-bold tracking-tight sm:text-4xl">
                        {prediction.predicted_breed}
                      </h2>

                      <p className="mt-3 text-sm text-green-200">
                        {Number(prediction.confidence).toFixed(2)}% confidence score
                      </p>

                      {/* CONFIDENCE BAR */}

                      <div className="mt-5 max-w-sm">

                        <div className="h-2 overflow-hidden rounded-full bg-white/15">

                          <div
                            className="h-full rounded-full bg-[#d8b47e] transition-all duration-700"
                            style={{
                              width: `${Math.min(100, Math.max(0, Number(prediction.confidence) || 0))}%`,
                            }}
                          />

                        </div>

                      </div>

                      {/* DISCLAIMER */}

                      <p className="mt-4 max-w-md text-xs leading-6 text-green-200/75">
                        Confidence is model-estimated and not a guarantee
                        of breed identity. These figures are prediction
                        scores, not verified probabilities. Results may
                        vary with image quality, lighting, camera angle
                        and visual similarities between cattle breeds.
                      </p>

                    </div>

                    {/* TOP 3 PREDICTIONS */}

                    <div>

                      <h3 className="mb-7 text-base font-bold text-white">
                        Top 3 Breed Predictions
                      </h3>

                      <div className="space-y-6">

                        {(prediction.top_predictions || []).slice(0, 3).map((item, index) => {

                          const score = Math.min(
                            100,
                            Math.max(0, Number(item.confidence) || 0)
                          )

                          return (

                            <div key={`${item.breed}-${index}`}>

                              <div className="mb-2 flex items-center justify-between gap-3">

                                <span className="text-sm font-medium text-green-100">
                                  {index + 1}. {item.breed}
                                </span>

                                <span className="text-sm font-bold text-white">
                                  {score.toFixed(2)}%
                                </span>

                              </div>

                              <div className="h-2 overflow-hidden rounded-full bg-white/20">

                                <div
                                  className="h-full rounded-full bg-[#d8b47e] transition-all duration-700"
                                  style={{
                                    width: `${score}%`,
                                  }}
                                />

                              </div>

                            </div>

                          )
                        })}

                      </div>

                    </div>

                  </div>

                  {/* IDENTIFY ANOTHER */}

                  <div className="mt-8 border-t border-white/15 pt-5">

                    <button
                      type="button"
                      onClick={resetWorkspace}
                      className="flex items-center gap-2 text-sm font-semibold text-green-100 transition hover:text-white"
                    >
                      <span className="text-lg">↻</span>
                      Identify another
                    </button>

                  </div>

                </>

              ) : (

                /* BEFORE ANALYSIS */

                <div className="py-5">

                  <span className="text-xs font-bold uppercase tracking-widest text-green-300">
                    AI Identification
                  </span>

                  <h3 className="mt-4 text-2xl font-bold">
                    Ready for Analysis
                  </h3>

                  <p className="mt-2 text-sm text-green-200">
                    Click Analyze Image to identify the cattle breed.
                  </p>

                </div>

              )}

            </div>

            {/* ================================= */}
            {/* BREED PROFILE */}
            {/* ONLY AFTER SUCCESSFUL PREDICTION */}
            {/* ================================= */}

            {prediction && (

              <div className="rounded-2xl bg-[#f8f9f5] p-5 sm:p-7 md:p-8">

                {/* PROFILE HEADING */}

                <div className="mb-6">

                  <span className="text-[10px] font-bold uppercase tracking-[0.18em] text-green-700">
                    Breed Information
                  </span>

                  <h3 className="mt-2 text-2xl font-bold text-green-950">
                    Breed Profile
                  </h3>

                  <p className="mt-2 text-sm text-gray-500">
                    Learn more about the identified cattle breed.
                  </p>

                </div>

                {currentBreedDetails ? (

                  <>

                    {/* NATIVE REGION AND CATEGORY */}

                    <div className="grid gap-4 sm:grid-cols-2">

                      {/* NATIVE REGION */}

                      <div className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">

                        <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-lg bg-green-50 text-lg text-green-800">
                          ⌖
                        </div>

                        <p className="text-[10px] font-bold uppercase tracking-widest text-gray-400">
                          Native Region
                        </p>

                        <p className="mt-2 text-sm font-bold text-green-950">
                          {currentBreedDetails.nativeRegion}
                        </p>

                      </div>

                      {/* BREED CATEGORY */}

                      <div className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">

                        <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-lg bg-green-50 text-lg text-green-800">
                          ◈
                        </div>

                        <p className="text-[10px] font-bold uppercase tracking-widest text-gray-400">
                          Breed Category
                        </p>

                        <p className="mt-2 text-sm font-bold text-green-950">
                          {currentBreedDetails.category}
                        </p>

                      </div>

                    </div>

                    {/* PHYSICAL CHARACTERISTICS AND USES */}

                    <div className="mt-4 grid gap-4 md:grid-cols-2">

                      {/* PHYSICAL CHARACTERISTICS */}

                      <div className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">

                        <div className="mb-4 flex items-center gap-3">

                          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-green-50 text-green-800">
                            <span className="text-lg">◉</span>
                          </div>

                          <h4 className="text-sm font-bold text-green-950">
                            Physical Characteristics
                          </h4>

                        </div>

                        <p className="text-sm leading-7 text-gray-600">
                          {currentBreedDetails.physicalCharacteristics ||
                            'Physical characteristics are not currently available for this breed.'}
                        </p>

                      </div>

                      {/* TRADITIONAL USES */}

                      <div className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">

                        <div className="mb-4 flex items-center gap-3">

                          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-green-50 text-green-800">
                            <span className="text-lg">⌁</span>
                          </div>

                          <h4 className="text-sm font-bold text-green-950">
                            Traditional Uses
                          </h4>

                        </div>

                        <p className="text-sm leading-7 text-gray-600">
                          {currentBreedDetails.traditionalUses ||
                            'Traditional uses are not currently available for this breed.'}
                        </p>

                      </div>

                    </div>

                  </>

                ) : (

                  <p className="rounded-xl border border-gray-100 bg-white p-5 text-sm text-gray-500">
                    Additional breed information is currently unavailable for{' '}
                    <strong>{prediction.predicted_breed}</strong>.
                  </p>

                )}

              </div>

            )}

          </div>

        )}

      </div>
    </section>
  )
}













// featuredBreeds



const featuredBreeds = [
  {
    name: 'Bargur',
    image: bargurImg,
    description:
      'An agile breed associated with the hilly Bargur region of Tamil Nadu.',
  },
  {
    name: 'Kangayam',
    image: kangayamImg,
    description:
      'A Tamil Nadu breed recognized for its sturdy build and working heritage.',
  },
  {
    name: 'Gir',
    image: girImg,
    description:
      'A breed from Gujarat, known for its distinctive ears and curved horns.',
  },
  {
    name: 'Hallikar',
    image: hallikarImg,
    description:
      'A Karnataka breed traditionally valued for its strength in farm work.',
  },
  {
    name: 'Ongole',
    image: ongoleImg,
    description:
      'A prominent Andhra Pradesh breed with a strong frame and pale coat.',
  },
  {
    name: 'Pulikulam',
    image: pulikulamImg,
    description:
      'A hardy cattle breed associated with southern Tamil Nadu.',
  },
  {
    name: 'Dangi',
    image: dangiImg,
    description:
      'An indigenous Indian cattle breed included in CattleVision.',
  },
  {
    name: 'Himachali Pahari',
    image: himachaliPahariImg,
    description:
      'A cattle breed associated with the Himalayan region.',
  },
  {
    name: 'Mewati',
    image: mewatiImg,
    description:
      'An indigenous cattle breed associated with the Mewat region.',
  },
  {
    name: 'Nari',
    image: nariImg,
    description:
      'An indigenous Indian cattle breed included in CattleVision.',
  },
  {
    name: 'Poda Thirupu',
    image: podaThirupuImg,
    description:
      'An indigenous cattle breed included in CattleVision.',
  },
  {
    name: 'Purnea',
    image: purneaImg,
    description:
      'An indigenous cattle breed included in CattleVision.',
  },
  {
    name: 'Red kandhari',
    image: redKandhariImg,
    description:
      'A cattle breed recognized for its characteristic red coat.',
  },
  {
    name: 'Tharparkar',
    image: tharparkarImg,
    description:
      'An Indian cattle breed known for its adaptability to dry regions.',
  },
  {
    name: 'Umblachery',
    image: umblacheryImg,
    description:
      'An indigenous cattle breed from Tamil Nadu.',
  },
  {
    name: 'motu',
    image: motuImg,
    description:
      'An indigenous Indian cattle breed included in CattleVision.',
  },
  {
    name: 'ponwar',
    image: ponwarImg,
    description:
      'An indigenous Indian cattle breed included in CattleVision.',
  },
  {
    name: 'siri',
    image: siriImg,
    description:
      'An indigenous Indian cattle breed included in CattleVision.',
  },
]











//breed library section







function BreedLibrary() {
  const [visibleCount, setVisibleCount] = useState(6)
  const [selectedBreed, setSelectedBreed] = useState(null)

  const selectedDetails = selectedBreed
    ? breedDetails[selectedBreed.name]
    : null

  return (
    <section
      id="breeds"
      className="bg-[#f7f4eb] px-6 py-24"
    >
      <div className="mx-auto max-w-7xl">

        {/* Section Heading */}
        <div className="mb-12">
          <span className="text-xs font-semibold uppercase tracking-[0.2em] text-green-800">
            Discover & Learn
          </span>

          <h2 className="mt-4 text-3xl font-semibold tracking-tight text-green-950 md:text-4xl">
            Explore the breed library
          </h2>

          <p className="mt-4 max-w-xl text-sm leading-7 text-gray-600">
            Get acquainted with some of India's distinctive cattle breeds
            and the traits often associated with them.
          </p>
        </div>

        {/* Breed Cards */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">

          {featuredBreeds.slice(0, visibleCount).map((breed) => (
            <article
              key={breed.name}
              className="group overflow-hidden rounded-[22px] border border-black/5 bg-white transition duration-300 hover:-translate-y-1 hover:shadow-xl"
            >

              <div className="h-64 overflow-hidden">
                <img
                  src={breed.image}
                  alt={`${breed.name} cattle`}
                  className="h-full w-full object-cover transition duration-500 group-hover:scale-105"
                />
              </div>

              <div className="p-6">

                <h3 className="text-xl font-semibold text-green-950">
                  {breed.name}
                </h3>

                <p className="mt-3 min-h-12 text-sm leading-6 text-gray-600">
                  {breed.description}
                </p>

                {/* View Breed Button */}
                <button
                  type="button"
                  onClick={() => setSelectedBreed(breed)}
                  className="mt-5 inline-flex items-center gap-2 text-sm font-semibold text-green-950 transition hover:text-green-700"
                >
                  View breed
                  <ArrowRight
                    size={16}
                    className="transition group-hover:translate-x-1"
                  />
                </button>

              </div>
            </article>
          ))}

        </div>

        {/* View More Button */}
        {visibleCount < featuredBreeds.length && (
          <div className="mt-12 flex justify-center">
            <button
              type="button"
              onClick={() => setVisibleCount((previous) => previous + 6)}
              className="rounded-full bg-green-800 px-8 py-3 text-sm font-semibold text-white transition hover:bg-green-900"
            >
              View More
            </button>
          </div>
        )}

        <p className="mt-6 text-center text-xs text-gray-400">
          Photographs are provided for breed exploration and visual reference.
        </p>

      </div>

      {/* Breed Details Modal */}
      {selectedBreed && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm"
          onClick={() => setSelectedBreed(null)}
        >

          <div
            role="dialog"
            aria-modal="true"
            aria-labelledby="breed-modal-title"
            className="relative max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-3xl bg-[#f7f4eb] shadow-2xl"
            onClick={(event) => event.stopPropagation()}
          >

            {/* Close Button */}
            <button
              type="button"
              onClick={() => setSelectedBreed(null)}
              aria-label="Close breed details"
              className="absolute right-4 top-4 z-10 flex h-9 w-9 items-center justify-center rounded-full bg-white text-2xl text-gray-700 shadow-md transition hover:bg-green-800 hover:text-white"
            >
              &times;
            </button>

            {/* Breed Image */}
            <div className="h-64 overflow-hidden sm:h-80">
              <img
                src={selectedBreed.image}
                alt={`${selectedBreed.name} cattle`}
                className="h-full w-full object-cover"
              />
            </div>

            {/* Breed Information */}
            <div className="p-6 sm:p-8">

              <span className="text-xs font-semibold uppercase tracking-[0.2em] text-green-800">
                Breed Information
              </span>

              <h2
                id="breed-modal-title"
                className="mt-3 text-3xl font-semibold text-green-950"
              >
                {selectedBreed.name}
              </h2>

              {selectedDetails ? (
                <div className="mt-6 space-y-6">

                  {/* Native Region */}
                  <div>
                    <h3 className="font-semibold text-green-950">
                      Native Region
                    </h3>
                    <p className="mt-2 text-sm leading-7 text-gray-600">
                      {selectedDetails.nativeRegion || 'Information unavailable.'}
                    </p>
                  </div>

                  {/* Category */}
                  <div>
                    <h3 className="font-semibold text-green-950">
                      Breed Category
                    </h3>
                    <p className="mt-2 text-sm leading-7 text-gray-600">
                      {selectedDetails.category || 'Information unavailable.'}
                    </p>
                  </div>

                  {/* Physical Characteristics */}
                  <div>
                    <h3 className="font-semibold text-green-950">
                      Physical Characteristics
                    </h3>
                    <p className="mt-2 text-sm leading-7 text-gray-600">
                      {Array.isArray(selectedDetails.physicalCharacteristics)
                        ? selectedDetails.physicalCharacteristics.join(', ')
                        : selectedDetails.physicalCharacteristics || 'Information unavailable.'}
                    </p>
                  </div>

                  {/* Traditional Uses */}
                  <div>
                    <h3 className="font-semibold text-green-950">
                      Traditional Uses
                    </h3>
                    <p className="mt-2 text-sm leading-7 text-gray-600">
                      {Array.isArray(selectedDetails.traditionalUses)
                        ? selectedDetails.traditionalUses.join(', ')
                        : selectedDetails.traditionalUses || 'Information unavailable.'}
                    </p>
                  </div>

                </div>
              ) : (
                <p className="mt-6 text-sm text-gray-600">
                  Breed details are currently unavailable.
                </p>
              )}

              {/* Close Modal */}
              <button
                type="button"
                onClick={() => setSelectedBreed(null)}
                className="mt-8 rounded-full bg-green-800 px-7 py-3 text-sm font-semibold text-white transition hover:bg-green-900"
              >
                Close
              </button>

            </div>
          </div>
        </div>
      )}

    </section>
  )
}







function HowItWorks() {
  const steps = [
    {
      number: '01',
      icon: Upload,
      title: 'Upload Image',
      description: 'Choose a clear image of the cattle you want to identify.',
    },
    {
      number: '02',
      icon: Scan,
      title: 'AI Analysis',
      description: 'Our MobileNetV2 model analyzes the image features.',
    },
    {
      number: '03',
      icon: Sparkles,
      title: 'Get Results',
      description: 'View the predicted cattle breed and confidence score.',
    },
  ]

  return (
    <section className="bg-white px-6 py-24">

      <div className="mx-auto max-w-6xl">

        <div className="text-center">

          <span className="text-sm font-bold uppercase tracking-widest text-green-700">
            Simple Process
          </span>

          <h2 className="mt-4 text-3xl font-bold text-green-950 md:text-4xl">
            How CattleVision Works
          </h2>

        </div>

        <div className="mt-14 grid gap-8 md:grid-cols-3">

          {steps.map((step) => {
            const Icon = step.icon

            return (
              <div
                key={step.number}
                className="rounded-3xl border border-green-100 bg-[#f9faf6] p-8 text-center"
              >

                <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-green-800 text-white">
                  <Icon size={28} />
                </div>

                <p className="mt-6 text-sm font-bold text-green-700">
                  STEP {step.number}
                </p>

                <h3 className="mt-2 text-xl font-bold text-green-950">
                  {step.title}
                </h3>

                <p className="mt-3 text-sm leading-7 text-gray-500">
                  {step.description}
                </p>

              </div>
            )
          })}

        </div>

      </div>
    </section>
  )
}


function AboutSection() {
  return (
    <section id="about" className="bg-[#f6f8ef] px-6 py-20">

      <div className="mx-auto max-w-4xl text-center">

        <Leaf size={35} className="mx-auto text-green-800" />

        <h2 className="mt-5 text-3xl font-bold text-green-950">
          About CattleVision
        </h2>

        <p className="mt-5 leading-8 text-gray-600">
          CattleVision is an AI-based cattle breed classification project
          designed to recognize 18 cattle breeds from images using a
          fine-tuned MobileNetV2 deep learning model.
        </p>

      </div>

    </section>
  )
}


function Footer() {
  return (
    <footer className="bg-green-950 px-6 py-10 text-white">

      <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-5 md:flex-row">

        <div>
          <h2 className="text-xl font-bold">
            CattleVision
          </h2>

          <p className="mt-2 text-sm text-green-200">
            AI-powered Cattle Breed Identification
          </p>
        </div>

        <p className="text-sm text-green-200">
          © {new Date().getFullYear()} CattleVision. All rights reserved.
        </p>

      </div>

    </footer>
  )
}


function App() {
  return (
    <>
      <Navbar />
      <main>
        <Hero />
        <IdentifySection />
        <BreedLibrary />
        <HowItWorks />
        <AboutSection />
      </main>
      <Footer />
    </>
  )
}

export default App