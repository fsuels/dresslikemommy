import { createHash } from 'node:crypto';

export function digestStream() {
  const hash = createHash('sha256'); let resolve, reject;
  const digest = new Promise((yes, no) => { resolve = yes; reject = no; });
  const stream = new WritableStream({
    write(chunk) { hash.update(chunk); },
    close() { const bytes = hash.digest(); resolve(bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength)); },
    abort(reason) { reject(reason); },
  });
  stream.digest = digest; return stream;
}
export function fixedLengthStream(length) {
  let written = 0;
  return new TransformStream({
    transform(chunk, controller) { written += chunk.byteLength; if (written > length) throw new Error('too_many_bytes'); controller.enqueue(chunk); },
    flush() { if (written !== length) throw new Error('too_few_bytes'); },
  });
}
export const streamOptions = { digestStream, fixedLengthStream };
