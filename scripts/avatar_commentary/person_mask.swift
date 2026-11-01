// Person segmentation masks with Apple's built-in Vision framework (no model download).
// Usage: person_mask <frames_dir> <masks_dir>
// Reads every *.png in frames_dir, writes a same-named grayscale mask PNG (white = person).
import AppKit
import CoreImage
import Foundation
import Vision

let arguments = CommandLine.arguments
guard arguments.count == 3 else {
    FileHandle.standardError.write("usage: person_mask <frames_dir> <masks_dir>\n".data(using: .utf8)!)
    exit(2)
}
let framesURL = URL(fileURLWithPath: arguments[1])
let masksURL = URL(fileURLWithPath: arguments[2])
try FileManager.default.createDirectory(at: masksURL, withIntermediateDirectories: true)

let context = CIContext()
let request = VNGeneratePersonSegmentationRequest()
request.qualityLevel = .accurate
request.outputPixelFormat = kCVPixelFormatType_OneComponent8

let frames = try FileManager.default.contentsOfDirectory(at: framesURL, includingPropertiesForKeys: nil)
    .filter { $0.pathExtension == "png" }
    .sorted { $0.lastPathComponent < $1.lastPathComponent }

for (index, frameURL) in frames.enumerated() {
    guard let image = CIImage(contentsOf: frameURL) else {
        FileHandle.standardError.write("cannot read \(frameURL.path)\n".data(using: .utf8)!)
        exit(1)
    }
    let handler = VNImageRequestHandler(ciImage: image)
    try handler.perform([request])
    guard let buffer = request.results?.first?.pixelBuffer else {
        FileHandle.standardError.write("no mask for \(frameURL.lastPathComponent)\n".data(using: .utf8)!)
        exit(1)
    }
    // Scale the low-res mask back to the frame size.
    var mask = CIImage(cvPixelBuffer: buffer)
    let scaleX = image.extent.width / mask.extent.width
    let scaleY = image.extent.height / mask.extent.height
    mask = mask.transformed(by: CGAffineTransform(scaleX: scaleX, y: scaleY))
    guard let cgMask = context.createCGImage(mask, from: image.extent,
                                             format: .L8, colorSpace: CGColorSpaceCreateDeviceGray()) else {
        exit(1)
    }
    let rep = NSBitmapImageRep(cgImage: cgMask)
    let outURL = masksURL.appendingPathComponent(frameURL.lastPathComponent)
    try rep.representation(using: .png, properties: [:])!.write(to: outURL)
    if index % 100 == 0 { print("\(index)/\(frames.count)") }
}
print("done \(frames.count)")
