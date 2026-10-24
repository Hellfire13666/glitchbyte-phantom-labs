# GLITCHBYTE SHARE CARD DOCTOR

[![Approved Facebook Sharing Debugger artwork](../../creative-utilities-showcase-v1.0.3/01-FACEBOOK-SHARING-DEBUGGER/assets/APPROVED-FACEBOOK-SHARING-DEBUGGER.png)](../../creative-utilities-showcase-v1.0.3/01-FACEBOOK-SHARING-DEBUGGER/assets/APPROVED-FACEBOOK-SHARING-DEBUGGER.png)

**🎨 Official visual:** the approved Facebook Sharing Debugger image from the [GlitchByte Creative Utilities v1.0.3 showcase](../../docs/creative-utilities-showcase-v1.0.3/README.md). This is illustration for the external Meta debugger, not a screenshot of live results from Share Card Doctor.

A **separate tool** from the Art Vault Converter. Checks the public Hangout's Open Graph and X Card tags, link canonicalization, and whether the preview image responds to an HTTPS HEAD request.

- The live link guests share: <https://glitchbyte.alwaysdata.net/hangout>
- The picture: <https://glitchbyte.alwaysdata.net/social-preview-assets/og-image.jpg>
- The Facebook/Messenger cache tool: **[Meta Sharing Debugger](https://developers.facebook.com/tools/debug/)**

## SIMPLE (MX Linux / Ubuntu)

```bash
python3 tools/glitchbyte-share-card-doctor/share_card_doctor.py
```

## MEDIUM: inspect the public Welcome link

```bash
python3 tools/glitchbyte-share-card-doctor/share_card_doctor.py \
  --url 'https://glitchbyte.alwaysdata.net/welcome'
```

## EXTRA: structured output for your own test notes

```bash
python3 tools/glitchbyte-share-card-doctor/share_card_doctor.py --json
```

These commands should run from the cloned **glitchbyte-phantom-labs** repository root. No third-party packages or GitHub token required. Output is terminal-only unless you intentionally redirect it into a file.

The utility removes Facebook's `fbclid` and marketing `utm_` query parameters from the submitted Hangout/Welcome URL, checks the page's `og:url`, `og:title`, `og:description`, `og:image`, and `twitter:card`, and checks the image response. It only accepts approved public paths on `glitchbyte.alwaysdata.net`: never point it at a private one-use invite link.

**Important:** This script is read-only, does not post to Facebook, does not call Meta's private APIs, and **cannot forcibly refresh Meta's cache**. Open the Sharing Debugger link above, paste the clean public Hangout URL, and press **Scrape Again**. Messenger/X can retain old previews for some time; creating a fresh post with the clean URL may be necessary.

**Result interpretation:** `[PASS]` checks indicate metadata is present and the linked image responds. That does not guarantee every social platform will draw a preview card, since they control their own preview rendering and caches.
