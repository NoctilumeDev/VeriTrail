import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const projectRoot = dirname(dirname(fileURLToPath(import.meta.url)))

try {
  const html = readFileSync(join(projectRoot, 'site', 'index.html'), 'utf8')
  const payload = JSON.parse(readFileSync(join(projectRoot, 'site', 'data.json'), 'utf8'))
  const markers = [
    'data-testid="run-label"',
    'data-testid="load-evidence"',
    'data-testid="status"',
    'data-testid="evidence-list"',
  ]
  if (!markers.every((marker) => html.includes(marker))) throw new Error('missing marker')
  if (JSON.stringify(payload) !== JSON.stringify({ items: ['direct node.exe', 'no shell', 'bounded cleanup'] })) {
    throw new Error('unexpected evidence payload')
  }
  process.stdout.write(`${JSON.stringify({ check: 'node-project', items: payload.items.length, status: 'PASS' })}\n`)
} catch {
  process.stderr.write('node-project-check:FAIL\n')
  process.exitCode = 3
}
