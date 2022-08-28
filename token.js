class Token {
    constructor(tokenString, expiry) {
        this.tokenString = tokenString
        this.expiry = expiry
    }

    checkExpiration() {
        console.log('checking Expiration...')
        now = new Date()
        console.log(this.expiry, now)
        if (this.expiry > now) {
            return true
        }
        else return false
    }
}

export default Token