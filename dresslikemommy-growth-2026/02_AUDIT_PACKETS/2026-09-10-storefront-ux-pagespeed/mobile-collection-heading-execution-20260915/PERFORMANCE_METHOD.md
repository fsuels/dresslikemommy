# Cold-load comparison method

The owned background preview tab uses HTTP cache bypass (`Network.setCacheDisabled`) with its existing US/USD preview session. Cookies, connection reuse, CPU speed and network speed are retained. This is a desktop Chromium browser at explicit viewport widths, not a throttled mobile-device or PageSpeed run.

The accepted captures use a complete CDP trace stream (`dataLossOccurred=false`). Navigation is bound to the current tab's main-frame ID and document loader ID. FCP and layout-shift events are scoped to that frame after its navigation start. Duplicate near-zero DOMContentLoaded events are not interpreted. The initial event-buffer capture was truncated and is diagnostic only.

Reported main-frame CLS is the largest session window: non-input shift scores are accumulated with at most a one-second gap and a five-second maximum window. Preview-bar iframe shifts are excluded and are not represented as full-page or field CLS. The preview bar can still affect the main document. Each comparable run observes approximately eight seconds after navigation; the earlier longer phone capture is corroborating only.

The filmstrip preserves the first available frame per 100 ms through two seconds, per 500 ms through six seconds, and the final frame. All screenshot timestamps and all main-frame shift events are retained. Resource evidence retains only the three collection CSS request IDs, without headers, cookies or unrelated telemetry URLs. The served CSS is compared to source after removing comments, whitespace and optional terminal semicolons; Shopify minification means byte equality is not expected for the response.

Compare the 390, 760 and 1280 pixel runs, actual stylesheet completion relative to first paint, and heading visibility in the filmstrip. A few unthrottled preview samples do not establish a PageSpeed improvement, real-user Core Web Vitals, conversion lift or production acceptance.
