const crypto = require('crypto')

let i
const IDs = crypto.randomBytes(16)
const IDr = crypto.randomBytes(16)
const info = Buffer.concat([IDr, IDs], 32)

// using crypto
let keyBuf

console.time('prng-crypto')

i = 10000
while (i--) keyBuf = crypto.randomBytes(16)

console.timeEnd('prng-crypto')

console.log(`prng-crypto's result is: ${keyBuf.toString('hex')}`)

/* test HKDF using one-iteration PBKDF2: deriving 160-bit key for HMAC-SHA1 */
let keyDer

console.time('HKDF')

i = 10000
while (i--) keyDer = crypto.pbkdf2Sync(keyBuf, info, 1, 20, 'sha256')

console.timeEnd('HKDF')

console.log(`HKDF's result is: ${keyDer.toString('hex')}`)

/* test HMAC-SHA1 */
let hmac, hmacResult
console.time('HMAC-SHA1')

i = 10000
while (i--) {
	hmac = crypto.createHmac('sha1', keyDer)
	hmac.update(IDr)
	hmacResult = hmac.digest('hex')
}

console.timeEnd('HMAC-SHA1')

console.log(`HMAC-SHA1's result is: ${hmacResult}`)

let hmacMD5, hmacMD5Result
console.time('HMAC-MD5')

i = 10000
while (i--) {
	hmacMD5 = crypto.createHmac('md5', keyDer)
	hmacMD5.update(IDr)
	hmacMD5Result = hmac.digest('hex')
}

console.timeEnd('HMAC-MD5')

console.log(`HMAC-MD5's result is: ${hmacMD5Result}`)

/* test AES-128 */
let cipher, encrypted

console.time('AES128 encryption')

i = 10000
while (i--) {
	cipher = crypto.createCipher('aes128', keyBuf)

	encrypted = cipher.update('some clear text data', 'utf8', 'hex')
	encrypted += cipher.final('hex')
}

console.timeEnd('AES128 encryption')

console.log(`AES128's result is: ${encrypted}`)

/* test SHA-256 */
let hash, hashResult

console.time('SHA-256')

i = 10000
while (i--) {
	hash = crypto.createHash('sha256')

	hash.update(keyBuf)
	hashResult = hash.digest('hex')
}

console.timeEnd('SHA-256')

console.log(`SHA-256's result is: ${hashResult}`)

/* test Equal-probability quantization */
const target = 7.5
let intervals = new Array(17)
intervals = intervals.map((el, index) => index)

console.time('Equal-probability quantization')

i = 100000
while (i--) {
	for (let j = 0; j < 16; j++) {
		if (target < intervals[j + 1] && target >= intervals[j]) break
	}
}

console.timeEnd('Equal-probability quantization')
