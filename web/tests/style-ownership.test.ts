import { readFileSync, readdirSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'

const testDirectory = dirname(fileURLToPath(import.meta.url))
const styleDirectory = resolve(testDirectory, '..', 'src', 'styles')

function styleSource(name: string): string {
  return readFileSync(resolve(styleDirectory, name), 'utf8')
}

function styleNames(): string[] {
  return readdirSync(styleDirectory)
    .filter((name) => name.endsWith('.css'))
    .sort()
}

function styleRules(source: string): Array<{ selectors: string; declarations: string }> {
  const withoutComments = source.replace(/\/\*[\s\S]*?\*\//g, '')
  return Array.from(withoutComments.matchAll(/([^{}]+)\{([^{}]*)\}/g), (match) => ({
    selectors: match[1].trim(),
    declarations: match[2],
  })).filter((rule) => rule.selectors.length > 0 && !rule.selectors.startsWith('@'))
}

function declarationBlocks(source: string, selector: string): string[] {
  const matches = styleRules(source)
    .filter((rule) => rule.selectors.split(',').some((candidate) => candidate.trim() === selector))
    .map((rule) => rule.declarations)
  expect(matches.length, `missing style owner ${selector}`).toBeGreaterThan(0)
  return matches
}

function declarationBlock(source: string, selector: string): string {
  return declarationBlocks(source, selector)[0] ?? ''
}

function selectorLists(source: string): string[] {
  return styleRules(source).map((rule) => rule.selectors)
}

function fullBorderDeclarations(block: string): string[] {
  return block
    .split(';')
    .map((declaration) => declaration.trim())
    .filter((declaration) => /^border\s*:/.test(declaration))
}

describe('reference page style ownership', () => {
  it('keeps Batch and Comparison page rules inside their sole owner sheets', () => {
    for (const name of styleNames()) {
      const source = styleSource(name)
      if (name !== 'batch-reference.css') {
        expect(source, `${name} must not own Batch page selectors`).not.toMatch(/\.batch-/)
      }
      if (name !== 'comparison-reference.css') {
        expect(source, `${name} must not own Comparison page selectors`).not.toMatch(/\.rerun-/)
      }
    }
  })

  it('scopes every Batch and Comparison selector to its page owner', () => {
    const owners = [
      { name: 'batch-reference.css', selector: /\.batch-/, scope: '.app-shell--batch' },
      { name: 'comparison-reference.css', selector: /\.rerun-/, scope: '.app-shell--comparison' },
    ]

    for (const owner of owners) {
      const ownedSelectors = selectorLists(styleSource(owner.name))
        .filter((selectorList) => owner.selector.test(selectorList))
        .flatMap((selectorList) => selectorList.split(',').map((selector) => selector.trim()))
        .filter((selector) => owner.selector.test(selector))

      expect(ownedSelectors.length).toBeGreaterThan(0)
      expect(
        ownedSelectors.every((selector) => selector.includes(owner.scope)),
        `${owner.name} contains an unscoped page selector`,
      ).toBe(true)
    }
  })

  it('leaves cross-axis navigation geometry to the shared reference owner', () => {
    for (const name of [
      'pairing-reference.css',
      'comparison-reference.css',
      'batch-reference.css',
    ]) {
      expect(styleSource(name), `${name} must not resize shared navigation`).not.toMatch(
        /navigation-courtyard|cross-axis-navigation/,
      )
    }
  })

  it('keeps the valid empty Catalog on the Catalog-owned continuous paper', () => {
    const sharedComponents = styleSource('components.css')
    const catalog = styleSource('catalog-reference.css')
    const emptyState = declarationBlocks(catalog, '.app-shell--catalog .catalog-empty').join('\n')

    expect(sharedComponents, 'the historical generic empty card must not return').not.toMatch(
      /\.catalog-empty/,
    )
    expect(emptyState).toMatch(/\bborder\s*:\s*0/)
    expect(emptyState).not.toMatch(/\bborder-(?:radius|style)\s*:/)
    expect(emptyState).not.toMatch(/\b(?:dashed|box-shadow|surface-plinth)\b/)
  })

  it('does not reintroduce the retired vermilion intro rule', () => {
    const sharedComponents = styleSource('components.css')
    const catalogReference = styleSource('catalog-reference.css')

    for (const selector of [
      '.view-introduction__heading::before',
      '.view-introduction__heading::after',
    ]) {
      expect(sharedComponents).not.toContain(selector)
      expect(catalogReference).not.toContain(selector)
    }
  })

  it('gives the mobile Run status ledger enough width for complete labels', () => {
    const source = styleSource('run-detail-reference.css')
    const statusGate = declarationBlocks(
      source,
      '.app-shell--run-detail .status-gate--detail',
    ).join('\n')
    const integritySeal = declarationBlocks(
      source,
      '.app-shell--run-detail .status-gate--detail .integrity-seal',
    ).join('\n')

    expect(statusGate).toMatch(/grid-template-columns:\s*repeat\(2,\s*minmax\(0,\s*1fr\)\)/)
    expect(integritySeal).toMatch(/grid-column:\s*1\s*\/\s*-1/)
  })

  it('keeps Rerun Comparison on one continuous frame', () => {
    const source = styleSource('comparison-reference.css')
    const page = declarationBlock(source, '.app-shell--comparison .rerun-page')
    const mirror = declarationBlocks(source, '.app-shell--comparison .rerun-mirror').join('\n')
    const summary = declarationBlocks(source, '.app-shell--comparison .rerun-summary-grid').join('\n')
    const ledgerValues = declarationBlocks(source, '.app-shell--comparison .rerun-ledger__values').join('\n')

    expect(page).toMatch(/\bborder:/)
    expect(page).not.toMatch(/box-shadow/)
    expect(mirror).not.toMatch(/\b(?:background|box-shadow):/)
    expect(mirror).not.toMatch(/(?:^|\n)\s*border\s*:/)
    expect(summary).not.toMatch(/\b(?:background|box-shadow):/)
    expect(summary).not.toMatch(/(?:^|\n)\s*border\s*:/)
    expect(ledgerValues).not.toMatch(/\b(?:background|box-shadow):/)
    expect(ledgerValues).not.toMatch(/(?:^|\n)\s*border\s*:/)
  })

  it('keeps Comparison source regions as ruled cells instead of independent cards', () => {
    const source = styleSource('comparison-reference.css')
    const mirrorBeam = declarationBlocks(source, '.app-shell--comparison .rerun-mirror__beam').join('\n')
    const sourceRegion = declarationBlocks(source, '.app-shell--comparison .rerun-source').join('\n')
    const mobileTitle = declarationBlocks(source, '.app-shell--comparison .rerun-source__mobile-title').join('\n')
    const sourceStatuses = declarationBlocks(source, '.app-shell--comparison .rerun-source__statuses').join('\n')
    const sourceFacts = declarationBlocks(source, '.app-shell--comparison .rerun-source__facts').join('\n')

    expect(source, 'source cards must not regain their own repeated lintel').not.toMatch(
      /\.rerun-source\s*>\s*header/,
    )

    for (const [selector, block] of [
      ['.rerun-mirror__beam', mirrorBeam],
      ['.rerun-source', sourceRegion],
      ['.rerun-source__mobile-title', mobileTitle],
      ['.rerun-source__statuses', sourceStatuses],
      ['.rerun-source__facts', sourceFacts],
    ] as const) {
      expect(block, `${selector} must not regain a card shadow`).not.toMatch(/\bbox-shadow\s*:/)
      expect(block, `${selector} must not regain rounded card corners`).not.toMatch(/\bborder-radius\s*:/)
      expect(
        fullBorderDeclarations(block).every((declaration) =>
          /^border\s*:\s*(?:0|none)$/.test(declaration),
        ),
        `${selector} may use edge rules but not a complete four-sided border`,
      ).toBe(true)
    }

    for (const [selector, block] of [
      ['.rerun-source', sourceRegion],
      ['.rerun-source__statuses', sourceStatuses],
      ['.rerun-source__facts', sourceFacts],
    ] as const) {
      expect(block, `${selector} must stay on the continuous paper ground`).not.toMatch(
        /\bbackground(?:-color|-image)?\s*:/,
      )
    }

    expect(source, 'mobile source labels must stay on the shared paper ground').toMatch(
      /\.app-shell--comparison \.rerun-source__mobile-title\s*\{[^}]*\bbackground\s*:\s*transparent/s,
    )
  })
})
