#!/usr/bin/env python3
"""Static QA gates for the sync-subject skill.

Run:  python3 .claude/skills/sync-subject/reference/checks.py PAGE.html [PAGE.html ...]

This is a *verification* tool, not a build step — it never writes to a page and
nothing in the deploy path calls it. It covers QA gates 2, 3, 5 and 6 from SKILL.md:

  structure  tag balance, duplicate ids, aria-* targets, relative links,
             unlisted-content links
  svg        <text> estimated to overflow its parent <rect>
  layout     a <span> given box properties without being blockified
             (this is the class of bug the flashcard shipped with)
  length     flowing prose per topic against the fragment-spec budget

Gate 1 (fidelity) and gate 4 (privacy) are model work and are not automatable —
see SKILL.md.

Gate 6 exists because the first DMBA 6008 build shipped ~4,000 words per topic
against a stated 900-1400 budget. The number was in the spec and was ignored,
because nothing measured it. Pass --lengths to print the table without failing.

Exit 0 = clean. Exit 1 = at least one finding. Findings print as
FILE:LINE  GATE  message
"""

import os
import re
import sys
from html.parser import HTMLParser

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
        'meta', 'param', 'source', 'track', 'wbr'}

# SVG width estimate, px per character, by font-size. Deliberately generous —
# a false positive costs a glance, a false negative ships a broken figure.
PX_PER_CHAR = {10: 5.4, 11: 5.9, 12: 6.5, 13: 7.0, 14: 7.6, 16: 8.7, 18: 9.8}

# Only the properties a non-blockified inline element *silently drops*. Padding
# and margin are deliberately excluded: horizontal padding works on an inline
# span and the repo uses it all over for chips and pills.
BOX_PROPS = ('width', 'height', 'min-height', 'min-width', 'max-height')
BLOCKIFIERS = ('block', 'inline-block', 'flex', 'inline-flex', 'grid',
               'inline-grid', 'table', 'list-item', 'contents')


class Structure(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errs = [], []
        self.ids, self.dup = {}, []
        self.aria_refs, self.hrefs, self.srcs = [], [], []
        self.spans = []          # (line, own classes, ancestor classes)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        line = self.getpos()[0]
        ancestors = [c for frame in self.stack for c in frame[2]]
        if tag not in VOID:
            self.stack.append((tag, self.getpos(), a.get('class', '').split()))
        if 'id' in a:
            if a['id'] in self.ids:
                self.dup.append((line, a['id'], self.ids[a['id']]))
            else:
                self.ids[a['id']] = line
        for k in ('aria-labelledby', 'aria-describedby', 'aria-controls'):
            if k in a:
                for ref in a[k].split():
                    self.aria_refs.append((line, k, ref))
        if 'href' in a:
            self.hrefs.append((line, a['href']))
        if 'src' in a:
            self.srcs.append((line, a['src']))
        if tag == 'span':
            self.spans.append((line, a.get('class', ''), ancestors))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errs.append((self.getpos()[0], 'stray </%s>' % tag))
            return
        t, pos, _ = self.stack.pop()
        if t != tag:
            self.errs.append((self.getpos()[0],
                              '</%s> closes <%s> opened at line %d' % (tag, t, pos[0])))


def css_rules(text):
    """Very small CSS reader: {selector: {prop: value}} for the inline <style>."""
    out = {}
    for style in re.findall(r'<style>(.*?)</style>', text, re.S):
        style = re.sub(r'/\*.*?\*/', '', style, flags=re.S)
        for sel, body in re.findall(r'([^{}]+)\{([^{}]*)\}', style):
            decls = {}
            for d in body.split(';'):
                if ':' in d:
                    k, v = d.split(':', 1)
                    decls[k.strip().lower()] = v.strip().lower()
            for s in sel.split(','):
                out.setdefault(s.strip(), {}).update(decls)
    return out


def check_structure(path, text, found):
    p = Structure()
    p.feed(text)
    for line, msg in p.errs:
        found.append((path, line, 'structure', msg))
    if p.stack:
        for t, pos, _ in p.stack:
            found.append((path, pos[0], 'structure', 'unclosed <%s>' % t))
    for line, i, first in p.dup:
        found.append((path, line, 'structure',
                      'duplicate id "%s" (first at line %d)' % (i, first)))
    for line, attr, ref in p.aria_refs:
        if ref not in p.ids:
            found.append((path, line, 'structure',
                          '%s="%s" resolves to nothing' % (attr, ref)))

    base = os.path.dirname(os.path.abspath(path)) or '.'
    for line, href in p.hrefs + p.srcs:
        if href.startswith(('http://', 'https://', '#', 'mailto:', 'data:', '//')):
            continue
        if 'only-accessible-by-url' in href:
            found.append((path, line, 'structure',
                          'links to unlisted content: %s' % href))
            continue
        target = href.split('?')[0].split('#')[0]
        if target and not os.path.exists(os.path.join(base, target)):
            found.append((path, line, 'structure',
                          'relative path does not resolve: %s' % href))
    return p


def check_svg(path, text, found):
    """Estimate whether an SVG <text> overflows the <rect> it sits in."""
    for m in re.finditer(r'<svg\b[^>]*>(.*?)</svg>', text, re.S):
        body = m.group(1)
        svg_line = text[:m.start()].count('\n') + 1
        rects = []
        for r in re.finditer(r'<rect\b([^>]*)>', body):
            at = r.group(1)

            def num(name):
                g = re.search(r'\b%s="([-\d.]+)"' % name, at)
                return float(g.group(1)) if g else None
            x, y, w, h = num('x'), num('y'), num('width'), num('height')
            if None not in (x, y, w, h):
                rects.append((x, y, w, h))

        for t in re.finditer(r'<text\b([^>]*)>(.*?)</text>', body, re.S):
            at, label = t.group(1), re.sub(r'<[^>]+>', '', t.group(2)).strip()
            if not label:
                continue
            line = svg_line + body[:t.start()].count('\n')

            def num(name, default=None):
                g = re.search(r'\b%s="([-\d.]+)"' % name, at)
                return float(g.group(1)) if g else default
            tx, ty = num('x'), num('y')
            if tx is None or ty is None:
                continue
            cls = re.search(r'class="([^"]*)"', at)
            cls = cls.group(1) if cls else ''
            size = 12
            if 'svg-sub' in cls or 'svg-eyebrow' in cls:
                size = 10
            if 'svg-mono' in cls:
                size = 11
            fs = num('font-size')
            if fs:
                size = fs
            per = PX_PER_CHAR.get(int(size), size * 0.55)
            width = len(label) * per
            anchor = re.search(r'text-anchor="([^"]*)"', at)
            anchor = anchor.group(1) if anchor else 'start'
            left = tx - width / 2 if anchor == 'middle' else (tx - width if anchor == 'end' else tx)
            right = left + width

            host = None
            for (x, y, w, h) in rects:
                if x <= tx <= x + w and y <= ty <= y + h:
                    if host is None or w < host[2]:
                        host = (x, y, w, h)
            if host:
                x, y, w, _ = host
                over = max(x - left, right - (x + w))
                if over > 2:
                    found.append((path, line, 'svg',
                                  '"%s" overflows its rect by ~%.0fpx' % (label[:44], over)))

        vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', m.group(0))
        if vb:
            vw = float(vb.group(1))
            for t in re.finditer(r'<text\b([^>]*)>(.*?)</text>', body, re.S):
                at = t.group(1)
                g = re.search(r'\bx="([-\d.]+)"', at)
                if g and not (0 <= float(g.group(1)) <= vw):
                    line = svg_line + body[:t.start()].count('\n')
                    found.append((path, line, 'svg', 'text x=%s is outside the viewBox' % g.group(1)))


def check_layout(path, text, found, parser):
    """A <span> given box properties must be blockified, or the box is ignored.

    This is the rule that would have caught the collapsed flashcard: .flip-inner
    was a <span> with width/min-height and no display, so both were dropped.
    """
    rules = css_rules(text)
    boxed = {}
    for sel, decls in rules.items():
        if not any(p in decls for p in BOX_PROPS):
            continue
        disp = decls.get('display')
        if disp and any(disp.startswith(b) for b in BLOCKIFIERS):
            continue
        if disp in ('none',) or decls.get('position') in ('absolute', 'fixed'):
            continue
        # The rule only lands on the selector's SUBJECT — the last compound.
        # ".pill .dot { width }" styles .dot, not .pill. Pseudo-elements are
        # their own boxes and are never the span.
        subject = sel.split()[-1].split('>')[-1].strip()
        if '::' in subject or re.search(r':(before|after)\b', subject):
            continue
        for cls in re.findall(r'\.([A-Za-z0-9_-]+)', subject):
            boxed.setdefault(cls, sel)

    # A flex or grid container blockifies its children, so a span inside one is
    # fine. Collect the classes that make an element a flex/grid container.
    containers = set()
    for sel, decls in rules.items():
        if decls.get('display', '').split()[0:1] and any(
                decls['display'].startswith(d)
                for d in ('flex', 'grid', 'inline-flex', 'inline-grid')):
            subject = sel.split()[-1].split('>')[-1].strip()
            for cls in re.findall(r'\.([A-Za-z0-9_-]+)', subject):
                containers.add(cls)

    for line, classattr, ancestors in parser.spans:
        if any(a in containers for a in ancestors):
            continue          # a flex/grid ancestor blockifies it
        for cls in classattr.split():
            if cls in boxed:
                found.append((path, line, 'layout',
                              '<span class="%s"> gets box properties from "%s" but has no '
                              'display and no flex/grid ancestor — the box is silently '
                              'dropped' % (cls, boxed[cls])))


# Flowing-prose budget, from reference/fragment-spec.md section 5.
# "Prose" deliberately excludes tables, figures, worked examples, callouts,
# formulas and list artefacts: those carry the study material and are not the
# thing that bloats. Connective paragraphs are.
#
# The budget is per BLOCK, not per topic. A DMBA 6008 week-0 topic is a whole
# financial statement across ten .block sections; a DMBA 6005 topic may be one.
# A flat per-topic number punishes the first and lets the second sail through.
PROSE_PER_BLOCK = 160
PROSE_FLOOR = 900

# Balanced-div blocks that count as artefacts rather than prose.
ARTEFACT_DIVS = ('table-scroll', 'example-grid', 'callout', 'formula',
                 'principles', 'fig-frame')


def _strip_balanced(text, class_name):
    """Remove <div class="...class_name..."> ... </div>, honouring nesting."""
    spans = []
    for m in re.finditer(r'<div\b[^>]*class="[^"]*\b%s\b[^"]*"[^>]*>' % class_name, text):
        if spans and m.start() < spans[-1][1]:
            continue
        depth, end = 0, len(text)
        for t in re.finditer(r'<div\b|</div>', text[m.start():]):
            depth += 1 if t.group(0) == '<div' else -1
            if depth == 0:
                end = m.start() + t.end()
                break
        spans.append((m.start(), end))
    for a, b in reversed(spans):
        text = text[:a] + text[b:]
    return text


def prose_words(html):
    """Words of flowing prose — artefacts removed."""
    t = re.sub(r'<figure\b.*?</figure>', '', html, flags=re.S)
    t = re.sub(r'<table\b.*?</table>', '', t, flags=re.S)
    t = re.sub(r'<(ol|ul)\b[^>]*class="[^"]*\b(steps|takeaways)\b[^"]*".*?</\1>', '', t, flags=re.S)
    for cls in ARTEFACT_DIVS:
        t = _strip_balanced(t, cls)
    t = re.sub(r'<svg\b.*?</svg>', '', t, flags=re.S)
    return len(re.sub(r'<[^>]+>', ' ', t).split())


def topics(text):
    """[(name, html)] for each summary topic — subpanels if present, else one."""
    m = re.search(r'<section\b[^>]*id="panel-summary".*?(?=<section\b[^>]*id="panel-|</main>)',
                  text, re.S)
    if not m:
        return []
    panel = m.group(0)
    subs = re.findall(r'<div\b[^>]*class="subpanel[^"]*"[^>]*id="([^"]+)"[^>]*>', panel)
    if not subs:
        return [('summary', panel)]
    out, bounds = [], []
    for sid in subs:
        i = panel.index('id="%s"' % sid)
        bounds.append((sid, i))
    for n, (sid, i) in enumerate(bounds):
        j = bounds[n + 1][1] if n + 1 < len(bounds) else len(panel)
        out.append((sid, panel[i:j]))
    return out


def check_length(path, text, found, report):
    for name, html in topics(text):
        prose = prose_words(html)
        total = len(re.sub(r'<[^>]+>', ' ',
                           re.sub(r'<svg\b.*?</svg>', '', html, flags=re.S)).split())
        if total < 60:
            continue                      # an honest "not yet written" panel
        # `class="block"` may carry attributes (e.g. data-topic), so match the
        # opening tag rather than one exact string.
        blocks = len(re.findall(r'<div class="block"[ >]', html)) or 1
        budget = max(PROSE_FLOOR, blocks * PROSE_PER_BLOCK)
        report.append((path, name, blocks, prose, budget, total))
        if prose > budget:
            line = text[:text.index(html[:60])].count('\n') + 1 if html[:60] in text else 1
            found.append((path, line, 'length',
                          'topic "%s" has %d words of flowing prose over %d blocks, against '
                          'a %d budget (+%d) — condense before publishing'
                          % (name, prose, blocks, budget, prose - budget)))


def main(paths):
    lengths_only = '--lengths' in paths
    paths = [p for p in paths if p != '--lengths']
    found, report = [], []
    for path in paths:
        try:
            text = open(path, encoding='utf-8').read()
        except OSError as e:
            print('cannot read %s: %s' % (path, e))
            return 1
        parser = check_structure(path, text, found)
        check_svg(path, text, found)
        check_layout(path, text, found, parser)
        check_length(path, text, found, report)

    if report:
        print('%-24s %-9s %7s %7s %7s %7s' %
              ('FILE', 'TOPIC', 'BLOCKS', 'PROSE', 'BUDGET', 'TOTAL'))
        for path, name, blocks, prose, budget, total in report:
            print('%-24s %-9s %7d %7d %7d %7d%s'
                  % (os.path.basename(path), name, blocks, prose, budget, total,
                     '  OVER' if prose > budget else ''))
        print('budget = %d prose words per .block (floor %d); TOTAL adds tables, '
              'figures and examples\n' % (PROSE_PER_BLOCK, PROSE_FLOOR))

    if lengths_only:
        return 0

    if not found:
        print('OK — %d file(s), no findings' % len(paths))
        return 0
    for path, line, gate, msg in sorted(found, key=lambda f: (f[0], f[1])):
        print('%s:%d  %-9s %s' % (path, line, gate, msg))
    print('\n%d finding(s). Every one blocks publication until resolved or '
          'explicitly judged a false positive.' % len(found))
    return 1


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
