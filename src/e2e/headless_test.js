const fs = require('fs')
const path = require('path')
const puppeteer = require('puppeteer')

const APP_URL = 'http://localhost:5173/'

async function writeTestImage(dest) {
  // 1x1 white JPEG
  const b64 = '/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAICAgICAgICAgICAgICAgICAgICAgICAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAALCAABAAEBAREA/8QAFQABAQAAAAAAAAAAAAAAAAAAAAb/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIQAxAAAAGf/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPwA//8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAgBAgEBPwB//8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAgBAwEBPwB//9k='
  const buf = Buffer.from(b64, 'base64')
  fs.writeFileSync(dest, buf)
}

;(async () => {
  const imagePath = path.resolve(__dirname, '../../test-image.jpg')
  writeTestImage(imagePath)

  const browser = await puppeteer.launch({ args: ['--no-sandbox', '--disable-setuid-sandbox'] })
  const page = await browser.newPage()
  page.setDefaultTimeout(15000)

  await page.goto(APP_URL, { waitUntil: 'networkidle2' })

  // Open encoder panel (avoid XPath for broader Puppeteer compatibility)
  const encClicked = await page.evaluate(() => {
    const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === 'Inverted math')
    if (!btn) return false
    btn.click()
    return true
  })
  if (!encClicked) throw new Error('Encoder nav button not found')
  await page.waitForSelector('input[type="text"]')

  // Type text and encode
  await page.type('input[type="text"]', 'hello')
  await page.evaluate(() => {
    const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === 'Encode')
    if (btn) btn.click()
  })

  // Wait a moment for logging
  await new Promise(r => setTimeout(r, 500))

  const before = await page.evaluate(() => ({
    metaLog: localStorage.getItem('positron_imaging_meta_log'),
    activeMeta: localStorage.getItem('positron_imaging_meta')
  }))
  console.log('After encode -> metaLog length:', before.metaLog ? JSON.parse(before.metaLog).length : 0)

  // Open seam panel
  const seamClicked = await page.evaluate(() => {
    const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === 'Seam Carve')
    if (!btn) return false
    btn.click()
    return true
  })
  if (!seamClicked) throw new Error('Seam nav button not found')

  await page.waitForSelector('input[type="file"]')
  const fileHandle = await page.$('input[type="file"]')
  await fileHandle.uploadFile(imagePath)

  const runClicked = await page.evaluate(() => {
    const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === 'Run Seam Carve')
    if (!btn) return false
    btn.click()
    return true
  })
  if (!runClicked) throw new Error('Run button not found')

  // Wait for the seam processor to write meta
  await page.waitForFunction(() => !!localStorage.getItem('positron_imaging_meta'), { timeout: 10000 })
  const after = await page.evaluate(() => ({
    activeMeta: localStorage.getItem('positron_imaging_meta'),
    metaLog: localStorage.getItem('positron_imaging_meta_log')
  }))

  console.log('Active meta:', after.activeMeta)
  console.log('Meta log entries:', after.metaLog ? JSON.parse(after.metaLog).length : 0)

  await browser.close()
  process.exit(0)
})().catch(err => { console.error(err); process.exit(2) })
