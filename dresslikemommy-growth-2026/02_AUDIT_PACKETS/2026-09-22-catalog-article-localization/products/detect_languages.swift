import Foundation
import NaturalLanguage
// Offline, on-device language hypotheses only. No network or translation service.
while let line = readLine() {
    guard let data = line.data(using: .utf8),
          let input = try? JSONSerialization.jsonObject(with: data) as? [String:String],
          let key = input["sha256"], let value = input["text"] else { continue }
    let recognizer = NLLanguageRecognizer()
    recognizer.processString(value)
    let hypotheses = recognizer.languageHypotheses(withMaximum: 3)
    let values = hypotheses.map { ["language": $0.key.rawValue, "probability": $0.value] as [String:Any] }.sorted { ($0["probability"] as! Double) > ($1["probability"] as! Double) }
    let result: [String:Any] = ["sha256":key,"hypotheses":values]
    if let resultData = try? JSONSerialization.data(withJSONObject:result,options:[.sortedKeys]), let resultString=String(data:resultData,encoding:.utf8) { print(resultString) }
}
