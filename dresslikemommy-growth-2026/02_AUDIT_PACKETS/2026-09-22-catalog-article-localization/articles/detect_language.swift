import Foundation
import NaturalLanguage

// On-device language classification only; no network or model-provider client.
while let line = readLine() {
    guard let data = line.data(using: .utf8),
          let row = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
          let identifier = row["id"] as? String,
          let input = row["text"] as? String else { continue }
    let recognizer = NLLanguageRecognizer()
    recognizer.processString(input)
    let hypotheses = recognizer.languageHypotheses(withMaximum: 3)
    var mapped: [String: Double] = [:]
    for (language, confidence) in hypotheses { mapped[language.rawValue] = confidence }
    let out: [String: Any] = ["id": identifier, "dominant": recognizer.dominantLanguage?.rawValue ?? "und", "hypotheses": mapped]
    if let encoded = try? JSONSerialization.data(withJSONObject: out, options: [.sortedKeys]),
       let text = String(data: encoded, encoding: .utf8) { print(text) }
}
